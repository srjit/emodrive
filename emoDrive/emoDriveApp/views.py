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

from watson_developer_cloud import SpeechToTextV1
from os.path import join, dirname

from .app_settings import *
from .forms import UploadFileForm


def index(request):
    from emoDrive.settings import BASE_DIR
    return HttpResponse("Hello, world. You're at the emoDriveApp index." +  BASE_DIR)

def upload_to_dropbox(request):
    if request.method == "GET":
        form = UploadFileForm()
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            dbx = dropbox.Dropbox(DROPBOX_ACCESS_TOKEN)
            file_name = request.FILES["image"].name
            upload_path="/images/" + str(uuid.uuid1()) + "__" + file_name
            dbx.files_upload(request.FILES["image"].read(), upload_path, mute=True)
            return HttpResponseRedirect("/emoDrive/analyze/" + upload_path)
    else:
        form = UploadFileForm()
    return render(request, 'upload.html', {'form': form})


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
