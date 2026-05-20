from sync import sync
from pathlib import Path
import shutil
import tempfile
from sync import determine_actions


class FakeFileSystem():
    def __init__(self,path_hashes):
        self.path_hashes=path_hashes
        self.action=[]

    def read(self,path):
        return self.path_hashes[path]
    def copy(self,source,dest):
        self.action.append(("COPY",
                                  source,dest))
    
    def move(self,source,dest):
        self.action.append(("MOVE",
                                  source,dest))
    
    def delete(self,dest):
        self.action.append(("DELETE",dest ))


            




def test_when_a_file_exists_in_source_but_not_the_destination():
    fakefs=FakeFileSystem({'/src':{'hash1':'fn1',},'/dst':{}})

    sync('/src','/dst',fakefs)

    assert fakefs.action==[('COPY','/src/fn1',
                      '/dst/fn1')]

def test_when_a_file_is_renamed_in_source():
    fakefs=FakeFileSystem({'/src':{'hash1':'fn1',},'/dst':{'hash1':'fn2'}})

    sync('/src','/dst',fakefs)

    assert fakefs.action==[('MOVE','/dst/fn2',
                      '/dst/fn1')]
