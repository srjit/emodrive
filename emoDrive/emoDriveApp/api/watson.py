import json
from watson_developer_cloud import SpeechToTextV1, ToneAnalyzerV3
from os.path import join, dirname


import sys
sys.path.insert(0, '../');
from app_settings import *

def call_to_watson_speech_to_text(filepath):
    speech_to_text = SpeechToTextV1(
        username=WATSON_SPT_SERVICE_USERNAME,
        password=WATSON_SPT_SERVICE_PASSWORD,
        x_watson_learning_opt_out=False
    )
    models = speech_to_text.models()
    us_model = speech_to_text.get_model('en-US_BroadbandModel')
    with open(filepath,'rb') as audio_file:
        results = speech_to_text.recognize(
            audio_file, content_type='audio/wav', timestamps=True,
            word_confidence=True, speaker_labels=True)
    return results


def call_to_watson_tone_analysis_api(utterance):
    """
    Returns the tone analysis result for the passed
    text
    """
    tone_analyzer = ToneAnalyzerV3(
        username=WATSON_TONE_SERVICE_USERNAME,
        password=WATSON_TONE_SERVICE_PASSWORD,
        version='2016-05-19')
    result = tone_analyzer.tone(utterance)
    return result
