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

def determine_actions(source_hashes,dest_hashes,source_folder,dest_folder):
    #if file present in source but no in destinations
    for sha,filename in source_folder.items():
        if sha not in dest_hashes:
            yield "COPY",Path(source_folder)/filename,Path(dest_folder)/filename
        
    #if file present in destination but renamed in destination
        elif dest_hashes[sha]!=filename:
            old_dest_path=Path(dest_folder)/dest_hashes[sha]
            new_dest_path=Path(dest_folder)/filename
            yield 'MOVE',old_dest_path,new_dest_path

    #if destnation file not present in source file the delete action
    for sha,filename in dest_hashes.items():
        if sha not in source_hashes:
            yield "DELETE",Path(filename)



