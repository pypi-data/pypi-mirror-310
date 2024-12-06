import asyncio
import time
import shutil
import os


async def run_find_files_asyncio(root: str) -> list[str]:
    """
    异步调用 find 命令并返回结果, 仅支持 Linux 系统, 返回文件，不包括目录

    Args:
        root (str): 要扫描的目录

    Returns:
        List[str]: 文件的路径列表
    """
    process = await asyncio.create_subprocess_exec(
        'find', root, '-type', 'f',
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    if process.returncode != 0:
        raise RuntimeError(f"find error: {stderr.decode().strip()}")
    return stdout.decode().strip().split('\n')


async def run_fd_files_asyncio(root: str, allow_find: bool = False) -> list[str]:
    """
    异步调用 fd 或 fdfind 或 find 命令并返回结果，仅支持 Linux 系统，返回文件路径列表，不包括目录。

    Args:
        root (str): 要扫描的目录
        allow_find (bool): 是否允许回退到 find 命令

    Returns:
        List[str]: 文件的路径列表
    """
    # 自动检测可用的命令
    fd_command = shutil.which('fd') or shutil.which('fdfind')

    if fd_command:
        # 使用 fd 或 fdfind
        process = await asyncio.create_subprocess_exec(
            fd_command, '--type', 'f', '--hidden', '--absolute-path', '.',
            root,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await process.communicate()

        if process.returncode != 0:
            raise RuntimeError(f"{fd_command} error: {stderr.decode().strip()}")
        return stdout.decode().strip().split('\n')
    elif allow_find:
        # 回退到 find
        return await run_find_files_asyncio(root)
    else:
        raise RuntimeError("fd or fdfind not found, 'apt install fd-find' can be used to install.")


async def main():
    root_directory = os.path.dirname(os.getcwd())
    start = time.time()
    files = await run_fd_files_asyncio(root_directory)
    print(f"Found {len(files)} files.", time.time() - start)


if __name__ == "__main__":
    asyncio.run(main())
