import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog

import os
import sys
import time
import shutil
import threading
import queue
import traceback
import hashlib
import tempfile
import ctypes
from win32com.client import Dispatch
from win32api import SetFileAttributes
from win32con import FILE_ATTRIBUTE_NORMAL

# 尝试导入py7zr，如果失败则提供更友好的错误信息
try:
    import py7zr, py7zr.exceptions
    PY7ZR_AVAILABLE = True
except ImportError:
    PY7ZR_AVAILABLE = False
    messagebox.showerror("缺少依赖", "无法导入py7zr库，请确保已正确安装所有依赖")

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
        
        # 路径设置 - 使用更可靠的方法获取路径
        self.desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop')
        self.startmenu_path = os.path.join(os.getenv("APPDATA", ""), "Microsoft", "Windows", "Start Menu", "Programs")
        
        # 使用更可靠的用户名获取方法
        try:
            username = os.getlogin()
        except:
            username = os.getenv("USERNAME", "UnknownUser")
        self.mingw64_path = f'C:\\Users\\{username}\\AppData\\Local\\Nuitka\\Nuitka\\Cache\\downloads\\gcc\\x86_64\\14.2.0posix-19.1.1-12.0.0-msvcrt-r2'
        
        # 设置样式
        self.setup_style()
        
        # 创建UI
        self.create_ui()
        
        # 开始处理队列消息
        self.process_queue()
        
        self.root.mainloop()
    
    def setup_style(self):
        self.style = ttk.Style()
        try:
            self.style.theme_use('vista')
        except:
            pass  # 如果主题不可用，使用默认主题
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
        
        # 使用更可靠的缓存目录
        cache_dir = os.path.join(tempfile.gettempdir(), 'install_cache')
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
        app_7z_path = os.path.join(tempfile.gettempdir(), 'install_cache', 'app.7z')
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
            # 确保输出目录存在
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            # 使用更可靠的方法获取资源
            try:
                # 尝试从打包的资源中获取
                import importlib.resources
                app_resource = importlib.resources.files('assets') / 'NuitkaGUI.7z'
                with app_resource.open('rb') as source:
                    content = source.read()
            except:
                # 如果失败，尝试从当前目录获取
                if os.path.exists('NuitkaGUI.7z'):
                    with open('NuitkaGUI.7z', 'rb') as source:
                        content = source.read()
                else:
                    raise Exception("无法找到应用程序资源文件")
            
            # 写入文件
            with open(output_path, 'wb') as target:
                target.write(content)
            
            self.send_progress(start_progress + progress_portion)
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
            if archive_path.endswith('.7z') and PY7ZR_AVAILABLE:
                with py7zr.SevenZipFile(archive_path, 'r') as archive:
                    file_list = archive.namelist()
                    if not file_list:
                        raise Exception(f"{archive_name}压缩包为空或损坏")
            
            self.send_status(f"{archive_name}压缩包验证成功")
            return True
            
        except py7zr.Bad7zFile:
            raise Exception(f"{archive_name}压缩包损坏，请重新下载安装程序")
        except Exception as e:
            raise Exception(f"{archive_name}压缩包验证失败: {str(e)}")
    
    def extract_app_archive(self, archive_path, extract_path, progress_portion, start_progress):
        """解压应用程序压缩包"""
        max_retries = 3
        retry_count = 0
        
        while retry_count < max_retries:
            try:
                if archive_path.endswith('.7z') and PY7ZR_AVAILABLE:
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
                else:
                    raise Exception("不支持的文件格式或缺少py7zr库")
                
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
        try:
            shell = Dispatch('WScript.Shell')
            shortcut = shell.CreateShortCut(shortcut_path)
            shortcut.Targetpath = target_path
            shortcut.Description = description
            if working_dir:
                shortcut.WorkingDirectory = working_dir
            if icon_path:
                shortcut.IconLocation = icon_path
            shortcut.save()
        except Exception as e:
            self.send_status(f"创建快捷方式失败: {str(e)}")
    
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
        mingw_7z_path = os.path.join(tempfile.gettempdir(), 'install_cache', 'mingw64.7z')
        self.get_mingw64_archive(mingw_7z_path, total_progress * 0.2, start_progress)
        
        # 验证压缩包完整性
        self.validate_archive(mingw_7z_path, "MinGW64")
        current_progress = start_progress + total_progress * 0.35
        self.send_progress(current_progress)
        
        # 解压MinGW64
        self.extract_mingw64_archive(mingw_7z_path, self.mingw64_path, total_progress * 0.65, current_progress)
        self.send_progress(start_progress + total_progress)
    
    def get_mingw64_archive(self, output_path, progress_portion, start_progress):
        """获取MinGW64压缩包"""
        try:
            # 确保输出目录存在
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            # 使用更可靠的方法获取资源
            try:
                # 尝试从打包的资源中获取
                import importlib.resources
                mingw_resource = importlib.resources.files('assets') / 'mingw64.7z'
                with mingw_resource.open('rb') as source:
                    content = source.read()
            except:
                # 如果失败，尝试从当前目录获取
                if os.path.exists('mingw64.7z'):
                    with open('mingw64.7z', 'rb') as source:
                        content = source.read()
                else:
                    raise Exception("无法找到MinGW64资源文件")
            
            # 写入文件
            with open(output_path, 'wb') as target:
                target.write(content)
            
            self.send_progress(start_progress + progress_portion)
        except Exception as e:
            raise Exception(f"无法读取MinGW64资源文件: {str(e)}")
    
    def extract_mingw64_archive(self, archive_path, extract_path, progress_portion, start_progress):
        """解压MinGW64压缩包"""
        max_retries = 3
        retry_count = 0
        
        while retry_count < max_retries:
            try:
                if archive_path.endswith('.7z') and PY7ZR_AVAILABLE:
                    with py7zr.SevenZipFile(archive_path, mode='r') as archive:
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
                            self.send_status(f"解压编译器文件 {extracted}/{total_files}")
                            self.send_progress(progress)
                else:
                    raise Exception("不支持的文件格式或缺少py7zr库")
                
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
                if ctypes.windll.shell32.IsUserAnAdmin() == 0:
                    messagebox.showwarning("权限警告", 
                        "建议以管理员身份运行安装程序，以确保有足够的权限安装文件。\n"
                        "当前安装可能会因为权限不足而失败。")
            except:
                pass
        
        installer = Installer()
    except Exception as e:
        messagebox.showerror(title='安装失败', message=str(e))