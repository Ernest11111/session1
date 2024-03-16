import os.path

import requests
from django.conf import settings
from django.core.files.storage import default_storage
from django.db import connection
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt


def dictfetchall(cursor):
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]


@csrf_exempt
def api_patients(request, id_patient=None):
    if not id_patient:
        if request.method == "POST":
            name = request.POST.get("name", '')
            surname = request.POST.get("surname", '')
            patronymic = request.POST.get("patronymic", None)
            photo_title = request.POST.get("photo_file", None)
            photo_file = request.FILES.get("photo_file", '')
            dob = request.POST.get("dob", '')
            gender = request.POST.get("gender", '')
            working_place = request.POST.get("working_place", '')
            phone = request.POST.get("phone", '')
            email = request.POST.get("email", '')
            polis_id = request.POST.get("polis_id", '')
            polis_end_date = request.POST.get("polis_end_date", '')
            polis_company = request.POST.get("polis_company", '')

            with connection.cursor() as cursor:
                cursor.callproc('patients_post', [name, surname, patronymic,
                                                  photo_title, dob, gender, working_place, phone,
                                                  email, polis_id, polis_end_date, polis_company])
                data = dictfetchall(cursor)
                last_id_patient = data[0]['last_id_patient']
                if last_id_patient and photo_file and photo_title:
                    path = os.path.join(settings.MEDIA_ROOT, 'photos', f'{last_id_patient}.{photo_title}')
                    default_storage.save(path, photo_file)
                return JsonResponse(last_id_patient, safe=False)
        else:
            return HttpResponse(status=404)
    else:
        if request.method == "GET":
            with connection.cursor() as cursor:
                cursor.callproc('patients_get_id', [id_patient])
                patient = dictfetchall(cursor)
            return JsonResponse(patient, safe=False)
        elif request.method == "POST":
            URL = request.build_absolute_uri(reverse('api_patients', kwargs={'id_patient': id_patient}))
            response = requests.get(URL)
            patient = response.json()[0]

            name = request.POST.get("name", patient['name'])
            surname = request.POST.get("surname", patient['surname'])
            patronymic = request.POST.get("patronymic", patient['patronymic'])
            photo_title = request.POST.get("photo_file", patient['photo_file'])
            photo_file = request.FILES.get("photo_file", patient['photo_file'])
            dob = request.POST.get("dob", patient['dob'])
            gender = request.POST.get("gender", patient['gender'])
            working_place = request.POST.get("working_place", patient['working_place'])
            phone = request.POST.get("phone", patient['phone'])
            email = request.POST.get("email", patient['email'])
            polis_id = request.POST.get("polis_id", patient['polis_id'])
            polis_end_date = request.POST.get("polis_end_date", patient['polis_end_date'])
            polis_company = request.POST.get("polis_company", patient['polis_company'])

            with connection.cursor() as cursor:
                cursor.callproc('patients_post_id', [name, surname, patronymic,
                                                  photo_title, dob, gender, working_place, phone,
                                                  email, polis_id, polis_end_date, polis_company])
            if id_patient and photo_file and photo_title:
                path = os.path.join(settings.MEDIA_ROOT, 'photos', f'{id_patient}.{photo_title}')
                default_storage.save(path, photo_file)
            return HttpResponse(status=201)
        else:
            return HttpResponse(status=404)


def api_passports(request):
    if request.method == 'GET':
        id_patient = request.GET.get('id_patient', None)
        with connection.cursor() as cursor:
            cursor.callproc('passports_get', [id_patient])
    else:
        return HttpResponse(status=404)


def api_addresses(request):
    if request.method == 'GET':
        id_patient = request.GET.get('id_patient', None)
        with connection.cursor() as cursor:
            cursor.callproc('addresses_get', [id_patient])
    else:
        return HttpResponse(status=404)


def api_organizations(request):
    if request.method == 'GET':
        with connection.cursor() as cursor:
            cursor.callproc('organizations_get')
    else:
        return HttpResponse(status=404)


def api_managers(request):
    if request.method == 'GET':
        with connection.cursor() as cursor:
            cursor.callproc('managers_get')
    else:
        return HttpResponse(status=404)


def api_licenses(request):
    if request.method == 'GET':
        with connection.cursor() as cursor:
            cursor.callproc('licenses_get')
    else:
        return HttpResponse(status=404)
