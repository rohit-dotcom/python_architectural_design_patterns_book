BLOCKSIZE=65536
import hashlib
import os
from pathlib import Path
import shutil

def sync(source, dest):
    #walk the source folder and build a dict of file name and their hashes
    source_hashes={}
    for folder,_,files in os.walk(source):
        for fn in files:
            source_hashes[hash_file(Path(folder)/fn)]=fn
    
    seen=set() #keep a track of the files we've fond in the target

    #walk the target folder and get the file
    for folder,_,files in os.walk(dest):
        for fn in files:
            dest_path=Path(folder)/fn
            dest_hash=hash_file(dest_path)
            seen.add(dest_hash)

            #if there's a file in the target thats not in the source, delete it!
            if dest_hash not in source_hashes:
                dest_path.remove()

            #if there's a file in target that has a different path in source.
            #move it to the correct path
            elif dest_hash in source_hash and fn!=source_hashes[dest_hash]:
                shutil.move(dest_path,Path(folder)/source_hashes[dest_hash])

            #for every file that appears in the source but not on the target 
            #copy the file to the target

            for source_hash,fn in source_hases.item():
                if source_hash not in seen:
                    shutil.copy(Path(soruce)/fn,Path(dest)/fn)


def hash_file(path):
    hasher=hashlib.sha1()

    with path.open("rb") as file:
        buf=file.read(BLOCKSIZE)
        while buf:
            hasher.update(buf)
            buf=file.read(BLOCKSIZE)
    return hasher.hexdigest()