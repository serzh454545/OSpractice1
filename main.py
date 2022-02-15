import win32api
import win32file

DRIVE_TYPES = """
0     Unknown
1     No Root Directory
2     Removable Disk
3     Local Disk
4     Network Drive
5     Compact Disc
6     RAM Disk
"""

drive_types = dict((int(i), j) for (i, j) in (l.split("\t") for l in DRIVE_TYPES.splitlines() if l))


def get_drives_info():
    drive_list = win32api.GetLogicalDriveStrings()
    drive_list = drive_list.split("\x00")[0:-1]
    dict_drives = {}
    for drive in drive_list:
        drive_type = win32file.GetDriveType(drive)
        drive_size = win32file.GetDiskFreeSpace(drive)
        drive_volume = win32file.GetVolumePathName(drive)
        dict_drives[str(drive)] = {
            'type': drive_types[drive_type],
            'size': round((drive_size[0] * drive_size[1] * drive_size[3]) / (1024 * 1024 * 1024), 1),
            'free_size': round(drive_size[0] * drive_size[1] * drive_size[2] / (1024 * 1024 * 1024), 1),
            'volume_label': drive_volume if drive_volume != drive else "Don't have volume label"
        }
    return dict_drives


drives_data = get_drives_info()
for disk in drives_data.keys():
    s = f'''
    Название: {disk}
    Тип: {drives_data[disk]['type']}
    Пространство: {drives_data[disk]['size']} GiB
    Свободное пространство: {drives_data[disk]['free_size']} GiB
    Метка: {drives_data[disk]['volume_label']}
    '''
    print(s)