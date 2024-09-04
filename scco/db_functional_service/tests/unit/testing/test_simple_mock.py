from pytest_mock import MockerFixture

from testing.simple_mock import outer_function


def test_pytest_mock_works(mocker: MockerFixture):
    assert outer_function() == 42
    mocker.patch(
        "testing.simple_mock.inner_function",
        return_value=10
    )
    assert outer_function() == 10
