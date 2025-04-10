import os
import tempfile
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import zipfile
import json
from shutil import copyfile
import io

# 替换映射表（代码: [中文名, 英文代码]）
REPLACEMENT_MAP = {
    'rus': ['苏联', 'rus'],
    'ger': ['德国', 'ger'],
    'usa': ['美国', 'usa'],
    'fin': ['芬兰', 'fin'],
    'fra': ['法国', 'fra'],
    'eng': ['英国', 'eng'],
    'jap': ['日本', 'jap'],
    'hun': ['匈牙利', 'hun'],
    'ita': ['意大利', 'ita'],
    'usu': ['乌索比亚联邦', 'usu'],
    'sax': ['萨克森帝国', 'sax'],
    'rsv': ['俄苏维埃', 'rsv'],
    'pol': ['波兰共和国', 'pol']
}

CONFIG_FILE = "config.json"


class SaveFileEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("地狱之门征服阵营修改工具")
        self.root.geometry("800x800")

        # 加载配置
        self.config = self.load_config()

        self.create_widgets()

        # 不再自动扫描，只在点击按钮时扫描
        if 'last_path' in self.config:
            self.path_var.set(self.config['last_path'])

    def load_config(self):
        """加载配置文件"""
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return {}
        return {}

    def save_config(self):
        """保存配置文件"""
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, ensure_ascii=False, indent=2)
    def create_widgets(self):
        # 主框架 - 使用PanedWindow实现可调整大小的分割
        main_pane = tk.PanedWindow(self.root, orient=tk.VERTICAL)
        main_pane.pack(fill=tk.BOTH, expand=True)

        # 上部框架 - 原有功能
        top_frame = ttk.Frame(main_pane)
        main_pane.add(top_frame)

        # 顶部控制区域
        control_frame = ttk.Frame(top_frame, padding="10")
        control_frame.pack(fill=tk.X)

        ttk.Label(control_frame, text="搜索路径:").pack(side=tk.LEFT)

        self.path_var = tk.StringVar()
        self.path_entry = ttk.Entry(control_frame, textvariable=self.path_var, width=50)
        self.path_entry.pack(side=tk.LEFT, padx=5, expand=True, fill=tk.X)

        browse_btn = ttk.Button(control_frame, text="浏览...", command=self.browse_directory)
        browse_btn.pack(side=tk.LEFT, padx=5)

        scan_btn = ttk.Button(control_frame, text="扫描存档文件", command=self.scan_directory)
        scan_btn.pack(side=tk.LEFT)

        # 文件列表区域
        list_frame = ttk.Frame(top_frame, padding="10")
        list_frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(list_frame, text="找到的存档文件:").pack(anchor=tk.W)

        self.file_listbox = tk.Listbox(list_frame, selectmode=tk.SINGLE)
        self.file_listbox.pack(fill=tk.BOTH, expand=True, pady=5)

        # 操作按钮区域
        button_frame = ttk.Frame(top_frame, padding="10")
        button_frame.pack(fill=tk.X)

        open_btn = ttk.Button(button_frame, text="修改选中的存档文件",
                              command=self.process_selected_file)
        open_btn.pack(pady=5)

        exit_btn = ttk.Button(button_frame, text="退出", command=self.on_exit)
        exit_btn.pack()

        # 下部框架 - 新增说明栏
        bottom_frame = ttk.Frame(main_pane, height=150)
        main_pane.add(bottom_frame)

        # 说明栏内容
        help_text = tk.Text(bottom_frame, wrap=tk.WORD, padx=10, pady=10)
        help_text.pack(fill=tk.BOTH, expand=True)

        # 添加说明内容
        instructions = """
        【地狱之门征服存档修改工具V0.1使用说明】
        1. 使用步骤：
           - 点击"浏览..."按钮选择存档文件目录
           - 存档文件目录一般会在
           C:\ Users\你的用户名\Documents\My Games\gates of hell\profiles\你的steam用户代码\campaign内'
           - 点击"扫描存档文件"按钮列出所有.sav文件
           - 从列表中选择要修改的存档文件
           - 在下拉菜单中选择新的军队代码
           - 点击"确认修改"后会提示错误
           - 再次点击"确认修改"修改成功
           - 点击进入征服开始缴获新国家的载具吧！
        2. 功能说明：
           - 本工具用于修改存档中的军队代码
           - 支持修改我军(army)和敌军(enemyArmy)
           - 自动保存上次使用的路径
           - 支持勇气valour和winds of iron 1920模组，请不要修改没有加载模组的存档！
        3. 注意事项：
           - 修改前建议备份存档文件
           - 确保游戏没有加载征服存档
           - 本程序由qionghaiBW调试，AI辅助制作
           - 使用本程序意味着您愿意承担本程序带来的风险，造成损失与本程序作者无关
        """
        help_text.insert(tk.END, instructions)
        help_text.configure(state='disabled')

        # 左下角署名
        self.signature = ttk.Label(bottom_frame, text="by: qionghaiBW", font=('Arial', 8))
        self.signature.place(relx=0.01, rely=0.95, anchor='sw')

    def on_exit(self):
        """退出时保存配置"""
        self.save_config()
        self.root.quit()

    def browse_directory(self):
        """让用户选择目录"""
        initial_dir = self.path_var.get() if self.path_var.get() else os.path.dirname(os.path.abspath(__file__))
        directory = filedialog.askdirectory(
            title="选择包含存档文件的目录",
            initialdir=initial_dir
        )
        if directory:
            self.path_var.set(directory)
            self.config['last_path'] = directory
            self.save_config()

    def scan_directory(self):
        """扫描指定目录下的存档文件"""
        directory = self.path_var.get()
        if not directory:
            messagebox.showwarning("警告", "请先选择或输入一个有效的目录路径")
            return

        if not os.path.isdir(directory):
            messagebox.showerror("错误", "指定的路径不是一个有效的目录！")
            return

        self.file_listbox.delete(0, tk.END)
        save_files = self.find_save_files(directory)

        if not save_files:
            messagebox.showinfo("信息", "未找到任何存档文件")
        else:
            for file in save_files:
                self.file_listbox.insert(tk.END, file)

    def find_save_files(self, directory):
        """查找指定目录下的所有.sav文件"""
        return [f for f in os.listdir(directory) if f.lower().endswith('.sav')]

    def process_selected_file(self):
        """处理用户选中的存档文件"""
        selection = self.file_listbox.curselection()
        if not selection:
            messagebox.showwarning("警告", "请先选择一个存档文件")
            return

        selected_file = self.file_listbox.get(selection[0])
        save_path = os.path.join(self.path_var.get(), selected_file)

        # 自动提取并处理status文件
        status_content, status_path_in_zip = self.extract_status_file(save_path)
        if not status_content:
            return

        # 修改status文件
        if self.modify_status_file_interactive(status_content, save_path, status_path_in_zip):
            # 询问用户是否完成
            if messagebox.askyesno("完成", "存档修改已完成！是否关闭程序？"):
                self.on_exit()

    def extract_status_file(self, save_path):
        """从存档中自动提取status文件内容"""
        try:
            # 使用zipfile模块直接读取存档文件
            with zipfile.ZipFile(save_path, 'r') as zip_ref:
                # 查找存档中的status文件
                status_path_in_zip = None
                for file_info in zip_ref.infolist():
                    if 'status' in file_info.filename.lower():
                        status_path_in_zip = file_info.filename
                        with zip_ref.open(file_info) as file:
                            # 读取原始内容，保留原始换行符
                            content = file.read().decode('utf-8')
                            # 标准化换行符为\n
                            content = content.replace('\r\n', '\n').replace('\r', '\n')
                            return content, status_path_in_zip

                # 如果没有找到status文件
                messagebox.showerror("错误", "存档中未找到status文件！")
                return None, None

        except Exception as e:
            messagebox.showerror("错误", f"读取存档文件时出错: {str(e)}")
            return None, None

    def modify_status_file_interactive(self, content, save_path, status_path_in_zip):
        """提供交互界面修改status文件内容"""
        # 创建选择对话框
        choice_window = tk.Toplevel(self.root)
        choice_window.title("选择修改项目")
        choice_window.geometry("500x350")

        # 查找可修改的目标
        targets = []
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if '{army ' in line:
                current_value = line.split('{army ')[1].split('}')[0].strip()
                targets.append(('army', current_value, i))
            if '{enemyArmy ' in line:
                current_value = line.split('{enemyArmy ')[1].split('}')[0].strip()
                targets.append(('enemyArmy', current_value, i))

        if not targets:
            messagebox.showinfo("提示", "未找到需要替换的军队代码！")
            return False

        # 创建修改界面
        ttk.Label(choice_window, text="请选择要修改的项目:", font=('Arial', 10, 'bold')).pack(pady=10)

        self.original_lines = lines  # 保存原始行列表
        self.save_path = save_path
        self.status_path_in_zip = status_path_in_zip

        # 准备下拉框选项（显示中文名，存储英文代码）
        options = [(f"{name[0]} ({code})", code) for code, name in REPLACEMENT_MAP.items()]

        for target_type, current_value, line_num in targets:
            frame = ttk.Frame(choice_window)
            frame.pack(fill=tk.X, padx=15, pady=8)

            current_chinese = REPLACEMENT_MAP.get(current_value, ["未知", ""])[0]
            label_text = f"{'我军' if target_type == 'army' else '敌军'}当前: {current_chinese} ({current_value})"
            ttk.Label(frame, text=label_text).pack(side=tk.LEFT, anchor='w')

            # 创建带中文的下拉选择框
            new_value = tk.StringVar()

            # 设置当前值为默认选项
            current_display = f"{REPLACEMENT_MAP.get(current_value, ['未知', ''])[0]} ({current_value})"
            new_value.set(current_display)

            # 创建OptionMenu
            option_menu = ttk.OptionMenu(frame, new_value, current_display, *[opt[0] for opt in options])
            option_menu.pack(side=tk.RIGHT, padx=10)

            # 保存引用
            setattr(frame, 'target_type', target_type)
            setattr(frame, 'current_value', current_value)
            setattr(frame, 'new_value', new_value)
            setattr(frame, 'options', options)
            setattr(frame, 'line_num', line_num)  # 保存行号

        # 确认按钮
        ttk.Button(choice_window, text="确认修改",
                   command=lambda: self.apply_changes(choice_window, targets)).pack(pady=15)

        choice_window.transient(self.root)
        choice_window.grab_set()
        self.root.wait_window(choice_window)

        return True

    def apply_changes(self, window, targets):
        """应用用户选择的修改"""
        # 创建原始行的副本
        modified_lines = self.original_lines.copy()

        # 收集所有修改
        for child in window.winfo_children():
            if isinstance(child, ttk.Frame):
                target_type = getattr(child, 'target_type')
                current_value = getattr(child, 'current_value')
                selected_display = getattr(child, 'new_value').get()
                options = getattr(child, 'options')
                line_num = getattr(child, 'line_num')

                # 从显示文本中解析出代码
                new_value = None
                for display, code in options:
                    if display == selected_display:
                        new_value = code
                        break

                if new_value and new_value != current_value:
                    # 直接修改特定行
                    old_line = modified_lines[line_num]
                    if target_type == 'army':
                        new_line = old_line.replace(
                            f'{{army {current_value}}}',
                            f'{{army {new_value}}}')
                    else:
                        new_line = old_line.replace(
                            f'{{enemyArmy {current_value}}}',
                            f'{{enemyArmy {new_value}}}')

                    modified_lines[line_num] = new_line
                    messagebox.showinfo("成功",
                                        f"已将{target_type}从{current_value}替换为{new_value}")

        # 保存修改后的文件
        temp_dir = tempfile.mkdtemp()
        temp_status_path = os.path.join(temp_dir, 'status')

        try:
            # 写入修改后的内容，保持原始换行符
            with open(temp_status_path, 'w', encoding='utf-8', newline='\n') as f:
                f.write('\n'.join(modified_lines))

            # 创建临时副本文件
            temp_zip_path = os.path.join(temp_dir, 'temp.sav')
            copyfile(self.save_path, temp_zip_path)

            # 更新存档文件 - 使用临时副本操作
            with zipfile.ZipFile(temp_zip_path, 'a', compression=zipfile.ZIP_DEFLATED) as zipf:
                # 先删除原有的status文件
                if self.status_path_in_zip in zipf.namelist():
                    self.remove_specific_file_from_zip(zipf, self.status_path_in_zip)
                # 添加新的status文件
                zipf.write(temp_status_path, self.status_path_in_zip)

            # 替换原文件
            os.remove(self.save_path)
            os.rename(temp_zip_path, self.save_path)

            messagebox.showinfo("完成", "存档文件已成功更新！")
            window.destroy()

        except Exception as e:
            messagebox.showerror("错误", f"保存修改时出错: {str(e)}")
        finally:
            # 清理临时文件
            if os.path.exists(temp_zip_path):
                try:
                    os.remove(temp_zip_path)
                except:
                    pass
            if os.path.exists(temp_status_path):
                try:
                    os.remove(temp_status_path)
                except:
                    pass

    def remove_specific_file_from_zip(self, zipf, file_to_remove):
        """从ZIP文件中删除指定文件（内存高效方式）"""
        # 创建临时内存文件
        temp_zip_data = io.BytesIO()

        # 创建新zip文件
        with zipfile.ZipFile(temp_zip_data, 'w', compression=zipfile.ZIP_DEFLATED) as new_zip:
            for item in zipf.infolist():
                if item.filename != file_to_remove:
                    # 复制除目标文件外的所有文件
                    new_zip.writestr(item, zipf.read(item.filename))

        # 关闭原始zip文件
        zipf.close()

        # 将内存数据写回原文件
        with open(self.save_path, 'wb') as f:
            f.write(temp_zip_data.getvalue())


if __name__ == "__main__":
    root = tk.Tk()
    app = SaveFileEditor(root)
    root.mainloop()