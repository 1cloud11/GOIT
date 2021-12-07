import asyncio
import shutil
from aiopath import AsyncPath, AsyncPurePosixPath


directory = 'Разобрать'

formats = {'images': ['.jpeg', '.png', '.jpg', '.svg', '.bmp'],
           'videos': ['.avi', '.mp4', '.mov', '.mkv'],
           'documents': ['.doc', '.docx', '.txt',
                         '.pdf', '.xlsx', '.pptx', '.fb2'],
           'music': ['.mp3', '.ogg', '.wav', '.amr', '.m4a'],
           'archives': ['.zip', '.gz', '.tar']}


async def folder_scanner(directory, folders=[AsyncPath('Разобрать'),]):
    path = AsyncPath(directory)
    async for file_ in path.iterdir():
        if await AsyncPath(file_).is_dir():
            folders.append(AsyncPath(file_))
            await folder_scanner(file_)
    return folders


async def folder_creator(directory, get_folders=set()):
    path = AsyncPath(directory)
    async for elem in path.iterdir():
        if not await AsyncPath(elem).is_dir():
            for key in formats:
                if elem.suffix in formats[key]:
                    get_folders.add(key)
        else:
            await folder_creator(elem)
    for elem in get_folders:
        if not await AsyncPath(elem).exists():
            await AsyncPath(elem).mkdir()


async def archive_unpacker(archive):
    shutil.unpack_archive(AsyncPath(archive),
                          'archives' + '\\'
                          + str(AsyncPurePosixPath(archive).stem))
    await AsyncPath(archive).unlink()


async def sort(directory):
    base_folder = AsyncPath().cwd()
    files = AsyncPath(directory)
    async for file_ in files.iterdir():
        for key in formats:
            if file_.suffix in formats[key] and file_.suffix not in formats['archives']:
                target = AsyncPath(
                                str(base_folder)
                                + "\\" + str(key) + '\\'
                                + AsyncPurePosixPath(file_).name
                                )
                await AsyncPath(file_).replace(target)

            elif file_.suffix in formats['archives']:
                try:
                    await archive_unpacker(file_)
                except shutil.ReadError:
                    print(f'{file_} is already unpacked')


async def main():
    await folder_creator(directory)
    directories = await folder_scanner(directory)
    futures = [asyncio.ensure_future(sort(i)) for i in directories]
    await asyncio.wait(futures)


ioloop = asyncio.get_event_loop()
ioloop.run_until_complete(main())
ioloop.close()
