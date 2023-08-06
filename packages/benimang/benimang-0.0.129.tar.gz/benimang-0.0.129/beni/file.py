from pathlib import Path

import aiofiles

import beni
import beni.lock as block

_limit = 50


@block.limit(_limit)
async def write_text(file: Path | str, content: str, encoding: str = 'utf8', newline: str = '\n'):
    if type(file) is not Path:
        file = beni.getpath(file)
    beni.makedir(file.parent)
    async with aiofiles.open(file, 'w', encoding=encoding, newline=newline) as f:
        return await f.write(content)


@block.limit(_limit)
async def write_bytes(file: Path | str, data: bytes):
    if type(file) is not Path:
        file = beni.getpath(file)
    beni.makedir(file.parent)
    async with aiofiles.open(file, 'wb') as f:
        return await f.write(data)


@block.limit(_limit)
async def read_text(file: Path | str, encoding: str = 'utf8', newline: str = '\n'):
    async with aiofiles.open(file, 'r', encoding=encoding, newline=newline) as f:
        return await f.read()


@block.limit(_limit)
async def read_bytes(file: Path | str):
    async with aiofiles.open(file, 'rb') as f:
        return await f.read()


async def md5file(file: Path | str):
    return beni.md5bytes(
        await read_bytes(file)
    )


async def crcfile(file: Path | str):
    return beni.crcbytes(
        await read_bytes(file)
    )
