from utils.calculator import multiply

def test_multiply_simple_case():
    # given
    a = 6
    b = 7

    # when
    result = multiply(a, b)

    # then
    assert result == 42
