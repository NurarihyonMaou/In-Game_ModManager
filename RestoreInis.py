import os


current_inis = []
backup_inis = []


def collect_ini(folder_path):
    global current_inis
    global backup_inis

    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)

        if 'BufferValues' in file_path:
            continue

        if os.path.isdir(file_path) and 'disabled' not in file_path.lower():
            collect_ini(file_path)
#('DISABLED_ModManagerBackup_' in filename for filenames in os.listdir(folder_path))
        elif any(File.startswith("DISABLED_ModManagerBackup_") for File in os.listdir(folder_path)) and os.path.splitext(filename)[1] == ".ini" and "desktop" not in filename.lower() and "ntuser" not in filename.lower():
            print(os.path.join(folder_path, filename) + '\n')
            if 'DISABLED_ModManagerBackup_' in filename:
                backup_inis.append(os.path.join(folder_path, filename))

            if 'disabled' not in filename.lower():
                current_inis.append(os.path.join(folder_path, filename))


           # if 'disabled' not in filename.lower():
           #     print('Disabling - '+file_path)
           #     filename2 = 'DISABLED'+filename.replace('.ini', '')+'ModManager.ini'
           #     file_path2 = os.path.join(folder_path, filename2)
           #     try:
           #         os.rename(file_path, file_path2)
           #     except Exception as e:
           #         print('Something went Wrong - '+file_path+'\n'+file_path2)
           #         print(f"Error: {e}")
#
           # elif 'DISABLED' in filename and 'ModManager' in filename:
           #     print('Enabling - '+file_path)
           #     filename2 = filename.replace('DISABLED_', '').replace('Backup', '')
           #     file_path2 = os.path.join(folder_path, filename2)
           #     try:
           #         os.rename(file_path, file_path2)
           #     except Exception as e:
           #         print('Something went Wrong - '+file_path+'\n'+file_path2)
           #         print(f"Error: {e}")
#

def delete_inis():

    for current_ini in current_inis:
        print('Deleting - ' + current_ini + '\n')
        try:
            os.remove(current_ini)
        except Exception as e:
            print('Something went Wrong - ' + current_ini + '\n')
            print(f"Error: {e}" + '\n')


def restore_inis():
    for backup_ini in backup_inis:
        backup2 = (backup_ini.replace('DISABLED_ModManagerBackup_', ''))
        if 'disabled' in backup2.lower():
            continue

        print('Enabling - ' + backup_ini + '\n')
        try:
            os.rename(backup_ini, backup2)
        except Exception as e:
            print('Something went Wrong - ' + backup_ini + '\n' + backup2 + '\n')
            print(f"Error: {e}" + '\n')


def main():
    try:
        print(f'Trying to Remove - {os.path.join(os.getcwd(), "ModsIDs.json")}\n')
        os.remove(os.path.join(os.getcwd(), 'ModsIDs.json'))
    except Exception as e:
        print('Something went Wrong\n')
        print(f"Error: {e}" + '\n')

    collect_ini(os.getcwd())
    delete_inis()
    restore_inis()


main()