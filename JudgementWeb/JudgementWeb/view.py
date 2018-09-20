# coding: utf-8
import time
from django.http import HttpResponse
from django.shortcuts import render
import textScore
import os, sys


def upload_file(myfile):
    nowTime = int(time.time())    
    UploadFolder = sys.path[0]+os.sep+"UploadFiles"
    newPath = os.path.join(UploadFolder, myfile.name + str(nowTime))
    newFile = open(newPath, 'wb+')
    for chunk in myfile.chunks():
        newFile.write(chunk)
    newFile.close()

    fob = open(newPath)
    text = fob.read()
    newFile.close()
    return text


def processReq(request):
    ctx = {}
    if request.POST:
        text = request.POST['user_input']
        if text == "":
            myfile = request.FILES.get("user_file", None)
            if not myfile:
                return HttpResponse("no file and no text!")

            text = upload_file(myfile)

        ctx['score'] = round(float(textScore.mainProcess(text)),3)
        ctx['hidden'] = ""
        ctx['text'] = text
        if ctx['score'] <= 0.1:
            ctx['style'] = "danger"
            ctx['grade'] = "BAD"
        if ctx['score'] > 0.1 and ctx['score'] <= 0.25:
            ctx['style'] = "info"
            ctx['grade'] = "NORMAL"
        if ctx['score'] > 0.25 and ctx['score'] <= 0.6:
            ctx['style'] = "success"
            ctx['grade'] = "GOOD"
        if ctx['score'] >0.6:
            ctx['style'] = "success"
            ctx['grade'] = "EXCELLENT"
        print ctx
        return render(request, "index.html", ctx)
    else:
        ctx['hidden'] = "hidden"
        ctx['style'] = "default"
        print ctx
        return render(request, "index.html",ctx)
