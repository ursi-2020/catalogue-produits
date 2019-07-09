import sys
import os
import django
from ..myapp.models import *

sys.dont_write_bytecode = True
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

django.setup()

for q in Question.objects.all():
    print("ID: " + str(q.id) + "\tQuestion: " + q.question_text)
