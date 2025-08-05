#GUI相关模块
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import scrolledtext
from tkinter import messagebox
import tkinter.font

#子进程处理相关模块
import subprocess
import sys

#多线程处理相关模块
import threading
import queue

#相关模块
import os
import socket
import platform
import re
import time


class NuitkaGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title('Nuitka打包工具')
        self.root.geometry('1300x900+50+50')

        self.style = ttk.Style()
        self.style.theme_use('vista')
        self.style.configure("TNotebook", background="#f0f0f0")
        self.style.configure("TNotebook.Tab", padding=(10, 5), font=('Consolas', 10))
        self.style.configure("TFrame", background="#f0f0f0")
        self.style.configure("TButton", font=('Consolas', 10), padding=5)
        self.style.configure("TLabel", background="#f0f0f0", font=('Consolas', 10))
        self.style.configure("TEntry", font=('Consolas', 10))
        self.style.configure("TCombobox", font=('Consolas', 10))
        self.style.configure("TCheckbutton", background="#f0f0f0", font=('Consolas', 10))
        self.style.configure("TRadiobutton", background="#f0f0f0", font=('Consolas', 10))
        self.style.configure("TListbox", font=('Consolas', 10))
        
        self.main = ttk.LabelFrame(self.root,labelanchor='nw',text='基础选项')
        self.main.place(x=20,y=20,width=1260,height=160)

        self.notebook = ttk.Notebook(self.root)
        self.notebook.place(x=20,y=200,width=1260,height=580)
        #创建线程通信队列
        #self.exc_space = queue.Queue()

        self.simple()

        #创建所有标签页
        self.basic_tab()
        self.C_compiler_tab()
        self.compile_tab()
        self.data_tab()
        self.debug_tab()
        self.deployment_tab()
        self.dll_tab()
        self.imports_tab()
        self.info_tab()
        self.onefile_tab()
        self.OS_tab()
        self.output_tab()
        self.package_tab()
        self.plugin_tab()
        self.run_tab()
        self.warn_tab()
        #self.test_tab()
        self.console_tab()

        ...

        self.console.config(state='disabled')
        self.stat = ttk.Frame(self.root)
        self.stat.place(x=20, y=800, width=1260, height=90)
        self.status()

        self.root.mainloop()

    def simple(self):
        self.lb_0 = ttk.Label(self.main, text='Python脚本路径:')
        self.lb_0.grid(column=0, row=0)
        self.lb_1 = ttk.Label(self.main, text='Python解释器路径:')
        self.lb_1.grid(column=0, row=1)
        self.script = tk.StringVar()
        self.interpreter = tk.StringVar()
        self.e_0 = ttk.Entry(self.main, textvariable=self.script, width=130)
        self.e_0.config(state='readonly')
        self.e_0.grid(column=1, row=0)
        self.e_1 = ttk.Entry(self.main, textvariable=self.interpreter, width=130)
        self.e_1.config(state='readonly')
        self.e_1.grid(column=1, row=1)
        self.btn_0 = ttk.Button(self.main, text='浏览',command=self.select_script)
        self.btn_0.grid(column=2, row=0)
        self.btn_1 = ttk.Button(self.main, text='浏览', command=self.select_interpreter)
        self.btn_1.grid(column=2,row=1)

    def basic_tab(self):
        self.tab_0 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_0, text='基本选项')
        self.f_0 = ttk.Labelframe(self.tab_0, labelanchor='nw', text='编译模式')
        self.f_0.place(x=20,y=20,width=600,height=500)
        self.mode = tk.StringVar(value='accelerated')
        #
        self.rbtn_0 = ttk.Radiobutton(self.f_0, text='依赖Python解释器模式', variable=self.mode, value='accelerated')
        self.rbtn_0.bind('<<RadioButtonSelected>>', lambda event: self.mode.set('accelerated'))
        self.rbtn_0.pack(anchor='w', fill='y')
        #
        self.rbtn_1 = ttk.Radiobutton(self.f_0, text='独立文件夹模式', variable=self.mode, value='standalone')
        self.rbtn_1.bind('<<RadioButtonSelected>>', lambda event: self.mode.set('standalone'))
        self.rbtn_1.pack(anchor='w', fill='y')
        #
        self.rbtn_2 = ttk.Radiobutton(self.f_0, text='单文件模式', variable=self.mode, value='onefile')
        self.rbtn_2.bind('<<RadioButtonSelected>>', lambda event: self.mode.set('onefile'))
        #这里以后要处理标签页，暂时跳过
        self.rbtn_2.pack(anchor='w', fill='y')
        #
        self.rbtn_3 = ttk.Radiobutton(self.f_0, text='APP模式', variable=self.mode, value='app')
        self.rbtn_3.bind('<<RadioButtonSelected>>', lambda event: self.mode.set('app'))
        self.rbtn_3.pack(anchor='w', fill='y')
        #
        self.rbtn_4 = ttk.Radiobutton(self.f_0, text='二进制动态模块模式', variable=self.mode, value='module')
        self.rbtn_4.bind('<<RadioButtonSelected>>', lambda event: self.mode.set('module'))
        self.rbtn_4.pack(anchor='w', fill='y')
        #
        self.rbtn_5 = ttk.Radiobutton(self.f_0, text='二进制动态包模式', variable=self.mode, value='package')
        self.rbtn_5.bind('<<RadioButtonSelected>>', lambda event: self.mode.set('package'))
        self.rbtn_5.pack(anchor='w', fill='y')
        #
        self.rbtn_6 = ttk.Radiobutton(self.f_0, text='动态链接库模式', variable=self.mode, value='dll')
        self.rbtn_6.bind('<<RadioButtonSelected>>', lambda event: self.mode.set('dll'))
        self.rbtn_6.pack(anchor='w', fill='y')
        ##
        ##
        self.py_flags = ['isolated','main','no_asserts','no_docstrings','no_site',\
                         'no_warnings','safe_path','static_hashes','unbuffered','dont_write_bytecode']
        self.f_1 = ttk.LabelFrame(self.tab_0, text='Python标志', labelanchor='nw')
        self.f_1.place(x=620,y=20,width=600,height=280)
        #
        self.lb_2 = ttk.Label(self.f_1, text='Python标志:')
        self.lb_2.grid(column=0, row=0)
        #
        self.py_flag = tk.StringVar(value='no_site')
        self.cbox_0 = ttk.Combobox(self.f_1, values=self.py_flags, state='readonly')
        self.cbox_0.bind('<<ComboboxSelected>>', lambda event: self.py_flag.set(self.cbox_0.get()))
        self.cbox_0.grid(column=1, row=0)
        ##
        ##
        self.f_2 = ttk.Labelframe(self.tab_0, text='调试选项', labelanchor='nw')
        self.f_2.place(x=620, y=320, width=600,height=280)
        #
        self.py_dbg = tk.IntVar(value=0)
        self.cbtn_0 = ttk.Checkbutton(self.f_2, text='Python Debug', offvalue=0, onvalue=1)
        self.cbtn_0.pack(anchor='w', fill='y')
        

    def package_tab(self):
        pass

    def imports_tab(self):
        self.tab_2 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_2, text='导入选项')
        #
        self.f_3 = ttk.Labelframe(self.tab_2, text='包含包', labelanchor='nw')
        self.f_3.place(x=20, y=20, width=600, height=540)
        #
        self.follow_imports = tk.IntVar(value=1)
        self.cbtn_1 = ttk.Checkbutton(self.f_3, text='递归处理导入模块(推荐)', offvalue=0, onvalue=1)
        self.cbtn_1.grid(column=0, columnspan=2, row=0, sticky='w')
        #
        self.follow_stdlib = tk.IntVar(value=1)
        self.cbtn_2 = ttk.Checkbutton(self.f_3, text='递归处理标准库导入(推荐)', offvalue=0, onvalue=1)
        self.cbtn_2.grid(column=0, columnspan=2, row=1, sticky='w')
        ##
        self.lb_3 = ttk.Label(self.f_3, text='递归处理导入库:')
        self.lb_3.grid(column=0, row=2, sticky='w')
        #
        self.pkg_name_1 = tk.StringVar()
        self.e_2 = ttk.Entry(self.f_3, state='normal', textvariable=self.pkg_name_1, width=40)
        self.e_2.grid(column=1, columnspan=2 ,row=2)
        #
        self.btn_2 = ttk.Button(self.f_3, text='添加库')#...
        self.btn_2.grid(column=3, row=2)
        #
        self.btn_3 = ttk.Button(self.f_3, text='删除选中库')#...
        self.btn_3.grid(column=4, row=2)
        #
        self.f_4 = ttk.Labelframe(self.f_3, text='包含库列表', labelanchor='nw')
        self.f_4.grid(column=0, row=3, columnspan=5, rowspan=5)
        self.lbox_0 = tk.Listbox(self.f_4, activestyle='dotbox')
        self.scr_0 = tk.Scrollbar(self.f_4, command=self.lbox_0.yview)
        self.lbox_0.config(yscrollcommand=self.scr_0.set)
        self.lbox_0.pack(side='left', fill='both')
        self.scr_0.pack(side='right', fill='both')
        #^
        self.follow_imports_list = []
        self.btn_2.config(command=lambda:self.insert(self.lbox_0, self.pkg_name_1.get(),self.follow_imports_list))
        self.btn_3.config(command=lambda:self.delete_selection(self.lbox_0))
        ##
        ##
        self.f_5 = ttk.Labelframe(self.tab_2, text='不包含库', labelanchor='nw')
        self.f_5.place(x=640, y=20, width=600, height=540)
        #
        self.no_follow_imports = tk.IntVar(value=0)
        self.cbtn_3 = ttk.Checkbutton(self.f_5, text='不递归处理一切导入库(覆盖所有包含选项)(不推荐)',\
                                      variable=self.no_follow_imports, offvalue=0, onvalue=1)
        self.cbtn_3.grid(column=0, columnspan=2, row=0, sticky='w')
        #
        self.lb_4 = ttk.Label(self.f_5, text='不递归处理导入库')
        self.lb_4.grid(column=0, row=1)
        #
        self.pkg_name_2 = tk.StringVar(value='')
        self.e_3 = ttk.Entry(self.f_5, width=40, textvariable=self.pkg_name_2, state='normal')
        self.e_3.grid(column=1, columnspan=2, row=1)
        #
        self.btn_4 = ttk.Button(self.f_5, text='添加库')
        self.btn_4.grid(column=3, row=1)
        #
        self.btn_5 = ttk.Button(self.f_5, text='删除选中库')
        self.btn_5.grid(column=4, row=1)
        #^
        self.f_6 = ttk.Labelframe(self.f_5, text='不包含库列表', labelanchor='nw')
        self.f_6.grid(column=0, row=2, columnspan=5, rowspan=5)
        self.lbox_1 = tk.Listbox(self.f_6, activestyle='dotbox')
        self.scr_1 = tk.Scrollbar(self.f_6, command=self.lbox_1.yview)
        self.lbox_1.config(yscrollcommand=self.scr_1.set)
        self.lbox_1.pack(side='left', fill='both')
        self.scr_1.pack(side='left', fill='both')
        #^
        self.no_follow_imports_list = []
        self.btn_4.config(command=lambda:self.insert(self.lbox_1, self.pkg_name_2.get(), self.no_follow_imports_list))
        self.btn_5.config(command=lambda:self.delete_selection(self.lbox_1))

    def onefile_tab(self):
        self.tab_3 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_3, text='单文件选项')
        #setattr(self.tab_3, 'id', 'onefile')
        ...

    def data_tab(self):
        pass

    def dll_tab(self):
        pass

    def warn_tab(self):
        pass

    def run_tab(self):
        pass

    def compile_tab(self):
        pass

    def output_tab(self):
        pass

    def deployment_tab(self):
        pass

    def debug_tab(self):
        pass

    def C_compiler_tab(self):
        pass

    def OS_tab(self):
        pass

    def info_tab(self):
        pass

    def plugin_tab(self):
        pass

    def console_tab(self):
        self.tab_15 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_15,text='打包控制台')
        
        self.console = scrolledtext.ScrolledText(self.tab_15,
                                                 background='#1e1e1e',
                                                 foreground='#f9f9f9',
                                                 font=tkinter.font.Font(family='Consolas',size=14))
        self.console.pack(fill='both',expand=True)

    '''
    def test_tab(self):
        self.tab_16 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_16, text='Test')
        self.btn_test = ttk.Button(self.tab_16, text='Test',\
                                   command=self.test)
        self.btn_test.pack(anchor='w', fill='y')
    '''

    def status(self):
        self.left = ttk.Frame(self.stat)
        self.left.pack(side='left',fill='both',expand=True)
    
    def get_system_info(self):   #Just on Linux
        try:
            # 获取登录用户名 (可靠方法)
            username = os.getlogin()
        except OSError:
            # 备选方案：从环境变量获取
            username = os.environ.get('USER', os.environ.get('LOGNAME', 'unknown'))
        
        # 获取主机名
        full_hostname = socket.gethostname()
        
        # 提取不含域名的主机名
        try:
            hostname = socket.gethostbyaddr(full_hostname)[0].split('.')[0]
        except socket.herror:
            hostname = full_hostname.split('.')[0]
        
        return f'{username}@{hostname} ~$ '
    
    def run_command(self, command:list|str):
        self.console.config(state='normal')
        self.console.insert(tk.END, f'操作系统: {platform.platform()}\n')
        self.console.see(tk.END)
        head = r'C:\Windows\System32 > ' if platform.system()=='Windows' \
        else self.get_system_info()
        cmd = ' '.join(command) if isinstance(command,list) else command
        self.console.insert(tk.END, head+cmd+'\n')
        self.console.see(tk.END)
        self.console.config(state='disabled')
        proc = subprocess.Popen(command,\
                                stdout=subprocess.PIPE,\
                                    stderr=subprocess.PIPE,\
                                        text=True,\
                                            bufsize=1,\
                                                universal_newlines=True)
        while True:
            output = proc.stdout.readline()  # type: ignore
            if output=='' and proc.poll() is not None:
                break
            if output:
                self.console.config(state='normal')
                self.console.insert(tk.END, output)
                self.console.see(tk.END)
                self.console.config(state='disabled')
                self.root.update_idletasks()
            time.sleep(0.1)
        ret_code = proc.poll()
        self.console.config(state='normal')
        self.console.insert(tk.END, '\n' + head + '\n')
        self.console.config(state='disabled')
        return ret_code
    
    def select_script(self): #Select Python script
        s = filedialog.askopenfilename(filetypes=[('Python脚本','*.py;*.pyw')])
        self.script.set(s)

    def select_interpreter(self):
        i = filedialog.askopenfilename(filetypes=[('Python解释器','*.exe')])
        pat = r'python(\d{1}\.\d{2}t)?.exe'
        if re.findall(pat, i):
            self.interpreter.set(i)
            return
        else:
            messagebox.showerror(title='错误',message='不是CPython解释器')
            return
    '''
    def test(self):
        t = threading.Thread(target=self.run_command,args=('ping 8.8.8.8',),daemon=True)
        t.start()
    '''

    def delete_selection(self, listbox:tk.Listbox):
        selection = listbox.curselection()
        if selection:
            listbox.delete(selection)
        else:
            messagebox.showwarning(title='警告', message='没有选中的项目!')
    
    def insert(self, listbox:tk.Listbox, content:str, cache:list):
        listbox.insert(tk.END, content)
        cache.append(content)



if __name__=='__main__':
    app = NuitkaGUI()
    