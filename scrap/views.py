import os

from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse
from .tasks import get_categories


def testview(request):
    get_categories.delay()
    return HttpResponse('this is testview')
