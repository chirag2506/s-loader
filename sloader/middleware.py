from __future__ import absolute_import, division, print_function

try:
    from threading import local
except ImportError:
    from django.utils._threading_local import local

_thread_locals = local()

def get_current_request():
    return getattr(_thread_locals, "request", None)

def get_current_user():

    request = get_current_request()
    if request:
        return getattr(request, "user", None)

class ThreadLocalMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_request(self, request):
        _thread_locals.request = request

    def process_response(self, request, response):
        if hasattr(_thread_locals, 'request'):
            del _thread_locals.request
        return response


# try:
#     from threading import local
# except ImportError:
#     from django.utils._threading_local import local
#
# _user = local()
#
# class CurrentUserMiddleware(object):
#     def process_request(self, request):
#         _user.value = request.user
#
# def get_current_user():
#     return _user.value
