import pytest

@pytest.mark.fast
@pytest.mark.smoke
def test_import():
    import {{name}}

    print({{name}})
