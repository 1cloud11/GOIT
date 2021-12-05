import asyncio
import shutil

from aiopath import AsyncPath
from pathlib import Path, PurePosixPath


directory = 'Разобрать'
path = Path(directory)
base_folder = (Path().cwd()).resolve()
folders = [path, ]


def folder_scanner(path, folders):
    for file_ in path.iterdir():
        if Path.is_dir(file_):
            folders.append(Path(file_))
            folder_scanner(file_, folders)
    return folders


async def sort(directory):
    formats = {'images': ['.jpeg', '.png', '.jpg', '.svg', '.bmp'],
               'videos': ['.avi', '.mp4', '.mov', '.mkv'],
               'documents': ['.doc', '.docx', '.txt',
                             '.pdf', '.xlsx', '.pptx'],
               'music': ['.mp3', '.ogg', '.wav', '.amr', '.m4a'],
               'archives': ['.zip', '.gz', '.tar']}

    files = AsyncPath(directory)
    async for file_ in files.iterdir():
        if file_.suffix in formats['images']:
            if not Path('images').exists():
                Path('images').mkdir()
            target = AsyncPath(
                               str(base_folder)
                               + "\\" + 'images' + '\\'
                               + PurePosixPath(file_).name
                               )
            await AsyncPath(file_).replace(target)

        elif file_.suffix in formats['videos']:
            if not Path('videos').exists():
                Path('videos').mkdir()
            target = AsyncPath(
                               str(base_folder)
                               + "\\" + 'videos' + '\\'
                               + PurePosixPath(file_).name
                               )
            await AsyncPath(file_).replace(target)

        elif file_.suffix in formats['documents']:
            if not Path('documents').exists():
                Path('documents').mkdir()
            target = AsyncPath(
                               str(base_folder)
                               + "\\" + 'documents' + '\\'
                               + PurePosixPath(file_).name
                               )
            await AsyncPath(file_).replace(target)

        elif file_.suffix in formats['music']:
            if not Path('music').exists():
                Path('music').mkdir()
            target = AsyncPath(
                               str(base_folder)
                               + "\\" + 'music' + '\\'
                               + PurePosixPath(file_).name
                               )
            await AsyncPath(file_).replace(target)

        elif file_.suffix in formats['archives']:
            if not Path('archives').exists():
                Path('archives').mkdir()
            shutil.unpack_archive(Path(file_),
                                  'archives' + '\\'
                                  + str(PurePosixPath(file_).stem))
            await AsyncPath(file_).unlink()


async def main():
    directories = folder_scanner(path, folders)
    tasks = [asyncio.ensure_future(sort(i)) for i in directories]
    await asyncio.wait(tasks)


ioloop = asyncio.get_event_loop()
ioloop.run_until_complete(main())
ioloop.close()
