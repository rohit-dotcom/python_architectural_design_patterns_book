BLOCKSIZE=65536
import hashlib
import os
from pathlib import Path
import shutil

def sync(source, dest):
    #impetative shell step1, gather inputs
    source_hashes=read_paths_and_hashes(source)
    dest_hashes=read_paths_and_hashes(dest)

    #step 2: call functional core
    actions=determine_actions(source_hashes,dest_hashes,source,dest)

    #imperative shell step2, apply outputs
    for action,*paths in actions:
        if action=="COPY":
            shutil.copy(*paths)
        if action=="MOVE":
            shutil.move(*paths)
        if action=='DELETE':
            os.remove(paths[0])


def read_paths_and_hases(root):

    hashes={}
    for folder,_,files in os.walk(root):
        for fn in files:
            path=Path(folder)/fn
            hash=hash_file(path)
            hashes[hash]=fn
    return hashes


def hash_file(path):
    hasher=hashlib.sha1()

    with path.open("rb") as file:
        buf=file.read(BLOCKSIZE)
        while buf:
            hasher.update(buf)
            buf=file.read(BLOCKSIZE)
    return hasher.hexdigest()