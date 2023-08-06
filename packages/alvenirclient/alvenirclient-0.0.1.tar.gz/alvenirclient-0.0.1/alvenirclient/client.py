import os
import sys
import threading
import time
from typing import List

import grpc
import numpy as np
import soundfile as sf

from alvenirclient.handle_full_document import handle_full_document
from alvenirclient.response_wrapper import AlvenirResponse
from .audio_pb2 import STOP, CONTINUE, AudioRequest, AudioResponse
from .audio_pb2_grpc import TranscriptionAPIServiceStub

continue_recording = True


class GrpcAuth(grpc.AuthMetadataPlugin):
    """
    GrPC Authentication used to authenticate user on a secure channel.
    """

    def __init__(self, key):
        self._key = key

    def __call__(self, context, callback):
        callback((('rpc-auth-header', self._key),), None)


def stop():
    input("Press Enter to stop the recording:\n")
    global continue_recording
    continue_recording = False


class AlvenirClient:
    """
    Alvenir Client for the gRPC integration. The gRPC integration is SSL secured and requires an api_key for
    authentication.
    """

    def __init__(self, key: str = None):
        """
        Alvenir Client for the gRPC integration. The gRPC integration is SSL secured and requires an api_key for
        authentication.

        :param key: API key received from alvenir.ai organization.
        """
        self.key = key
        self.channel = "grpc.danspeech.io:443"
        self.chunk_size = 6000
        from . import __path__ as ROOT_PATH
        cert_path = os.path.join(ROOT_PATH[0], "./cert/public_key.crt")

        with open(cert_path, 'rb') as f:
            self.creds = grpc.ssl_channel_credentials(f.read())

    def set_api_key(self, key: str):
        """
        Sets the API key to the given parameter
        :param key: API key received from alvenir.ai organization.
        :return:
        """
        self.key = key

    def get_secure_channel(self) -> grpc.Channel:
        """
        Gets a secure channel using the public certificate shipped with the client and the key given to client.
        :return:
        """
        return grpc.secure_channel(self.channel,
                                   grpc.composite_channel_credentials(
                                       self.creds,
                                       grpc.metadata_call_credentials(
                                           GrpcAuth(self.key)
                                       )
                                   )
                                   )

    def send_file_bytes(self, file_bytes: List[bytes]):
        """
        Sends list of bytes to the alvenir server.
        :param file_bytes: List of bytes read from a file
        :return: The AudioResponse
        """
        generator = self.bytes_generator(file_bytes)
        channel = self.get_secure_channel()
        stub = TranscriptionAPIServiceStub(channel)
        response = stub.TranscribeAudioStream(generator)
        channel.close()
        return response

    def send_audio_array(self, audio: np.array) -> AudioResponse:
        """
        Send a numpy array to the alvenir server.
        :param audio: Numpy array containing audio.
        :return: The AudioResponse
        """
        generator = self.audio_generator(audio)
        channel = self.get_secure_channel()
        stub = TranscriptionAPIServiceStub(channel)
        response = stub.TranscribeAudioStream(generator)
        channel.close()
        return response

    def bytes_generator(self, bytes_data: List[bytes]):
        """
        Generator for Audio Requests to the Alvenir Service based on bytes.
        :param bytes_data: List of bytes data
        """
        for i, bytes_obj in enumerate(bytes_data):
            if i == len(bytes_data) - 1:
                break
            yield AudioRequest(audio=bytes_obj, status=CONTINUE, server_transcoding=True)

        yield AudioRequest(audio=bytes_data[-1], status=STOP, server_transcoding=True)

    def audio_generator(self, audio_data: np.array):
        """
        Generator for Audio Requests to the Alvenir Service based on a numpy array.
        :param audio_data: Numpy array of audio data.
        """
        # If below chunk size, still send
        if len(audio_data) < self.chunk_size:
            yield AudioRequest(audio=audio_data.tobytes(), status=STOP, server_transcoding=False)
            return

        arrays = np.array_split(audio_data, int(len(audio_data) / self.chunk_size))
        number_iterations = len(arrays) - 1
        for i in range(number_iterations):
            yield AudioRequest(audio=arrays[i].tobytes(), status=CONTINUE, server_transcoding=False)

        yield AudioRequest(audio=arrays[-1].tobytes(), status=STOP, server_transcoding=False)

    def load_bytes_from_file(self, path: str):
        """
        Loads a file as binary / bytes

        :param path: Path to file.
        :return: List of bytes
        """
        still_read = True
        bytes_list = []
        with open(path, "rb") as f:
            while still_read:
                awesome_bytes = f.read(self.chunk_size)
                if awesome_bytes:
                    bytes_list.append(awesome_bytes)
                else:
                    still_read = False

        return bytes_list

    @staticmethod
    def load_audio_wavPCM(path: str):
        """
        Fast load of wav.
        This works well if you are certain that your wav files are PCM encoded.
        :param str path: Path to wave file.
        :return: Input array ready for speech recognition.
        :rtype: ``numpy.array``
        """
        sound, _ = sf.read(path)

        if len(sound.shape) > 1:
            if sound.shape[1] == 1:
                sound = sound.squeeze()
            else:
                sound = sound.mean(axis=1)  # multiple channels, average

        return sound.astype(float)[0:16000 * 5 * 60]

    def transcribe_file(self, file_path: str, server_transcoding: bool = True) -> AlvenirResponse:
        """
        Transcribes a full file using the Alvenir transcription service.

        :param file_path: Path to the local file
        :return: AlvenirResponse with transcription and full_document
        """
        if not server_transcoding:
            audio = self.load_audio_wavPCM(file_path)
            response = self.send_audio_array(audio)
        else:
            file_bytes = self.load_bytes_from_file(file_path)
            response = self.send_file_bytes(file_bytes)

        document = handle_full_document(response.full_document)
        return AlvenirResponse(status=response.status, transcription=response.transcription, full_document=document)

    def transcribe_microphone_realtime(self):
        """
        Transcribes the input directly from the microphone and provides intermediate transcriptions.

         See the following example:
            final_response = None

            responses_iterable = client.transcribe_microphone_realtime()
            for response in responses_iterable:
                if response.status == STOP:
                    final_response = response
                    break
                else:
                    print(response.transcription)

            print("Final Response:")
            print(final_response)

        :return: Generator object that can be iterated over. Each iteration has an AlvenirResponse.
        """
        transcribe_mic_generator = self._transcribe_microphone()
        return self.continue_sending_real_time(transcribe_mic_generator)

    def transcribe_microphone(self) -> AlvenirResponse:
        """
        Transcribes the input from the microphone continuously but does not provide intermediate transcriptions.
        The final transcription of the recording should however come quite fast.
        :return: AlvenirResponse with transcription and full_document
        """
        transcribe_mic_generator = self._transcribe_microphone()
        return self.continue_sending(transcribe_mic_generator)

    def continue_sending_real_time(self, generator) -> AlvenirResponse:
        """
        Method for handling real time transcription.
        :param generator: Audio generator, usually the microphone.
        """
        response = None
        channel = self.get_secure_channel()
        stub = TranscriptionAPIServiceStub(channel)
        responses = stub.TranscribeRealTimeAudioStream(generator)
        for recieved_transcript in responses:
            if recieved_transcript.status == STOP:
                response = recieved_transcript
                document = handle_full_document(response.full_document)
                response = AlvenirResponse(status=response.status, transcription=response.transcription,
                                           full_document=document)
                break
            else:
                yield AlvenirResponse(status=recieved_transcript.status,
                                      transcription=recieved_transcript.transcription)

        channel.close()
        yield response

    def continue_sending(self, generator) -> AlvenirResponse:
        """
        Method for handling real time transcription.
        :param generator: Audio generator, usually the microphone.
        :return: AlvenirResponse with transcription and full_document
        """
        channel = self.get_secure_channel()
        stub = TranscriptionAPIServiceStub(channel)
        response = stub.TranscribeAudioStream(generator)
        channel.close()
        new_document = handle_full_document(response.full_document)
        return AlvenirResponse(status=response.status, transcription=response.transcription, full_document=new_document)

    def _transcribe_microphone(self):
        """
        Uses the microphone and yields chunks from it.
        :return: generator with audio from microphone.
        """
        try:
            import pyaudio
        except Exception:
            print("You need to have pyaudio installed as an additional step to use transcribe microphone.")
            sys.exit(0)

        audio = pyaudio.PyAudio()

        global continue_recording
        continue_recording = True

        stream = audio.open(format=pyaudio.paInt16,
                            channels=1,
                            rate=16000,
                            input=True,
                            frames_per_buffer=self.chunk_size)

        stop_listener = threading.Thread(target=stop)
        stop_listener.start()

        while continue_recording:
            audio_chunk = stream.read(self.chunk_size)
            sampwidth = 2
            dt_char = 'u' if sampwidth == 1 else 'i'
            a = np.frombuffer(audio_chunk, dtype='<%s%d' % (dt_char, sampwidth))
            audio_float32 = a.astype(float)
            yield AudioRequest(audio=audio_float32.tobytes(), status=CONTINUE, server_transcoding=False)

        stream.close()
        audio.terminate()
        last_audio = np.zeros(self.chunk_size, dtype=np.float)
        yield AudioRequest(audio=last_audio.tobytes(), status=STOP, server_transcoding=False)

