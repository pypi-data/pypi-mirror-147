from shapesort import model


def test_text(test_batch):
    tbatch = model.TranscribeBatch(**test_batch)
    tc = tbatch[0]
    text = tc.transcript
    assert isinstance(tc, model.Transcript)
    assert text == "text of transcript"
    assert len(tbatch) == 1

    tbatch = model.TranscribeBatch(**test_batch)
    item = tbatch.results.items[0]
    assert isinstance(item, model.TranscriptItem)
    assert item.start_time == 2.64

    alt = item.alternatives[0]
    assert isinstance(alt, model.ItemAlternative)
    assert item.type == "pronunciation"
