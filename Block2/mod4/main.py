import concurrent.futures
import os
from pathlib import Path
import shutil


directory = 'Разобрать'
folders = [os.path.abspath(directory), ]


def folder_scanner(directory):
    files = Path(directory)
    directories = []
    for file_ in files.iterdir():
        if os.path.isdir(file_):
            directories.append(os.path.abspath(file_))
            folder_scanner(file_)
    return directories


def sort(directory):
    formats = {'images': ['.jpeg', '.png', '.jpg', '.svg', '.bmp'],
               'videos': ['.avi', '.mp4', '.mov', '.mkv'],
               'documents': ['.doc', '.docx', '.txt',
                             '.pdf', '.xlsx', '.pptx'],
               'music': ['.mp3', '.ogg', '.wav', '.amr', '.m4a'],
               'archives': ['.zip', '.gz', '.tar']}

    files = Path(directory)
    for file_ in files.iterdir():
        if file_.suffix in formats['images']:
            if not os.path.exists('images'):
                os.mkdir('images')
            os.replace(file_, 'images'+'\\'+os.path.basename(file_))

        elif file_.suffix in formats['videos']:
            if not os.path.exists('videos'):
                os.mkdir('videos')
            os.replace(file_, 'videos'+'\\'+os.path.basename(file_))

        elif file_.suffix in formats['documents']:
            if not os.path.exists('documents'):
                os.mkdir('documents')
            os.replace(file_, 'documents'+'\\'+os.path.basename(file_))

        elif file_.suffix in formats['music']:
            if not os.path.exists('music'):
                os.mkdir('music')
            os.replace(file_, 'music'+'\\'+os.path.basename(file_))

        elif file_.suffix in formats['archives']:
            if not os.path.exists('archives'):
                os.mkdir('archives')
            shutil.unpack_archive(os.path.abspath(file_), 'archives'+'\\'+str(os.path.splitext(os.path.basename(file_))[0]))
            os.remove(os.path.abspath(file_))


if __name__ == '__main__':
    included_folders = folder_scanner(directory)
    folders = folders + included_folders

    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        executor.map(sort, folders)
