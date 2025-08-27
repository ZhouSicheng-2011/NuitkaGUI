import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog

import os
from importlib.resources import files  # Python 3.9+ is required
import py7zr
from win32com.client import Dispatch
import sys
import time
import shutil
from win32api import SetFileAttributes
from win32con import FILE_ATTRIBUTE_NORMAL
import threading
import queue
import traceback

class Installer:
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry('500x350+200+200')
        self.root.resizable(False, False)
        self.root.title('安装NuitkaGUI')
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # 初始化变量
        self.installing = False
        self.install_thread = None
        self.queue = queue.Queue()
        self.total_progress = 0
        self.current_step = 0
        self.total_steps = 100
        
        # 路径设置
        self.desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop')
        self.startmenu_path = os.path.join(os.getenv("APPDATA"), "Microsoft", "Windows", "Start Menu", "Programs") # type: ignore
        self.mingw64_path = f'C:\\Users\\{os.getlogin()}\\AppData\\Local\\Nuitka\\Nuitka\\Cache\\downloads\\gcc\\x86_64\\14.2.0posix-19.1.1-12.0.0-msvcrt-r2'
        
        # 设置样式
        self.setup_style()
        
        # 创建UI
        self.create_ui()
        
        # 开始处理队列消息
        self.process_queue()
        
        self.root.mainloop()
    
    def setup_style(self):
        self.style = ttk.Style()
        self.style.theme_use('vista')
        self.style.configure("TFrame", background="#f0f0f0")
        self.style.configure("TButton", font=('Consolas', 10), padding=5)
        self.style.configure("TLabel", background="#f0f0f0", font=('Consolas', 10))
        self.style.configure("TEntry", font=('Consolas', 10))
        self.style.configure("TCheckbutton", background="#f0f0f0", font=('Consolas', 10))
    
    def create_ui(self):
        # 创建配置区域
        self.install_config_area = ttk.Frame(self.root)
        self.install_config_area.place(x=0, y=0, width=500, height=250)
        
        # 创建按钮区域
        self.button_area = ttk.Frame(self.root)
        self.button_area.place(x=0, y=250, width=500, height=100)
        
        # 初始化UI组件
        self.init_config_ui()
    
    def init_config_ui(self):
        # MinGW64安装选项
        self.mingw64 = tk.BooleanVar(value=True)
        self.cbtn_0 = ttk.Checkbutton(
            self.install_config_area, 
            variable=self.mingw64,
            text='安装MinGW64(GCC version 14.2.0\n (MinGW-W64 x86_64-msvcrt-posix-seh,\n built by Brecht Sanders, r2))'
        )
        self.cbtn_0.grid(column=0, row=0, columnspan=2, sticky='w', padx=5, pady=5)
        
        # 桌面快捷方式选项
        self.create_desktop_link = tk.BooleanVar(value=False)
        self.cbtn_1 = ttk.Checkbutton(
            self.install_config_area, 
            variable=self.create_desktop_link,
            text='创建桌面快捷方式'
        )
        self.cbtn_1.grid(column=0, row=1, columnspan=2, sticky='w', padx=5, pady=5)
        
        # 开始菜单快捷方式选项
        self.cerate_startmenu_link = tk.BooleanVar(value=False)
        self.cbtn_2 = ttk.Checkbutton(
            self.install_config_area, 
            variable=self.cerate_startmenu_link,
            text='创建开始菜单快捷方式'
        )
        self.cbtn_2.grid(column=0, row=2, columnspan=2, sticky='w', padx=5, pady=5)
        
        # 安装目录选择
        self.install_path = tk.StringVar(value=r'C:\Program Files\NuitkaGUI')
        self.lb_0 = ttk.Label(self.install_config_area, text='安装目录:')
        self.lb_0.grid(column=0, row=3, padx=5, pady=5)
        
        self.entry = ttk.Entry(self.install_config_area, textvariable=self.install_path, width=44)
        self.entry.grid(column=1, row=3, padx=5, pady=5)
        
        self.btn_0 = ttk.Button(self.install_config_area, text='浏览', command=self.browse_install_path)
        self.btn_0.grid(column=2, row=3, padx=5, pady=5)
        
        # 开始安装和取消按钮
        self.btn_1 = ttk.Button(self.button_area, text='开始安装', command=self.start_installation)
        self.btn_1.place(x=260, y=20, width=110, height=40)
        
        self.btn_2 = ttk.Button(self.button_area, text='取消安装', command=self.on_closing)
        self.btn_2.place(x=380, y=20, width=110, height=40)
    
    def browse_install_path(self):
        path = filedialog.askdirectory()
        if path:
            self.install_path.set(path)
    
    def on_closing(self):
        if self.installing:
            if messagebox.askokcancel("退出", "安装正在进行中，确定要退出吗？"):
                self.root.destroy()
                sys.exit()
        else:
            self.root.destroy()
            sys.exit()
    
    def start_installation(self):
        self.installing = True
        
        # 禁用按钮
        self.btn_1.config(state='disabled')
        self.btn_2.config(state='disabled')
        
        # 隐藏配置区域，显示安装进度区域
        self.install_config_area.destroy()
        
        # 创建安装进度区域
        self.install_area = ttk.Frame(self.root)
        self.install_area.place(x=0, y=0, width=500, height=250)
        
        # 安装状态标签
        self.install_status = tk.StringVar(value='准备安装...')
        self.lb_status = ttk.Label(self.install_area, textvariable=self.install_status, width=50, justify='left')
        self.lb_status.grid(column=0, row=0, padx=10, pady=10, sticky='w')
        
        # 进度条
        self.progress_bar = ttk.Progressbar(self.install_area, mode='determinate', maximum=100)
        self.progress_bar.grid(column=0, row=1, padx=10, pady=10, sticky='ew')
        
        # 进度百分比标签
        self.progress_percent = tk.StringVar(value='0%')
        self.lb_percent = ttk.Label(self.install_area, textvariable=self.progress_percent)
        self.lb_percent.grid(column=0, row=2, padx=10, pady=5, sticky='e')
        
        # 启动安装线程
        self.install_thread = threading.Thread(target=self.installation_worker)
        self.install_thread.daemon = True
        self.install_thread.start()
    
    def process_queue(self):
        """处理从工作线程发送到主线程的消息"""
        try:
            while True:
                msg = self.queue.get_nowait()
                if msg[0] == 'progress':
                    self.update_progress(msg[1])
                elif msg[0] == 'status':
                    self.install_status.set(msg[1])
                elif msg[0] == 'complete':
                    self.installation_complete()
                elif msg[0] == 'error':
                    self.installation_error(msg[1])
        except queue.Empty:
            pass
        finally:
            self.root.after(100, self.process_queue)
    
    def update_progress(self, increment):
        """更新进度条"""
        self.total_progress += increment
        if self.total_progress > 100:
            self.total_progress = 100
        self.progress_bar['value'] = self.total_progress
        self.progress_percent.set(f"{int(self.total_progress)}%")
    
    def installation_complete(self):
        """安装完成处理"""
        self.installing = False
        self.progress_bar['value'] = 100
        self.progress_percent.set("100%")
        self.install_status.set("安装完成!")
        messagebox.showinfo(title='成功', message='安装完成!')
        self.root.after(2000, self.root.destroy)  # 2秒后关闭窗口
    
    def installation_error(self, error_msg):
        """安装错误处理"""
        self.installing = False
        messagebox.showerror(title='安装失败', message=error_msg)
        self.btn_1.config(state='normal')
        self.btn_2.config(state='normal')
    
    def send_progress(self, increment):
        """发送进度更新到队列"""
        self.queue.put(('progress', increment))
    
    def send_status(self, status):
        """发送状态更新到队列"""
        self.queue.put(('status', status))
    
    def send_complete(self):
        """发送安装完成消息到队列"""
        self.queue.put(('complete',))
    
    def send_error(self, error_msg):
        """发送错误消息到队列"""
        self.queue.put(('error', error_msg))
    
    def installation_worker(self):
        """在后台线程中执行安装工作"""
        try:
            # 获取安装配置
            install_path = self.install_path.get()
            install_mingw64 = self.mingw64.get()
            create_desktop_link = self.create_desktop_link.get()
            create_startmenu_link = self.cerate_startmenu_link.get()
            
            # 准备安装目录和缓存目录
            self.prepare_directories(install_path)
            
            # 安装应用程序
            self.install_application(install_path)
            
            # 创建快捷方式
            if create_startmenu_link:
                self.create_startmenu_shortcut(install_path)
            
            if create_desktop_link:
                self.create_desktop_shortcut(install_path)
            
            # 安装MinGW64
            if install_mingw64:
                self.install_mingw64()
            
            # 安装完成
            self.send_complete()
            
        except Exception as e:
            error_msg = f"安装过程中出现错误:\n{str(e)}\n\n详细信息:\n{traceback.format_exc()}"
            self.send_error(error_msg)
    
    def prepare_directories(self, install_path):
        """准备安装目录和缓存目录"""
        self.send_status("准备安装目录...")
        
        # 清理缓存目录
        cache_dir = r'C:\install_cache'
        if os.path.exists(cache_dir):
            try:
                shutil.rmtree(cache_dir)
            except:
                self.delete_special_dir(cache_dir)
        
        os.makedirs(cache_dir, exist_ok=True)
        self.send_progress(5)
        
        # 清理安装目录
        if os.path.exists(install_path):
            try:
                shutil.rmtree(install_path)
            except:
                self.delete_special_dir(install_path)
        
        os.makedirs(install_path, exist_ok=True)
        self.send_progress(5)
    
    def install_application(self, install_path):
        """安装应用程序"""
        self.send_status("正在提取应用程序...")
        
        # 获取应用程序压缩包
        app_7z_path = r'C:\install_cache\app.7z'
        self.get_app_archive(app_7z_path)
        self.send_progress(10)
        
        # 解压应用程序
        self.extract_app_archive(app_7z_path, install_path)
        self.send_progress(15)
    
    def get_app_archive(self, output_path):
        """获取应用程序压缩包"""
        app_resource = files('assets') / 'NuitkaGUI.7z'
        BLOCK_SIZE = 1024 * 1024  # 1MB
        FILE_SIZE = 6985023
        downloaded = 0
        
        with app_resource.open('rb') as source, open(output_path, 'wb') as target:
            while True:
                data = source.read(BLOCK_SIZE)
                if not data:
                    break
                target.write(data)
                downloaded += len(data)
                # 更新进度 (这部分占5%的总进度)
                progress = (downloaded / FILE_SIZE) * 5
                self.send_progress(progress)
    
    def extract_app_archive(self, archive_path, extract_path):
        """解压应用程序压缩包"""
        max_retries = 3
        retry_count = 0
        
        while retry_count < max_retries:
            try:
                with py7zr.SevenZipFile(archive_path, 'r') as archive:
                    file_list = archive.namelist()
                    total_files = len(file_list)
                    extracted = 0
                    
                    for file_info in archive.files:
                        # 尝试解压文件，如果失败则重试
                        success = False
                        file_retries = 0
                        
                        while not success and file_retries < 3:
                            try:
                                archive.extract(targets=[file_info.filename], path=extract_path)
                                success = True
                            except Exception as e:
                                file_retries += 1
                                self.send_status(f"解压 {file_info.filename} 失败，重试 {file_retries}/3...")
                                time.sleep(1)  # 等待1秒后重试
                                
                                # 如果是最后一次尝试，抛出异常
                                if file_retries >= 3:
                                    raise e
                        
                        extracted += 1
                        # 更新进度 (这部分占10%的总进度)
                        progress = (extracted / total_files) * 10
                        self.send_status(f"解压程序文件 {extracted}/{total_files}")
                        self.send_progress(progress)
                
                # 如果成功解压所有文件，跳出重试循环
                break
                
            except Exception as e:
                retry_count += 1
                self.send_status(f"解压失败，重试 {retry_count}/{max_retries}...")
                
                if retry_count >= max_retries:
                    raise Exception(f"无法解压应用程序文件: {str(e)}")
                
                time.sleep(2)  # 等待2秒后重试
    
    def create_startmenu_shortcut(self, install_path):
        """创建开始菜单快捷方式"""
        self.send_status("创建开始菜单快捷方式...")
        target_path = os.path.join(install_path, 'NuitkaGUI.exe')
        shortcut_path = os.path.join(self.startmenu_path, 'NuitkaGUI.lnk')
        
        # 确保开始菜单目录存在
        os.makedirs(os.path.dirname(shortcut_path), exist_ok=True)
        
        self.create_shortcut(target_path, shortcut_path, 'NuitkaGUI')
        self.send_progress(2)
    
    def create_desktop_shortcut(self, install_path):
        """创建桌面快捷方式"""
        self.send_status("创建桌面快捷方式...")
        target_path = os.path.join(install_path, 'NuitkaGUI.exe')
        shortcut_path = os.path.join(self.desktop_path, 'NuitkaGUI.lnk')
        self.create_shortcut(target_path, shortcut_path, 'NuitkaGUI')
        self.send_progress(2)
    
    def create_shortcut(self, target_path, shortcut_path, description='', working_dir='', icon_path=''):
        """创建快捷方式"""
        shell = Dispatch('WScript.Shell')
        shortcut = shell.CreateShortCut(shortcut_path)
        shortcut.Targetpath = target_path
        shortcut.Description = description
        if working_dir:
            shortcut.WorkingDirectory = working_dir
        if icon_path:
            shortcut.IconLocation = icon_path
        shortcut.save()
    
    def install_mingw64(self):
        """安装MinGW64"""
        self.send_status("准备安装MinGW64...")
        
        # 清理MinGW64目录
        if os.path.exists(self.mingw64_path):
            try:
                shutil.rmtree(self.mingw64_path)
            except:
                self.delete_special_dir(self.mingw64_path)
        
        os.makedirs(self.mingw64_path, exist_ok=True)
        self.send_progress(5)
        
        # 获取MinGW64压缩包
        mingw_7z_path = r'C:\install_cache\mingw64.7z'
        self.get_mingw64_archive(mingw_7z_path)
        self.send_progress(10)
        
        # 解压MinGW64
        self.extract_mingw64_archive(mingw_7z_path, self.mingw64_path)
        self.send_progress(30)
    
    def get_mingw64_archive(self, output_path):
        """获取MinGW64压缩包"""
        mingw_resource = files('assets') / 'mingw64.7z'
        BLOCK_SIZE = 1024 * 1024  # 1MB
        FILE_SIZE = 167169998
        downloaded = 0
        
        with mingw_resource.open('rb') as source, open(output_path, 'wb') as target:
            while True:
                data = source.read(BLOCK_SIZE)
                if not data:
                    break
                target.write(data)
                downloaded += len(data)
                # 更新进度 (这部分占10%的总进度)
                progress = (downloaded / FILE_SIZE) * 10
                self.send_progress(progress)
    
    def extract_mingw64_archive(self, archive_path, extract_path):
        """解压MinGW64压缩包"""
        max_retries = 3
        retry_count = 0
        
        while retry_count < max_retries:
            try:
                with py7zr.SevenZipFile(archive_path, mode='r') as archive:
                    file_list = archive.namelist()
                    total_files = len(file_list)
                    extracted = 0
                    
                    for file_info in archive.files:
                        # 尝试解压文件，如果失败则重试
                        success = False
                        file_retries = 0
                        
                        while not success and file_retries < 3:
                            try:
                                archive.extract(targets=[file_info.filename], path=extract_path)
                                success = True
                            except Exception as e:
                                file_retries += 1
                                self.send_status(f"解压 {file_info.filename} 失败，重试 {file_retries}/3...")
                                time.sleep(1)  # 等待1秒后重试
                                
                                # 如果是最后一次尝试，抛出异常
                                if file_retries >= 3:
                                    raise e
                        
                        extracted += 1
                        # 更新进度 (这部分占30%的总进度)
                        progress = (extracted / total_files) * 30
                        self.send_status(f"解压编译器文件 {extracted}/{total_files}")
                        self.send_progress(progress)
                
                # 如果成功解压所有文件，跳出重试循环
                break
                
            except Exception as e:
                retry_count += 1
                self.send_status(f"解压失败，重试 {retry_count}/{max_retries}...")
                
                if retry_count >= max_retries:
                    raise Exception(f"无法解压MinGW64文件: {str(e)}")
                
                time.sleep(2)  # 等待2秒后重试
    
    def delete_special_dir(self, path):
        """递归删除目录，包括只读文件"""
        if not os.path.isdir(path) or not os.path.exists(path):
            return
        
        # 首先尝试修改所有文件的属性为正常
        for root, dirs, files in os.walk(path):
            for file in files:
                file_path = os.path.join(root, file)
                try:
                    SetFileAttributes(file_path, FILE_ATTRIBUTE_NORMAL)
                except:
                    pass
            
            for dir in dirs:
                dir_path = os.path.join(root, dir)
                try:
                    SetFileAttributes(dir_path, FILE_ATTRIBUTE_NORMAL)
                except:
                    pass
        
        # 然后尝试删除目录
        try:
            shutil.rmtree(path)
        except:
            # 如果标准删除失败，尝试逐个文件删除
            for root, dirs, files in os.walk(path, topdown=False):
                for file in files:
                    file_path = os.path.join(root, file)
                    try:
                        SetFileAttributes(file_path, FILE_ATTRIBUTE_NORMAL)
                        os.remove(file_path)
                    except:
                        pass
                
                for dir in dirs:
                    dir_path = os.path.join(root, dir)
                    try:
                        SetFileAttributes(dir_path, FILE_ATTRIBUTE_NORMAL)
                        os.rmdir(dir_path)
                    except:
                        pass
            
            # 最后尝试删除根目录
            try:
                SetFileAttributes(path, FILE_ATTRIBUTE_NORMAL)
                os.rmdir(path)
            except:
                pass

if __name__ == '__main__':
    try:
        installer = Installer()
    except Exception as e:
        messagebox.showerror(title='安装失败', message=str(e))