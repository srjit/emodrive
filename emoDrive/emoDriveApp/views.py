# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render

import dropbox
import uuid
import json
import Algorithmia
import decision_engine

from watson_developer_cloud import SpeechToTextV1
from os.path import join, dirname

from .app_settings import *
from .forms import UploadFileForm

from watson_developer_cloud import SpeechToTextV1, ToneAnalyzerV3
from os.path import join, dirname


def format(image_response, audio_response):
    processed_data = {}
    a_response = audio_response["document_tone"]["tone_categories"][0]["tones"]
    processed_data["a"] = {emotion["tone_name"].lower() : emotion["score"] for emotion in a_response}
    processed_data["v"] = {emotion[1].lower():emotion[0] for emotion in image_response['results']}
    return processed_data


# from api.watson import call_to_watson_tone_analysis_api
def call_to_watson_tone_analysis_api(utterances):
    """
    Returns the tone analysis result for the passed
    text
    """
    tone_analyzer = ToneAnalyzerV3(
        username=WATSON_TONE_SERVICE_USERNAME,
        password=WATSON_TONE_SERVICE_PASSWORD,
        version='2016-05-19')
    result = tone_analyzer.tone(text=utterances)
    return result


def get_transcripts(json_string):
    parsed_json = json.loads(json_string)
    results = parsed_json["results"]

    alternatives = [result["alternatives"] for result in results]
    all_alternatives = [item for sublist in alternatives for item in sublist]
    return [alternative["transcript"] for alternative in all_alternatives]

def index(request):
    from emoDrive.settings import BASE_DIR
    return HttpResponse("Hello, world. You're at the emoDriveApp index." +  BASE_DIR)

def data_input(request):
    if request.method == "POST":
        image_file_name = request.FILES["image"].name
        audio_file_name = request.FILES["audio"].name
        image_file_binary = request.FILES["image"].read()
        audio_file_binary = request.FILES["audio"].read()
        speed = request.POST.get("speed")

        # Image Analysis
        dbx = dropbox.Dropbox(DROPBOX_ACCESS_TOKEN)
        image_path="/images/" + str(uuid.uuid1()) + "__" + image_file_name
        dbx.files_upload(image_file_binary, image_path, mute=True)
        client = Algorithmia.client(ALGO_ACCESS_KEY)
        algo = client.algo(ALGO_EMOTION_API)
        params = {}
        params["image"] = "dropbox://" + image_path
        params["numResults"] = 7
        image_analysis = algo.pipe(params).result

        # speech Analysis
        speech_to_text = SpeechToTextV1(
            username=WATSON_SPT_SERVICE_USERNAME,
            password=WATSON_SPT_SERVICE_PASSWORD,
            x_watson_learning_opt_out=False
        )
        models = speech_to_text.models()
        us_model = speech_to_text.get_model('en-US_BroadbandModel')
        results = speech_to_text.recognize(
            audio_file_binary, content_type='audio/wav', timestamps=True,
            word_confidence=True, speaker_labels=True)

        transcripts = get_transcripts(json.dumps(results))
        transcripts_str = ". ".join(transcripts)
        tone_analysis = call_to_watson_tone_analysis_api(transcripts_str)

        response = format(image_analysis, tone_analysis)

        response.update({"speed": float(speed), "weather": 0})



        (score, (msg, aloc)) = decision_engine.decide(response)

        # a = decision_engine.decide(response)
        #
        # if a:
        #     score = a[0]
        #     msg = a[1][0]
        #     aloc = a[1][1]

        #import ipdb; ipdb.set_trace()

        return render(request, 'results.html' , {
            "score": score ,
            "msg": msg,
            "score_breakup": response
            })
        #return render(request, 'results.html')
        #return HttpResponseRedirect("/emoDrive/analyze/" + upload_path)
    else:
        return render(request, 'upload.html')


def get_image_analysis(request, *args, **kwargs):
    if request.method == "GET":
        path = kwargs.get("path")
        client = Algorithmia.client(ALGO_ACCESS_KEY)
        algo = client.algo(ALGO_EMOTION_API)
        params = {}
        params["image"] = "dropbox://" + path
        params["numResults"] = 7
        result = algo.pipe(params).result
        return render(request, 'results.html' , {"result": result})
