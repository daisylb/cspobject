from django.conf import settings

from . import CSPObject


def csp_middleware(get_response):

    base_csp = CSPObject.union(*settings.CONTENT_SECURITY_POLICIES)
    unchanged_csp_string = str(base_csp)

    def middleware(request):
        response = get_response(request)
        # Never set the Content-Security-Policy header if it has already
        # been set by client code.
        if 'Content-Security-Policy' not in response:
            response['Content-Security-Policy'] = unchanged_csp_string
        return response

    return middleware
