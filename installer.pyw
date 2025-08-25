import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

import os
from importlib.resources import files  #Python 3.9+ is required
from pathlib import Path
import py7zr

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

def extract_app(progress_bar:ttk.Progressbar, total:int | float, to:str):
    ...