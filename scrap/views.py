import os

from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse
from selenium import webdriver


def testview(request):
    # driver_path = os.path.join(settings.BASE_DIR, 'bin/geckodriver')
    # browser = webdriver.Firefox(executable_path=driver_path)
    # browser.get('http://m.irr.ru/food/')
    # msg = browser.title
    return HttpResponse('this is testview')
