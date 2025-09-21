import pytest


def test_src_importable():
    try:
        from src import main

        main.main()
    except ImportError:
        pytest.fail(
            (
                "Папка src не доступна для импорта!"
                " Убедитесь, что PYTHONPATH настроен."
            )
        )
