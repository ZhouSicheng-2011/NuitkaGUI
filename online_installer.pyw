import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog

import os
from importlib.resources import files  # Python 3.9+ is required
import py7zr, py7zr.exceptions
from win32com.client import Dispatch
import sys
import time
import shutil
from win32api import SetFileAttributes
from win32con import FILE_ATTRIBUTE_NORMAL
import threading
import queue
import traceback
import hashlib
import requests
from urllib.parse import urlparse
import zipfile

class Installer:
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry('500x400+200+200')  # 增加高度以容纳新的UI元素
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
        self.download_canceled = False
        
        # 路径设置
        self.desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop')
        self.startmenu_path = os.path.join(os.getenv("APPDATA"), "Microsoft", "Windows", "Start Menu", "Programs") # type: ignore
        self.mingw64_path = f'C:\\Users\\{os.getlogin()}\\AppData\\Local\\Nuitka\\Nuitka\\Cache\\downloads\\gcc\\x86_64\\14.2.0posix-19.1.1-12.0.0-msvcrt-r2'
        
        # MinGW64下载镜像
        self.mirrors = [
            {"name": "GitHub (官方源)", "url": "https://github.com/brechtsanders/winlibs_mingw/releases/download/14.2.0posix-19.1.1-12.0.0-msvcrt-r2/winlibs-x86_64-posix-seh-gcc-14.2.0-llvm-19.1.1-mingw-w64msvcrt-12.0.0-r2.zip"},
            {"name": "国内镜像1 (腾讯云)", "url": "https://mirrors.cloud.tencent.com/winlibs_mingw/14.2.0posix-19.1.1-12.0.0-msvcrt-r2/winlibs-x86_64-posix-seh-gcc-14.2.0-llvm-19.1.1-mingw-w64msvcrt-12.0.0-r2.zip"},
            {"name": "国内镜像2 (阿里云)", "url": "https://mirrors.aliyun.com/winlibs_mingw/14.2.0posix-19.1.1-12.0.0-msvcrt-r2/winlibs-x86_64-posix-seh-gcc-14.2.0-llvm-19.1.1-mingw-w64msvcrt-12.0.0-r2.zip"},
            {"name": "国内镜像3 (Cloudflare代理)", "url": "https://gh-proxy.com/https://github.com/brechtsanders/winlibs_mingw/releases/download/14.2.0posix-19.1.1-12.0.0-msvcrt-r2/winlibs-x86_64-posix-seh-gcc-14.2.0-llvm-19.1.1-mingw-w64msvcrt-12.0.0-r2.zip"}
        ]
        
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
        self.style.configure("TCombobox", font=('Consolas', 10))
    
    def create_ui(self):
        # 创建配置区域
        self.install_config_area = ttk.Frame(self.root)
        self.install_config_area.place(x=0, y=0, width=500, height=300)
        
        # 创建按钮区域
        self.button_area = ttk.Frame(self.root)
        self.button_area.place(x=0, y=300, width=500, height=100)
        
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
        
        # 下载镜像选择
        self.mirror_var = tk.StringVar()
        self.mirror_var.set(self.mirrors[0]["name"])
        self.lb_mirror = ttk.Label(self.install_config_area, text='下载镜像:')
        self.lb_mirror.grid(column=0, row=1, padx=5, pady=5, sticky='w')
        
        self.mirror_combo = ttk.Combobox(
            self.install_config_area, 
            textvariable=self.mirror_var,
            values=[m["name"] for m in self.mirrors],
            state="readonly",
            width=40
        )
        self.mirror_combo.grid(column=1, row=1, padx=5, pady=5, sticky='w')
        
        # 桌面快捷方式选项
        self.create_desktop_link = tk.BooleanVar(value=False)
        self.cbtn_1 = ttk.Checkbutton(
            self.install_config_area, 
            variable=self.create_desktop_link,
            text='创建桌面快捷方式'
        )
        self.cbtn_1.grid(column=0, row=2, columnspan=2, sticky='w', padx=5, pady=5)
        
        # 开始菜单快捷方式选项
        self.cerate_startmenu_link = tk.BooleanVar(value=False)
        self.cbtn_2 = ttk.Checkbutton(
            self.install_config_area, 
            variable=self.cerate_startmenu_link,
            text='创建开始菜单快捷方式'
        )
        self.cbtn_2.grid(column=0, row=3, columnspan=2, sticky='w', padx=5, pady=5)
        
        # 安装目录选择
        self.install_path = tk.StringVar(value=r'C:\Program Files\NuitkaGUI')
        self.lb_0 = ttk.Label(self.install_config_area, text='安装目录:')
        self.lb_0.grid(column=0, row=4, padx=5, pady=5, sticky='w')
        
        self.entry = ttk.Entry(self.install_config_area, textvariable=self.install_path, width=44)
        self.entry.grid(column=1, row=4, padx=5, pady=5, sticky='w')
        
        self.btn_0 = ttk.Button(self.install_config_area, text='浏览', command=self.browse_install_path)
        self.btn_0.grid(column=2, row=4, padx=5, pady=5, sticky='w')
        
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
                self.download_canceled = True
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
        self.install_area.place(x=0, y=0, width=500, height=350)
        
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
        
        # 下载速度标签
        self.download_speed = tk.StringVar(value='')
        self.lb_speed = ttk.Label(self.install_area, textvariable=self.download_speed)
        self.lb_speed.grid(column=0, row=3, padx=10, pady=5, sticky='e')
        
        # 取消下载按钮（只在下载MinGW64时显示）
        self.cancel_download_btn = ttk.Button(self.install_area, text='取消下载', command=self.cancel_download)
        self.cancel_download_btn.grid(column=0, row=4, padx=10, pady=10, sticky='e')
        self.cancel_download_btn.grid_remove()  # 默认隐藏
        
        # 启动安装线程
        self.install_thread = threading.Thread(target=self.installation_worker)
        self.install_thread.daemon = True
        self.install_thread.start()
    
    def cancel_download(self):
        self.download_canceled = True
        self.cancel_download_btn.config(state='disabled')
        self.send_status("正在取消下载...")
    
    def process_queue(self):
        """处理从工作线程发送到主线程的消息"""
        try:
            while True:
                msg = self.queue.get_nowait()
                if msg[0] == 'progress':
                    self.update_progress(msg[1])
                elif msg[0] == 'status':
                    self.install_status.set(msg[1])
                elif msg[0] == 'speed':
                    self.download_speed.set(msg[1])
                elif msg[0] == 'show_cancel':
                    self.cancel_download_btn.grid()
                elif msg[0] == 'hide_cancel':
                    self.cancel_download_btn.grid_remove()
                elif msg[0] == 'complete':
                    self.installation_complete()
                elif msg[0] == 'error':
                    self.installation_error(msg[1])
        except queue.Empty:
            pass
        finally:
            self.root.after(100, self.process_queue)
    
    def update_progress(self, value):
        """更新进度条"""
        self.total_progress = value
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
    
    def send_progress(self, value):
        """发送进度更新到队列"""
        self.queue.put(('progress', value))
    
    def send_status(self, status):
        """发送状态更新到队列"""
        self.queue.put(('status', status))
    
    def send_speed(self, speed):
        """发送下载速度到队列"""
        self.queue.put(('speed', speed))
    
    def send_show_cancel(self):
        """显示取消下载按钮"""
        self.queue.put(('show_cancel',))
    
    def send_hide_cancel(self):
        """隐藏取消下载按钮"""
        self.queue.put(('hide_cancel',))
    
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
            
            # 验证安装路径
            if not install_path or not os.path.isabs(install_path):
                raise Exception("安装路径无效，请选择有效的安装目录")
            
            # 计算各阶段进度分配
            total_steps = 100
            base_progress = 10  # 基础准备阶段占10%
            app_progress = 30   # 应用程序安装占30%
            shortcut_progress = 4  # 快捷方式创建占4%
            mingw_progress = 56  # MinGW64安装占56%
            
            # 如果不安装MinGW64，重新分配进度
            if not install_mingw64:
                total_without_mingw = base_progress + app_progress + shortcut_progress
                # 按比例重新分配
                base_progress = int(base_progress * 100 / total_without_mingw)
                app_progress = int(app_progress * 100 / total_without_mingw)
                shortcut_progress = 100 - base_progress - app_progress
            
            # 准备安装目录和缓存目录
            self.prepare_directories(install_path, base_progress)
            
            # 安装应用程序
            current_progress = base_progress
            self.install_application(install_path, app_progress, current_progress)
            
            # 创建快捷方式
            current_progress += app_progress
            if create_startmenu_link:
                self.create_startmenu_shortcut(install_path, shortcut_progress/2, current_progress)
                current_progress += shortcut_progress/2
            
            if create_desktop_link:
                self.create_desktop_shortcut(install_path, shortcut_progress/2, current_progress)
                current_progress += shortcut_progress/2
            
            # 如果没有创建任何快捷方式，直接增加进度
            if not create_startmenu_link and not create_desktop_link:
                self.send_progress(current_progress + shortcut_progress)
                current_progress += shortcut_progress
            
            # 安装MinGW64
            if install_mingw64:
                self.install_mingw64(mingw_progress, current_progress)
            
            # 安装完成
            self.send_progress(100)
            self.send_complete()
            
        except Exception as e:
            error_msg = f"安装过程中出现错误:\n{str(e)}\n\n这可能是因为安装文件损坏或系统权限问题。\n请尝试以管理员身份运行安装程序，或联系技术支持。"
            self.send_error(error_msg)
    
    def prepare_directories(self, install_path, total_progress):
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
        self.send_progress(total_progress * 0.5)
        
        # 清理安装目录
        if os.path.exists(install_path):
            try:
                shutil.rmtree(install_path)
            except:
                self.delete_special_dir(install_path)
        
        os.makedirs(install_path, exist_ok=True)
        self.send_progress(total_progress)
    
    def install_application(self, install_path, total_progress, start_progress):
        """安装应用程序"""
        self.send_status("正在提取应用程序...")
        
        # 获取应用程序压缩包
        app_7z_path = r'C:\install_cache\app.7z'
        self.get_app_archive(app_7z_path, total_progress * 0.2, start_progress)
        
        # 验证压缩包完整性
        self.validate_archive(app_7z_path, "应用程序")
        current_progress = start_progress + total_progress * 0.25
        self.send_progress(current_progress)
        
        # 解压应用程序
        self.extract_app_archive(app_7z_path, install_path, total_progress * 0.55, current_progress)
        self.send_progress(start_progress + total_progress)
    
    def get_app_archive(self, output_path, progress_portion, start_progress):
        """获取应用程序压缩包"""
        try:
            app_resource = files('assets') / 'NuitkaGUI.7z'
            BLOCK_SIZE = 1024 * 1024  # 1MB
            FILE_SIZE = 6985023
            
            with app_resource.open('rb') as source, open(output_path, 'wb') as target:
                downloaded = 0
                while True:
                    data = source.read(BLOCK_SIZE)
                    if not data:
                        break
                    target.write(data)
                    downloaded += len(data)
                    # 更新进度
                    progress = start_progress + (downloaded / FILE_SIZE) * progress_portion
                    self.send_progress(progress)
        except Exception as e:
            raise Exception(f"无法读取应用程序资源文件: {str(e)}")
    
    def validate_archive(self, archive_path, archive_name):
        """验证压缩包完整性"""
        self.send_status(f"验证{archive_name}压缩包完整性...")
        
        try:
            # 检查文件是否存在
            if not os.path.exists(archive_path):
                raise Exception(f"{archive_name}压缩包不存在")
            
            # 检查文件大小
            file_size = os.path.getsize(archive_path)
            if file_size == 0:
                raise Exception(f"{archive_name}压缩包为空")
            
            # 尝试打开压缩包验证完整性
            if archive_path.endswith('.7z'):
                with py7zr.SevenZipFile(archive_path, 'r') as archive:
                    file_list = archive.namelist()
                    if not file_list:
                        raise Exception(f"{archive_name}压缩包为空或损坏")
            elif archive_path.endswith('.zip'):
                with zipfile.ZipFile(archive_path, 'r') as archive:
                    if archive.testzip() is not None:
                        raise Exception(f"{archive_name}压缩包损坏")
            
            self.send_status(f"{archive_name}压缩包验证成功")
            return True
            
        except py7zr.Bad7zFile:
            raise Exception(f"{archive_name}压缩包损坏，请重新下载安装程序")
        except zipfile.BadZipFile:
            raise Exception(f"{archive_name}压缩包损坏，请重新下载")
        except Exception as e:
            raise Exception(f"{archive_name}压缩包验证失败: {str(e)}")
    
    def extract_app_archive(self, archive_path, extract_path, progress_portion, start_progress):
        """解压应用程序压缩包"""
        max_retries = 3
        retry_count = 0
        
        while retry_count < max_retries:
            try:
                if archive_path.endswith('.7z'):
                    with py7zr.SevenZipFile(archive_path, 'r') as archive:
                        file_list = archive.namelist()
                        total_files = len(file_list)
                        extracted = 0
                        
                        # 先创建所有目录结构
                        for file_info in archive.files:
                            if file_info.is_directory:
                                dir_path = os.path.join(extract_path, file_info.filename)
                                os.makedirs(dir_path, exist_ok=True)
                        
                        # 然后提取文件
                        for file_info in archive.files:
                            if file_info.is_directory:
                                continue
                                
                            # 尝试解压文件，如果失败则重试
                            success = False
                            file_retries = 0
                            
                            while not success and file_retries < 3:
                                try:
                                    # 确保目标目录存在
                                    target_dir = os.path.dirname(os.path.join(extract_path, file_info.filename))
                                    os.makedirs(target_dir, exist_ok=True)
                                    
                                    # 提取文件
                                    archive.extract(targets=[file_info.filename], path=extract_path)
                                    success = True
                                except py7zr.exceptions.CrcError as e:
                                    # 如果是CRC错误，尝试跳过这个文件
                                    self.send_status(f"警告: 文件 {file_info.filename} CRC校验失败，跳过此文件")
                                    success = True  # 标记为成功以继续处理其他文件
                                except Exception as e:
                                    file_retries += 1
                                    self.send_status(f"解压 {file_info.filename} 失败，重试 {file_retries}/3...")
                                    time.sleep(1)  # 等待1秒后重试
                                    
                                    # 如果是最后一次尝试，抛出异常
                                    if file_retries >= 3:
                                        raise e
                            
                            extracted += 1
                            # 更新进度
                            progress = start_progress + (extracted / total_files) * progress_portion
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
    
    def create_startmenu_shortcut(self, install_path, progress_portion, start_progress):
        """创建开始菜单快捷方式"""
        self.send_status("创建开始菜单快捷方式...")
        target_path = os.path.join(install_path, 'NuitkaGUI.exe')
        shortcut_path = os.path.join(self.startmenu_path, 'NuitkaGUI.lnk')
        
        # 确保开始菜单目录存在
        os.makedirs(os.path.dirname(shortcut_path), exist_ok=True)
        
        self.create_shortcut(target_path, shortcut_path, 'NuitkaGUI')
        self.send_progress(start_progress + progress_portion)
    
    def create_desktop_shortcut(self, install_path, progress_portion, start_progress):
        """创建桌面快捷方式"""
        self.send_status("创建桌面快捷方式...")
        target_path = os.path.join(install_path, 'NuitkaGUI.exe')
        shortcut_path = os.path.join(self.desktop_path, 'NuitkaGUI.lnk')
        self.create_shortcut(target_path, shortcut_path, 'NuitkaGUI')
        self.send_progress(start_progress + progress_portion)
    
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
    
    def install_mingw64(self, total_progress, start_progress):
        """安装MinGW64"""
        self.send_status("准备安装MinGW64...")
        
        # 清理MinGW64目录
        if os.path.exists(self.mingw64_path):
            try:
                shutil.rmtree(self.mingw64_path)
            except:
                self.delete_special_dir(self.mingw64_path)
        
        os.makedirs(self.mingw64_path, exist_ok=True)
        self.send_progress(start_progress + total_progress * 0.1)
        
        # 获取MinGW64压缩包
        mingw_zip_path = r'C:\install_cache\mingw64.zip'
        
        # 获取选中的镜像
        selected_mirror_name = self.mirror_var.get()
        selected_mirror = next((m for m in self.mirrors if m["name"] == selected_mirror_name), self.mirrors[0])
        
        # 下载MinGW64
        self.download_mingw64(selected_mirror["url"], mingw_zip_path, total_progress * 0.3, start_progress + total_progress * 0.1)
        
        # 验证压缩包完整性
        self.validate_archive(mingw_zip_path, "MinGW64")
        current_progress = start_progress + total_progress * 0.45
        self.send_progress(current_progress)
        
        # 解压MinGW64
        self.extract_mingw64_archive(mingw_zip_path, self.mingw64_path, total_progress * 0.55, current_progress)
        self.send_progress(start_progress + total_progress)
    
    def download_mingw64(self, url:str, output_path, progress_portion, start_progress):
        """下载MinGW64压缩包，支持断点续传"""
        self.send_status(f"开始下载MinGW64编译器...")
        self.send_show_cancel()  # 显示取消下载按钮
        self.download_canceled = False
        headers = {
            # 用户代理 - 模拟真实浏览器
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            
            # 引用来源 - 对抗防盗链
            "Referer": url.split('//')[0] + '//' + url.split('//')[1].split('/')[0],
            
            # 接受内容类型
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            
            # 接受编码
            "Accept-Encoding": "gzip, deflate, br",
            
            # 接受语言
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            
            # 连接状态
            "Connection": "keep-alive",
            
            # 缓存控制
            "Cache-Control": "max-age=0",
            
            # 安全相关头部
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-User": "?1",
            
            # 升级不安全请求
            "Upgrade-Insecure-Requests": "1",
            
            # DNT (Do Not Track)
            "DNT": "1",
            
            # 设备内存（较新的浏览器支持）
            "Device-Memory": "8",
            
            # 视口宽度
            "Viewport-Width": "1920",
            
            # 宽度
            "Width": "1920",
            
            # 向下兼容的用户代理
            "X-Requested-With": "XMLHttpRequest",
            
            # 原始来源
            "Origin": url.split('//')[0] + '//' + url.split('//')[1].split('/')[0]
        }
        
        try:
            # 获取文件大小
            head_response = requests.head(url, allow_redirects=True, timeout=10)
            total_size = int(head_response.headers.get('content-length', 0))
            
            # 检查是否支持断点续传
            accept_ranges = head_response.headers.get('accept-ranges', '').lower() == 'bytes'
            
            # 检查已下载的部分
            downloaded_size = 0
            if os.path.exists(output_path):
                downloaded_size = os.path.getsize(output_path)
                if downloaded_size >= total_size:
                    self.send_status("MinGW64已下载完成，跳过下载")
                    self.send_hide_cancel()
                    return
                
                if not accept_ranges:
                    # 服务器不支持断点续传，需要重新下载
                    os.remove(output_path)
                    downloaded_size = 0
            
            mode = 'ab' if downloaded_size > 0 and accept_ranges else 'wb'
            headers = {}
            if downloaded_size > 0 and accept_ranges:
                headers['Range'] = f'bytes={downloaded_size}-'
            
            # 开始下载
            with requests.get(url, stream=True, headers=headers, timeout=30) as response:
                response.raise_for_status()
                
                # 如果服务器不支持断点续传但我们已经下载了一部分，需要重新下载
                if downloaded_size > 0 and not accept_ranges and response.status_code != 206:
                    downloaded_size = 0
                    mode = 'wb'
                
                with open(output_path, mode) as file:
                    start_time = time.time()
                    for chunk in response.iter_content(chunk_size=8192):
                        if self.download_canceled:
                            self.send_status("下载已取消")
                            self.send_hide_cancel()
                            raise Exception("下载被用户取消")
                        
                        if chunk:  # 过滤掉保持连接的新块
                            file.write(chunk)
                            downloaded_size += len(chunk)
                            
                            # 计算下载速度
                            elapsed_time = time.time() - start_time
                            if elapsed_time > 0:
                                speed = downloaded_size / elapsed_time  # bytes per second
                                speed_str = f"{speed / 1024 / 1024:.2f} MB/s"
                                self.send_speed(speed_str)
                            
                            # 更新进度
                            if total_size > 0:
                                progress = start_progress + (downloaded_size / total_size) * progress_portion
                                self.send_progress(progress)
                                self.send_status(f"下载MinGW64: {downloaded_size/1024/1024:.1f}MB / {total_size/1024/1024:.1f}MB")
            
            self.send_status("MinGW64下载完成")
            self.send_hide_cancel()
            
        except requests.exceptions.RequestException as e:
            if self.download_canceled:
                raise Exception("下载被用户取消")
            else:
                raise Exception(f"下载MinGW64失败: {str(e)}")
        except Exception as e:
            if self.download_canceled:
                raise Exception("下载被用户取消")
            else:
                raise Exception(f"下载MinGW64时发生错误: {str(e)}")
    
    def extract_mingw64_archive(self, archive_path, extract_path, progress_portion, start_progress):
        """解压MinGW64压缩包"""
        max_retries = 3
        retry_count = 0
        
        while retry_count < max_retries:
            try:
                with zipfile.ZipFile(archive_path, 'r') as archive:
                    file_list = archive.namelist()
                    total_files = len(file_list)
                    extracted = 0
                    
                    # 先创建所有目录结构
                    for file_info in archive.filelist:
                        if file_info.is_dir():
                            dir_path = os.path.join(extract_path, file_info.filename)
                            os.makedirs(dir_path, exist_ok=True)
                    
                    # 然后提取文件
                    for file_info in archive.filelist:
                        if file_info.is_dir():
                            continue
                            
                        # 尝试解压文件，如果失败则重试
                        success = False
                        file_retries = 0
                        
                        while not success and file_retries < 3:
                            try:
                                # 确保目标目录存在
                                target_dir = os.path.dirname(os.path.join(extract_path, file_info.filename))
                                os.makedirs(target_dir, exist_ok=True)
                                
                                # 提取文件
                                with archive.open(file_info) as source, open(os.path.join(extract_path, file_info.filename), 'wb') as target:
                                    shutil.copyfileobj(source, target)
                                success = True
                            except Exception as e:
                                file_retries += 1
                                self.send_status(f"解压 {file_info.filename} 失败，重试 {file_retries}/3...")
                                time.sleep(1)  # 等待1秒后重试
                                
                                # 如果是最后一次尝试，抛出异常
                                if file_retries >= 3:
                                    raise e
                        
                        extracted += 1
                        # 更新进度
                        progress = start_progress + (extracted / total_files) * progress_portion
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
        # 检查是否以管理员权限运行
        if os.name == 'nt':
            try:
                import ctypes
                if ctypes.windll.shell32.IsUserAnAdmin() == 0:
                    messagebox.showwarning("权限警告", 
                        "建议以管理员身份运行安装程序，以确保有足够的权限安装文件。\n"
                        "当前安装可能会因为权限不足而失败。")
            except:
                pass
        
        installer = Installer()
    except Exception as e:
        messagebox.showerror(title='安装失败', message=str(e))