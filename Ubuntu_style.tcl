# ubuntu-24.04-theme.tcl
# Ubuntu 24.04 LTS 风格主题 for Tkinter/ttk
# 使用方法: 
#   root = tk.Tk()
#   root.tk.call("source", "ubuntu-24.04-theme.tcl")
#   root.tk.call("set_theme", "ubuntu-light")  # 或 "ubuntu-dark"

namespace eval ttk::theme::ubuntu {
    variable version 1.0
    variable colors
    array set colors {
        -fg             "#2c2c2c"
        -bg             "#f5f5f5"
        -disabledfg     "#9c9c9c"
        -selectfg       "#ffffff"
        -selectbg       "#e95420"
        -window         "#ffffff"
        -focuscolor     "#e95420"
        -borderwidth    1
        -dark           "#dedede"
        -darker         "#c8c8c8"
        -light          "#f5f5f5"
        -lighter        "#ffffff"
        -activebg       "#f0f0f0"
        -disabledbg     "#f5f5f5"
        -entrybg        "#ffffff"
        -troughcolor    "#e0e0e0"
        -slidercolor    "#ffffff"
        -arrowcolor     "#5e5e5e"
        -tabbg          "#f0f0f0"
    }
}

namespace eval ttk::theme::ubuntu-dark {
    variable version 1.0
    variable colors
    array set colors {
        -fg             "#ffffff"
        -bg             "#2d2d2d"
        -disabledfg     "#7a7a7a"
        -selectfg       "#ffffff"
        -selectbg       "#e95420"
        -window         "#383838"
        -focuscolor     "#e95420"
        -borderwidth    1
        -dark           "#242424"
        -darker         "#1a1a1a"
        -light          "#353535"
        -lighter        "#404040"
        -activebg       "#353535"
        -disabledbg     "#2d2d2d"
        -entrybg        "#383838"
        -troughcolor    "#404040"
        -slidercolor    "#4a4a4a"
        -arrowcolor     "#b0b0b0"
        -tabbg          "#353535"
    }
}

