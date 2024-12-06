import tkinter as tk
from tkinter import ttk

class SplitLayout(ttk.Frame):
    """左右布局组件"""
    
    def __init__(
        self,
        master,
        left_width: int = None,   
        right_width: int = None,  
        spacing: int = 10,        
        **kwargs
    ):
        super().__init__(master, **kwargs)
        
        self.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 添加一个权重配置
        self.grid_columnconfigure(0, weight=1)  # 左侧面板列
        self.grid_columnconfigure(1, weight=1)  # 右侧面板列
        
        # 创建左右面板容器，使用grid布局
        left_container = self._create_container(
            fixed_width=left_width,
            padding=(0, spacing//2)
        )
        left_container.grid(row=0, column=0, sticky='nsew')
        
        right_container = self._create_container(
            fixed_width=right_width,
            padding=(spacing//2, 0)
        )
        right_container.grid(row=0, column=1, sticky='nsew')
        
        # 创建实际的左右面板
        self.left = ttk.Frame(left_container)
        self.left.pack(fill=tk.BOTH, expand=True)
        
        self.right = ttk.Frame(right_container)
        self.right.pack(fill=tk.BOTH, expand=True)
        
    def _create_container(self, fixed_width: int = None, padding: tuple = (0, 0)) -> ttk.Frame:
        """创建容器并设置布局"""
        container = ttk.Frame(self)
        
        if fixed_width:
            container.configure(width=fixed_width)
            container.pack_propagate(0)
            
        return container