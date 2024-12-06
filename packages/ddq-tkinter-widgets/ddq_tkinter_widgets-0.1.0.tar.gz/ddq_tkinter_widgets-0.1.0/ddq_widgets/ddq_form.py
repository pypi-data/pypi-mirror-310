import tkinter as tk
from tkinter import ttk
from typing import Optional, Any, Dict, List, Union

# 使用相对导入
from .ddq_card import Card
from .ddq_form_item import FormItem

class Form(ttk.Frame):
    """表单容器组件，自动处理表单项的布局和样式"""
    
    def __init__(
        self,
        master,
        title: str = "",
        label_width: int = 6,
        spacing: int = 8,
        columns: int = 1,  # 添加列数参数
        use_card: bool = False,  # 添加是否使用卡片样式的选项
        **kwargs
    ):
        super().__init__(master, **kwargs)
        
        # 移除 expand=True，只保留水平方向的填充
        self.pack(fill=tk.X, padx=5, pady=2)
        
        # 如果需要卡片样式，创建 Card 作为容器
        if use_card:
            self.container = Card(self, title=title)
            self.container.pack(fill=tk.X)  # 这里也改为只填充水平方向
            parent = self.container.content
        else:
            parent = self
            
        # 创建网格布局容器
        self.grid_frame = ttk.Frame(parent)
        self.grid_frame.pack(fill=tk.X)  # 这里也改为只填充水平方向
        
        self.label_width = label_width
        self._items: Dict[str, FormItem] = {}
        self._change_callback = None
        self._current_row = 0
        self._current_col = 0
        self.columns = columns
        
        # 设置列权重
        for i in range(columns):
            self.grid_frame.columnconfigure(i, weight=1)
            
        self._default_values: Dict[str, Any] = {}
        self._initializing = True
        
        # 绑定点击事件，用于失去焦点
        self.bind('<Button-1>', self._handle_click)
        self.grid_frame.bind('<Button-1>', self._handle_click)
        
        # 如果使用了卡片样式，也需要绑定卡片的点击事件
        if use_card:
            self.container.bind('<Button-1>', self._handle_click)
            self.container.content.bind('<Button-1>', self._handle_click)
        
    def _handle_click(self, event):
        """处理点击事件，使当前焦点的输入框失去焦点"""
        # 获取当前焦点控件
        focused = self.focus_get()
        if focused:
            # 如果当前有焦点控件，且点击的不是这个控件
            if event.widget != focused:
                # 将焦点转移到表单容器上
                self.focus_set()
        
    def on_change(self, callback):
        """设置表单化回调"""
        self._change_callback = callback
        
        # 如果是在初始化完成后设置回调，立即触发一次通知
        if not self._initializing:
            self._notify_change()
        return self
        
    def _notify_change(self):
        """通知表单变化"""
        if self._change_callback:
            values = self.get_values()
            self._change_callback(values)
            
    def _create_change_callback(self, name: str):
        """创建变化回调"""
        def callback(*args):
            self._notify_change()
        return callback
        
    def _add_item(self, name: str, item: FormItem):
        """添加表单项到网格"""
        item.pack(fill=tk.X, padx=5, pady=5)
        self._items[name] = item
        
    def set_columns(self, columns: int):
        """动态设置列数"""
        if columns < 1:
            return
            
        self.columns = columns
        
        # 重新配置列权重
        for i in range(columns):
            self.grid_frame.columnconfigure(i, weight=1)
            
        # 重新布局所有项
        self._current_row = 0
        self._current_col = 0
        
        for item in self._items.values():
            item.grid_forget()
            
        for name, item in self._items.items():
            self._add_item(name, item)
            
    def section(self, title: str = "", columns: int = 1) -> 'Form':
        """创建表单分区"""
        # 创建子表单
        sub_form = Form(
            self.grid_frame,
            title=title,
            columns=columns,
            use_card=True,
            label_width=self.label_width
        )
        sub_form.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # 设置变更通知
        sub_form.on_change(lambda values: self._notify_change())
        
        # 添加到父表单
        self._items[f"section_{len(self._items)}"] = sub_form
        return sub_form
        
    def group(self, title: str = "", columns: int = 1) -> 'Form':
        """创建表单分组（section的别名，保持向后兼容）"""
        return self.section(title, columns)
        
    def input(self, name: str, label: str, **kwargs) -> FormItem:
        """添加文本输入框"""
        item = FormItem.input(self.grid_frame, label, **kwargs)
        self._add_item(name, item)
        item.widget.bind('<KeyRelease>', self._create_change_callback(name))
        return item
        
    def password(self, name: str, label: str, **kwargs) -> FormItem:
        """添加密码输入框"""
        item = FormItem.password(self.grid_frame, label, **kwargs)
        self._add_item(name, item)
        item.widget.bind('<KeyRelease>', self._create_change_callback(name))
        return item
        
    def select(self, name: str, label: str, options: List[str], **kwargs) -> FormItem:
        """添加下拉选择框"""
        item = FormItem.select(self.grid_frame, label, options, **kwargs)
        self._add_item(name, item)
        item.widget.bind('<<ComboboxSelected>>', self._create_change_callback(name))
        if kwargs.get('editable', False):
            item.widget.bind('<KeyRelease>', self._create_change_callback(name))
        return item
        
    def textarea(self, name: str, label: str, **kwargs) -> FormItem:
        """添加多行文本框"""
        item = FormItem.textarea(self.grid_frame, label, **kwargs)
        self._add_item(name, item)
        item.widget.bind('<KeyRelease>', self._create_change_callback(name))
        return item
        
    def radio(self, name: str, label: str, options: List[str], **kwargs) -> FormItem:
        """添加单选框组"""
        item = FormItem.radio(self.grid_frame, label, options, **kwargs)
        self._add_item(name, item)
        item.var.trace_add('write', self._create_change_callback(name))
        return item
        
    def checkbox(self, name: str, label: str, options: List[str], **kwargs) -> FormItem:
        """添加复选框组"""
        item = FormItem.checkbox(self.grid_frame, label, options, **kwargs)
        self._add_item(name, item)
        for var in item.vars:
            var.trace_add('write', self._create_change_callback(name))
        return item
        
    def get_values(self) -> Dict[str, Any]:
        """获取所有表单项的值，包括分区中的表单项"""
        values = {}
        
        # 遍历所有表单项
        for name, item in self._items.items():
            if isinstance(item, Form):  # 改为检查是否是 Form 实例
                # 如果是分区，获取分区中的所有值
                section_values = item.get_values()
                # 合并分区的值到主表单的值中
                values.update(section_values)
            else:
                # 普通单项，直接获取值
                if hasattr(item, 'var'):  # Radio
                    values[name] = item.var.get()
                elif hasattr(item, 'vars'):  # Checkbox
                    values[name] = [var.get() for var in item.vars]
                else:
                    values[name] = item.value
        
        return values
        
    def set_values(self, values: Dict[str, Any]):
        """设置表单项的值"""
        for name, value in values.items():
            if name in self._items:
                item = self._items[name]
                if hasattr(item, 'var'):  # Radio
                    item.var.set(value)
                elif hasattr(item, 'vars'):  # Checkbox
                    if isinstance(value, (list, tuple)) and len(value) == len(item.vars):
                        for var, val in zip(item.vars, value):
                            var.set(val)
                elif isinstance(item.widget, ttk.Combobox):
                    item.widget.set(value)
                else:
                    item.value = value
                    
    def set_disabled(self, names: List[str] = None):
        """设置表单项禁用状态"""
        if names is None:
            # 禁用所有表单项
            for item in self._items.values():
                self._set_item_disabled(item)
        else:
            # 禁用指定的表单项
            for name in names:
                if name in self._items:
                    self._set_item_disabled(self._items[name])
                    
    def _set_item_disabled(self, item: FormItem):
        """设置单个表单项禁用"""
        if isinstance(item.widget, (ttk.Entry, ttk.Combobox)):
            item.widget.configure(state='disabled')
        elif isinstance(item.widget, tk.Text):
            item.widget.configure(state='disabled')
        elif isinstance(item.widget, ttk.Frame):
            for child in item.widget.winfo_children():
                if isinstance(child, (ttk.Radiobutton, ttk.Checkbutton)):
                    child.configure(state='disabled')
                    
    def set_enabled(self, names: List[str] = None):
        """设置表单项启用状态"""
        if names is None:
            # 启用所有表单项
            for item in self._items.values():
                self._set_item_enabled(item)
        else:
            # 启用指定的表单项
            for name in names:
                if name in self._items:
                    self._set_item_enabled(self._items[name])
                    
    def _set_item_enabled(self, item: FormItem):
        """设置单个表单项启用"""
        if isinstance(item.widget, (ttk.Entry, ttk.Combobox, tk.Text)):  # 包含 Text 控件
            item.widget.configure(state='normal')
        elif isinstance(item.widget, ttk.Frame):  # Radio 或 Checkbox
            for child in item.widget.winfo_children():
                if isinstance(child, (ttk.Radiobutton, ttk.Checkbutton)):
                    child.configure(state='normal')
                    
    def set_readonly(self, names: List[str] = None):
        """设置表单项只读状态"""
        if names is None:
            # 设置所有表单项只读，包括分区中的
            for item in self._items.values():
                if isinstance(item, Form):  # 改为 Form
                    item.set_readonly()  # 设置分区中的所有表单项只读
                else:
                    self._set_item_readonly(item)
        else:
            # 设置指定的表单项只读
            for name in names:
                for item in self._items.values():
                    if isinstance(item, Form):  # 改为 Form
                        if name in item._items:
                            item._set_item_readonly(item._items[name])
                    elif name in self._items:
                        self._set_item_readonly(self._items[name])
                        
    def _set_item_readonly(self, item: FormItem):
        """设置单个表单项只读"""
        if isinstance(item.widget, ttk.Entry):
            item.widget.configure(state='readonly')
            item._readonly = True
        elif isinstance(item.widget, ttk.Combobox):
            item.widget.configure(state='readonly')
            item._readonly = True
        elif isinstance(item.widget, tk.Text):
            item.widget.configure(state='disabled')
            item._readonly = True
        elif isinstance(item.widget, ttk.Frame):  # Radio 或 Checkbox
            for child in item.widget.winfo_children():
                if isinstance(child, (ttk.Radiobutton, ttk.Checkbutton)):
                    child.configure(state='disabled')
            item._readonly = True
            
    def is_disabled(self, name: str) -> bool:
        """检查表单项是否禁用"""
        if name not in self._items:
            return False
            
        item = self._items[name]
        if isinstance(item.widget, (ttk.Entry, ttk.Combobox)):
            return str(item.widget.cget('state')) == 'disabled'
        elif isinstance(item.widget, tk.Text):  # 特别处理 Text 控件
            return str(item.widget.cget('state')) == 'disabled'
        elif isinstance(item.widget, ttk.Frame):
            children = item.widget.winfo_children()
            return all(str(child.cget('state')) == 'disabled' 
                      for child in children 
                      if isinstance(child, (ttk.Radiobutton, ttk.Checkbutton)))
        return False
        
    def is_readonly(self, name: str) -> bool:
        """检查表单项是否只读"""
        if name not in self._items:
            return False
            
        item = self._items[name]
        return hasattr(item, '_readonly') and item._readonly
        
    def set_defaults(self, values: Dict[str, Any]):
        """设置表单默认值"""
        self._default_values = values.copy()  # 保存默认值的副本
        
        # 遍历所有分区和表单项
        for name, item in self._items.items():
            if isinstance(item, Form):  # 如果是分区
                # 过滤出属于这个分区的默认值
                section_values = {k: v for k, v in values.items() 
                                if k in item._items}
                item.set_defaults(section_values)  # 递归设置分区的默认值
        
        self.set_values(values)  # 设置当前值
        
        # 如果不是在初始化阶段，才触发变更通知
        if not self._initializing:
            self._notify_change()
        return self
        
    def reset(self, names: List[str] = None):
        """重置表单项到默认值"""
        if names is None:
            # 重置所有表单项，包括分区中的
            for name, item in self._items.items():
                if isinstance(item, Form):  # 如果是分区
                    item.reset()  # 递归重置分区
                elif name in self._default_values:
                    if hasattr(item, 'var'):  # Radio
                        item.var.set(self._default_values[name])
                    elif hasattr(item, 'vars'):  # Checkbox
                        value = self._default_values[name]
                        if isinstance(value, (list, tuple)) and len(value) == len(item.vars):
                            for var, val in zip(item.vars, value):
                                var.set(val)
                    elif isinstance(item.widget, ttk.Combobox):
                        item.widget.set(self._default_values[name])
                    else:
                        item.value = self._default_values[name]
        else:
            # 重置指定的表单项
            for name in names:
                if name in self._default_values:
                    for item_name, item in self._items.items():
                        if isinstance(item, Form):  # 如果是分区
                            if name in item._items:
                                item.reset([name])  # 递归重置指定的表单项
                        elif item_name == name:
                            if hasattr(item, 'var'):  # Radio
                                item.var.set(self._default_values[name])
                            elif hasattr(item, 'vars'):  # Checkbox
                                value = self._default_values[name]
                                if isinstance(value, (list, tuple)) and len(value) == len(item.vars):
                                    for var, val in zip(item.vars, value):
                                        var.set(val)
                            elif isinstance(item.widget, ttk.Combobox):
                                item.widget.set(self._default_values[name])
                            else:
                                item.value = self._default_values[name]
        
        # 触发变更通知
        self._notify_change()
        
    def is_modified(self, name: str = None) -> Union[bool, Dict[str, bool]]:
        """检查表单项是否被修改"""
        current_values = self.get_values()
        
        if name is not None:
            # 检指定单
            if name not in self._default_values:
                return False
            return current_values[name] != self._default_values[name]
            
        # 检查所有表单项
        modified = {}
        for name, value in current_values.items():
            if name in self._default_values:
                modified[name] = value != self._default_values[name]
                
        return modified