"""
    Dummy conftest.py for shapesort.

    If you don't know what this is for, just leave it empty.
    Read more about conftest.py under:
    - https://docs.pytest.org/en/stable/fixture.html
    - https://docs.pytest.org/en/stable/writing_plugins.html
"""

import pytest


@pytest.fixture(scope="module")
def test_batch():
    dct = {
        "jobName": "ttest",
        "accountId": "193048895737",
        "results": {
            "transcripts": [{"transcript": "text of transcript"}],
            "items": [
                {
                    "start_time": "2.64",
                    "end_time": "3.27",
                    "alternatives": [{"confidence": "0.9448", "content": "Okay"}],
                    "type": "pronunciation",
                },
                {
                    "alternatives": [{"confidence": "0.0", "content": ","}],
                    "type": "punctuation",
                },
            ],
        },
    }
    return dct
