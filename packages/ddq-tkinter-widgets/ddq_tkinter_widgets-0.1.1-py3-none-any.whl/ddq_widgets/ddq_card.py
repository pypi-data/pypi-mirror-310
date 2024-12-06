import tkinter as tk
from tkinter import ttk

class Card(ttk.LabelFrame):
    """卡片容器组件
    
    特性：
    1. 默认只填充水平方向
    2. 内置内容区域
    3. 统一的内边距
    4. 可选的标题
    """
    
    def __init__(
        self,
        master,
        title: str = "",
        padding: int = 5,
        expand: bool = False,  # 默认改为 False
        fill: str = tk.X,     # 新增 fill 参数，默认只填充水平方向
        **kwargs
    ):
        super().__init__(master, text=title, **kwargs)
        
        # 自动布局
        self.pack(fill=fill, expand=expand, padx=padding, pady=padding)
        
        # 创建内容区域，内容区域的填充方式跟随外层设置
        self.content = ttk.Frame(self)
        self.content.pack(fill=fill, expand=expand, padx=padding, pady=padding)
