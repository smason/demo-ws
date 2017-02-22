from __future__ import print_function
import sys

from django.http import HttpResponse

try:
    import uwsgi
except:
    print(" *** ERROR: Unable to talk to uWSGI", file=sys.stderr)
    pass

def subscribe(request):
    uwsgi.add_var("CC_USER", str(request.user))
    uwsgi.route("uwsgi", "uwsgi-websocket.S,0,0")
    return HttpResponse("output that shouldn't appear")
