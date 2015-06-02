# python 3
# arekm@maven.pl, public domain

import zipfile
import sys
import os
import traceback
import time
import tempfile
import subprocess
import winreg

def winreg_subkeys(key):
    i = 0
    while True:
        try:
            subkey = winreg.EnumKey(key, i)
            yield subkey
            i+=1
        except WindowsError as e:
            break

def winreg_get(key, cmds):
    mainkey = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key, 0, winreg.KEY_READ)

    try:
        kname, kval = winreg.QueryValueEx(mainkey, "InstallLocation")
    except:
        pass
    else:
        if kname.find('DesignSpark') >= 0 or kname.find('SpaceClaim') >= 0:
            cmdsabsat = os.path.join(kname, "SabSatConverter.exe")
            if os.path.exists(cmdsabsat):
                cmds.append(cmdsabsat)

    for subkey in winreg_subkeys(mainkey):
        nkey = key + "\\" + subkey
        winreg_get(nkey, cmds)

def find_dsm_path():
    cmds = []
    key = "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall"
    winreg_get(key, cmds)
    cmds.sort(reverse=True)
    return cmds[0] if len(cmds) else False

def runme():
    sabsat = find_dsm_path()
    if not sabsat:
        print("SabSatConverter.exe not found. Please install DesignSpark Mechanical.")
        sys.exit(1)

    if len(sys.argv) < 2:
        print("Usage: %s <rsdoc file> ...")
        sys.exit(1)

    for archive in sys.argv[1:]:
        try:
            with zipfile.ZipFile(archive, 'r') as mzip:
                archivefile, archiveext = os.path.splitext(archive)
                sab_files = []
                for file in mzip.namelist():
                    bfile, bext = os.path.splitext(file)
                    if bext.lower() == '.sab':
                        sab_files.append(file)

                if len(sab_files) == 0:
                    print("Found 0 sab files in %s." % archive)
                else:
                    nr = 0
                    nrstr = ""
                    if len(sab_files) > 1:
                        nr = 1
                    for file in sab_files:
                        rsdoc_sab = mzip.read(file)
                        tfile = tempfile.NamedTemporaryFile(mode='wb', suffix='.sab', delete=False)
                        tfile.write(rsdoc_sab)
                        tfile.close()
                        if nr:
                            nrstr = "-%d" % nr
                        outfile = archivefile + nrstr + '.sat'
                        cmd = [sabsat, '-i', tfile.name, '-o', outfile, '-v', '8']
                        with open(os.devnull, 'w') as nullf:
                            subprocess.call(cmd, stdout=nullf)
                        os.unlink(tfile.name)
                        nr += 1
        except Exception as e:
            print("Failed to process file %s: %s" % (archive, str(e)))

if __name__ == '__main__':
    try:
        runme()
    except (Exception, KeyboardInterrupt):
        print(sys.exc_info()[0])
        print(traceback.format_exc())
        input("Press Enter to continue ...")
