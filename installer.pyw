import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog

import os
from importlib.resources import files  #Python 3.9+ is required
from pathlib import Path
import py7zr
from win32com.client import Dispatch
import sys
import time
import shutil

def get_mingw64(progress_bar:ttk.Progressbar, total:int | float):
    mingw64 = files('assets') / 'mingw64.7z'
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
            time.sleep(0.01)

def extract_mingw64(progress_bar:ttk.Progressbar, total:int | float, to:str, var_progress:tk.StringVar):
    var_progress.set('解压编译器文件 0 / 0')
    with py7zr.SevenZipFile(r'C:\install_cache\mingw64.7z', mode='r') as fp:
        file_list = fp.namelist()
        TOTAL_FILES = len(file_list)
        done = 0
        var_progress.set(f'解压编译器文件 0 / {TOTAL_FILES}')

        for f in fp.files:
            fp.extract(targets=[f.filename], path=to)
            done += 1
            progress_bar.step(done / TOTAL_FILES * total)
            var_progress.set(f'解压编译器文件 {done} / {TOTAL_FILES}')
            time.sleep(0.01)

def get_app(progress_bar:ttk.Progressbar, total:int | float):
    app = files('assets') / 'NuitkaGUI.7z'
    BLOCK_SIZE = 1024 ** 2
    FILE_SIZE = 6985023
    done = 0
    with app.open('rb') as fp, open(r'C:\install_cache\app.7z', 'wb') as fn:
        while True:
            data = fp.read(BLOCK_SIZE)
            if not data:
                break
            fn.write(data)
            done += len(data)
            progress_bar.step((done / FILE_SIZE) * total)
            time.sleep(0.01)

def extract_app(progress_bar:ttk.Progressbar, total:int | float, install_dir:str, var_progress:tk.StringVar):
    var_progress.set('解压程序文件 0 / 0')
    with py7zr.SevenZipFile(r'C:\install_cache\app.7z', 'r') as fp:
        file_list = fp.namelist()
        TOTAL_FILES = len(file_list)
        done = 0
        var_progress.set(f'解压程序文件 0 / {TOTAL_FILES}')
        for f in fp.files:
            fp.extract(targets=[f.filename], path=install_dir)
            done += 1
            progress_bar.step(done / TOTAL_FILES * total)
            var_progress.set(f'解压程序文件 {done} / {TOTAL_FILES}')
            time.sleep(0.01)

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
        self.root.title('安装NuitkaGUI')
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
        self.mingw64_path = f'C:\\Users\\{os.getlogin()}\\AppData\\Local\\Nuitka\\Nuitka\\Cache\\downloads\\gcc\\x86_64\\14.2.0posix-19.1.1-12.0.0-msvcrt-r2'

        self.inital_ui()

        self.root.mainloop()
    
    def inital_ui(self):
        self.install_mingw64 = tk.BooleanVar(value=True)
        self.cbtn_0 = ttk.Checkbutton(self.install_config_area, variable=self.install_mingw64,\
                                      offvalue=False, onvalue=True, text='安装MinGW64(GCC version 14.2.0\n (MinGW-W64 x86_64-msvcrt-posix-seh,\n built by Brecht Sanders, r2))')
        self.cbtn_0.grid(column=0, row=0, columnspan=2, sticky='w', padx=5, pady=5)

        self.create_desktop_link = tk.BooleanVar(value=False)
        self.cbtn_1 = ttk.Checkbutton(self.install_config_area, variable=self.create_desktop_link,\
                                      offvalue=False, onvalue=True, text='创建桌面快捷方式')
        self.cbtn_1.grid(column=0, row=1, columnspan=2, sticky='w', padx=5, pady=5)

        self.cerate_startmenu_link = tk.BooleanVar(value=False)
        self.cbtn_2 = ttk.Checkbutton(self.install_config_area, variable=self.cerate_startmenu_link,\
                                      offvalue=False, onvalue=True, text='创建开始菜单快捷方式')
        self.cbtn_2.grid(column=0, row=2, columnspan=2, sticky='w', padx=5, pady=5)

        self.install_path = tk.StringVar(value=r'C:\Program Files\NuitkaGUI')
        self.lb_0 = ttk.Label(self.install_config_area, text='安装目录:')
        self.lb_0.grid(column=0, row=3, padx=5, pady=5)

        self.entry = ttk.Entry(self.install_config_area, textvariable=self.install_path, width=44)
        self.entry.grid(column=1, row=3, padx=5, pady=5)

        self.btn_0 = ttk.Button(self.install_config_area, text='浏览', command=self.browse_install_path)
        self.btn_0.grid(column=2, row=3, padx=5, pady=5)

        self.btn_1 = ttk.Button(self.button_area, text='开始安装', command=self.install)
        self.btn_1.place(x=260, y=20, width=110, height=40)

        self.btn_2 = ttk.Button(self.button_area, text='取消安装', command=sys.exit)
        self.btn_2.place(x=380, y=20, width=110, height=40)

    def browse_install_path(self):
        p = filedialog.askdirectory()
        self.install_path.set(p)
    
    def install(self):
        mingw64 = self.install_mingw64.get()
        startmenu_link = self.cerate_startmenu_link.get()
        desktop_link = self.create_desktop_link.get()
        install_path = self.install_path.get()

        self.install_config_area.destroy()

        self.btn_1.config(state='disabled')
        self.btn_2.config(state='disabled')

        self.install_area = ttk.Frame(self.root)
        self.install_area.place(x=0, y=0, width=500, height=250)
        
        self.install_status = tk.StringVar(value='正在安装')
        self.lb_1 = ttk.Label(self.install_area, textvariable=self.install_status, width=50, justify='right')
        self.lb_1.grid(column=0, row=0)

        self.progress_bar = ttk.Progressbar(self.install_area)
        self.progress_bar.grid(column=0, row=1, sticky='ew')
        if os.path.exists(r'C:\install_cache'):
            shutil.rmtree(r'C:\install_cache')

        os.makedirs(r'C:\install_cache')
        
        if os.path.exists(install_path):
            shutil.rmtree(install_path)

        os.makedirs(install_path)

        self.install_status.set('正在提取应用程序...')

        get_app(self.progress_bar, 5)
        extract_app(self.progress_bar, 20, install_path, self.install_status)

        if startmenu_link:
            self.install_status.set('正在创建开始菜单快捷方式...')
            create_shortcut(os.path.join(install_path, 'NuitkaGUI.exe'), os.path.join(self.startmenu_path, 'NuitkaGUI.lnk'),\
                            'NuitkaGUI')
            time.sleep(0.01)
        
        self.progress_bar.step(1)

        if desktop_link:
            create_shortcut(os.path.join(install_path, 'NuitkaGUI.exe'), os.path.join(self.desktop_path, 'NuitkaGUI.lnk'), description='NuitkaGUI')
            time.sleep(0.01)

        self.progress_bar.step(1)

        if mingw64:
            get_mingw64(self.progress_bar, 13)
            extract_mingw64(self.progress_bar, 60, self.mingw64_path, self.install_status)
        
        else:
            self.progress_bar.step(60)
        
        messagebox.showinfo(title='成功', message='安装完成!')
        time.sleep(5)
        self.root.destroy()
        sys.exit()

if __name__ == '__main__':
    try:
        installer = Installer()
    except Exception as e:
        messagebox.showerror(title='安装失败', message=str(e))
        