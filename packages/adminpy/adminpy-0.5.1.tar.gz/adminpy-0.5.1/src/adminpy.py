#Module for system platform listing and admin privilege for needed scripts
'''
adminpy module
V0.5.0 21/4/22
leezhiwei
'''
import platform
SysPlat = platform.system()
Admin = False
def sysinfo():
    if SysPlat == "Windows":
        print("You are running a Windows-based system.")
    elif SysPlat in ['Darwin', 'Linux', 'FreeBSD']:
        print("You are running a *NIX system")
    else:
        print("I have no idea what your system's OS is, please report this issue to https://github.com/leezhiwei/adminpy")
def admincheck():
    if SysPlat == "Windows":
        print("Runnning on Windows, continuing.")
        import pyuac
        Admin = pyuac.isUserAdmin()
        if Admin == False:
            print("No")
        elif Admin == True:
            print("Yes")
    elif SysPlat in ['Darwin', 'Linux', 'FreeBSD']:
        print("You are running a *NIX system, continuing")
        import os, sys
        if not os.geteuid()==0:
            print("No")
        else:
            print("Yes")
    else:
        print("Unable to continue, unknown system OS type, please report this issue to https://github.com/leezhiwei/adminpy")
def runadmin(cmdLine=None, wait=True):
    if SysPlat == "Windows":
        import pyuac
        if not pyuac.isUserAdmin():
            import ctypes, sys
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
        elif pyuac.isUserAdmin():
            print("Already running as admin")
    elif SysPlat in ['Darwin', 'Linux', 'FreeBSD']:
        import os, sys
        if not os.geteuid()==0:
            AdminPrivilege = 0
        else:
            AdminPrivilege = 1
        if AdminPrivilege == 1:
            print("Already running as admin")
        else:
            import subprocess
            sudocheck = subprocess.getoutput('sudo')
            print(sudocheck)
            if "usage" in sudocheck:
              os.execvp("sudo", ["sudo"] + ["python3"] + sys.argv)
            else:
                print("Sudo is not installed, please install sudo or manually run this script as root.")