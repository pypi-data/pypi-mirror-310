from collections.abc import Generator
from typing import Any

from winsys._kernel32 import FindFirstVolume, FindNextVolume
from win32api import GetLogicalDrives
from win32com.client import GetObject
from win32file import GetDiskFreeSpaceEx


def volumes() -> list[str]:
    """
    List volumes.

    Unlike logical drive letters, amount of volumes are not limited.

    In NTFS, you can [mount volume on directories](https://learn.microsoft.com/en-us/windows/win32/fileio/volume-mount-points).
    """
    handle, first = FindFirstVolume()
    volumes = [first]

    while (volume := FindNextVolume(handle)) and isinstance(volume, str):
        volumes.append(volume)

    return volumes


def logical_drives() -> Generator[str, Any, None]:
    """
    This yields each existing logical drive letter in order from A-Z.
    """
    bit_mask = GetLogicalDrives()
    for offset in range(26):
        alpha = chr(ord("A") + offset)
        if (1 << offset) & bit_mask:
            yield alpha


def logical_drives_list() -> list[str]:
    """
    Returns a `list` containing each existing logical drive letter in order from A-Z.
    """
    return list(logical_drives())


def diskdrive_info():
    """
    List all diskdrive information
    """

    wmi = GetObject(r"winmgmts:\\.\root\cimv2")
    disks = wmi.ExecQuery("SELECT * FROM Win32_DiskDrive")

    disk_info = {disk.Index: disk.Model for disk in disks}
    return disk_info


def disk_free_space(driveletter: str):
    """
    May raise `pywintypes.error`
    """

    driveletter = driveletter.upper()
    return tuple(
        map(lambda size: size / (1024**3), GetDiskFreeSpaceEx(f"{driveletter}:"))
    )
