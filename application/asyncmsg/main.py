import sys
import os
import json

from apipkg import queue_manager as queue
sys.dont_write_bytecode = True

import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()

from application.djangoapp.models import *

def test_mq(ch, method, properties, body):
        j = json.loads(body)
        if j['functioname'] == 'catalogue-add-product':
	        print(" [x] Received from queue %r" % body)

def main():
    queue.receive(os.environ['DJANGO_APP_NAME'], test_mq)
    print("Liste des ventes:")
    for v in Vente.objects.all():
        print("ID: " + str(v.id) + "\tArticle: " + v.article.nom + "\tDate: " + str(v.date))


if __name__ == '__main__':
    main()