proc ttk::theme::ubuntu::init {} {
    variable colors
    ttk::style theme settings ubuntu-light {
        # 配置基本颜色
        ttk::style configure . \
            -background $colors(-bg) \
            -foreground $colors(-fg) \
            -troughcolor $colors(-troughcolor) \
            -focuscolor $colors(-focuscolor) \
            -selectbackground $colors(-selectbg) \
            -selectforeground $colors(-selectfg) \
            -fieldbackground $colors(-entrybg) \
            -font {Ubuntu 10} \
            -borderwidth $colors(-borderwidth) \
            -relief flat

        # 映射状态相关颜色
        ttk::style map . \
            -background [list disabled $colors(-disabledbg) active $colors(-activebg)] \
            -foreground [list disabled $colors(-disabledfg)] \
            -selectbackground [list !focus $colors(-darker)] \
            -selectforeground [list !focus $colors(-fg)]

        # 配置按钮
        ttk::style configure TButton \
            -anchor center \
            -width -10 \
            -padding {10 4} \
            -relief flat \
            -focuscolor $colors(-focuscolor)
        
        ttk::style map TButton \
            -background [list \
                pressed $colors(-darker) \
                active $colors(-dark) \
                !disabled $colors(-light)] \
            -lightcolor [list pressed $colors(-darker)] \
            -darkcolor [list pressed $colors(-darker)]

        # 配置工具栏按钮
        ttk::style configure Toolbutton -anchor center -padding {6 4} -relief flat
        ttk::style map Toolbutton \
            -background [list \
                selected $colors(-dark) \
                pressed $colors(-darker) \
                active $colors(-dark)]

        # 配置单选按钮和复选框
        ttk::style configure TCheckbutton -indicatorbackground $colors(-window) -indicatormargin {0 2 4 2}
        ttk::style configure TRadiobutton -indicatorbackground $colors(-window) -indicatormargin {0 2 4 2}
        
        ttk::style map TCheckbutton \
            -indicatorbackground [list \
                pressed $colors(-window) \
                alternate $colors(-darker) \
                selected $colors(-selectbg)]
        
        ttk::style map TRadiobutton \
            -indicatorbackground [list \
                pressed $colors(-window) \
                alternate $colors(-darker) \
                selected $colors(-selectbg)]

        # 配置组合框
        ttk::style configure TCombobox -padding {6 4} -arrowsize 12
        ttk::style map TCombobox \
            -fieldbackground [list readonly $colors(-lighter)] \
            -background [list \
                pressed $colors(-darker) \
                active $colors(-dark)] \
            -arrowcolor [list disabled $colors(-disabledfg)]

        # 配置滚动条
        ttk::style configure Horizontal.TScrollbar -background $colors(-bg)
        ttk::style configure Vertical.TScrollbar -background $colors(-bg)
        
        ttk::style map TScrollbar \
            -background [list \
                pressed $colors(-darker) \
                active $colors(-dark)] \
            -arrowcolor [list disabled $colors(-disabledfg)]

        # 配置进度条
        ttk::style configure Horizontal.TProgressbar \
            -background $colors(-selectbg) \
            -troughcolor $colors(-troughcolor) \
            -borderwidth 0 \
            -lightcolor $colors(-selectbg) \
            -darkcolor $colors(-selectbg)
            
        ttk::style configure Vertical.TProgressbar \
            -background $colors(-selectbg) \
            -troughcolor $colors(-troughcolor) \
            -borderwidth 0 \
            -lightcolor $colors(-selectbg) \
            -darkcolor $colors(-selectbg)

        # 配置标签框架
        ttk::style configure TLabelframe -background $colors(-bg)
        ttk::style configure TLabelframe.Label -background $colors(-bg) -foreground $colors(-fg)

        # 配置分页控件
        ttk::style configure TNotebook -background $colors(-tabbg) -tabmargins {2 2 2 0}
        ttk::style configure TNotebook.Tab \
            -padding {12 4} \
            -background $colors(-tabbg) \
            -lightcolor $colors(-tabbg) \
            -darkcolor $colors(-tabbg)
            
        ttk::style map TNotebook.Tab \
            -background [list selected $colors(-lighter)] \
            -lightcolor [list selected $colors(-lighter)] \
            -darkcolor [list selected $colors(-lighter)] \
            -expand [list selected {2 2 2 0}]

        # 配置标尺
        ttk::style configure Horizontal.TScale -troughcolor $colors(-troughcolor)
        ttk::style configure Vertical.TScale -troughcolor $colors(-troughcolor)
        
        ttk::style map TScale \
            -slidercolor [list active $colors(-dark)] \
            -sliderwidth [list active 16]

        # 配置分离器
        ttk::style configure TSeparator -background $colors(-dark)

        # 配置树视图
        ttk::style configure Treeview \
            -background $colors(-window) \
            -fieldbackground $colors(-window) \
            -foreground $colors(-fg)
            
        ttk::style map Treeview \
            -background [list selected $colors(-selectbg)] \
            -foreground [list selected $colors(-selectfg)]

        # 配置菜单
        option add *Menu.background $colors(-lighter)
        option add *Menu.foreground $colors(-fg)
        option add *Menu.activeBackground $colors(-selectbg)
        option add *Menu.activeForeground $colors(-selectfg)
        option add *Menu.disabledForeground $colors(-disabledfg)
        option add *Menu.borderWidth 1
        option add *Menu.relief flat

        # 配置滚动条箭头
        ttk::style layout Vertical.TScrollbar {
            Vertical.Scrollbar.trough -sticky ns -children {
                Vertical.Scrollbar.uparrow -side top
                Vertical.Scrollbar.downarrow -side bottom
                Vertical.Scrollbar.thumb -expand 1 -side top
            }
        }

        ttk::style layout Horizontal.TScrollbar {
            Horizontal.Scrollbar.trough -sticky ew -children {
                Horizontal.Scrollbar.leftarrow -side left
                Horizontal.Scrollbar.rightarrow -side right
                Horizontal.Scrollbar.thumb -expand 1 -side left
            }
        }
    }
}

