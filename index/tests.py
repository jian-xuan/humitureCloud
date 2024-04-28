# from django.test import TestCase
from index import models
from django.shortcuts import render, redirect

from index import models
from django.http import FileResponse, JsonResponse, HttpResponse
import os

from index.untils import judge_filepath, format_size
from django.utils import timezone
from django.utils.http import urlquote
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
import shutil

# Create your views here.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

dev_obj = models.DevInfo.objects
print(dev_obj)