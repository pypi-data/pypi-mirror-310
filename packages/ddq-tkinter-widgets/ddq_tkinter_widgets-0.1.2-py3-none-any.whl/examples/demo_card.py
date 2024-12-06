import tkinter as tk
from tkinter import ttk

from ddq_widgets import Card, Form

class CardDemo:
    def __init__(self, root):
        self.root = root
        self.root.title("Card 组件示例")
        self.root.geometry("600x400")
        
        # 创建一个简单的卡片
        simple_card = Card(root, title="简单卡片")
        # ttk.Label(simple_card.content, text="这是一个简单的卡片示例").pack(pady=10)
        
        # 创建一个带表单的卡片
        form_card = Card(root, title="带表单的卡片")
        form = Form(form_card.content)
        
        # 添加表单项
        form.input("name", "姓名:")
        form.select("type", "类型:", options=["选项1", "选项2", "选项3"])
        form.radio("gender", "性别:", options=["男", "女"])
        form.checkbox("hobby", "爱好:", options=["阅读", "音乐", "运动"])
        
        # 设置表单变化回调
        def on_form_change(values):
            print("表单值变化:", values)
            
        form.on_change(on_form_change)

def main():
    root = tk.Tk()
    app = CardDemo(root)
    root.mainloop()

if __name__ == "__main__":
    main() 