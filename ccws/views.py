from django.http import HttpResponse

try:
    import uwsgi
except:
    pass

def subscribe(request):
    uwsgi.add_var("CC_USER", str(request.user))
    uwsgi.route("uwsgi", "/tmp/foo,0,0")
    return HttpResponse("output that shouldn't appear")
