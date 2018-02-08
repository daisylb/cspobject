from .. import CSPObject


def test_empty_cspobject_is_empty():
    csp = CSPObject()
    assert str(csp) == ""


def test_blank_sandbox():
    csp = CSPObject(sandbox=True)
    assert str(csp) == "sandbox"


def test_sandbox_with_exceptions():
    csp = CSPObject(sandbox=('allow-scripts',))
    assert str(csp) == "sandbox allow-scripts"