proc ttk::theme::ubuntu-dark::init {} {
    variable colors
    ttk::style theme settings ubuntu-dark {
        # 配置基本颜色
        ttk::style configure . \
            -background $colors(-bg) \
            -foreground $colors(-fg) \
            -troughcolor $colors(-troughcolor) \
            -focuscolor $colors(-focuscolor) \
            -selectbackground $colors(-selectbg) \
            -selectforeground $colors(-selectfg) \
            -fieldbackground $colors(-entrybg) \
            -font {Ubuntu 10} \
            -borderwidth $colors(-borderwidth) \
            -relief flat

        # 映射状态相关颜色
        ttk::style map . \
            -background [list disabled $colors(-disabledbg) active $colors(-activebg)] \
            -foreground [list disabled $colors(-disabledfg)] \
            -selectbackground [list !focus $colors(-darker)] \
            -selectforeground [list !focus $colors(-fg)]

        # 配置按钮
        ttk::style configure TButton \
            -anchor center \
            -width -10 \
            -padding {10 4} \
            -relief flat \
            -focuscolor $colors(-focuscolor)
        
        ttk::style map TButton \
            -background [list \
                pressed $colors(-darker) \
                active $colors(-dark) \
                !disabled $colors(-light)] \
            -lightcolor [list pressed $colors(-darker)] \
            -darkcolor [list pressed $colors(-darker)]

        # 配置工具栏按钮
        ttk::style configure Toolbutton -anchor center -padding {6 4} -relief flat
        ttk::style map Toolbutton \
            -background [list \
                selected $colors(-dark) \
                pressed $colors(-darker) \
                active $colors(-dark)]

        # 配置单选按钮和复选框
        ttk::style configure TCheckbutton -indicatorbackground $colors(-window) -indicatormargin {0 2 4 2}
        ttk::style configure TRadiobutton -indicatorbackground $colors(-window) -indicatormargin {0 2 4 2}
        
        ttk::style map TCheckbutton \
            -indicatorbackground [list \
                pressed $colors(-window) \
                alternate $colors(-darker) \
                selected $colors(-selectbg)]
        
        ttk::style map TRadiobutton \
            -indicatorbackground [list \
                pressed $colors(-window) \
                alternate $colors(-darker) \
                selected $colors(-selectbg)]

        # 配置组合框
        ttk::style configure TCombobox -padding {6 4} -arrowsize 12
        ttk::style map TCombobox \
            -fieldbackground [list readonly $colors(-lighter)] \
            -background [list \
                pressed $colors(-darker) \
                active $colors(-dark)] \
            -arrowcolor [list disabled $colors(-disabledfg)]

        # 配置滚动条
        ttk::style configure Horizontal.TScrollbar -background $colors(-bg)
        ttk::style configure Vertical.TScrollbar -background $colors(-bg)
        
        ttk::style map TScrollbar \
            -background [list \
                pressed $colors(-darker) \
                active $colors(-dark)] \
            -arrowcolor [list disabled $colors(-disabledfg)]

        # 配置进度条
        ttk::style configure Horizontal.TProgressbar \
            -background $colors(-selectbg) \
            -troughcolor $colors(-troughcolor) \
            -borderwidth 0 \
            -lightcolor $colors(-selectbg) \
            -darkcolor $colors(-selectbg)
            
        ttk::style configure Vertical.TProgressbar \
            -background $colors(-selectbg) \
            -troughcolor $colors(-troughcolor) \
            -borderwidth 0 \
            -lightcolor $colors(-selectbg) \
            -darkcolor $colors(-selectbg)

        # 配置标签框架
        ttk::style configure TLabelframe -background $colors(-bg)
        ttk::style configure TLabelframe.Label -background $colors(-bg) -foreground $colors(-fg)

        # 配置分页控件
        ttk::style configure TNotebook -background $colors(-tabbg) -tabmargins {2 2 2 0}
        ttk::style configure TNotebook.Tab \
            -padding {12 4} \
            -background $colors(-tabbg) \
            -lightcolor $colors(-tabbg) \
            -darkcolor $colors(-tabbg)
            
        ttk::style map TNotebook.Tab \
            -background [list selected $colors(-lighter)] \
            -lightcolor [list selected $colors(-lighter)] \
            -darkcolor [list selected $colors(-lighter)] \
            -expand [list selected {2 2 2 0}]

        # 配置标尺
        ttk::style configure Horizontal.TScale -troughcolor $colors(-troughcolor)
        ttk::style configure Vertical.TScale -troughcolor $colors(-troughcolor)
        
        ttk::style map TScale \
            -slidercolor [list active $colors(-dark)] \
            -sliderwidth [list active 16]

        # 配置分离器
        ttk::style configure TSeparator -background $colors(-dark)

        # 配置树视图
        ttk::style configure Treeview \
            -background $colors(-window) \
            -fieldbackground $colors(-window) \
            -foreground $colors(-fg)
            
        ttk::style map Treeview \
            -background [list selected $colors(-selectbg)] \
            -foreground [list selected $colors(-selectfg)]

        # 配置菜单
        option add *Menu.background $colors(-lighter)
        option add *Menu.foreground $colors(-fg)
        option add *Menu.activeBackground $colors(-selectbg)
        option add *Menu.activeForeground $colors(-selectfg)
        option add *Menu.disabledForeground $colors(-disabledfg)
        option add *Menu.borderWidth 1
        option add *Menu.relief flat

        # 配置滚动条箭头
        ttk::style layout Vertical.TScrollbar {
            Vertical.Scrollbar.trough -sticky ns -children {
                Vertical.Scrollbar.uparrow -side top
                Vertical.Scrollbar.downarrow -side bottom
                Vertical.Scrollbar.thumb -expand 1 -side top
            }
        }

        ttk::style layout Horizontal.TScrollbar {
            Horizontal.Scrollbar.trough -sticky ew -children {
                Horizontal.Scrollbar.leftarrow -side left
                Horizontal.Scrollbar.rightarrow -side right
                Horizontal.Scrollbar.thumb -expand 1 -side left
            }
        }
    }
}

