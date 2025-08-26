import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

import os
from importlib.resources import files  #Python 3.9+ is required
from pathlib import Path
import py7zr
from win32com.client import Dispatch

def get_mingw64(progress_bar:ttk.Progressbar, total:int | float):
    mingw64 = files('') / 'assets/mingw64.7z'
    BLOCK_SIZE = 1024 ** 2
    FILE_SIZE = 167169998
    done = 0

    with mingw64.open('rb') as fp, open(r'C:\install_cache\mingw64.7z', 'wb') as fn:
        while True:
            data = fp.read(BLOCK_SIZE)
            if not data:
                break
            fn.write(data)
            done += len(data)
            progress_bar.step((done / FILE_SIZE) * total)

def extract_mingw64(progress_bar:ttk.Progressbar, total:int | float, to:str, var_done:tk.StringVar, var_total:tk.StringVar):
    var_done.set('0')
    with py7zr.SevenZipFile(r'C:\install_cache\mingw64.7z', mode='r') as fp:
        file_list = fp.namelist()
        TOTAL_FILES = len(file_list)
        done = 0
        var_total.set(str(len(file_list)))

        for f in fp.files:
            fp.extract(targets=[f.filename], path=to)
            done += 1
            progress_bar.step(done / TOTAL_FILES * total)
            var_done.set(str(done))

def get_app(progress_bar:ttk.Progressbar, total:int | float):
    app = files('') / 'assets/NuitkaGUI.7z'
    BLOCK_SIZE = 1024 ** 2
    FILE_SIZE = 6978352
    done = 0
    with app.open('rb') as fp, open(r'C:\install_cache\app.7z', 'wb') as fn:
        while True:
            data = fp.read(BLOCK_SIZE)
            if not data:
                break
            fn.write(data)
            done += len(data)
            progress_bar.step((done / FILE_SIZE) * total)

def extract_app(progress_bar:ttk.Progressbar, total:int | float, install_dir:str):
    with py7zr.SevenZipFile(r'C:\install_cache\app.7z', 'r') as fp:
        file_list = fp.namelist()
        TOTAL_FILES = len(file_list)
        done = 0
        for f in fp.files:
            fp.extract(targets=[f.filename], path=install_dir)
            done += 1
            progress_bar.step(done / TOTAL_FILES * total)

def create_shortcut(target_path:str, shortcut_path:str, description='', working_dir='', icon_path=''):
    shell = Dispatch('WScript.Shell')
    shortcut = shell.CreateShortCut(shortcut_path)
    shortcut.Targetpath = target_path
    shortcut.Description = description
    if working_dir:
        shortcut.WorkingDirectory = working_dir
    if icon_path:
        shortcut.IconLocation = icon_path
    shortcut.save()

class Installer:
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry('500x350+200+200')
        self.root.resizable(False, False)
        self.theme = 'vista'

        self.style = ttk.Style()
        self.style.theme_use(self.theme)
        self.style.configure("TFrame", background="#f0f0f0")
        self.style.configure("TButton", font=('Consolas', 10), padding=5)
        self.style.configure("TLabel", background="#f0f0f0", font=('Consolas', 10))
        self.style.configure("TEntry", font=('Consolas', 10))
        self.style.configure("TCheckbutton", background="#f0f0f0", font=('Consolas', 10))
        #self.style.configure("TRadiobutton", background="#f0f0f0", font=('Consolas', 10))

        self.install_config_area = ttk.Frame(self.root)
        self.install_config_area.place(x=0, y=0, width=500, height=250)

        self.button_area = ttk.Frame(self.root)
        self.button_area.place(x=0, y=250, width=500, height=100)

        self.desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop')
        self.startmenu_path = os.path.join(os.getenv("APPDATA"), "Microsoft", "Windows", "Start Menu", "Programs") # type: ignore
        self.mingw64_path = f'C:\\Users\\{os.getlogin()}\\AppData\\Local\\Nuitka\\Nuitka\\Cache\\DOWNLO~1\\gcc\\x86_64\\14.2.0posix-19.1.1-12.0.0-msvcrt-r2'

        self.inital_ui()
    
    def inital_ui(self):
        self.install_mingw64 = tk.BooleanVar(value=True)
        self.cbtn_0 = ttk.Checkbutton(self.install_config_area, variable=self.install_mingw64,\
                                      offvalue=False, onvalue=True, text='安装MinGW64(GCC version 14.2.0 (MinGW-W64 x86_64-msvcrt-posix-seh, built by Brecht Sanders, r2))')
        self.cbtn_0.grid(column=0, row=0, columnspan=2)

        self.create_desktop_link = tk.BooleanVar(value=False)