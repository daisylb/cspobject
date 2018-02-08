from .. import CSPObject


def test_constructor_takes_lists():
    csp = CSPObject(default_src=['https://foo', 'https://bar'])
    assert csp.default_src == frozenset(('https://foo', 'https://bar'))


def test_constructor_takes_strings():
    csp = CSPObject(default_src='https://foo https://bar')
    assert csp.default_src == frozenset(('https://foo', 'https://bar'))


def test_constructor_takes_strings_sandbox():
    csp = CSPObject(sandbox='allow-scripts allow-same-origin')
    assert csp.sandbox == frozenset(('allow-scripts', 'allow-same-origin'))
