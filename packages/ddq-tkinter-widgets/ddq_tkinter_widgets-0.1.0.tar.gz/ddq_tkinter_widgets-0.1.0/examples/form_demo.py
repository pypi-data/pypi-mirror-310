import tkinter as tk
from tkinter import ttk

from ddq_widgets import Form, Card, SplitLayout, Table, ButtonGroup, FormItem, TextArea, Text

class FormDemo:
    def __init__(self, root):
        self.root = root
        self.root.title("Form 组件示例")
        self.root.geometry("1000x600")
        
        # 创建左右布局容器
        self.split = SplitLayout(root, left_width=200)
        
        # 创建主表单 - 不需要再次设置 pack
        self.form = Form(self.split.left)
        
        # 创建基本信息分区，保存引用
        self.basic_section = self.form.section("基本信息")
        self.basic_section.input("username", "用户名:", )
        self.basic_section.password("password", "密码:", )
        self.basic_section.select("type", "类型:", options=["选项1", "选项2", "选项3"], )
        
        # 创建其他信息分区，保存引用
        self.other_section = self.form.section("其他信息")
        self.other_section.radio("gender", "性别:", options=["男", "女"], )
        self.other_section.checkbox("hobby", "爱好:", options=["阅读", "音乐", "运动"], )
        self.other_section.textarea("desc", "描述:" )
        
        # 右侧不需要额外的容器，直接使用 split.right
        # 创建按钮组
        self.button_group = ButtonGroup(
            self.split.right,  # 直接使用 split.right
            direction="horizontal",
            align="left"
        )
        
        # 添加按钮
        self.button_group.add_new("全部禁用", command=self._handle_disable_all)
        self.button_group.add_new("全部启用", command=self._handle_enable_all)
        self.button_group.add_new("全部只读", command=self._handle_readonly_all)
        self.button_group.add_new("重置", command=self._handle_reset)
        
        # 创建数据显示卡片
        self.data_card = Card(
            self.split.right, 
            title="实时数据",
            expand=True,
            fill=tk.BOTH
        )

        # 使用 Text 组件替代 Label
        self.data_text = Text(
            self.data_card.content,
            wraplength=400,
            justify=tk.LEFT
        )
        self.data_text.pack(fill=tk.X, padx=5, pady=5, anchor='nw')
        
        # 测试显示 - 修改这一行
        self.data_text.set_text("测试内容 123")  # 使用 set_text 方法
        
        # 创建表格
        columns = [
            {'id': 'username', 'text': '用户名'},
            {'id': 'type', 'text': '类型'},
            {'id': 'gender', 'text': '性别'},
            {'id': 'hobby', 'text': '爱好'},
            {'id': 'desc', 'text': '描述'}
        ]
        
        buttons = [
            {'text': '刷新', 'command': self._refresh_table}
        ]
        
        self.table = Table(
            self.split.right,  # 直接使用 split.right
            title="查询结果",
            columns=columns,
            buttons=buttons,
        )
        
        # 先设置回调
        self._setup_callbacks()
        print("Callback setup done")  # 调试日志
        
        # 再设置默认值
        self.form.set_defaults({
            "username": "admin",
            "password": "",
            "type": "选项1",
            "gender": "男",
            "hobby": [True, False, False],
            "desc": "这是默认描述"
        })
        print("Defaults set")  # 调试日志
        
        # 最后标记初始化完成，并手动触发回调
        self.form._initializing = False
        print("Before notify change")  # 调试日志
        self.form._notify_change()
        print("After notify change")  # 调试日志

    def _handle_disable_all(self):
        """处理全部禁用按钮点击"""
        # 遍历所有分区和表单项
        for section in ["basic_section", "other_section"]:
            section_form = getattr(self, section)
            for item in section_form._items.values():
                if isinstance(item.widget, (ttk.Entry, ttk.Combobox)):
                    item.widget.configure(state='disabled')
                elif isinstance(item.widget, tk.Text):
                    item.widget.configure(state='disabled')
                elif isinstance(item.widget, ttk.Frame):
                    for child in item.widget.winfo_children():
                        if isinstance(child, (ttk.Radiobutton, ttk.Checkbutton)):
                            child.configure(state='disabled')

    def _handle_enable_all(self):
        """处理全部启用按钮点击"""
        # 遍历所有分区和表单项
        for section in ["basic_section", "other_section"]:
            section_form = getattr(self, section)
            for item in section_form._items.values():
                if isinstance(item.widget, (ttk.Entry, ttk.Combobox, tk.Text)):
                    item.widget.configure(state='normal')
                elif isinstance(item.widget, ttk.Frame):
                    for child in item.widget.winfo_children():
                        if isinstance(child, (ttk.Radiobutton, ttk.Checkbutton)):
                            child.configure(state='normal')

    def _handle_readonly_all(self):
        """处理全部只读按钮点击"""
        # 遍历所有分区和表单项
        for section in ["basic_section", "other_section"]:
            section_form = getattr(self, section)
            for item in section_form._items.values():
                if isinstance(item.widget, ttk.Entry):
                    item.widget.configure(state='readonly')
                elif isinstance(item.widget, ttk.Combobox):
                    item.widget.configure(state='readonly')
                elif isinstance(item.widget, tk.Text):
                    item.widget.configure(state='disabled')
                elif isinstance(item.widget, ttk.Frame):
                    for child in item.widget.winfo_children():
                        if isinstance(child, (ttk.Radiobutton, ttk.Checkbutton)):
                            child.configure(state='disabled')

    def _handle_reset(self):
        """处理重置按钮点击"""
        # 使用 reset 方法而不是 set_values
        self.form.reset()

    def _setup_callbacks(self):
        """设置所有回调"""
        def handle_change(values):
            print("handle_change called with values:", values)  # 调试日志
            # 更新文本显示
            formatted_text = []
            # 按固定顺序显示字
            fields = ["username", "password", "type", "gender", "hobby", "desc"]
            field_names = {
                "username": "用户名",
                "password": "密码",
                "type": "类型",
                "gender": "性别",
                "hobby": "爱好",
                "desc": "描述"
            }
            
            for key in fields:
                if key in values:
                    value = values[key]
                    formatted_value = value
                    if isinstance(value, list):
                        if key == "hobby":
                            selected = [opt for opt, sel in zip(["阅读", "音乐", "运动"], value) if sel]
                            formatted_value = ", ".join(selected) if selected else "无"
                        else:
                            formatted_value = ", ".join(str(v) for v in value)
                    elif value == "":
                        formatted_value = "无"
                    formatted_text.append(f"{field_names[key]}: {formatted_value}")
            
            # 使用 set_text 方法更新文本
            self.data_text.set_text("\n".join(formatted_text))
            
            # 自动刷新表格
            self._refresh_table()
            
        # 设置表单变化回调
        self.form.on_change(handle_change)
        
    def _refresh_table(self):
        """刷新表格数据"""
        # 获取表单数据
        values = self.form.get_values()
        
        # 处理爱好选项
        hobby_value = values.get('hobby', [])
        hobby_text = ", ".join(opt for opt, sel in zip(["阅读", "音乐", "运动"], hobby_value) if sel) or "无"
        
        # 清空表格
        self.table.clear_records()
        
        # 添加新记录
        self.table.insert_record([
            values.get('username', ''),
            values.get('type', ''),
            values.get('gender', ''),
            hobby_text,  # 使用正确处理后的爱好文本
            values.get('desc', '')
        ])

def main():
    root = tk.Tk()
    app = FormDemo(root)
    root.mainloop()

if __name__ == "__main__":
    main() 