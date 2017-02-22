from django.http import HttpResponse

import uwsgi

def subscribe(request):
    uwsgi.add_var("CC_USER", str(request.user))
    uwsgi.route("uwsgi", "/tmp/foo,0,0,sam")
    return HttpResponse()
