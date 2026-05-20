BLOCKSIZE=65536
import hashlib
import os
from pathlib import Path
import shutil

class FileSystem():

    def read(self,path):
        return read_paths_and_hashes(path)
    
    def copy(self,source,dest):
        shutil.copy(source,dest)

    def move(self,source,dest):
        shutil.move(source,dest)

    def delete(dest):
        os.remove(dest)


def sync(source, dest,filesystem=FileSystem):
    source_hashes=filesystem.read(source)
    dest_hashes=filesystem.read(dest)

    for sha,filename in source_hashes.items():
        if sha not in dest_hashes:
            filesystem.copy(Path(source)/filename,Path(dest)/filename)
        elif filename!=dest_hashes[sha]:
            filesystem.move(Path(dest)/dest_hashes[sha],Path(dest)/filename)
    
    for sha,filename in dest_hashes.items():
        if sha not in source_hashes:
            os.remove(dest/filename)


def read_paths_and_hashes(root):

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
    for sha,filename in source_hashes.items():
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
            yield "DELETE",Path(dest_folder)/filename


