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
        self.style.configure("TNotebook.Tab", padding=(5, 5), font=('Consolas', 10))
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
        # 展开循环 - 为每个Python标志创建独立的控件和变量
        self.f_1 = ttk.LabelFrame(self.tab_0, text='Python标志', labelanchor='nw')
        self.f_1.place(x=620,y=20,width=600,height=280)
        
        # 为每个标志创建独立的IntVar和Checkbutton
        self.var_isolated = tk.IntVar(value=0)
        self.cbtn_isolated = ttk.Checkbutton(self.f_1, variable=self.var_isolated, offvalue=0, onvalue=1, text='isolated')
        self.cbtn_isolated.pack(anchor='w', fill='y')
        
        self.var_main = tk.IntVar(value=0)
        self.cbtn_main = ttk.Checkbutton(self.f_1, variable=self.var_main, offvalue=0, onvalue=1, text='main')
        self.cbtn_main.pack(anchor='w', fill='y')
        
        self.var_no_asserts = tk.IntVar(value=0)
        self.cbtn_no_asserts = ttk.Checkbutton(self.f_1, variable=self.var_no_asserts, offvalue=0, onvalue=1, text='no_asserts')
        self.cbtn_no_asserts.pack(anchor='w', fill='y')
        
        self.var_no_docstrings = tk.IntVar(value=0)
        self.cbtn_no_docstrings = ttk.Checkbutton(self.f_1, variable=self.var_no_docstrings, offvalue=0, onvalue=1, text='no_docstrings')
        self.cbtn_no_docstrings.pack(anchor='w', fill='y')
        
        self.var_no_site = tk.IntVar(value=0)
        self.cbtn_no_site = ttk.Checkbutton(self.f_1, variable=self.var_no_site, offvalue=0, onvalue=1, text='no_site')
        self.cbtn_no_site.pack(anchor='w', fill='y')
        
        self.var_no_warnings = tk.IntVar(value=0)
        self.cbtn_no_warnings = ttk.Checkbutton(self.f_1, variable=self.var_no_warnings, offvalue=0, onvalue=1, text='no_warnings')
        self.cbtn_no_warnings.pack(anchor='w', fill='y')
        
        self.var_safe_path = tk.IntVar(value=0)
        self.cbtn_safe_path = ttk.Checkbutton(self.f_1, variable=self.var_safe_path, offvalue=0, onvalue=1, text='safe_path')
        self.cbtn_safe_path.pack(anchor='w', fill='y')
        
        self.var_static_hashes = tk.IntVar(value=0)
        self.cbtn_static_hashes = ttk.Checkbutton(self.f_1, variable=self.var_static_hashes, offvalue=0, onvalue=1, text='static_hashes')
        self.cbtn_static_hashes.pack(anchor='w', fill='y')
        
        self.var_unbuffered = tk.IntVar(value=0)
        self.cbtn_unbuffered = ttk.Checkbutton(self.f_1, variable=self.var_unbuffered, offvalue=0, onvalue=1, text='unbuffered')
        self.cbtn_unbuffered.pack(anchor='w', fill='y')
        
        self.var_dont_write_bytecode = tk.IntVar(value=0)
        self.cbtn_dont_write_bytecode = ttk.Checkbutton(self.f_1, variable=self.var_dont_write_bytecode, offvalue=0, onvalue=1, text='dont_write_bytecode')
        self.cbtn_dont_write_bytecode.pack(anchor='w', fill='y')
        
        ##
        ##
        self.f_2 = ttk.Labelframe(self.tab_0, text='调试选项', labelanchor='nw')
        self.f_2.place(x=620, y=320, width=600,height=280)
        #
        self.py_dbg = tk.IntVar(value=0)
        self.cbtn_0 = ttk.Checkbutton(self.f_2, text='Python Debug', variable=self.py_dbg, offvalue=0, onvalue=1)
        self.cbtn_0.pack(anchor='w', fill='y')
        

    def package_tab(self):
        self.tab_1 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_1, text='包含包选项')
        #
        self.prefer_source_code = tk.BooleanVar(value=False)
        self.cbtn_17 = ttk.Checkbutton(self.tab_1, text='优先使用源代码而不是已经编译的扩展模块',
                                       variable=self.prefer_source_code, offvalue=False,
                                        onvalue=True)
        self.cbtn_17.place(x=20, y=20, width=1220, height=30)
        ##
        ##
        # 为每个包含类型创建独立的变量和控件
        self.includes_content = {
            'include_package': [],
            'include_module': [],
            'include_plugin_directory': [],
            'include_plugin_files': []
        }

        # 创建include_package控件组
        self.include_package_var = tk.StringVar(value='')
        self.include_package_frame = ttk.Frame(self.tab_1)
        self.include_package_frame.place(x=20, y=60, width=600, height=240)
        ttk.Label(self.include_package_frame, text='包含整个包:').place(x=10, y=10, width=80, height=30)
        self.include_package_entry = ttk.Entry(self.include_package_frame, textvariable=self.include_package_var)
        self.include_package_entry.place(x=100, y=10, width=250, height=25)
        self.include_package_add = ttk.Button(self.include_package_frame, text='添加', command=lambda: self.insert(self.include_package_list, self.include_package_var, self.includes_content['include_package']))
        self.include_package_add.place(x=360, y=10, width=80, height=35)
        self.include_package_del = ttk.Button(self.include_package_frame, text='删除选中', command=lambda: self.delete_selection(self.include_package_list))
        self.include_package_del.place(x=450, y=10, width=140, height=35)
        self.include_package_list = tk.Listbox(self.include_package_frame, width=45, font=tkinter.font.Font(family='Consolas', size=10), activestyle='dotbox')
        self.include_package_list.place(x=10, y=50, width=360, height=170)
        self.include_package_scroll_y = ttk.Scrollbar(self.include_package_frame, orient='vertical', command=self.include_package_list.yview)
        self.include_package_scroll_y.place(x=370, y=50, width=20, height=170)
        self.include_package_scroll_x = ttk.Scrollbar(self.include_package_frame, orient='horizontal', command=self.include_package_list.xview)
        self.include_package_scroll_x.place(x=10, y=220, width=360, height=20)
        self.include_package_list.config(yscrollcommand=self.include_package_scroll_y.set, xscrollcommand=self.include_package_scroll_x.set)

        # 创建include_module控件组
        self.include_module_var = tk.StringVar(value='')
        self.include_module_frame = ttk.Frame(self.tab_1)
        self.include_module_frame.place(x=640, y=60, width=600, height=240)
        ttk.Label(self.include_module_frame, text='包含单个模块:').place(x=10, y=10, width=80, height=30)
        self.include_module_entry = ttk.Entry(self.include_module_frame, textvariable=self.include_module_var)
        self.include_module_entry.place(x=100, y=10, width=250, height=25)
        self.include_module_add = ttk.Button(self.include_module_frame, text='添加', command=lambda: self.insert(self.include_module_list, self.include_module_var, self.includes_content['include_module']))
        self.include_module_add.place(x=360, y=10, width=80, height=35)
        self.include_module_del = ttk.Button(self.include_module_frame, text='删除选中', command=lambda: self.delete_selection(self.include_module_list))
        self.include_module_del.place(x=450, y=10, width=140, height=35)
        self.include_module_list = tk.Listbox(self.include_module_frame, width=45, font=tkinter.font.Font(family='Consolas', size=10), activestyle='dotbox')
        self.include_module_list.place(x=10, y=50, width=360, height=170)
        self.include_module_scroll_y = ttk.Scrollbar(self.include_module_frame, orient='vertical', command=self.include_module_list.yview)
        self.include_module_scroll_y.place(x=370, y=50, width=20, height=170)
        self.include_module_scroll_x = ttk.Scrollbar(self.include_module_frame, orient='horizontal', command=self.include_module_list.xview)
        self.include_module_scroll_x.place(x=10, y=220, width=360, height=20)
        self.include_module_list.config(yscrollcommand=self.include_module_scroll_y.set, xscrollcommand=self.include_module_scroll_x.set)

        # 创建include_plugin_directory控件组
        self.include_plugin_directory_var = tk.StringVar(value='')
        self.include_plugin_directory_frame = ttk.Frame(self.tab_1)
        self.include_plugin_directory_frame.place(x=20, y=320, width=600, height=240)
        ttk.Label(self.include_plugin_directory_frame, text='包含插件目录:').place(x=10, y=10, width=80, height=30)
        self.include_plugin_directory_entry = ttk.Entry(self.include_plugin_directory_frame, textvariable=self.include_plugin_directory_var)
        self.include_plugin_directory_entry.place(x=100, y=10, width=250, height=25)
        self.include_plugin_directory_add = ttk.Button(self.include_plugin_directory_frame, text='添加', command=lambda: self.insert(self.include_plugin_directory_list, self.include_plugin_directory_var, self.includes_content['include_plugin_directory']))
        self.include_plugin_directory_add.place(x=360, y=10, width=80, height=35)
        self.include_plugin_directory_del = ttk.Button(self.include_plugin_directory_frame, text='删除选中', command=lambda: self.delete_selection(self.include_plugin_directory_list))
        self.include_plugin_directory_del.place(x=450, y=10, width=140, height=35)
        self.include_plugin_directory_list = tk.Listbox(self.include_plugin_directory_frame, width=45, font=tkinter.font.Font(family='Consolas', size=10), activestyle='dotbox')
        self.include_plugin_directory_list.place(x=10, y=50, width=360, height=170)
        self.include_plugin_directory_scroll_y = ttk.Scrollbar(self.include_plugin_directory_frame, orient='vertical', command=self.include_plugin_directory_list.yview)
        self.include_plugin_directory_scroll_y.place(x=370, y=50, width=20, height=170)
        self.include_plugin_directory_scroll_x = ttk.Scrollbar(self.include_plugin_directory_frame, orient='horizontal', command=self.include_plugin_directory_list.xview)
        self.include_plugin_directory_scroll_x.place(x=10, y=220, width=360, height=20)
        self.include_plugin_directory_list.config(yscrollcommand=self.include_plugin_directory_scroll_y.set, xscrollcommand=self.include_plugin_directory_scroll_x.set)

        # 创建include_plugin_files控件组
        self.include_plugin_files_var = tk.StringVar(value='')
        self.include_plugin_files_frame = ttk.Frame(self.tab_1)
        self.include_plugin_files_frame.place(x=640, y=320, width=600, height=240)
        ttk.Label(self.include_plugin_files_frame, text='包含插件文件:').place(x=10, y=10, width=80, height=30)
        self.include_plugin_files_entry = ttk.Entry(self.include_plugin_files_frame, textvariable=self.include_plugin_files_var)
        self.include_plugin_files_entry.place(x=100, y=10, width=250, height=25)
        self.include_plugin_files_add = ttk.Button(self.include_plugin_files_frame, text='添加', command=lambda: self.insert(self.include_plugin_files_list, self.include_plugin_files_var, self.includes_content['include_plugin_files']))
        self.include_plugin_files_add.place(x=360, y=10, width=80, height=35)
        self.include_plugin_files_del = ttk.Button(self.include_plugin_files_frame, text='删除选中', command=lambda: self.delete_selection(self.include_plugin_files_list))
        self.include_plugin_files_del.place(x=450, y=10, width=140, height=35)
        self.include_plugin_files_list = tk.Listbox(self.include_plugin_files_frame, width=45, font=tkinter.font.Font(family='Consolas', size=10), activestyle='dotbox')
        self.include_plugin_files_list.place(x=10, y=50, width=360, height=170)
        self.include_plugin_files_scroll_y = ttk.Scrollbar(self.include_plugin_files_frame, orient='vertical', command=self.include_plugin_files_list.yview)
        self.include_plugin_files_scroll_y.place(x=370, y=50, width=20, height=170)
        self.include_plugin_files_scroll_x = ttk.Scrollbar(self.include_plugin_files_frame, orient='horizontal', command=self.include_plugin_files_list.xview)
        self.include_plugin_files_scroll_x.place(x=10, y=220, width=360, height=20)
        self.include_plugin_files_list.config(yscrollcommand=self.include_plugin_files_scroll_y.set, xscrollcommand=self.include_plugin_files_scroll_x.set)

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
        self.btn_2.config(command=lambda:self.insert(self.lbox_0, self.pkg_name_1,self.follow_imports_list))
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
        self.btn_4.config(command=lambda:self.insert(self.lbox_1, self.pkg_name_2, self.no_follow_imports_list))
        self.btn_5.config(command=lambda:self.delete_selection(self.lbox_1))

    def onefile_tab(self):
        self.tab_3 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_3, text='单文件选项')
        #setattr(self.tab_3, 'id', 'onefile')
        #
        self.onefile_no_compression = tk.BooleanVar(value=False)
        self.cbtn_10 = ttk.Checkbutton(self.tab_3, variable=self.onefile_no_compression,\
                                        offvalue=False, onvalue=True, text='不压缩单文件包')
        self.cbtn_10.grid(column=0, row=1, sticky='w', columnspan=2)
        #
        self.onefile_as_archive = tk.BooleanVar(value=False)
        self.cbtn_12 = ttk.Checkbutton(self.tab_3, variable=self.onefile_as_archive,\
                                        offvalue=False, onvalue=True,\
                                            text='创建可以使用nuitka-onefile-unapck解包的归档格式')
        self.cbtn_12.grid(column=0, row=2, sticky='w', columnspan=2)
        #
        self.onefile_no_dll = tk.BooleanVar(value=False)
        self.cbtn_14 = ttk.Checkbutton(self.tab_3, variable=self.onefile_no_dll,\
                                        offvalue=False, onvalue=True,\
                                            text='不使用DLL文件在运行之前解压, 使用EXE解压')
        self.cbtn_14.grid(column=0, row=3, sticky='w', columnspan=2)
        #
        self.onefile_tempdir_spec = tk.StringVar(value='')
        self.lb_19 = ttk.Label(self.tab_3, text='单文件临时目录:')
        self.lb_19.grid(column=0, row=4)
        #
        self.e_16 = ttk.Entry(self.tab_3, textvariable=self.onefile_tempdir_spec, width=100)
        self.e_16.grid(column=1, row=4, columnspan=4)
        #
        self.onefile_cache_mode = tk.StringVar(value='auto')
        self.lb_20 = ttk.Label(self.tab_3, text='单文件缓存模式:')
        self.lb_20.grid(column=0, row=5)
        #
        self.cbox_4 = ttk.Combobox(self.tab_3, values=['auto','tempdir','userdir'],\
                                      state='readonly', width=20)
        self.cbox_4.bind('<<ComboboxSelected>>', lambda event:self.onefile_cache_mode.set(self.cbox_4.get()))
        self.cbox_4.grid(column=1, row=5, sticky='w')
        #
        self.onefile_child_grace = tk.IntVar(value=5000)
        self.lb_21 = ttk.Label(self.tab_3, text='单文件子进程终止等待时间(毫秒):')
        self.lb_21.grid(column=0, row=6)
        #
        self.sbox_1 = ttk.Spinbox(self.tab_3, from_=0, to=30_000, increment=500, textvariable=self.onefile_child_grace)
        self.sbox_1.grid(column=1, row=6, sticky='w')

    def data_tab(self):
        self.tab_16 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_16, text='数据文件')
        #
        self.font_0 = tkinter.font.Font(family='Consolas', size=10)
        
        # 创建主框架容器
        self.main_container = ttk.Frame(self.tab_16)
        self.main_container.pack(fill='both', expand=True)
        
        # 创建 Canvas 和滚动条
        self.canvas = tk.Canvas(self.main_container)
        self.scr_4 = ttk.Scrollbar(self.main_container, orient='vertical', command=self.canvas.yview)
        self.scr_5 = ttk.Scrollbar(self.main_container, orient='horizontal', command=self.canvas.xview)
        
        # 配置 Canvas
        self.canvas.configure(
            yscrollcommand=self.scr_4.set,
            xscrollcommand=self.scr_5.set
        )
        
        # 放置 Canvas 和滚动条
        self.scr_4.pack(side='right', fill='y')
        self.scr_5.pack(side='bottom', fill='x')
        self.canvas.pack(side='left', fill='both', expand=True)
        
        # 创建内部框架
        self.frame = ttk.Frame(self.canvas)
        self.frame_id = self.canvas.create_window((0, 0), window=self.frame, anchor='nw')
        
        # 绑定事件
        self.frame.bind('<Configure>', lambda e: self.canvas.configure(scrollregion=self.canvas.bbox('all')))
        self.canvas.bind('<Configure>', lambda e: self.canvas.itemconfig(self.frame_id, width=e.width))
        self.canvas.bind_all('<MouseWheel>', self.on_mousewheel)
        ############################################################
        # 创建包含包数据文件的框架
        self.f_19 = ttk.Labelframe(self.frame, text='包含包数据文件', labelanchor='nw')
        self.f_19.pack(fill='x', padx=10, pady=10)
        
        # 包含包数据文件的控件
        self.include_package_data = []
        self.include_package_data_var = tk.StringVar(value='')
        
        ttk.Label(self.f_19, text='包含包数据文件的包').grid(row=0, column=0, padx=5, pady=5, sticky='w')
        self.e_17 = ttk.Entry(self.f_19, textvariable=self.include_package_data_var, width=70)
        self.e_17.grid(row=0, column=1, padx=5, pady=5, sticky='ew')
        
        self.btn_14 = ttk.Button(self.f_19, text='添加', command=lambda: self.insert(self.lbox_3, self.include_package_data_var, self.include_package_data))
        self.btn_14.grid(row=0, column=2, padx=5, pady=5)
        
        self.btn_15 = ttk.Button(self.f_19, text='删除选中', command=lambda: self.delete_selection(self.lbox_3))
        self.btn_15.grid(row=0, column=3, padx=5, pady=5)
        
        # 创建 Listbox 和滚动条
        self.list_frame_0 = ttk.Frame(self.f_19)
        self.list_frame_0.grid(row=1, column=0, columnspan=4, sticky='nsew', padx=5, pady=5)
        
        self.lbox_3 = tk.Listbox(self.list_frame_0, activestyle='dotbox', height=8, font=self.font_0)
        self.lbox_3_scroll_y = ttk.Scrollbar(self.list_frame_0, orient='vertical', command=self.lbox_3.yview)
        self.lbox_3_scroll_x = ttk.Scrollbar(self.list_frame_0, orient='horizontal', command=self.lbox_3.xview)
        
        self.lbox_3.config(
            yscrollcommand=self.lbox_3_scroll_y.set,
            xscrollcommand=self.lbox_3_scroll_x.set
        )
        
        # 放置 Listbox 和滚动条
        self.lbox_3.grid(row=0, column=0, sticky='nsew')
        self.lbox_3_scroll_y.grid(row=0, column=1, sticky='ns')
        self.lbox_3_scroll_x.grid(row=1, column=0, sticky='ew')
        
        # 配置网格权重
        self.list_frame_0.columnconfigure(0, weight=1)
        self.list_frame_0.rowconfigure(0, weight=1)
        self.f_19.columnconfigure(1, weight=1)
        ###########################################################

        #################################################################
        #不包含数据文件
        self.f_20 = ttk.Labelframe(self.frame, labelanchor='nw', text='不包含的数据文件模式')
        self.f_20.pack(fill='x', padx=10, pady=10)
        #
        self.lb_22 = ttk.Label(self.f_20, text='不包含的数据文件模式')
        self.lb_22.grid(column=0, row=0, padx=5, pady=5, sticky='ew')
        #
        self.noinclude_data_files = []
        self.noinclude_data_files_var = tk.StringVar(value='')
        self.e_18 = ttk.Entry(self.f_20, textvariable=self.noinclude_data_files_var, width=70)
        self.e_18.grid(column=1, row=0, padx=5, pady=5, sticky='ew')
        #
        self.btn_16 = ttk.Button(self.f_20, text='添加', command=lambda: self.insert(self.lbox_4, self.noinclude_data_files_var, self.noinclude_data_files))
        self.btn_16.grid(column=2, row=0, padx=5, pady=5)
        #
        self.btn_17 = ttk.Button(self.f_20, text='删除选中', command=lambda: self.delete_selection(self.lbox_4))
        self.btn_17.grid(column=3, row=0, padx=5, pady=5)
        ##
        self.list_frame_1 = ttk.Frame(self.f_20)
        self.list_frame_1.grid(column=0, row=1, columnspan=4, padx=5, pady=5, sticky='nsew')
        #
        self.lbox_4 = tk.Listbox(self.list_frame_1, activestyle='dotbox', height=8, font=self.font_0)
        self.scr_6 = ttk.Scrollbar(self.list_frame_1, command=self.lbox_4.yview, orient='vertical')
        self.scr_7 = ttk.Scrollbar(self.list_frame_1, command=self.lbox_4.xview, orient='horizontal')
        self.lbox_4.configure(yscrollcommand=self.scr_6.set, xscrollcommand=self.scr_7.set)
        #
        self.lbox_4.grid(column=0, row=0, sticky='nsew')
        self.scr_6.grid(column=1, row=0, sticky='ns')
        self.scr_7.grid(column=0, row=1, sticky='ew')
        #
        self.list_frame_1.columnconfigure(0, weight=1)
        self.list_frame_1.rowconfigure(0, weight=1)
        self.f_20.columnconfigure(1, weight=1)
        ##############################################################################
        #包含的数据文件
        self.include_data_files = dict()
        self.include_data_files_src = tk.StringVar(value='')
        self.include_data_files_dst = tk.StringVar(value='')
        ##
        self.f_21 = ttk.Labelframe(self.frame, text='包含的数据文件', labelanchor='nw')
        self.f_21.pack(fill='x', padx=10, pady=10)
        #
        self.lb_23 = ttk.Label(self.f_21, text='包含数据文件:')
        self.lb_23.grid(column=0, row=0, padx=5, pady=5, sticky='ew')
        #
        self.e_19 = ttk.Entry(self.f_21, textvariable=self.include_data_files_src, width=60)
        self.e_19.grid(column=1, row=0, padx=5, pady=5, sticky='ew')
        #
        self.lb_24 = ttk.Label(self.f_21, text='到:')
        self.lb_24.grid(column=2, row=0, padx=2, pady=2, sticky='ew')
        #
        self.e_20 = ttk.Entry(self.f_21, textvariable=self.include_data_files_dst, width=25)
        self.e_20.grid(column=3, row=0, padx=5, pady=5, sticky='ew')
        #
        self.btn_18 = ttk.Button(self.f_21, text='浏览', command=lambda: self.select_data_file(self.include_data_files_src))
        self.btn_18.grid(column=4, row=0, padx=5, pady=5, sticky='ew')
        #
        self.btn_19 = ttk.Button(self.f_21, text='插入', command=lambda: self.insert_cascade(self.lbox_5, self.lbox_6, self.include_data_files, self.include_data_files_src, self.include_data_files_dst))
        self.btn_19.grid(column=5, row=0, padx=5, pady=5, sticky='ew')
        #
        self.btn_20 = ttk.Button(self.f_21, text='删除选中', command=lambda: self.delete_cascade_selection(self.lbox_5, self.lbox_6, self.include_data_files))
        self.btn_20.grid(column=6, row=0, padx=5, pady=5, sticky='ew')
        ##
        self.list_frame_2 = ttk.Frame(self.f_21)
        self.list_frame_2.grid(column=1, row=1, padx=5, pady=5, sticky='nsew')
        #
        self.lbox_5 = tk.Listbox(self.list_frame_2, activestyle='dotbox', font=self.font_0, height=8, width=60)
        self.scr_8 = ttk.Scrollbar(self.list_frame_2, orient='vertical', command=self.lbox_5.yview)
        self.scr_9 = ttk.Scrollbar(self.list_frame_2, orient='horizontal', command=self.lbox_5.xview)
        self.lbox_5.config(xscrollcommand=self.scr_9.set, yscrollcommand=self.scr_8.set)
        self.lbox_5.grid(column=0, row=0, sticky='nsew')
        self.scr_9.grid(column=0, row=1, sticky='ew')
        self.scr_8.grid(column=1, row=0, sticky='ns')
        #$
        self.list_frame_3 = ttk.Frame(self.f_21)
        self.list_frame_3.grid(column=3, row=1, padx=5, pady=5, sticky='nsew')
        #
        self.lbox_6 = tk.Listbox(self.list_frame_3, activestyle='dotbox', height=8, width=25)
        self.scr_10 = ttk.Scrollbar(self.list_frame_3, orient='horizontal', command=self.lbox_6.xview)
        self.scr_11 = ttk.Scrollbar(self.list_frame_3, orient='vertical', command=self.lbox_6.yview)
        self.lbox_6.config(xscrollcommand=self.scr_10.set, yscrollcommand=self.scr_11.set)
        self.lbox_6.grid(column=0, row=0, sticky='nsew')
        self.scr_10.grid(column=0, row=1, sticky='ew')
        self.scr_11.grid(column=1, row=0, sticky='ns')
        ######################################################################
        ##############################################################################
        #包含的单文件外部数据文件
        self.include_onefile_external_data = dict()
        self.include_onefile_external_data_src = tk.StringVar(value='')
        self.include_onefile_external_data_dst = tk.StringVar(value='')
        ##
        self.f_22 = ttk.Labelframe(self.frame, text='包含的单文件外部数据文件', labelanchor='nw')
        self.f_22.pack(fill='x', padx=10, pady=10)
        #
        self.lb_25 = ttk.Label(self.f_22, text='包含单文件外部数据文件:')
        self.lb_25.grid(column=0, row=0, padx=5, pady=5, sticky='ew')
        #
        self.e_21 = ttk.Entry(self.f_22, textvariable=self.include_onefile_external_data_src, width=60)
        self.e_21.grid(column=1, row=0, padx=5, pady=5, sticky='ew')
        #
        self.lb_26 = ttk.Label(self.f_22, text='到:')
        self.lb_26.grid(column=2, row=0, padx=2, pady=2, sticky='ew')
        #
        self.e_22 = ttk.Entry(self.f_22, textvariable=self.include_onefile_external_data_dst, width=25)
        self.e_22.grid(column=3, row=0, padx=5, pady=5, sticky='ew')
        #
        self.btn_21 = ttk.Button(self.f_22, text='浏览', command=lambda: self.select_data_file(self.include_onefile_external_data_src))
        self.btn_21.grid(column=4, row=0, padx=5, pady=5, sticky='ew')
        #
        self.btn_22 = ttk.Button(self.f_22, text='插入', command=lambda: self.insert_cascade(self.lbox_7, self.lbox_8, self.include_onefile_external_data, self.include_onefile_external_data_src, self.include_onefile_external_data_dst))
        self.btn_22.grid(column=5, row=0, padx=5, pady=5, sticky='ew')
        #
        self.btn_23 = ttk.Button(self.f_22, text='删除选中', command=lambda: self.delete_cascade_selection(self.lbox_7, self.lbox_8, self.include_onefile_external_data))
        self.btn_23.grid(column=6, row=0, padx=5, pady=5, sticky='ew')
        ##
        self.list_frame_4 = ttk.Frame(self.f_22)
        self.list_frame_4.grid(column=1, row=1, padx=5, pady=5, sticky='nsew')
        #
        self.lbox_7 = tk.Listbox(self.list_frame_4, activestyle='dotbox', font=self.font_0, height=8, width=60)
        self.scr_12 = ttk.Scrollbar(self.list_frame_4, orient='vertical', command=self.lbox_7.yview)
        self.scr_13 = ttk.Scrollbar(self.list_frame_4, orient='horizontal', command=self.lbox_7.xview)
        self.lbox_7.config(xscrollcommand=self.scr_13.set, yscrollcommand=self.scr_12.set)
        self.lbox_7.grid(column=0, row=0, sticky='nsew')
        self.scr_13.grid(column=0, row=1, sticky='ew')
        self.scr_12.grid(column=1, row=0, sticky='ns')
        #$
        self.list_frame_5 = ttk.Frame(self.f_22)
        self.list_frame_5.grid(column=3, row=1, padx=5, pady=5, sticky='nsew')
        #
        self.lbox_8 = tk.Listbox(self.list_frame_5, activestyle='dotbox', height=8, width=25)
        self.scr_14 = ttk.Scrollbar(self.list_frame_5, orient='horizontal', command=self.lbox_8.xview)
        self.scr_15 = ttk.Scrollbar(self.list_frame_5, orient='vertical', command=self.lbox_8.yview)
        self.lbox_8.config(xscrollcommand=self.scr_14.set, yscrollcommand=self.scr_15.set)
        self.lbox_8.grid(column=0, row=0, sticky='nsew')
        self.scr_14.grid(column=0, row=1, sticky='ew')
        self.scr_15.grid(column=1, row=0, sticky='ns')
        ##########################################################################
        ##############################################################################
        #包含的数据目录
        self.include_data_dir = dict()
        self.include_data_dir_src = tk.StringVar(value='')
        self.include_data_dir_dst = tk.StringVar(value='')
        ##
        self.f_23 = ttk.Labelframe(self.frame, text='包含的目录', labelanchor='nw')
        self.f_23.pack(fill='x', padx=10, pady=10)
        #
        self.lb_27 = ttk.Label(self.f_23, text='包含目录:')
        self.lb_27.grid(column=0, row=0, padx=5, pady=5, sticky='ew')
        #
        self.e_23 = ttk.Entry(self.f_23, textvariable=self.include_data_dir_src, width=60)
        self.e_23.grid(column=1, row=0, padx=5, pady=5, sticky='ew')
        #
        self.lb_28 = ttk.Label(self.f_23, text='到:')
        self.lb_28.grid(column=2, row=0, padx=2, pady=2, sticky='ew')
        #
        self.e_24 = ttk.Entry(self.f_23, textvariable=self.include_data_dir_dst, width=25)
        self.e_24.grid(column=3, row=0, padx=5, pady=5, sticky='ew')
        #
        self.btn_24 = ttk.Button(self.f_23, text='浏览', command=lambda: self.select_data_dir(self.include_data_dir_src))
        self.btn_24.grid(column=4, row=0, padx=5, pady=5, sticky='ew')
        #
        self.btn_25 = ttk.Button(self.f_23, text='插入', command=lambda: self.insert_cascade(self.lbox_9, self.lbox_10, self.include_data_dir, self.include_data_dir_src, self.include_data_dir_dst))
        self.btn_25.grid(column=5, row=0, padx=5, pady=5, sticky='ew')
        #
        self.btn_26 = ttk.Button(self.f_23, text='删除选中', command=lambda: self.delete_cascade_selection(self.lbox_9, self.lbox_10, self.include_data_dir))
        self.btn_26.grid(column=6, row=0, padx=5, pady=5, sticky='ew')
        ##
        self.list_frame_6 = ttk.Frame(self.f_23)
        self.list_frame_6.grid(column=1, row=1, padx=5, pady=5, sticky='nsew')
        #
        self.lbox_9 = tk.Listbox(self.list_frame_6, activestyle='dotbox', font=self.font_0, height=8, width=60)
        self.scr_16 = ttk.Scrollbar(self.list_frame_6, orient='vertical', command=self.lbox_9.yview)
        self.scr_17 = ttk.Scrollbar(self.list_frame_6, orient='horizontal', command=self.lbox_9.xview)
        self.lbox_9.config(xscrollcommand=self.scr_17.set, yscrollcommand=self.scr_16.set)
        self.lbox_9.grid(column=0, row=0, sticky='nsew')
        self.scr_17.grid(column=0, row=1, sticky='ew')
        self.scr_16.grid(column=1, row=0, sticky='ns')
        #$
        self.list_frame_7 = ttk.Frame(self.f_23)
        self.list_frame_7.grid(column=3, row=1, padx=5, pady=5, sticky='nsew')
        #
        self.lbox_10 = tk.Listbox(self.list_frame_7, activestyle='dotbox', height=8, width=25)
        self.scr_18 = ttk.Scrollbar(self.list_frame_7, orient='horizontal', command=self.lbox_10.xview)
        self.scr_19 = ttk.Scrollbar(self.list_frame_7, orient='vertical', command=self.lbox_10.yview)
        self.lbox_10.config(xscrollcommand=self.scr_18.set, yscrollcommand=self.scr_19.set)
        self.lbox_10.grid(column=0, row=0, sticky='nsew')
        self.scr_18.grid(column=0, row=1, sticky='ew')
        self.scr_19.grid(column=1, row=0, sticky='ns')
        ######################################################################
        ##############################################################################
        #包含的原始数据目录
        self.include_raw_dir = dict()
        self.include_raw_dir_src = tk.StringVar(value='')
        self.include_raw_dir_dst = tk.StringVar(value='')
        ##
        self.f_25 = ttk.Labelframe(self.frame, text='包含的原始目录(权限不变)', labelanchor='nw')
        self.f_25.pack(fill='x', padx=10, pady=10)
        #
        self.lb_29 = ttk.Label(self.f_25, text='包含原始目录:')
        self.lb_29.grid(column=0, row=0, padx=5, pady=5, sticky='ew')
        #
        self.e_25 = ttk.Entry(self.f_25, textvariable=self.include_raw_dir_src, width=60)
        self.e_25.grid(column=1, row=0, padx=5, pady=5, sticky='ew')
        #
        self.lb_30 = ttk.Label(self.f_25, text='到:')
        self.lb_30.grid(column=2, row=0, padx=2, pady=2, sticky='ew')
        #
        self.e_26 = ttk.Entry(self.f_25, textvariable=self.include_raw_dir_dst, width=25)
        self.e_26.grid(column=3, row=0, padx=5, pady=5, sticky='ew')
        #
        self.btn_27 = ttk.Button(self.f_25, text='浏览', command=lambda: self.select_data_dir(self.include_raw_dir_src))
        self.btn_27.grid(column=4, row=0, padx=5, pady=5, sticky='ew')
        #
        self.btn_28 = ttk.Button(self.f_25, text='插入', command=lambda: self.insert_cascade(self.lbox_11, self.lbox_12, self.include_raw_dir, self.include_raw_dir_src, self.include_raw_dir_dst))
        self.btn_28.grid(column=5, row=0, padx=5, pady=5, sticky='ew')
        #
        self.btn_29 = ttk.Button(self.f_25, text='删除选中', command=lambda: self.delete_cascade_selection(self.lbox_11, self.lbox_12, self.include_raw_dir))
        self.btn_29.grid(column=6, row=0, padx=5, pady=5, sticky='ew')
        ##
        self.list_frame_8 = ttk.Frame(self.f_25)
        self.list_frame_8.grid(column=1, row=1, padx=5, pady=5, sticky='nsew')
        #
        self.lbox_11 = tk.Listbox(self.list_frame_8, activestyle='dotbox', font=self.font_0, height=8, width=60)
        self.scr_20 = ttk.Scrollbar(self.list_frame_8, orient='vertical', command=self.lbox_11.yview)
        self.scr_21 = ttk.Scrollbar(self.list_frame_8, orient='horizontal', command=self.lbox_11.xview)
        self.lbox_11.config(xscrollcommand=self.scr_21.set, yscrollcommand=self.scr_20.set)
        self.lbox_11.grid(column=0, row=0, sticky='nsew')
        self.scr_21.grid(column=0, row=1, sticky='ew')
        self.scr_20.grid(column=1, row=0, sticky='ns')
        #$
        self.list_frame_9 = ttk.Frame(self.f_25)
        self.list_frame_9.grid(column=3, row=1, padx=5, pady=5, sticky='nsew')
        #
        self.lbox_12 = tk.Listbox(self.list_frame_9, activestyle='dotbox', height=8, width=25)
        self.scr_22 = ttk.Scrollbar(self.list_frame_9, orient='horizontal', command=self.lbox_12.xview)
        self.scr_23 = ttk.Scrollbar(self.list_frame_9, orient='vertical', command=self.lbox_12.yview)
        self.lbox_12.config(xscrollcommand=self.scr_22.set, yscrollcommand=self.scr_23.set)
        self.lbox_12.grid(column=0, row=0, sticky='nsew')
        self.scr_22.grid(column=0, row=1, sticky='ew')
        self.scr_23.grid(column=1, row=0, sticky='ns')

    def dll_tab(self):
        self.tab_4 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_4, text='DLL选项')
        #
        self.noinclude_dlls = tk.StringVar(value='')
        self.lb_5 = ttk.Label(self.tab_4, text='不包含DLL列表:')
        self.lb_5.grid(column=0, row=0, sticky='e')
        #
        self.e_13 = ttk.Entry(self.tab_4, textvariable=self.noinclude_dlls, width=100)
        self.e_13.grid(column=1, row=0)
        #
        self.list_package_dlls = tk.StringVar(value='')
        self.lb_17 = ttk.Label(self.tab_4, text='列出包所包含的DLL:')
        self.lb_17.grid(column=0, row=1, sticky='e')
        #
        self.e_14 = ttk.Entry(self.tab_4, textvariable=self.list_package_dlls, width=100)
        self.e_14.grid(column=1, row=1)
        #
        self.list_package_exe = tk.StringVar(value='')
        self.lb_18 = ttk.Label(self.tab_4, text='列出包所包含的EXE:')
        self.lb_18.grid(column=0, row=2, sticky='e')
        #
        self.e_15 = ttk.Entry(self.tab_4, textvariable=self.list_package_exe, width=100)
        self.e_15.grid(column=1, row=2)

    def warn_tab(self):
        self.tab_5 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_5, text='警告控制')
        #
        self.warn_implicit_exception = tk.BooleanVar(value=False)
        self.cbtn_13 = ttk.Checkbutton(self.tab_5, variable=self.warn_implicit_exception,\
                                       offvalue=False, onvalue=True, text='启用编译时隐式异常警告')
        self.cbtn_13.grid(column=0, row=0, sticky='w', columnspan=2)
        #
        self.warn_unusual_code = tk.BooleanVar(value=False)
        self.cbtn_14 = ttk.Checkbutton(self.tab_5, variable=self.warn_unusual_code,\
                                       offvalue=False, onvalue=True, text='启用编译时检测到的异常代码警告')
        self.cbtn_14.grid(column=0, row=1, sticky='w', columnspan=2)
        #
        self.assume_yes_for_downloads = tk.BooleanVar(value=True)
        self.cbtn_15 = ttk.Checkbutton(self.tab_5, #variable=self.assume_yes_for_downloads,\
                                       command=self.disable_or_enable_download,\
                                       offvalue=False, onvalue=True, text='允许Nuitka在必要时下载外部代码(主要是编译器及其依赖)')
        ###self.cbtn_15.bind('<<Toggled>>', lambda event:self.disable_or_enable_download())
        self.cbtn_15.grid(column=0, row=2, sticky='w', columnspan=2)
        #
        self.nowarn_mnemonic = tk.StringVar(value='')
        self.lb_13 = ttk.Label(self.tab_5, text='禁用特定助记符的警告:')
        self.lb_13.grid(column=0, row=3)
        #
        self.e_11 = ttk.Entry(self.tab_5, textvariable=self.nowarn_mnemonic)
        self.e_11.grid(column=1, row=3)

    def run_tab(self):
        self.tab_6 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_6, text='运行选项')
        #
        self.run = tk.BooleanVar(value=False)
        self.cbtn_11 = ttk.Checkbutton(self.tab_6, variable=self.run, offvalue=False,\
                                       onvalue=True, text='编译后立即执行')
        self.cbtn_11.pack(anchor='w', fill='y')
        #
        self.debugger = tk.BooleanVar(value=False)
        self.cbtn_12 = ttk.Checkbutton(self.tab_6, variable=self.debugger, offvalue=False,\
                                       onvalue=True, text='调试器中运行(自动选择gdb/lldb)')
        self.cbtn_12.pack(anchor='w', fill='y')

    def compile_tab(self):
        self.tab_7 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_7, text='编译选项')
        #
        self.full_compat = tk.BooleanVar(value=False)
        self.cbtn_16 = ttk.Checkbutton(self.tab_7, variable=self.full_compat, offvalue=False,\
                                       onvalue=True, text='启用完全兼容CPython模式(测试)')
        self.cbtn_16.grid(column=0, row=0, sticky='w', columnspan=2)
        #
        self.lb_14 = ttk.Label(self.tab_7, text='选择__file__变量的值:')
        self.lb_14.grid(column=0, row=1, sticky='e')
        self.file_reference_choice = tk.StringVar(value='runtime')
        self.cbox_2 = ttk.Combobox(self.tab_7, values=['runtime','original','frozen'],\
                                   state='readonly', width=20)
        self.cbox_2.bind('<<ComboboxSelected>>', lambda event:self.file_reference_choice.set(self.cbox_2.get()))
        self.cbox_2.grid(column=1, row=1, sticky='w')
        #
        self.lb_15 = ttk.Label(self.tab_7, text='选择__name__变量和__package__变量的值:')
        self.lb_15.grid(column=0, row=2, sticky='e')
        self.module_name_choice = tk.StringVar(value='runtime')
        self.cbox_3 = ttk.Combobox(self.tab_7, values=['runtime', 'original'],\
                                    state='readonly', width=20)
        self.cbox_3.bind('<<ComboboxSelected>>', lambda event:self.module_name_choice.set(self.cbox_3.get()))
        self.cbox_3.grid(column=1, row=2, sticky='w')
        #
        self.user_package_configuration = tk.StringVar(value='')
        self.lb_16 = ttk.Label(self.tab_7, text='用户包配置YAML文件路径:')
        self.lb_16.grid(column=0, row=3)
        #
        self.e_12 = ttk.Entry(self.tab_7, textvariable=self.user_package_configuration,\
                              width=100, state='readonly')
        self.e_12.grid(column=1, row=3, columnspan=5)
        #
        self.btn_13 = ttk.Button(self.tab_7, text='浏览', command=self.select_yaml_file)
        self.btn_13.grid(column=6, row=3)

    def output_tab(self):
        self.tab_8 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_8, text='输出控制')
        #
        self.remove_output = tk.IntVar(value=1)
        self.cbtn_9 = ttk.Checkbutton(self.tab_8, text='编译完成后删除中间文件',\
                                      variable=self.remove_output, offvalue=0, onvalue=1)
        self.cbtn_9.grid(column=0, row=0, columnspan=2, sticky='w')
        #
        self.no_pyi_file = tk.IntVar(value=0)
        self.cbtn_10 = ttk.Checkbutton(self.tab_8, variable=self.no_pyi_file, offvalue=0,\
                                       onvalue=1, text='不为扩展模块创建pyi文件')
        self.cbtn_10.grid(column=0, row=1, columnspan=2, sticky='w')
        #
        self.lb_11 = ttk.Label(self.tab_8, text='可执行文件名:')
        self.lb_11.grid(column=0, row=3)
        #
        self.output_filename = tk.StringVar(value='')
        self.e_9 = ttk.Entry(self.tab_8, textvariable=self.output_filename, width=100)
        self.e_9.grid(column=1, row=3, columnspan=2)
        ##
        self.lb_12 = ttk.Label(self.tab_8, text='输出文件目录:')
        self.lb_12.grid(column=0, row=4)
        #
        self.output_dir = tk.StringVar(value='')
        self.e_10 = ttk.Entry(self.tab_8, textvariable=self.output_dir, width=100)
        self.e_10.grid(column=1, row=4, columnspan=2)
        #
        self.btn_12 = ttk.Button(self.tab_8, text='浏览', command=self.select_save_dir)
        self.btn_12.grid(column=3, row=4)

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
        self.notebook.add(self.tab_11, text='C编译器')
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
        self.lb_8 = ttk.Label(self.f_13, text='并行编译作业数(先点击一下按钮才能调节)')
        self.lb_8.grid(column=0, row=0, sticky='w')
        #self.jobs_values = ...
        self.jobs = tk.StringVar()
        self.sbox_0 = ttk.Spinbox(self.f_13, from_=1-os.cpu_count(), to=os.cpu_count(), textvariable=self.jobs) # type: ignore
        self.sbox_0.grid(column=1, row=0)
        #
        self.lb_9 = ttk.Label(self.f_13, text='链接时优化(可进一步防反汇编)')
        self.lb_9.grid(column=0, row=2, sticky='w')
        #
        self.lto = tk.StringVar(value='yes')
        self.cbox_1 = ttk.Combobox(self.f_13, values=['yes','no','auto'], state='readonly', width=19)
        self.cbox_1.bind('<<ComboboxSelected>>', lambda event:self.lto.set(self.cbox_1.get()))
        self.cbox_1.grid(column=1, row=2)

    def OS_tab(self):
        self.tab_12 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_12, text='系统选项')
        #
        self.f_14 = ttk.LabelFrame(self.tab_12, text='Windows选项')
        self.f_14.place(x=20, y=20, width=1220, height=360)
        #
        self.windows_uac_admin = tk.IntVar(value=0)
        self.cbtn_8 = ttk.Checkbutton(self.f_14, variable=self.windows_uac_admin, offvalue=0,\
                                      onvalue=1, text='向Windows用户账户控制请求管理员权限')
        self.cbtn_8.place(x=20, y=20 ,width=500, height=40)
        #
        self.f_15 = ttk.Labelframe(self.f_14, text='控制台模式', labelanchor='nw')
        self.f_15.place(x=20, y=80, width=540, height=260)
        self.windows_console_mode = tk.StringVar(value='force')
        self.wincm = {'force':'执行时跳出控制台',
                      'disable':'禁用控制台',
                      'attach':'从命令行启动时控制台附加到原控制台, 双击启动无控制台',
                      'hide':'控制台会被创建, 但会被最小化, 中途可能突然跳出'}
        self.ctrl_group_3 = dict()
        for k in self.wincm.keys():
            self.ctrl_group_3[k] = ttk.Radiobutton(self.f_15, value=k, text=self.wincm[k],\
                                                   variable=self.windows_console_mode)
            self.ctrl_group_3[k].pack(anchor='w', fill='y')

        ##
        ##
        self.f_16 = ttk.Labelframe(self.f_14, text='Windows应用程序ICO图标', labelanchor='nw')
        self.f_16.place(x=580, y=20, width=600, height=320)
        #
        self.lb_10 = ttk.Label(self.f_16, text='ICO图标路径:')
        self.lb_10.place(x=0, y=10, width=80, height=40)
        #
        self.windows_icon_from_ico = []
        self.win_ico_path = tk.StringVar()
        self.e_7 = ttk.Entry(self.f_16, textvariable=self.win_ico_path, state='readonly',\
                             width=40)
        self.e_7.place(x=90, y=15, width=200, height=30)
        #
        self.btn_8 = ttk.Button(self.f_16, text='浏览', command=self.select_ico)
        self.btn_8.place(x=300, y=15, width=60, height=35)
        #
        self.btn_10 = ttk.Button(self.f_16, text='插入', command=lambda:self.insert(self.lbox_2, self.win_ico_path, self.windows_icon_from_ico))
        self.btn_10.place(x=370, y=15, width=60, height=35)
        #
        self.btn_9 = ttk.Button(self.f_16, text='删除选中', command=lambda:self.delete_selection(self.lbox_2))
        self.btn_9.place(x=450, y=15, width=140, height=35)
        #
        self.f_17 = ttk.Frame(self.f_16)
        self.f_17.place(x=10, y=50, width=580, height=300)
        #
        self.lbox_2 = tk.Listbox(self.f_17, activestyle='dotbox')
        self.scr_2 = ttk.Scrollbar(self.f_17, command=self.lbox_2.yview, orient='vertical')
        self.scr_3 = ttk.Scrollbar(self.f_17, command=self.lbox_2.xview, orient='horizontal')
        self.lbox_2.configure(xscrollcommand=self.scr_3.set, yscrollcommand=self.scr_2.set)
        self.lbox_2.place(x=0, y=0, width=560, height=200)
        self.scr_2.place(x=580, y=0, width=20, height=200)
        self.scr_3.place(x=0, y=200, width=560, height=20)
        ##
        ##
        self.f_18 = ttk.Labelframe(self.tab_12, text='Linux选项', labelanchor='nw')
        self.f_18.place(x=20, y=400, width=1220, height=100)
        #
        self.lb_2 = ttk.Label(self.f_18, text='Linux单文件图标:')
        self.lb_2.grid(column=0, row=0)
        #
        self.linux_icon = tk.StringVar(value='')
        self.e_8 = ttk.Entry(self.f_18, textvariable=self.linux_icon, width=100, state='readonly')
        self.e_8.grid(column=1, row=0)
        #
        self.btn_11 = ttk.Button(self.f_18, text='浏览', command=self.select_ico)
        self.btn_11.grid(column=2, row=0)

    def info_tab(self):
        self.tab_13 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_13, text='版本信息')
        #
        # 为每个信息项创建独立的标签和输入框
        self.company_name_var = tk.StringVar()
        ttk.Label(self.tab_13, text='版本信息中公司名称').grid(column=0, row=0, padx=10, pady=10)
        ttk.Entry(self.tab_13, textvariable=self.company_name_var, width=100).grid(column=1, row=0, padx=10, pady=10)
        
        self.product_name_var = tk.StringVar()
        ttk.Label(self.tab_13, text='版本信息中产品名称').grid(column=0, row=1, padx=10, pady=10)
        ttk.Entry(self.tab_13, textvariable=self.product_name_var, width=100).grid(column=1, row=1, padx=10, pady=10)
        
        self.file_version_var = tk.StringVar()
        ttk.Label(self.tab_13, text='版本信息中文件版本').grid(column=0, row=2, padx=10, pady=10)
        ttk.Entry(self.tab_13, textvariable=self.file_version_var, width=100).grid(column=1, row=2, padx=10, pady=10)
        
        self.product_version_var = tk.StringVar()
        ttk.Label(self.tab_13, text='版本信息中产品版本').grid(column=0, row=3, padx=10, pady=10)
        ttk.Entry(self.tab_13, textvariable=self.product_version_var, width=100).grid(column=1, row=3, padx=10, pady=10)
        
        self.copyright_text_var = tk.StringVar()
        ttk.Label(self.tab_13, text='版本信息中版权信息').grid(column=0, row=4, padx=10, pady=10)
        ttk.Entry(self.tab_13, textvariable=self.copyright_text_var, width=100).grid(column=1, row=4, padx=10, pady=10)

    def plugin_tab(self):
        self.plugins = [
            "anti-bloat", "data-files", "delvewheel", "dill-compat", "dll-files",
            "enum-compat", "eventlet", "gevent", "gi", "glfw", "implicit-imports",
            "kivy", "matplotlib", "multiprocessing", "no-qt", "options-nanny",
            "pbr-compat", "pkg-resources", "playwright", "pmw-freezer",
            "pylint-warnings", "pyqt5", "pyqt6", "pyside2", "pyside6", "pywebview",
            "spacy", "tk-inter", "transformers"
        ]
        
        self.tab_14 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_14, text='插件选项')
        
        self.f_7 = ttk.Labelframe(self.tab_14, text='启用插件', labelanchor='nw')
        self.f_7.place(x=20, y=20, width=1220, height=200)
        
        # 为每个插件创建独立的IntVar和Checkbutton
        self.plugin_vars = {}
        self.plugin_buttons = {}
        
        # 第1列
        self.anti_bloat = tk.IntVar(value=0)
        self.cbtn_18 = ttk.Checkbutton(self.f_7, variable=self.anti_bloat, text="anti-bloat")
        self.cbtn_18.grid(column=0, row=0, sticky='w', padx=5, pady=2)
        
        self.data_files = tk.IntVar(value=0)
        self.cbtn_19 = ttk.Checkbutton(self.f_7, variable=self.data_files, text="data-files")
        self.cbtn_19.grid(column=0, row=1, sticky='w', padx=5, pady=2)
        
        self.delvewheel = tk.IntVar(value=0)
        self.cbtn_20 = ttk.Checkbutton(self.f_7, variable=self.delvewheel, text="delvewheel")
        self.cbtn_20.grid(column=0, row=2, sticky='w', padx=5, pady=2)
        
        self.dill_compat = tk.IntVar(value=0)
        self.cbtn_21 = ttk.Checkbutton(self.f_7, variable=self.dill_compat, text="dill-compat")
        self.cbtn_21.grid(column=0, row=3, sticky='w', padx=5, pady=2)
        
        self.dll_files = tk.IntVar(value=0)
        self.cbtn_22 = ttk.Checkbutton(self.f_7, variable=self.dll_files, text="dll-files")
        self.cbtn_22.grid(column=0, row=4, sticky='w', padx=5, pady=2)
        
        # 第2列
        self.enum_compat = tk.IntVar(value=0)
        self.cbtn_23 = ttk.Checkbutton(self.f_7, variable=self.enum_compat, text="enum-compat")
        self.cbtn_23.grid(column=1, row=0, sticky='w', padx=5, pady=2)
        
        self.eventlet = tk.IntVar(value=0)
        self.cbtn_24 = ttk.Checkbutton(self.f_7, variable=self.eventlet, text="eventlet")
        self.cbtn_24.grid(column=1, row=1, sticky='w', padx=5, pady=2)
        
        self.gevent = tk.IntVar(value=0)
        self.cbtn_25 = ttk.Checkbutton(self.f_7, variable=self.gevent, text="gevent")
        self.cbtn_25.grid(column=1, row=2, sticky='w', padx=5, pady=2)
        
        self.gi = tk.IntVar(value=0)
        self.cbtn_26 = ttk.Checkbutton(self.f_7, variable=self.gi, text="gi")
        self.cbtn_26.grid(column=1, row=3, sticky='w', padx=5, pady=2)
        
        self.glfw = tk.IntVar(value=0)
        self.cbtn_27 = ttk.Checkbutton(self.f_7, variable=self.glfw, text="glfw")
        self.cbtn_27.grid(column=1, row=4, sticky='w', padx=5, pady=2)
        
        # 第3列
        self.implicit_imports = tk.IntVar(value=0)
        self.cbtn_28 = ttk.Checkbutton(self.f_7, variable=self.implicit_imports, text="implicit-imports")
        self.cbtn_28.grid(column=2, row=0, sticky='w', padx=5, pady=2)
        
        self.kivy = tk.IntVar(value=0)
        self.cbtn_29 = ttk.Checkbutton(self.f_7, variable=self.kivy, text="kivy")
        self.cbtn_29.grid(column=2, row=1, sticky='w', padx=5, pady=2)
        
        self.matplotlib = tk.IntVar(value=0)
        self.cbtn_30 = ttk.Checkbutton(self.f_7, variable=self.matplotlib, text="matplotlib")
        self.cbtn_30.grid(column=2, row=2, sticky='w', padx=5, pady=2)
        
        self.multiprocessing = tk.IntVar(value=0)
        self.cbtn_31 = ttk.Checkbutton(self.f_7, variable=self.multiprocessing, text="multiprocessing")
        self.cbtn_31.grid(column=2, row=3, sticky='w', padx=5, pady=2)
        
        self.no_qt = tk.IntVar(value=0)
        self.cbtn_32 = ttk.Checkbutton(self.f_7, variable=self.no_qt, text="no-qt")
        self.cbtn_32.grid(column=2, row=4, sticky='w', padx=5, pady=2)
        
        # 第4列
        self.options_nanny = tk.IntVar(value=0)
        self.cbtn_33 = ttk.Checkbutton(self.f_7, variable=self.options_nanny, text="options-nanny")
        self.cbtn_33.grid(column=3, row=0, sticky='w', padx=5, pady=2)
        
        self.pbr_compat = tk.IntVar(value=0)
        self.cbtn_34 = ttk.Checkbutton(self.f_7, variable=self.pbr_compat, text="pbr-compat")
        self.cbtn_34.grid(column=3, row=1, sticky='w', padx=5, pady=2)
        
        self.pkg_resources = tk.IntVar(value=0)
        self.cbtn_35 = ttk.Checkbutton(self.f_7, variable=self.pkg_resources, text="pkg-resources")
        self.cbtn_35.grid(column=3, row=2, sticky='w', padx=5, pady=2)
        
        self.playwright = tk.IntVar(value=0)
        self.cbtn_36 = ttk.Checkbutton(self.f_7, variable=self.playwright, text="playwright")
        self.cbtn_36.grid(column=3, row=3, sticky='w', padx=5, pady=2)
        
        self.pmw_freezer = tk.IntVar(value=0)
        self.cbtn_37 = ttk.Checkbutton(self.f_7, variable=self.pmw_freezer, text="pmw-freezer")
        self.cbtn_37.grid(column=3, row=4, sticky='w', padx=5, pady=2)
        
        # 第5列
        self.pylint_warnings = tk.IntVar(value=0)
        self.cbtn_38= ttk.Checkbutton(self.f_7, variable=self.pylint_warnings, text="pylint-warnings")
        self.cbtn_38.grid(column=4, row=0, sticky='w', padx=5, pady=2)
        
        self.pyqt5 = tk.IntVar(value=0)
        self.cbtn_39 = ttk.Checkbutton(self.f_7, variable=self.pyqt5, text="pyqt5")
        self.cbtn_39.grid(column=4, row=1, sticky='w', padx=5, pady=2)
        
        self.pyqt6 = tk.IntVar(value=0)
        self.cbtn_40 = ttk.Checkbutton(self.f_7, variable=self.pyqt6, text="pyqt6")
        self.cbtn_40.grid(column=4, row=2, sticky='w', padx=5, pady=2)
        
        self.pyside2= tk.IntVar(value=0)
        self.cbtn_41 = ttk.Checkbutton(self.f_7, variable=self.pyside2, text="pyside2")
        self.cbtn_41.grid(column=4, row=3, sticky='w', padx=5, pady=2)
        
        self.pyside6 = tk.IntVar(value=0)
        self.cbtn_42 = ttk.Checkbutton(self.f_7, variable=self.pyside6, text="pyside6")
        self.cbtn_42.grid(column=4, row=4, sticky='w', padx=5, pady=2)
        
        # 第6列
        self.pywebview = tk.IntVar(value=0)
        self.cbtn_43 = ttk.Checkbutton(self.f_7, variable=self.pywebview, text="pywebview")
        self.cbtn_43.grid(column=5, row=0, sticky='w', padx=5, pady=2)
        
        self.spacy = tk.IntVar(value=0)
        self.cbtn_44 = ttk.Checkbutton(self.f_7, variable=self.spacy, text="spacy")
        self.cbtn_44.grid(column=5, row=1, sticky='w', padx=5, pady=2)
        
        self.tk_inter = tk.IntVar(value=0)
        self.cbtn_45 = ttk.Checkbutton(self.f_7, variable=self.tk_inter, text="tk-inter")
        self.cbtn_45.grid(column=5, row=2, sticky='w', padx=5, pady=2)
        
        self.transformers = tk.IntVar(value=0)
        self.cbtn_46 = ttk.Checkbutton(self.f_7, variable=self.transformers, text="transformers")
        self.cbtn_46.grid(column=5, row=3, sticky='w', padx=5, pady=2)
        
        # 其余部分保持不变...
        self.help_plugin = """=======================================================================
anti-bloat 精简优化：从广泛使用的库模块源代码中移除不必要的导入。
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
    
    def insert(self, listbox:tk.Listbox, content:tk.StringVar, cache:list):
        if content.get():
            listbox.insert(tk.END, content.get())
            cache.append(content.get())
            content.set('')
        else:
            messagebox.showwarning(title='警告', message='你没有输入任何内容!')
    
    def browse_user_plugin(self):
        f = filedialog.askopenfilename()
        self.user_plugin.set(f)

    def select_xml(self):
        f = filedialog.asksaveasfilename(filetypes=[('XML文件', '*.xml')])
        self.xml_filename.set(f)

    def select_ico(self):
        f = filedialog.askopenfilename(filetypes=[('ICO图标文件', '*.ico')])
        self.win_ico_path.set(f)
    
    def select_save_dir(self):
        f = filedialog.askdirectory()
        self.output_dir.set(f)
    
    def disable_or_enable_download(self):
        if self.assume_yes_for_downloads.get():
            r = messagebox.askyesno(title='确认', message='禁止Nuitka在必要时下载外部代码(主要是编译器及其依赖)吗?')
            if r:
                self.assume_yes_for_downloads.set(False)
        else:
            self.assume_yes_for_downloads.set(True)

    def select_yaml_file(self):
        f = filedialog.askopenfilename(filetypes=[('YAML文件', '*.yml;*.yaml')])
        self.user_package_configuration.set(f)
    
    def on_mousewheel(self, event):
        """处理鼠标滚轮滚动"""
        if event.num == 5 or event.delta == -120:  # 向下滚动
            self.canvas.yview_scroll(1, "units")
        if event.num == 4 or event.delta == 120:   # 向上滚动
            self.canvas.yview_scroll(-1, "units")

    def insert_cascade(self, listbox_0:tk.Listbox, listbox_1:tk.Listbox, cache:dict, var_0:tk.StringVar, var_1:tk.StringVar):
        src = var_0.get()
        dst = var_1.get()
        if src and dst:
            listbox_0.insert(tk.END, src)
            listbox_1.insert(tk.END, dst)
            cache[src] = dst
            var_0.set('')
            var_1.set('')
        else:
            messagebox.showwarning(title='警告', message='你没有输入任何内容!')

    def select_data_file(self, var:tk.StringVar):
        f = filedialog.askopenfilename(filetypes=[('所有数据文件', '*.*')])
        if f:
            fn = f.replace('\\', '/')
            var.set(fn)

    def delete_cascade_selection(self, listbox_1:tk.Listbox, listbox_2:tk.Listbox, cache:dict):
        s1 = listbox_1.curselection()
        s2 = listbox_2.curselection()
        if s1:
            item_1 = listbox_1.get(s1)
            #item_2 = listbox_2.get(s1)
            listbox_1.delete(s1)
            listbox_2.delete(s1)
            cache.pop(item_1)
        elif s2:
            item_1 = listbox_1.get(s2)
            #item_2 = listbox_2.get(s2)
            listbox_1.delete(s2)
            listbox_2.delete(s2)
            cache.pop(item_1)
        else:
            messagebox.showwarning(title='警告', message='你没有选中任何项目')
    
    def select_data_dir(self, var:tk.StringVar):
        f = filedialog.askdirectory(mustexist=True)
        if f:
            fn = f.replace('\\', '/')
            var.set(fn)


if __name__=='__main__':
    app = NuitkaGUI()
    