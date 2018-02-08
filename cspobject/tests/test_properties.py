from hypothesis import given

from . import strategies
from .. import CSPObject


@given(strategies.csp_object, strategies.csp_object)
def test_union_operator(csp1, csp2):
    csp1 | csp2  # noqa


@given(strategies.csp_object, strategies.csp_object)
def test_union_method(csp1, csp2):
    csp1.union(csp2)  # noqa


@given(strategies.csp_object)
def test_string_parse_round_trip(csp):
    csp_str = str(csp)
    csp2 = CSPObject.parse(csp_str)
    assert csp == csp2
