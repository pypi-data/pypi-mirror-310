import tkinter as tk
from tkinter import ttk
from typing import Optional, Union, Literal, Any, List

class FormItem(ttk.Frame):
    """表单项组件,处理标签和输入控件的布局和对齐"""
    
    def __init__(
        self,
        master,
        label: str,
        widget: Optional[tk.Widget] = None,
        label_width: int = 0,
        label_anchor: Literal["w", "e"] = "e",
        **kwargs
    ):
        super().__init__(master, **kwargs)
        
        # 设置自身布局
        self.pack(fill=tk.BOTH, expand=True)
        
        # 创建标签
        self.label = ttk.Label(
            self,
            text=label,
            anchor=label_anchor,
            width=label_width if label_width > 0 else 8
        )
        self.label.pack(side="left", padx=(0, 4))
        
        # 设置输入控件
        if widget is None:
            self.widget = None
            return
            
        if isinstance(widget, (ttk.Entry, ttk.Combobox, tk.Text)):
            self.widget = type(widget)(self)
            widget_config = widget.configure()
            for key in widget_config:
                try:
                    self.widget[key] = widget[key]
                except:
                    pass
        else:
            self.widget = widget
            self.widget.master = self
            
            if hasattr(widget, 'var'):
                self.var = widget.var
            if hasattr(widget, 'vars'):
                self.vars = widget.vars
            
        if self.widget:
            self.widget.pack(side="left", fill=tk.BOTH, expand=True)

    # 工厂方法 - 创建不同类型的表单项
    @classmethod
    def input(cls, master, label: str, label_width: int = 0, **kwargs) -> 'FormItem':
        """创建文本输入框"""
        entry = ttk.Entry(None)
        return cls(master, label, widget=entry, label_width=label_width, **kwargs)
        
    @classmethod
    def password(cls, master, label: str, **kwargs) -> 'FormItem':
        """创建密码输入框"""
        entry = ttk.Entry(None, show="*")
        return cls(master, label, widget=entry, **kwargs)
        
    @classmethod
    def select(cls, master, label: str, options: List[str], editable: bool = False, **kwargs) -> 'FormItem':
        """创建下拉选择框"""
        combo = ttk.Combobox(None, values=options, state='normal' if editable else 'readonly')
        return cls(master, label, widget=combo, **kwargs)
        
    @classmethod
    def textarea(cls, master, label: str, height: int = 4, **kwargs) -> 'FormItem':
        """创建多行文本框"""
        text = tk.Text(None, height=height)
        return cls(master, label, widget=text, **kwargs)
        
    @classmethod
    def radio(cls, master, label: str, options: List[str], default: str = None, **kwargs) -> 'FormItem':
        """创建单选框组"""
        # 先创建 FormItem 实例
        item = cls(master, label, **kwargs)
        
        # 在 FormItem 中创建 Frame
        frame = ttk.Frame(item)
        var = tk.StringVar(value=default or options[0] if options else "")
        
        # 创建单选按钮
        for i, option in enumerate(options):
            radio = ttk.Radiobutton(
                frame,
                text=option,
                variable=var,
                value=option
            )
            radio.pack(side=tk.LEFT, padx=(0 if i == 0 else 5))
        
        # 将变量和frame绑定到item
        item.var = var
        item.widget = frame
        frame.pack(side="left", fill="x", expand=True)
        
        return item
        
    @classmethod
    def checkbox(cls, master, label: str, options: List[str], defaults: List[bool] = None, **kwargs) -> 'FormItem':
        """创建复选框组"""
        # 先创建 FormItem 实例
        item = cls(master, label, **kwargs)
        
        # 在 FormItem 中创建 Frame
        frame = ttk.Frame(item)
        vars = []
        
        if defaults is None:
            defaults = [False] * len(options)
        
        # 创建复选框
        for i, (option, default) in enumerate(zip(options, defaults)):
            var = tk.BooleanVar(value=default)
            vars.append(var)
            checkbox = ttk.Checkbutton(
                frame,
                text=option,
                variable=var
            )
            checkbox.pack(side=tk.LEFT, padx=(0 if i == 0 else 5))
        
        # 将变量列表和frame绑定到item
        item.vars = vars
        item.widget = frame
        frame.pack(side="left", fill="x", expand=True)
        
        return item
        
    @classmethod
    def text(cls, master, label: str, **kwargs) -> 'FormItem':
        """创建纯文本展示项"""
        from .ddq_text import Text  # 按需导入
        text = Text(None, **kwargs)
        return cls(master, label, widget=text, **kwargs)

    # 值管理相关方法保持不变
    @property
    def value(self) -> Any:
        """获取输入控件的值"""
        if hasattr(self, 'var'):
            return self.var.get()
        if hasattr(self, 'vars'):
            return [var.get() for var in self.vars]
        if isinstance(self.widget, (ttk.Entry, tk.Entry)):
            return self.widget.get()
        elif isinstance(self.widget, (ttk.Combobox, ttk.Spinbox)):
            return self.widget.get()
        elif isinstance(self.widget, tk.Text):
            return self.widget.get("1.0", "end-1c")
        return ""
        
    @value.setter
    def value(self, val: Any):
        """设置输入控件的值"""
        if hasattr(self, 'var'):
            self.var.set(val)
            return
        if hasattr(self, 'vars'):
            if isinstance(val, (list, tuple)) and len(val) == len(self.vars):
                for var, v in zip(self.vars, val):
                    var.set(v)
            return
        if isinstance(self.widget, (ttk.Entry, tk.Entry, ttk.Combobox, ttk.Spinbox)):
            self.widget.delete(0, "end")
            self.widget.insert(0, str(val))
        elif isinstance(self.widget, tk.Text):
            self.widget.delete("1.0", "end")
            self.widget.insert("1.0", str(val))
        
    def set_label_width(self, width: int):
        """设置标签宽度"""
        self.label.configure(width=width)
        
    def set_label_anchor(self, anchor: Literal["w", "e"]):
        """设置标签对齐方式"""
        self.label.configure(anchor=anchor) 