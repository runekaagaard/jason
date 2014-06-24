import simplejson
from django.http import HttpResponse
from django.core import serializers


def response(data={}, status=200, message='OK'):
    """
    Returns a HttpResponse class with json mimetype.

    The data dictionary is serialized using the DjangoJSONEncoder class.

    Example::
        import jason

        def my_view(request):
            return jason.response({'weight': 80}, 200, 'OK')
    """
    response_data = {
        'data': data,
        'status': status,
        'message': message,
    }
    content = simplejson.dumps(response_data, ensure_ascii=False,
                               cls=serializers.json.DjangoJSONEncoder)
    return HttpResponse(content, status=status, content_type='application/json')


def view(allowed_methods, exceptions={}):
    """
    Decorates a Django function based view which in turn should return a
    tuple or list of length 0 to 3 matching the signature of response().

    The view is also allow to raise a Bail() Exception.

    "allowed_methods" lists which HTTP methods are allowed,
    e.g. ['GET', 'POST'].

    "exceptions" is a dictionary that defines what happens when exceptions are
    thrown inside the wrapped function. The keys are Exception classes and
    values are callables. The callables will be called with the exception as
    the first parameter and should return a tuple or list that fits with
    the response() function.

    Example::
        import jason

        @jason.view(allowed_methods=['GET', 'POST'], exceptions={
            WebFault: lambda e: ({}, 400, e.message, )
        })
        def my_view(request):
            return {'numbers': 42, 43, 44},
    """
    def _(f):
        def __(request, *args, **kwargs):
            if request.method not in allowed_methods:
                return response({}, 405, 'Method Not Allowed')
            try:
                return response(*f(request, *args, **kwargs))
            except Bail as e:
                return response(*e.args)
            except Exception as e:
                if e.__class__ in exceptions:
                    return response(*exceptions[e.__class__](e))
                else:
                    return response({}, 500, 'Internal Server Error')
        return __
    return _


def permission_required(perm):
    """
    A json pendant to permission_required. Will return a 401 response if
    the user is not allowed.

    Example::

        import jason

        @jason.permission_required("my_perm")
        def my_view(request):
            ...
    """
    def _(f):
        def __(request, *args, **kwargs):
            if request.user.has_perm(perm):
                return f(request, *args, **kwargs)
            else:
                return response({}, 401, 'Unauthorized')
        return __
    return _


class Bail(Exception):
    """
    If raised inside a view wrapped in json.view, the return will be the
    arguments to the Bail class expanded with json_response().

    Example::
        import jason

        @jason.view(allowed_methods=['GET'])
        def my_view(request):
            if not_to_my_liking():
                raise jason.Bail({}, 400, 'Do not like!')
    """
    def __init__(self, *args):
        self.args = args