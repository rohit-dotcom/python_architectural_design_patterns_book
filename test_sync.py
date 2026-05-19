from sync import sync
from pathlib import Path
import shutil
import tempfile

def test_when_a_file_exists_in_source_but_not_the_destination():
    try:
        source=tempfile.mkdtemp()
        dest=tempfile.mkdtemp()

        content="i am a very useful file"
        (Path(source)/"my-file").write_text(content)
        sync(source,dest)
        expected_path=Path(dest)/"my-file"
        assert expected_path.exists()
        assert expected_path.read_text()==content

    finally:
        shutil.rmtree(source)
        shutil.rmtree(dest)

def test_when_a_file_is_renamed_in_source():
    try:
        source=tempfile.mkdtemp()
        dest=tempfile.mkdtemp()
        
        content="i am a renamed file"
        source_path=Path(source)/"source-filename"
        old_dest_path=Path(dest)/"dest_filename"
        expected_dest_path=Path(dest)/"source-filename"
        source_path.write_text(content)
        old_dest_path.write_text(content)

        sync(source,dest)
        
        assert old_dest_path.exists() is False
        assert expected_dest_path.read_text() == content

    finally:
        shutil.rmtree(source)
        shutil.rmtree(dest)
