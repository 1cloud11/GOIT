import os
import re
import shutil
from pathlib import Path
from transliterate import translit


directory = 'Разобрать'


def normalize(directory):
    files = os.listdir(directory)
    for name in files:
        # убираем суфикс чтоб не мешал манипуляциям
        name_wo_suf = name[:len(name)-len(Path(name).suffix)]
        # транслитерация с помощью модуля transliterate
        translit_name = translit(name_wo_suf, 'ru', reversed=True)
        # замена разделителей
        symbol_corrected = '_'.join(re.split(r'[^\w]', translit_name))
        # возвращаем суфикс опустив его в нижний регистр
        new_name = symbol_corrected + (Path(name).suffix).lower()
        # Непосредственно, переименовываем файл
        os.rename(str(directory)+'\\'+str(name), str(directory)+'\\'+str(new_name))


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

        elif os.path.isdir(file_):
            normalize(file_)
            sort(file_)
            os.rmdir(file_)


if __name__ == '__main__':
    normalize(directory)
    sort(directory)
