import os

import cv2
import requests
from django.core.files.storage import default_storage
from django.shortcuts import render, redirect
from django.urls import reverse


def main(request):
    template = 'main.html'
    context = {}

    return render(request, template, context)


def patient_search(request):
    template = 'misapp/patient_search.html'
    context = {}

    if 'search_patient' in request.POST:
        qrfile = request.FILES.get('qrfile', None)
        if qrfile:
            name = qrfile.name
            path = f"qrcheck.{name.split('.')[-1]}"
            if default_storage.exists(path):
                default_storage.delete(path)
            default_storage.save(path, qrfile)

            qr_file = cv2.imread(os.path.join('media', path))

            detect = cv2.QRCodeDetector()
            value = detect.detectAndDecode(qr_file)

            id_patient = list(value)[0]

            return redirect(to='patients', id_patient=id_patient)

    return render(request, template, context)


def patients(request, id_patient):
    template = 'misapp/patient_update.html'
    context = {}

    URL = request.build_absolute_uri(reverse('api_patients', kwargs={'id_patient': id_patient}))
    response = requests.get(URL)
    patient = response.json()[0]
    context['patient'] = patient

    return render(request, template, context)