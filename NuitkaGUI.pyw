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

        self.theme = 'vista' if platform.system()=='Windows' else 'clam'

        self.style = ttk.Style()
        self.style.theme_use(self.theme)
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
        self.style.configure("TSpinbox", font=('Consolas', 10))
        
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
        self.py_flag = []
        self.ctrl_group_1 = dict()
        self.var_group_1 = dict()
        for f in self.py_flags:
            self.var_group_1[f] = tk.IntVar(value=0)
            self.ctrl_group_1[f] = ttk.Checkbutton(self.f_1, variable=self.var_group_1[f],\
                                                   offvalue=0, onvalue=1, text=f)
            self.ctrl_group_1[f].pack(anchor='w', fill='y')
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
        self.lbox_0 = tk.Listbox(self.f_4, activestyle='dotbox', width=60)
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
        self.lbox_1 = tk.Listbox(self.f_6, activestyle='dotbox', width=60)
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
        self.tab_9 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_9, text='部署选项')
        #
        self.deployment = tk.IntVar(value=0)
        self.rbtn_7 = ttk.Radiobutton(self.tab_9, text='禁用使查找兼容性问题更容易的代码',\
                                      value=2, variable=self.deployment)
        self.rbtn_7.grid(column=0, row=0, sticky='w')
        #
        self.rbtn_8 = ttk.Radiobutton(self.tab_9, variable=self.deployment, value=1,\
                                      text='保持部署模式但禁用部分功能')
        self.rbtn_8.grid(column=0, row=1, sticky='w')

        self.lb_7 = ttk.Label(self.tab_9, text='禁用选项')
        self.lb_7.grid(column=0, row=2)

        self.no_deployment_flag = tk.StringVar()
        self.e_6 = ttk.Entry(self.tab_9, textvariable=self.no_deployment_flag)
        #self.e_6.config(state='disabled')
        self.e_6.grid(column=1, row=2, sticky='w')

        self.rbtn_8.bind('<<RadioButtonSelected>>', lambda event:self.e_6.config(state='normal'))
        self.rbtn_7.bind('<<RadioButtonSelected>>', lambda event:self.e_6.config(state='disabled'))
        #
        self.rbtn_9 = ttk.Radiobutton(self.tab_9, variable=self.deployment, value=0,\
                                      text='不进行处理')
        self.rbtn_9.bind('<<RadioButtonSelected>>', lambda event:self.e_6.config(state='disabled'))
        self.rbtn_9.grid(column=0, row=3, sticky='w')

    def debug_tab(self):
        self.tab_10 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_10, text='调试选项')
        #
        self.f_10 = ttk.Labelframe(self.tab_10, text='调试性选项(不建议)')
        self.f_10.place(x=20, y=20, width=1220, height=160)
        #
        self.debug = tk.IntVar(value=0)
        self.cbtn_4 = ttk.Checkbutton(self.f_10, variable=self.debug, offvalue=0, onvalue=1,\
                                      text='执行所有可能的自检以查错')
        self.cbtn_4.pack(anchor='w', fill='y')
        #
        self.unstripped = tk.IntVar(value=0)
        self.cbtn_5 = ttk.Checkbutton(self.f_10, variable=self.unstripped, offvalue=0,\
                                      onvalue=1, text='在结果对象文件中保留调试信息')
        self.cbtn_5.pack(anchor='w', fill='y')
        #
        self.trace_execution = tk.IntVar(value=0)
        self.cbtn_6 = ttk.Checkbutton(self.f_10, variable=self.trace_execution, offvalue=0,\
                                      onvalue=1, text='跟踪执行输出(执行前输出代码行)')
        self.cbtn_6.pack(anchor='w', fill='y')
        ##
        ##
        self.f_11 = ttk.Labelframe(self.tab_10, text='调试与优化')
        self.f_11.place(x=20, y=200, width=1220, height=200)
        #
        self.lb_6 = ttk.Label(self.f_11, text='将优化结果与程序结构写入的XML文件:')
        self.lb_6.grid(column=0, row=0)
        #
        self.xml_filename = tk.StringVar()
        self.e_5 = ttk.Entry(self.f_11, textvariable=self.xml_filename, width=70)
        self.e_5.grid(column=1, row=0)
        #
        self.btn_7 = ttk.Button(self.f_11, text='浏览', command=self.select_xml)
        self.btn_7.grid(column=2, row=0)
        #
        self.low_memory = tk.IntVar(value=1)
        self.cbtn_7 = ttk.Checkbutton(self.f_11, variable=self.low_memory, offvalue=0,\
                                      onvalue=1, text='降低内存用量')
        self.cbtn_7.grid(column=0, row=2, sticky='w')

    def C_compiler_tab(self):
        self.tab_11 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_11, text='C编译器选项')
        self.f_12 = ttk.LabelFrame(self.tab_11, text='C编译器', labelanchor='nw')
        self.f_12.place(x=20, y=20, width=1220, height=260)
        #
        self.C_complier = tk.StringVar(value='mingw64')
        self.rbtn_10 = ttk.Radiobutton(self.f_12, variable=self.C_complier, value='mingw64',\
                                       text='MinGW64编译器')
        self.rbtn_10.pack(anchor='w', fill='y')
        self.rbtn_11 = ttk.Radiobutton(self.f_12, variable=self.C_complier, value='clang',\
                                       text='Clang编译器')
        self.rbtn_11.pack(anchor='w', fill='y')
        self.rbtn_12 = ttk.Radiobutton(self.f_12, variable=self.C_complier, value='msvc',\
                                       text='MSVC编译器(下面填写版本)')
        self.rbtn_12.pack(anchor='w', fill='y')
        self.cbox_0 = ttk.Combobox(self.f_12, values=['latest'], state='normal')
        self.cbox_0.pack(anchor='w', fill='y')
        #
        self.f_13 = ttk.Labelframe(self.tab_11, text='加速与优化', labelanchor='nw')
        self.f_13.place(x=20, y=300, width=1220, height=260)
        #
        self.lb_8 = ttk.Label(self.f_13, text='并行编译作业数')
        self.lb_8.grid(column=0, row=0)
        #self.jobs_values = ...
        self.jobs = tk.StringVar()
        self.sbox_0 = ttk.Spinbox(self.f_13, from_=1-os.cpu_count(), to=os.cpu_count(), textvariable=self.jobs) # type: ignore
        self.sbox_0.grid(column=1, row=0)
        #
        self.lb_9 = ttk.Label(self.f_13, text='链接时优化')
        self.lb_9.grid(column=0, row=2)
        #
        self.lto = tk.StringVar(value='yes')
        self.cbox_1 = ttk.Combobox(self.f_13, values=['yes','no','auto'], state='readonly')
        self.cbox_1.bind('<<ComboboxSelected>>', lambda event:self.lto.set(self.cbox_1.get()))
        self.cbox_1.grid(column=1, row=2)

    def OS_tab(self):
        pass

    def info_tab(self):
        pass

    def plugin_tab(self):
        self.plugins = [
        "anti-bloat",
        "data-files",
        "delvewheel",
        "dill-compat",
        "dll-files",
        "enum-compat",
        "eventlet",
        "gevent",
        "gi",
        "glfw",
        "implicit-imports",
        "kivy",
        "matplotlib",
        "multiprocessing",
        "no-qt",
        "options-nanny",
        "pbr-compat",
        "pkg-resources",
        "playwright",
        "pmw-freezer",
        "pylint-warnings",
        "pyqt5",
        "pyqt6",
        "pyside2",
        "pyside6",
        "pywebview",
        "spacy",
        "tk-inter",
        "transformers",
        "upx"] #30 items,6 columns,5 rows
        #
        self.tab_14 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_14, text='插件选项')
        #
        self.f_7 = ttk.Labelframe(self.tab_14, text='启用插件', labelanchor='nw')
        self.f_7.place(x=20, y=20, width=1220, height=200)
        #
        self.ctrl_group_2 = dict()
        self.var_group_2 = dict()
        for i in range(30):
            p = self.plugins[i]
            self.var_group_2[p] = tk.IntVar(value=0)
            self.ctrl_group_2[p] = ttk.Checkbutton(self.f_7, variable=self.var_group_2[p],\
                                                   offvalue=0, onvalue=1, text=p)
            row = i % 5
            col = i % 6
            self.ctrl_group_2[p].grid(column=col, row=row, sticky='w')
        
        #
        self.help_plugin = """anti-bloat 精简优化：从广泛使用的库模块源代码中移除不必要的导入。
data-files 数据文件：根据包配置文件包含指定的数据文件。
delvewheel delvewheel 支持：在独立模式下支持使用 delvewheel 的包所必需。
dill-compat dill 兼容性：为 'dill' 包和 'cloudpickle' 提供兼容性支持所必需。
dll-files DLL 文件：根据包配置文件包含 DLL 文件。
enum-compat 枚举兼容性：为 Python2 和 'enum' 包提供兼容性支持所必需。
eventlet eventlet 支持：支持包含 'eventlet' 依赖项及其对 'dns' 包进行动态补丁的需求。
gevent gevent 支持：为 'gevent' 包所必需。
gi GI (GObject Introspection) 支持：支持 GI 包的 typelib 依赖。
glfw glfw 支持：在独立模式下为 'OpenGL' (PyOpenGL) 和 'glfw' 包所必需。
implicit-imports 隐式导入：根据包配置文件提供包的隐式导入。
kivy Kivy 支持：为 'kivy' 包所必需。
matplotlib Matplotlib 支持：为 'matplotlib' 模块所必需。
multiprocessing 多进程支持：为 Python 的 'multiprocessing' 模块所必需。
no-qt 禁用 Qt：禁止包含所有 Qt 绑定库。
options-nanny 选项保姆：根据包配置文件，向用户提示潜在问题。
pbr-compat pbr 兼容性：在独立模式下为 'pbr' 包所必需。
pkg-resources pkg_resources 支持：为 'pkg_resources' 提供解决方案。
playwright Playwright 支持：为 'playwright' 包所必需。
pmw-freezer Pmw 支持：为 'Pmw' 包所必需。
pylint-warnings PyLint 警告支持：支持 PyLint / PyDev 的源代码标记。
pyqt5 PyQt5 支持：为 PyQt5 包所必需。
pyqt6 PyQt6 支持：在独立模式下为 PyQt6 包所必需。
pyside2 PySide2 支持：为 PySide2 包所必需。
pyside6 PySide6 支持：在独立模式下为 PySide6 包所必需。
pywebview Webview 支持：为 'webview' 包 (PyPI 上的 pywebview) 所必需。
spacy spaCy 支持：为 'spacy' 包所必需。
tk-inter Tkinter 支持：为 Python 的 Tk 模块所必需。
transformers Transformers 支持：为 transformers 包提供隐式导入。
upx UPX 压缩：自动使用 UPX 压缩生成的可执行文件。
========================================================================"""
        #
        self.f_8 = ttk.Labelframe(self.tab_14, text='用户插件', labelanchor='nw')
        self.f_8.place(x=20, y=240, width=1220, height=100)
        self.lb_5 = ttk.Label(self.f_8, text='用户插件路径')
        self.lb_5.grid(column=0, row=0)
        #
        self.user_plugin = tk.StringVar(value='')
        self.e_4 = ttk.Entry(self.f_8, textvariable=self.user_plugin, width=100)
        self.e_4.grid(column=1, columnspan=2, row=0)
        #
        self.btn_6 = ttk.Button(self.f_8, text='浏览', command=self.browse_user_plugin)
        self.btn_6.grid(column=3, row=0)
        ##
        ##
        self.f_9 = ttk.Labelframe(self.tab_14, text='标准插件帮助', labelanchor='nw')
        self.f_9.place(x=20, y=360, width=1220, height=200)
        #
        self.stxt_0 = scrolledtext.ScrolledText(self.f_9, font=tkinter.font.Font(family='Consolas', size=12))
        self.stxt_0.pack(fill='both', expand=True)
        self.stxt_0.insert(tk.END, self.help_plugin)
        self.stxt_0.config(state='disabled')

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
    
    def browse_user_plugin(self):
        f = filedialog.askopenfilename()
        self.user_plugin.set(f)

    def select_xml(self):
        f = filedialog.asksaveasfilename(filetypes=[('XML文件', '*.xml')])
        self.xml_filename.set(f)



if __name__=='__main__':
    app = NuitkaGUI()
    