import os
import sys

# put the Django project on sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../")))

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../apps")))

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../ext")))
os.environ["DJANGO_SETTINGS_MODULE"] = "hello_newsroom.configs.common.settings"

from django.core.handlers.wsgi import WSGIHandler
application = WSGIHandler()
