from celery.result import AsyncResult
from django.shortcuts import render
from django.http import JsonResponse
from django.views.generic import View

from .tasks import get_categories


class HomeView(View):

    def get(self, request):
        return render(request, 'scrap/index.html')

    def post(self, request):
        r = get_categories.delay()
        response = dict(task_id=r.task_id)
        return JsonResponse(response)


def check_task(request):
    response = dict(status='', is_ready='')
    task_id = request.GET.get('id')
    if task_id:
        res = AsyncResult(task_id)
        response.update(status=res.status, is_ready=res.ready())
    return JsonResponse(response)
