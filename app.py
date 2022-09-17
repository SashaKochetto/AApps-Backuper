from sys import platform as sysplat
from os import system, path, getcwd, chdir, walk
from shutil import unpack_archive
import urllib.request
import zipfile

if sysplat == "win32":
    filep = "adb.exe"
elif sysplat == "linux":
    filep = "adb"

def clear_screen():
    if sysplat == "win32":
        a = system("cls")
    elif sysplat == "linux":
        a = system("clear")

path_installed = getcwd()

print("AApps Backuper 1.0.0\n(by SashaKochetto 2022)\n\n")

if not path.exists("saves"):
    a = system("mkdir saves")

if not path.isfile(f"platform-tools\\{filep}"):
    print("The app needs adb to work!")
    if input("Download? [Y/N] ").lower() == "y":
        print("\nDownloading...")
        if sysplat == "win32":
            urllib.request.urlretrieve("https://dl.google.com/android/repository/platform-tools_r33.0.2-windows.zip", "adb.zip")
        elif sysplat == "linux":
            urllib.request.urlretrieve("https://dl.google.com/android/repository/platform-tools_r33.0.2-linux.zip", "adb.zip")
        print("Unpacking archive...")
        unpack_archive("adb.zip")
        if sysplat == "win32":
            a = system("del adb.zip /s /q")
        elif sysplat == "linux":
            a = system("rm adb.zip")
        print("adb installed!\nPress any key to continue...")
        input()
        clear_screen()
        print("AApps Backuper 1.0\n(by SashaKochetto 2022)\n\n")

print("Before proceeding, make sure you have USB debugging enabled on your Android device!\nIf it's enabled, connect your Android device to your computer and press Enter.\n")
a = input()
system(f"platform-tools\\{filep} devices")
print("Allow USB debugging on your Android device and press Enter.")
a = input()

while True:
    clear_screen()
    print("AApps Backuper 1.0.0\n(by SashaKochetto 2022)\n\n")
    print("Select an action:\n1 - Create Backup\n2 - Restore\n3 - Show list installed apps\n4 - Exit")
    a = input()
    if a == "1":
        print("\nEnter application name (Example: com.example.app) (or press Enter to exit to the main menu):")
        name_app = input()
        if name_app == "":
            continue
        chdir("saves")
        print("Getting the .apk file...")
        a = system(f"mkdir {name_app}")
        chdir(name_app)
        a = system(f"\"{path_installed}\\platform-tools\\{filep}\" shell pm path {name_app} > path.aabt")
        with open("path.aabt", "r") as f:
            path_app = f.read().replace("package:", "")
        if sysplat == "win32":
            a = system("del path.aabt /s /q")
        elif sysplat == "linux":
            a = system("rm path.aabt")
        a = system(f"\"{path_installed}\\platform-tools\\{filep}\" pull {path_app}")
        print("Getting data...\n")
        print("Allow backup on Android device")
        a = system(f"\"{path_installed}\\platform-tools\\{filep}\" backup -apk {name_app} -f base.aab")
        chdir("..")
        a = zipfile.ZipFile(f"{name_app}.zip", "w")
        for folder, subfolders, files in walk(path.join(getcwd(), name_app)):
            for file in files:
                a.write(path.join(folder, file), path.relpath(path.join(folder,file), getcwd()), compress_type = zipfile.ZIP_DEFLATED)
        a.close()
        if sysplat == "win32":
            a = system(f"rmdir {name_app} /s /q")
        elif sysplat == "linux":
            a = system(f"rm {name_app} -r")
        chdir("..")
        print(f"\nBackup created!\nName archive: {name_app}.zip\nTo exit to the main menu, press Enter.")
        input()
    elif a == "2":
        print("\nEnter application name (Example: com.example.app) (or press Enter to exit to the main menu):")
        name_app = input()
        if name_app == "":
            continue
        chdir("saves")
        if path.isfile(f"{name_app}.zip"):
            print("Unpacking archive...")
            unpack_archive(f"{name_app}.zip")
            chdir(f"{name_app}")
            print("Installing app...")
            a = system(f"\"{path_installed}\\platform-tools\\{filep}\" install base.apk")
            print("Restoring app data...")
            a = system(f"\"{path_installed}\\platform-tools\\{filep}\" restore base.aab")
            chdir("..")
            if sysplat == "win32":
                a = system(f"rmdir {name_app} /s /q")
            elif sysplat == "linux":
                a = system(f"rm {name_app} -r")
            chdir("..")
            print("\nData restored!\nTo exit to the main menu, press Enter.")
            input()
    elif a == "3":
        system(f"\"{path_installed}\\platform-tools\\{filep}\" shell sh -c 'cmd package list packages -f'")
        print("Press Enter to return to the main menu...")
        input()
    elif a == "4":
        print("Good-bye!")
        if sysplat == "win32":
            a = system("taskkill /im adb.exe /f")
        exit()
exit()
