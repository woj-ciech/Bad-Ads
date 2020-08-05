from django.shortcuts import render
from bpscanner_app.models import *
from bpscanner.tasks import *
from django.http import HttpResponse
import json
from celery.result import AsyncResult

def dashboard(request):
    all_ads = Ad.objects.all()
    search = Search.objects.all()
    people = Person.objects.all()
    bad_ads = Ad.objects.filter(bad=True)
    bad_ads2 = Ad.objects.filter(checked=False, bad=True)
    images = Images.objects.all()

    emails = Person.objects.exclude(email='')
    mobile = Person.objects.exclude(phone='')


    context = {"ads":all_ads, "search":search, "people":people, "bad_ads":bad_ads, "emails":emails,
               "mobile":mobile, "bad_ads2":bad_ads2, "images":images}

    return render(request, "dashboard.html", context=context)

def search(request):
    return render(request, "search.html",{})

def database(request):
    ads = Ad.objects.all()
    context = {"ads":ads}

    return render(request, "database.html", context=context)

def search_city(request, city ):
    if request.is_ajax() and request.method == 'GET':
        print(request)
        search = Search(city=city)
        search.save()

        main_task = search_city_task.delay(fk=search.id, city=city)
        request.session['task_id'] = main_task.task_id
        #
        # return render(request, 'search.html', context={'task_id': gitlab_search_task.task_id, 'type':type})
        return HttpResponse(json.dumps({'task_id': main_task.task_id, "city": city}),
                            content_type='application/json')
    else:
        print('a')
        return HttpResponse(json.dumps({'OK2': '123123'}), content_type='application/json')

def get_task_info(request):
    task_id = request.GET.get('task_id', None)
    try:
        if task_id is not None:
            task = AsyncResult(task_id)
            print(task.result)
            data = {
                'state': task.state,
                'result': task.result,
            }
            return HttpResponse(json.dumps(data), content_type='application/json')
        else:
            return HttpResponse('No job id given.')
    except Exception as e:
        print(e)

def check_person(request):
    if request.is_ajax() and request.method == 'GET':
        link = request.GET["link"]
        ad = Ad.objects.get(link=link)
        ad.checked = True
        ad.save()

        main_task = check_person_task.delay(fk=ad.id, link=link)
        request.session['task_id'] = main_task.task_id
        #
        # return render(request, 'search.html', context={'task_id': gitlab_search_task.task_id, 'type':type})
        return HttpResponse(json.dumps({'task_id': main_task.task_id, "link": link}),
                            content_type='application/json')
    else:
        print('a')
        return HttpResponse(json.dumps({'OK2': '123123'}), content_type='application/json')

def people(request):
    people = Person.objects.all()

    context = {"people": people}

    return render(request, "people.html", context=context)

def check_photo(request):
    if request.is_ajax() and request.method == 'GET':
        link = request.GET["link"]
        ad = Ad.objects.get(link=link)
        Ad.objects.filter(id=ad.id).update(checked_photos=True)
        p = Person.objects.get(ad=ad.id)
        main_task = check_photo_task.delay(fk=p.id, link=link)
        request.session['task_id'] = main_task.task_id
        #
        # return render(request, 'search.html', context={'task_id': gitlab_search_task.task_id, 'type':type})
        return HttpResponse(json.dumps({'task_id': main_task.task_id, "link": link}),
                            content_type='application/json')
    else:
        print('a')
        return HttpResponse(json.dumps({'OK2': '123123'}), content_type='application/json')