import json

from shapesort.main import main

__author__ = "Taylor Monacelli"
__copyright__ = "Taylor Monacelli"
__license__ = "MPL-2.0"


def test_main(capsys, tmp_path, test_batch):
    """CLI Tests"""
    # capsys is a pytest fixture that allows asserts agains stdout/stderr
    # https://docs.pytest.org/en/stable/capture.html

    path = tmp_path / "test"
    _str = json.dumps(test_batch)
    path.write_text(_str)
    main([str(path)])
    assert "193048895737" in path.read_text()
