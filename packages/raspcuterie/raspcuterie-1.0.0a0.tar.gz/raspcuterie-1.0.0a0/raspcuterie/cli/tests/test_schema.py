from .. import schema


def test_schema(runner):

    result = runner.invoke(schema, catch_exceptions=False)
    assert result.exit_code == 0, result.exception
