"""
functions require administrator permission
"""

import os
import ctypes
from ctypes import wintypes

import win32file
import win32api
import winioctlcon


class STORAGE_DEVICE_NUMBER(ctypes.Structure):
    _fields_ = [
        ("DeviceType", wintypes.DWORD),
        ("DeviceNumber", wintypes.DWORD),
        ("PartitionNumber", wintypes.DWORD),
    ]


def get_device_number_by_letter(drive_letter: str) -> STORAGE_DEVICE_NUMBER:
    win32_path = f"\\\\.\\{drive_letter}"
    return get_device_number(win32_path)


def get_device_number(win32_path: str) -> STORAGE_DEVICE_NUMBER:
    """
    Requires Administrator privilege

    Usage:

    - get_device_number(r"\\.\C:") # Drive Letter
    - get_device_number(r"\\?\Volume{xxxxxxx-xxxxx-xxxxx-xxx}") # Volume Path
    """
    logical_drive_path = f"\\\\.\\{win32_path}:"
    try:
        hDevice = win32file.CreateFile(
            logical_drive_path,
            win32file.GENERIC_READ | win32file.GENERIC_WRITE,
            win32file.FILE_SHARE_READ | win32file.FILE_SHARE_WRITE,
            None,
            win32file.OPEN_EXISTING,
            0,
            None,
        )

        data = win32file.DeviceIoControl(
            Device=hDevice,
            IoControlCode=winioctlcon.IOCTL_STORAGE_GET_DEVICE_NUMBER,
            InBuffer=None,
            OutBuffer=ctypes.sizeof(STORAGE_DEVICE_NUMBER),
        )

        win32api.CloseHandle(hDevice)

        return STORAGE_DEVICE_NUMBER.from_buffer_copy(data)

    except Exception as e:
        print(f"Error: {e}")
        return -1


def _test():
    drive_letter = os.environ.get("systemdrive", "C").rstrip(":")
    info = get_device_number_by_letter(drive_letter)

    device_number = info.DeviceNumber
    device_type = info.DeviceType
    partition_number = info.PartitionNumber

    if device_number != -1:
        print(f"device number for {drive_letter}: is {device_number}")
        print(f"device type for {drive_letter}: is {device_type}")
        print(f"partition number for {drive_letter}: is {partition_number}")
    else:
        print(f"Failed to get device number for drive {drive_letter}:")


if __name__ == "__main__":
    _test()
