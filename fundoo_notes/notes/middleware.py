from django.utils.deprecation import MiddlewareMixin
from notes.models import Log

class RequestLogMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        
        method=request.method
        url=request.path
        try:
            log_entry = Log.objects.get(method=method, url=url)
            log_entry.count += 1
        except Log.DoesNotExist:
            log_entry = Log(method=method, url=url, count=1)
        log_entry.save()

        return response
