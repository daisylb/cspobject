from .. import CSPObject


def test_normal_request_behaves_normally(client):
    resp = client.get('/')
    assert resp.status_code == 200
    assert 'Content-Security-Policy' not in resp


def test_csp_object_is_attached(client, settings):
    settings.MIDDLEWARE += ['cspobject.django.csp_middleware']
    settings.CONTENT_SECURITY_POLICIES = [
        'default-src http:',
        'default-src https:',
    ]
    resp = client.get('/')
    print(repr(resp['Content-Security-Policy']))
    resp_csp = CSPObject.parse(resp['Content-Security-Policy'])
    assert resp_csp == CSPObject(default_src=('http:', 'https:'))
