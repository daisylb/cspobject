from .. import CSPObject


def test_equality():
    a = CSPObject(default_src=('https:',))
    b = CSPObject(default_src=('https:',))
    assert a == b


def test_union():
    a = CSPObject(default_src=('http:',))
    b = CSPObject(default_src=('https:',))
    assert a & b == CSPObject(default_src=('http:', 'https:'))


def test_union_fallback():
    a = CSPObject(default_src=('http:',))
    b = CSPObject(script_src=('https:',))
    assert a & b == CSPObject(default_src=('http:',),
                              script_src=('http:', 'https:'))


def test_union_child_src_fallback():
    a = CSPObject(child_src=('http:',))
    b = CSPObject(frame_src=('https:',))
    assert a & b == CSPObject(child_src=('http:',),
                              frame_src=('http:', 'https:'))


def test_union_no_fallback_when_both_specified():
    a = CSPObject(default_src=('http:',), script_src=('https:',))
    b = CSPObject(script_src=('https:',))
    assert a & b == CSPObject(default_src=('http:',),
                              script_src=('https:',))


def test_union_sandbox_removed():
    a = CSPObject(sandbox=True)
    b = CSPObject()
    assert a & b == CSPObject()


def test_union_sandbox_kept():
    a = CSPObject(sandbox=True)
    b = CSPObject(sandbox=True)
    assert a & b == CSPObject(sandbox=True)


def test_union_sandbox_exceptions_additive():
    a = CSPObject(sandbox='allow-scripts')
    b = CSPObject(sandbox='allow-same-origin')
    assert a & b == CSPObject(sandbox='allow-scripts allow-same-origin')
