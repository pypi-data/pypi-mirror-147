# Alvenir Client for Speech Recognition (BETA)
gRPC client for speech recognition using Alvenir as backend. 

The client and the gRPC integration is in **beta** and ongoing development. Hence, there might be
a few stability issues. It currently supports only Danish and you need to receive an API key from Alvenir to use.

Write an email to martin[at]alvenir.ai or rasmus[at]alvenir.ai if you want an API key!


## How to install
Installing the client is as easy as writing:
```commandline
pip install alvenirclient
```

## How to use
It is very simple to use! The preferred format of audio is single channel 16kHz wav with pcm_s16le audio encoding.

If you audio files is in different format, you can use a tool such as ffmpeg to do the transcoding. An example is:
```
ffmpeg -i <existing_audio_file_path> -acodec pcm_s16le -ar 16000 -ac 1 <new_wav_audio_file_path>
```

The server can also perform transcoding but this feature is still experimential.
 
### Basic usage
```python
from alvenirclient.client import AlvenirClient

client = AlvenirClient(key="<YOUR KEY HERE>")
response = client.transcribe_file("<Path to file>", server_transcoding=False)
print(response.transcription)
print(response.full_document)
```
The response is of class `AlvenirResponse` and contains:
* transcription; The transcription as a string
* full_document; A json document with confidences and timestamps. An example of a full document is
```json
{
  "confidence": 0.9141539366420111,
  "segments": [
    {
      "confidence": 0.9141539366420111,
      "end_time": 1.77,
      "start_time": 0.93,
      "word_list": [
        {
          "confidence": 0.995308015467965,
          "end_time": 1.01,
          "start_time": 0.93,
          "word": "Jeg"
        },
        {
          "confidence": 0.9983347185448589,
          "end_time": 1.1500000000000001,
          "start_time": 1.03,
          "word": "bor"
        },
        {
          "confidence": 0.9622011164767056,
          "end_time": 1.29,
          "start_time": 1.21,
          "word": "hos"
        },
        {
          "confidence": 0.9999113092492331,
          "end_time": 1.4500000000000002,
          "start_time": 1.37,
          "word": "min"
        },
        {
          "confidence": 0.6150145234712928,
          "end_time": 1.77,
          "start_time": 1.51,
          "word": "datter."
        }
      ]
    }
  ]
}
```

### Server transcoding
Performing server_transcoding just requires setting server_transcoding=True. This way, the samplerate and
fileformat does not matter as long as it is a common audio format (wav, mp3 etc.). 

```python
from alvenirclient.client import AlvenirClient

client = AlvenirClient(key="<YOUR KEY HERE>")
response = client.transcribe_file("<Path to file>", server_transcoding=True)
print(response.transcription)
print(response.full_document)
```


### Microphone transcription
The client allows you to use your own microphone for transcriptions. It does however require you
to additionally install [pyaudio](http://people.csail.mit.edu/hubert/pyaudio/). It is a very experimential
feature and the transcriptions might not be very accurate depending on the microphone and how the audio is recorded. 

The most simple usage with microphone is: 
```python
from alvenirclient.client import AlvenirClient

client = AlvenirClient(key="<YOUR KEY HERE>")
response = client.transcribe_microphone()
print(response.transcription)
print(response.full_document)
```
The microphone will stop recording when you press the key "enter". This will not be real time, but the transcription is being made while you speak, so the response should be pretty instant.

For real time transcription i.e. continously getting a response, use the following code.

```python
from alvenirclient.client import AlvenirClient
from alvenirclient.audio_pb2 import STOP

client = AlvenirClient(key="<YOUR KEY HERE>")
final_response = None
responses_iterable = client.transcribe_microphone_realtime()

for response in responses_iterable:
    if response.status == STOP:
        final_response = response
        break
    else:
        print(response.transcription)

print(final_response.transcription)
print(final_response.full_document)
```

Note, the intermediate responses do not have full_document but only text in the transcription.

