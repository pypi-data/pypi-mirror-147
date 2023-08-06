import os,sys,ctypes
from os import path
try:

    #dev_path = 'X:\\AYEDEK\\Software Projects\\pyfirmwareman\\pyfirmwareman'
    #print("DEV MODE ADDING PATH",dev_path)
    #sys.path.append(dev_path)

    # Current Working Directory
    cwd = os.getcwd()
    os.add_dll_directory(cwd)
    #print(cwd)

    #os.add_dll_directory("C:\\MinGW\\bin\\")
    #os.add_dll_directory("X:\\AYEDEK\\Software Projects\\pyfirmwareman\\pyfirmwareman\\")
    #dll_file_path = "X:\\AYEDEK\\Software Projects\\pyfirmwareman\\pyfirmwareman\\capifwb.so"
    # An exception occurred while loading dll Could not find module ' hatası alırsak minigw kur.

    dll_file_path = "capifwb.so"
    lib = ctypes.cdll.LoadLibrary(dll_file_path)
    print(dll_file_path,"dll is loaded successfully")
except Exception as e:
        print("An exception occurred while loading dll", e)
        print("Failed to load dll at:", dll_file_path)
        quit()

