from hypothesis import given

from . import strategies


@given(strategies.csp_object, strategies.csp_object)
def test_union_operator(csp1, csp2):
    csp1 & csp2


@given(strategies.csp_object, strategies.csp_object)
def test_union_method(csp1, csp2):
    csp1.union(csp2)
