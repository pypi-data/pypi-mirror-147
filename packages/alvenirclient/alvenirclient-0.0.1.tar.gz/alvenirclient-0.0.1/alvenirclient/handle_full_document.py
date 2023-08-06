import json


def handle_full_document(document: bytes):
    if not document:
        return None
    doc = json.loads(document)
    del doc["__faust"]
    for segment in doc["segments"]:
        del segment["__faust"]
        for word in segment["word_list"]:
            del word["__faust"]
    return doc
