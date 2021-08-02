import os
import re
import shutil
from pathlib import Path
from transliterate import translit


directory = 'Разобрать'

def normalize(directory):
    files = os.listdir(directory)
    for name in files:
        name_wo_suf = name[:len(name)-len(Path(name).suffix)] #убираем суфикс чтоб не мешал манипуляциям
        translit_name = translit(name_wo_suf, 'ru', reversed=True) #транслитерация с помощью модуля transliterate
        symbol_corrected ='_'.join(re.split(r'[^\w]', translit_name)) #замена разделителей
        new_name = symbol_corrected + (Path(name).suffix).upper() #возвращаем суфикс подняв его в верхний регистр
        os.rename(directory+'\\'+name, directory+'\\'+new_name) #Непосредственно, переименовываем файл

def sort(directory):
    formats = {'images':['.JPEG', '.PNG', '.JPG', '.SVG'],
               'videos':['.AVI', '.MP4', '.MOV', '.MKV'],
               'documents':['.DOC', '.DOCX', '.TXT', '.PDF', '.XLSX', '.PPTX'],
               'music':['.MP3', '.OGG', '.WAV', '.AMR', '.M4A'],
               'archives':['.ZIP', '.GZ', '.TAR'],
               }



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
            shutil.unpack_archive(str(file_).lower(), 'archives'+'\\'+os.path.splitext(os.path.basename(file_))[0])
        
        elif os.path.isdir(file_):
            sort(file_)
            os.rmdir(file_)

def directory_formats(directory):
    files = Path(directory)
    sorted_formats = []
    unsorted_format = []
    for file_ in files.iterdir():
        if file_.suffix in ['.JPEG', '.PNG', '.JPG', '.SVG', '.AVI', '.MP4', '.MOV', '.MKV', '.DOC', 
                            '.DOCX', '.TXT', '.PDF', '.XLSX', '.PPTX', '.MP3', '.OGG', '.WAV', '.AMR', 
                            '.M4A','.ZIP', '.GZ', '.TAR']:
            sorted_formats.append(file_.suffix)
        elif file_.suffix == '':
            continue
        else:
            unsorted_format.append(file_.suffix)
    sor = ', '.join(set(sorted_formats))
    unsor = ', '.join(set(unsorted_format))
    with open('formats.txt', 'w') as f:
        f.write(f'Founded known formats: {sor}\n')
        f.write(f'Founded unknown formats: {unsor}')


if __name__ == '__main__':
    normalize(directory)
    directory_formats(directory)
    sort(directory)
    