# 初始化主题
ttk::theme::ubuntu::init
ttk::theme::ubuntu-dark::init

# 设置主题的公共过程
proc set_theme {themeName} {
    if {$themeName eq "ubuntu-light"} {
        ttk::style theme use ubuntu-light
    } elseif {$themeName eq "ubuntu-dark"} {
        ttk::style theme use ubuntu-dark
    } else {
        error "未知主题: $themeName。可用主题: ubuntu-light, ubuntu-dark"
    }
    
    # 设置非ttk小部件的颜色
    array set colors [ttk::style theme settings $themeName]
    option add *background $colors(-bg)
    option add *foreground $colors(-fg)
    option add *selectBackground $colors(-selectbg)
    option add *selectForeground $colors(-selectfg)
    option add *activeBackground $colors(-activebg)
    option add *troughColor $colors(-troughcolor)
    option add *highlightColor $colors(-focuscolor)
    option add *disabledForeground $colors(-disabledfg)
    option add *Entry.background $colors(-entrybg)
    option add *Entry.foreground $colors(-fg)
    option add *Entry.selectBackground $colors(-selectbg)
    option add *Entry.selectForeground $colors(-selectfg)
    option add *Listbox.background $colors(-window)
    option add *Listbox.foreground $colors(-fg)
    option add *Listbox.selectBackground $colors(-selectbg)
    option add *Listbox.selectForeground $colors(-selectfg)
}

# 默认使用亮色主题
set_theme ubuntu-light

package provide ttk::theme::ubuntu 1.0