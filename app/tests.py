from app.functions import hello_function


def test_hello_function_does_something():
    input = 'someone'
    result = hello_function(input)
    assert len(result) > len(input)


def test_hello_function_says_hello():
    input = 'someone else'
    result = hello_function(input)
    assert result.startswith('Hello')
