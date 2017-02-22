from __future__ import print_function
import sys

from django.conf import settings
from django.http import HttpResponse

try:
    import uwsgi
except:
    print(" *** ERROR: Unable to talk to uWSGI", file=sys.stderr)
    pass

def subscribe(request):
    uwsgi.add_var("CC_USER", str(request.user))
    uwsgi.route("uwsgi", settings.UWSGI_WEBSOCKETS_SOCKET)
    return HttpResponse("output that shouldn't appear")
