import os
import zipfile
import tkinter as tk
from tkinter import filedialog, messagebox, ttk


class SaveGameEditor:

    def __init__(self, root):
        self.root = root
        self.root.title("地狱之门征服存档修改工具V0.2 by.qionghaiBW")
        self.root.geometry("1000x800")

        # 初始化变量
        self.current_file = ""
        self.status_content = []
        self.modified_values = {}
        # 新增备份选项变量
        self.backup_var = tk.BooleanVar(value=False)  # 默认开启备份

        # 初始化选项字典
        self.army_options = {
            "rus": "苏联",
            "ger": "德国",
            "usa": "美国",
            "fin": "芬兰",
            "fra": "法国",
            "eng": "英国",
            "jap": "日本",
            "hun": "匈牙利",
            "ita": "意大利",
            "usu": "乌索比亚联邦",
            "sax": "萨克森帝国",
            "rsv": "俄苏维埃",
            "pol": "波兰共和国"
        }

        self.difficulty_options = {
            "easy": "新手",
            "normal": "普通",
            "hard": "困难",
            "heroic": "英雄"
        }

        self.fog_options = {
            "fog_off": "关闭",
            "fog_realistic": "打开"
        }

        self.region_options = {
            "ostfront": "东线战区",
            "west": "西线战区",
            "talvisota": "芬兰战区"
        }

        # 配置网格权重
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)

        # 创建四个主要框架
        self.create_path_frame()
        self.create_info_frame()
        self.create_edit_frame()
        self.create_help_frame()
        # 修改创建编辑框架方法
        self.create_edit_frame()
        # 添加路径记忆文件
        self.memory_file = "path_memory.txt"
        # 初始化时加载记忆的路径
        self.load_remembered_path()

    def create_path_frame(self):
        """创建路径查找框架"""
        self.path_frame = ttk.LabelFrame(self.root, text="路径查找", padding=10)
        self.path_frame.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        self.path_frame.grid_rowconfigure(1, weight=1)
        self.path_frame.grid_columnconfigure(0, weight=1)

        # 路径输入框
        self.path_label = ttk.Label(self.path_frame, text="存档路径:")
        self.path_label.grid(row=0, column=0, sticky="w")

        self.path_entry = ttk.Entry(self.path_frame)
        self.path_entry.grid(row=1, column=0, sticky="ew", pady=5)

        # 浏览按钮
        self.browse_button = ttk.Button(
            self.path_frame,
            text="浏览",
            command=self.browse_files
        )
        self.browse_button.grid(row=1, column=1, padx=5)

        # 文件列表
        self.file_list_label = ttk.Label(self.path_frame, text="找到的存档文件:")
        self.file_list_label.grid(row=2, column=0, sticky="w", pady=(10, 0))

        self.file_listbox = tk.Listbox(self.path_frame)
        self.file_listbox.grid(row=3, column=0, columnspan=2, sticky="nsew", pady=5)
        self.file_listbox.bind("<<ListboxSelect>>", self.load_save_file)

        # 记忆路径按钮
        self.remember_button = ttk.Button(
            self.path_frame,
            text="记忆路径",
            command=self.remember_path
        )
        self.remember_button.grid(row=4, column=0, pady=5, sticky="w")

        # 添加清除记忆按钮
        self.clear_button = ttk.Button(
            self.path_frame,
            text="清除记忆",
            command=self.clear_memory
        )
        self.clear_button.grid(row=4, column=1, pady=5, sticky="e")

    def create_info_frame(self):
        """创建存档信息显示框架"""
        self.info_frame = ttk.LabelFrame(self.root, text="存档信息", padding=10)
        self.info_frame.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")
        self.info_frame.grid_rowconfigure(0, weight=1)
        self.info_frame.grid_columnconfigure(0, weight=1)

        # 信息显示文本框
        self.info_text = tk.Text(self.info_frame, wrap=tk.WORD)
        self.info_text.grid(row=0, column=0, sticky="nsew")

        # 添加滚动条
        scrollbar = ttk.Scrollbar(self.info_frame, command=self.info_text.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.info_text.config(yscrollcommand=scrollbar.set)

    def create_edit_frame(self):
        """创建存档修改框架（含同步显示和备份选项）"""
        self.edit_frame = ttk.LabelFrame(self.root, text="修改存档", padding=10)
        self.edit_frame.grid(row=1, column=1, padx=5, pady=5, sticky="nsew")

        # 配置网格布局
        for i in range(12):  # 增加行数容纳新控件
            self.edit_frame.grid_rowconfigure(i, weight=1)
        self.edit_frame.grid_columnconfigure(1, weight=1)

        # 当前值显示标签（新增）
        ttk.Label(self.edit_frame, text="当前值", font=('Arial', 9, 'bold')).grid(row=0, column=1, sticky="w")
        ttk.Label(self.edit_frame, text="新值", font=('Arial', 9, 'bold')).grid(row=0, column=2, sticky="w")

        # 存档版本
        ttk.Label(self.edit_frame, text="存档版本:").grid(row=1, column=0, sticky="e", pady=2)
        self.current_version = ttk.Label(self.edit_frame, text="", foreground="blue")
        self.current_version.grid(row=1, column=1, sticky="w")
        self.game_version_entry = ttk.Entry(self.edit_frame)
        self.game_version_entry.grid(row=1, column=2, sticky="ew", pady=2)

        # 人力点数
        ttk.Label(self.edit_frame, text="人力点数:").grid(row=2, column=0, sticky="e", pady=2)
        self.current_mp = ttk.Label(self.edit_frame, text="", foreground="blue")
        self.current_mp.grid(row=2, column=1, sticky="w")
        self.mp_entry = ttk.Entry(self.edit_frame)
        self.mp_entry.grid(row=2, column=2, sticky="ew", pady=2)

        # 支援点数
        ttk.Label(self.edit_frame, text="支援点数:").grid(row=3, column=0, sticky="e", pady=2)
        self.current_sp = ttk.Label(self.edit_frame, text="", foreground="blue")
        self.current_sp.grid(row=3, column=1, sticky="w")
        self.sp_entry = ttk.Entry(self.edit_frame)
        self.sp_entry.grid(row=3, column=2, sticky="ew", pady=2)

        # 补给点数
        ttk.Label(self.edit_frame, text="补给点数:").grid(row=4, column=0, sticky="e", pady=2)
        self.current_ap = ttk.Label(self.edit_frame, text="", foreground="blue")
        self.current_ap.grid(row=4, column=1, sticky="w")
        self.ap_entry = ttk.Entry(self.edit_frame)
        self.ap_entry.grid(row=4, column=2, sticky="ew", pady=2)

        # 研究点数
        ttk.Label(self.edit_frame, text="研究点数:").grid(row=5, column=0, sticky="e", pady=2)
        self.current_rp = ttk.Label(self.edit_frame, text="", foreground="blue")
        self.current_rp.grid(row=5, column=1, sticky="w")
        self.rp_entry = ttk.Entry(self.edit_frame)
        self.rp_entry.grid(row=5, column=2, sticky="ew", pady=2)

        # 我军军队代码
        ttk.Label(self.edit_frame, text="我军军队:").grid(row=6, column=0, sticky="e", pady=2)
        self.current_army = ttk.Label(self.edit_frame, text="", foreground="blue")
        self.current_army.grid(row=6, column=1, sticky="w")
        self.army_combobox = ttk.Combobox(self.edit_frame, state="readonly")
        self.army_combobox.grid(row=6, column=2, sticky="ew", pady=2)

        # 敌军军队代码
        ttk.Label(self.edit_frame, text="敌军军队:").grid(row=7, column=0, sticky="e", pady=2)
        self.current_enemy = ttk.Label(self.edit_frame, text="", foreground="blue")
        self.current_enemy.grid(row=7, column=1, sticky="w")
        self.enemy_army_combobox = ttk.Combobox(self.edit_frame, state="readonly")
        self.enemy_army_combobox.grid(row=7, column=2, sticky="ew", pady=2)

        # 存档难度
        ttk.Label(self.edit_frame, text="存档难度:").grid(row=8, column=0, sticky="e", pady=2)
        self.current_difficulty = ttk.Label(self.edit_frame, text="", foreground="blue")
        self.current_difficulty.grid(row=8, column=1, sticky="w")
        self.difficulty_combobox = ttk.Combobox(self.edit_frame, state="readonly")
        self.difficulty_combobox.grid(row=8, column=2, sticky="ew", pady=2)

        # 战争迷雾
        ttk.Label(self.edit_frame, text="战争迷雾:").grid(row=9, column=0, sticky="e", pady=2)
        self.current_fog = ttk.Label(self.edit_frame, text="", foreground="blue")
        self.current_fog.grid(row=9, column=1, sticky="w")
        self.fog_combobox = ttk.Combobox(self.edit_frame, state="readonly")
        self.fog_combobox.grid(row=9, column=2, sticky="ew", pady=2)

        # 战争区域
        ttk.Label(self.edit_frame, text="战争区域:").grid(row=10, column=0, sticky="e", pady=2)
        self.current_region = ttk.Label(self.edit_frame, text="", foreground="blue")
        self.current_region.grid(row=10, column=1, sticky="w")
        self.region_combobox = ttk.Combobox(self.edit_frame, state="readonly")
        self.region_combobox.grid(row=10, column=2, sticky="ew", pady=2)

        self.backup_cb = ttk.Checkbutton(
            self.edit_frame,
            text="修改前创建备份",
            variable=self.backup_var,
            onvalue=True,
            offvalue=False
        )
        self.backup_cb.grid(row=11, column=0, columnspan=3, pady=(10, 0), sticky="w")

        # 保存按钮
        self.save_button = ttk.Button(
            self.edit_frame,
            text="保存修改",
            command=self.save_changes
        )
        self.save_button.grid(row=12, column=0, columnspan=3, pady=(10, 0))

        # 设置下拉框选项
        self.setup_comboboxes()

    def create_help_frame(self):
        """创建程序说明框架"""
        self.help_frame = ttk.LabelFrame(self.root, text="程序说明", padding=10)
        self.help_frame.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")
        self.help_frame.grid_rowconfigure(0, weight=1)
        self.help_frame.grid_columnconfigure(0, weight=1)

        help_text = """
【地狱之门征服阵营修改工具V0.2使用说明 by.qionghaiBW★★★】
1. 使用步骤
    打开地狱之门征服存档修改工具V0.2（软件没有签名，可能会被杀毒软件报毒)
    点击"浏览..."按钮选择存档文件目录
    存档文件目录一般会在
    C:|Users|你的用户名|Documents|My Games|gates of hell|profiles|你的steam用户代码|campaign内
    点击"扫描存档文件"按钮列出所有.sav文件
    从列表中选择要修改的存档文件
    确定要更改的选项
    再次点击"确认修改"修改成功
2. 功能说明：
    本工具用于修改征服存档
    支持勇气valour和winds of iron 1920模组，请不要修改没有加载模组的存档！
3. 注意事项：
    修改前建议备份存档文件
    确保游戏没有加载征服存档
    本程序由qionghaiBW调试，deepseek AI辅助制作
    使用本程序意味着您愿意承担本程序带来的风险，造成损失与本程序作者无关
        """
        self.help_text = tk.Text(self.help_frame, wrap=tk.WORD, height=10)
        self.help_text.insert(tk.END, help_text)
        self.help_text.config(state=tk.DISABLED)
        self.help_text.grid(row=0, column=0, sticky="nsew")

    def setup_comboboxes(self):
        """设置下拉框的选项"""
        # 军队选项
        army_display = [f"{code}（{name}）" for code, name in self.army_options.items()]
        self.army_combobox["values"] = army_display
        self.enemy_army_combobox["values"] = army_display

        # 难度选项
        difficulty_display = [f"{code}（{name}）" for code, name in self.difficulty_options.items()]
        self.difficulty_combobox["values"] = difficulty_display

        # 战争迷雾选项
        fog_display = [f"{code}（{name}）" for code, name in self.fog_options.items()]
        self.fog_combobox["values"] = fog_display

        # 战区选项
        region_display = [f"{code}（{name}）" for code, name in self.region_options.items()]
        self.region_combobox["values"] = region_display

    def browse_files(self):
        """浏览文件夹，查找.sav文件"""
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.path_entry.delete(0, tk.END)
            self.path_entry.insert(0, folder_path)
            self.find_sav_files(folder_path)

    def remember_path(self):
        """记忆当前路径"""
        path = self.path_entry.get()
        if path and os.path.isdir(path):
            try:
                with open(self.memory_file, 'w', encoding='utf-8') as f:
                    f.write(path)
                messagebox.showinfo("成功", f"已记忆路径: {path}\n路径已保存到程序目录")
            except Exception as e:
                messagebox.showerror("错误", f"保存路径失败: {e}")
        else:
            messagebox.showerror("错误", "无效的路径，请选择有效目录")

    def load_remembered_path(self):
        """加载记忆的路径"""
        try:
            if os.path.exists(self.memory_file):
                with open(self.memory_file, 'r', encoding='utf-8') as f:
                    path = f.read().strip()
                    if path and os.path.isdir(path):
                        self.path_entry.delete(0, tk.END)
                        self.path_entry.insert(0, path)
                        self.find_sav_files(path)
        except Exception as e:
            print(f"加载记忆路径失败: {e}")

    def clear_memory(self):
        """清除记忆的路径"""
        try:
            if os.path.exists(self.memory_file):
                os.remove(self.memory_file)
                self.path_entry.delete(0, tk.END)
                self.file_listbox.delete(0, tk.END)
                messagebox.showinfo("成功", "已清除记忆路径")
        except Exception as e:
            messagebox.showerror("错误", f"清除记忆路径失败: {e}")

    def find_sav_files(self, folder_path):
        """查找指定文件夹中的.sav文件"""
        self.file_listbox.delete(0, tk.END)
        try:
            for file in os.listdir(folder_path):
                if file.endswith(".sav"):
                    self.file_listbox.insert(tk.END, file)
        except Exception as e:
            messagebox.showerror("错误", f"无法读取文件夹: {e}")

    def load_save_file(self, event):
        """加载存档文件并保留原始缩进"""
        selection = self.file_listbox.curselection()
        if not selection:
            return

        folder_path = self.path_entry.get()
        if not folder_path:
            return

        filename = self.file_listbox.get(selection[0])
        self.current_file = os.path.join(folder_path, filename)

        try:
            with zipfile.ZipFile(self.current_file, 'r') as zip_ref:
                if 'status' not in zip_ref.namelist():
                    messagebox.showerror("错误", "存档文件中缺少status文件")
                    return

                with zip_ref.open('status') as status_file:
                    # 读取原始内容（保留所有空白字符）
                    content = status_file.read()
                    try:
                        # 按行分割但保留行尾空白
                        self.status_content = content.decode('utf-8').splitlines(keepends=True)
                    except UnicodeDecodeError:
                        # 如果UTF-8失败尝试其他编码
                        self.status_content = content.decode('latin-1').splitlines(keepends=True)

                    self.parse_and_display_info()
                    self.update_edit_fields()
        except Exception as e:
            messagebox.showerror("错误", f"无法读取存档文件: {e}")

    def parse_and_display_info(self):
        """解析带缩进的status文件"""
        if not self.status_content:
            return

        self.info_text.config(state=tk.NORMAL)
        self.info_text.delete(1.0, tk.END)

        # 定义要提取的关键字段
        target_fields = {
            "gameVersion": "存档版本",
            "mp": "人力点数",
            "sp": "支援点数",
            "ap": "补给点数",
            "rp": "研究点数",
            "name": "存档名称",
            "army": "我军军队",
            "enemyArmy": "敌军军队",
            "difficulty": "难度",
            "fogofwar": "战争迷雾",
            "region": "战区"
        }

        # 逐行解析（保留缩进结构）
        brace_level = 0
        for line in self.status_content:
            stripped_line = line.strip()
            if not stripped_line:  # 跳过空行
                continue

            # 更新大括号层级
            brace_level += line.count('{') - line.count('}')

            # 只处理顶层字段（brace_level == 1）
            if brace_level == 1:
                for field, display in target_fields.items():
                    if stripped_line.startswith(f"{{{field} "):
                        # 提取值（保留原始字符串处理方式）
                        if '"' in line:
                            value = line.split('"')[1].strip()
                        else:
                            value = line[line.find(field) + len(field) + 1:line.rfind('}')].strip()

                        # 显示信息（带原始缩进格式）
                        indent = ' ' * (len(line) - len(line.lstrip()))
                        display_text = f"{indent}{display}: {value}"

                        # 添加额外描述
                        if field in ["army", "enemyArmy"]:
                            display_text += f"（{self.army_options.get(value, '未知')}）"
                        elif field == "difficulty":
                            display_text += f"（{self.difficulty_options.get(value, '未知')}）"
                        elif field == "fogofwar":
                            display_text += f"（{self.fog_options.get(value, '未知')}）"
                        elif field == "region":
                            display_text += f"（{self.region_options.get(value, '未知')}）"

                        self.info_text.insert(tk.END, display_text + '\n')

        self.info_text.config(state=tk.DISABLED)

    def update_edit_fields(self):
        """更新编辑框和当前值显示（修正版）"""
        if not self.status_content:
            return

        def extract_value(line, field):
            """更健壮的值提取方法"""
            try:
                # 查找字段后的第一个空格
                start = line.find(field) + len(field) + 1
                # 查找值结束位置
                if '"' in line:
                    # 带引号的值
                    start_quote = line.find('"', start) + 1
                    end_quote = line.find('"', start_quote)
                    return line[start_quote:end_quote]
                else:
                    # 不带引号的值
                    end = line.find('}', start)
                    return line[start:end].strip()
            except:
                return ""

        values = {}
        for line in self.status_content:
            line = line.strip()
            if line.startswith("{gameVersion"):
                values["gameVersion"] = extract_value(line, "gameVersion")
            elif line.startswith("{mp"):
                values["mp"] = extract_value(line, "mp")
            elif line.startswith("{sp"):
                values["sp"] = extract_value(line, "sp")
            elif line.startswith("{ap"):
                values["ap"] = extract_value(line, "ap")
            elif line.startswith("{rp"):
                values["rp"] = extract_value(line, "rp")
            elif line.startswith("{army"):
                values["army"] = extract_value(line, "army")
            elif line.startswith("{enemyArmy"):
                values["enemyArmy"] = extract_value(line, "enemyArmy")
            elif line.startswith("{difficulty"):
                values["difficulty"] = extract_value(line, "difficulty")
            elif line.startswith("{fogofwar"):
                values["fogofwar"] = extract_value(line, "fogofwar")
            elif line.startswith("{region"):
                values["region"] = extract_value(line, "region")

        # 更新当前值显示（确保不为空）
        self.current_version.config(text=values.get("gameVersion", ""))
        self.current_mp.config(text=values.get("mp", ""))
        self.current_sp.config(text=values.get("sp", ""))
        self.current_ap.config(text=values.get("ap", ""))
        self.current_rp.config(text=values.get("rp", ""))
        self.current_army.config(text=values.get("army", ""))
        self.current_enemy.config(text=values.get("enemyArmy", ""))
        self.current_difficulty.config(text=values.get("difficulty", ""))
        self.current_fog.config(text=values.get("fogofwar", ""))
        self.current_region.config(text=values.get("region", ""))

        # 更新输入框
        self.game_version_entry.delete(0, tk.END)
        self.game_version_entry.insert(0, values.get("gameVersion", ""))

        self.mp_entry.delete(0, tk.END)
        self.mp_entry.insert(0, values.get("mp", ""))

        self.sp_entry.delete(0, tk.END)
        self.sp_entry.insert(0, values.get("sp", ""))

        self.ap_entry.delete(0, tk.END)
        self.ap_entry.insert(0, values.get("ap", ""))

        self.rp_entry.delete(0, tk.END)
        self.rp_entry.insert(0, values.get("rp", ""))

        # 更新下拉框
        army_value = values.get("army", "")
        if army_value:
            self.army_combobox.set(f"{army_value}（{self.army_options.get(army_value, '未知')}）")

        enemy_army_value = values.get("enemyArmy", "")
        if enemy_army_value:
            self.enemy_army_combobox.set(f"{enemy_army_value}（{self.army_options.get(enemy_army_value, '未知')}）")

        difficulty_value = values.get("difficulty", "")
        if difficulty_value:
            self.difficulty_combobox.set(f"{difficulty_value}（{self.difficulty_options.get(difficulty_value, '未知')}）")

        fog_value = values.get("fogofwar", "")
        if fog_value:
            self.fog_combobox.set(f"{fog_value}（{self.fog_options.get(fog_value, '未知')}）")

        region_value = values.get("region", "")
        if region_value:
            self.region_combobox.set(f"{region_value}（{self.region_options.get(region_value, '未知')}）")

    def save_changes(self):
        """保存修改并保留原始格式（完整修复版）"""
        if not self.current_file:
            messagebox.showerror("错误", "请先选择存档文件")
            return

        try:
            # 构建修改映射
            field_map = {
                "gameVersion": self.game_version_entry.get(),
                "mp": self.mp_entry.get(),
                "sp": self.sp_entry.get(),
                "ap": self.ap_entry.get(),
                "rp": self.rp_entry.get(),
                "army": self.army_combobox.get().split("（")[0],
                "enemyArmy": self.enemy_army_combobox.get().split("（")[0],
                "difficulty": self.difficulty_combobox.get().split("（")[0],
                "fogofwar": self.fog_combobox.get().split("（")[0],
                "region": self.region_combobox.get().split("（")[0]
            }

            # 重建内容（完全保留原始格式）
            new_content = []
            brace_level = 0
            modified = False

            for line in self.status_content:
                original_line = line.rstrip('\n')  # 去掉末尾换行符（保留原始内容）
                new_line = original_line  # 默认不修改
                stripped_line = original_line.strip()

                # 更新大括号层级
                brace_level += line.count('{') - line.count('}')

                # 只处理顶层字段
                if brace_level == 1 and stripped_line:
                    for field, new_value in field_map.items():
                        if new_value and stripped_line.startswith(f"{{{field} "):
                            # 获取原始缩进（保留所有前导空白）
                            indent = line[:len(line) - len(line.lstrip())]

                            # 重建行（完全保留原始格式）
                            if '"' in stripped_line:
                                new_line = f"{indent}{{{field} \"{new_value}\"}}"
                            else:
                                new_line = f"{indent}{{{field} {new_value}}}"
                            modified = True
                            break

                # 保留原始换行符（可能是\n或\r\n）
                new_content.append(new_line + line[len(original_line):])

            if not modified:
                messagebox.showinfo("提示", "未检测到有效修改")
                return

            # 用户选择的备份选项
            create_backup = self.backup_var.get()

            # 创建临时zip文件
            temp_file = self.current_file + ".tmp"
            with zipfile.ZipFile(temp_file, 'w') as new_zip:
                with zipfile.ZipFile(self.current_file, 'r') as old_zip:
                    for item in old_zip.infolist():
                        if item.filename == 'status':
                            # 写入时保留原始换行风格
                            new_zip.writestr(item, ''.join(new_content))
                        else:
                            new_zip.writestr(item, old_zip.read(item.filename))

            # 处理备份
            if create_backup:
                backup_file = self.current_file + ".bak"
                os.replace(self.current_file, backup_file)
                message = f"修改已保存\n已创建备份: {os.path.basename(backup_file)}"
            else:
                os.remove(self.current_file)
                message = "修改已保存（未创建备份）"

            os.replace(temp_file, self.current_file)

            # 刷新显示
            self.load_save_file(None)
            messagebox.showinfo("成功", message)

        except Exception as e:
            messagebox.showerror("错误", f"保存失败: {str(e)}")
            if os.path.exists(temp_file):
                os.remove(temp_file)

if __name__ == "__main__":
    root = tk.Tk()
    app = SaveGameEditor(root)
    root.mainloop()