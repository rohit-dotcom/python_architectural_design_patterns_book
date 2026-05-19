from sync import sync
from pathlib import Path
import shutil
import tempfile
from sync import determine_actions

def test_when_a_file_exists_in_source_but_not_the_destination():
    source_hashes={"hash1":"fn1"}
    dest_hashes={}
    actions=determine_actions(source_hashes,
                              dest_hashes,
                              Path('src/'),
                              Path('dst/'))

    assert [("COPY",Path('src/fn1'),Path('dst/fn1'))]==list(actions)





def test_when_a_file_is_renamed_in_source():
    source_hashes={"hash1":"fn1"}
    dest_hashes={"hash1":"fn2"}
    actions=determine_actions(source_hashes,
                              dest_hashes,
                              Path('src/'),
                              Path('dst/'))
    assert [("MOVE",Path('dst/fn2'),Path('dst/fn1'))]==list(actions)