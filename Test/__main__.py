# python -m pip install maafw
# import maa.library

from maa.resource import Resource
from maa.controller import AdbController
from maa.tasker import Tasker
from maa.toolkit import Toolkit

# from maa.custom_recognition import CustomRecognition
# from maa.custom_action import CustomAction
# from maa.notification_handler import NotificationHandler, NotificationType
# from maa.job import Job, JobWithResult

from threading import Thread
import time
from tkinter import messagebox
import tkinter as tk
from tkinter import ttk
import threading
import json
import os


# 配置文件路径
CONFIG_FILE = "adb_config.json"
TASK_CONFIG_FILE = "task_config.json"
MULTI_INSTANCE_CONFIG_FILE = "multi_instance_config.json"  # 多开配置文件

# 定义一个字典来存储name和对应的expected与template值
data = {
    "迷宫兄弟（绿钥匙）": {"expected": "DM", "template": "迷宫兄弟.png"},
    "天上院明日香（青色钥匙）": {"expected": "GX", "template": "天上院明日香.png"},
    "丸藤翔（黄色钥匙）": {"expected": "GX", "template": "丸藤翔.png"},
    "暗貘良（黑色钥匙）": {"expected": "DM", "template": "暗貘良.png"},
    "帕伽索斯·J·克劳福德（白色钥匙）": {"expected": "DM", "template": "帕伽索斯·J·克劳福德.png"},
    "基斯·霍华德（红色钥匙）": {"expected": "DM", "template": "基斯·霍华德.png"}
}

# 修改 MultiInstanceManager 类中的实例ID管理
class MultiInstanceManager:
    def __init__(self):
        self.instances = {}  # {instance_id: {config}}
        self.load_multi_instance_config()
    
    def load_multi_instance_config(self):
        """加载多开配置"""
        if os.path.exists(MULTI_INSTANCE_CONFIG_FILE):
            try:
                with open(MULTI_INSTANCE_CONFIG_FILE, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                self.instances = config.get('instances', {})
            except Exception as e:
                print(f"加载多开配置失败: {e}")
    
    def save_multi_instance_config(self):
        """保存多开配置"""
        try:
            config = {
                'instances': self.instances
            }
            with open(MULTI_INSTANCE_CONFIG_FILE, 'w', encoding='utf-8') as f:
                json.dump(config, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"保存多开配置失败: {e}")
            return False
    
    def get_available_instance_id(self):
        """获取可用的实例ID"""
        if not self.instances:
            return 1
        
        # 找到当前最大的实例ID
        max_id = 0
        for instance_id in self.instances.keys():
            if instance_id.startswith("instance_"):
                try:
                    id_num = int(instance_id.replace("instance_", ""))
                    if id_num > max_id:
                        max_id = id_num
                except:
                    continue
        
        return max_id + 1
    
    def add_instance(self, instance_id, device_config):
        """添加实例"""
        instance_key = f"instance_{instance_id}"
        self.instances[instance_key] = {
            'device_config': device_config,
            'task_config': {},
            'created_time': time.time()
        }
        self.save_multi_instance_config()
    
    def remove_instance(self, instance_id):
        """移除实例"""
        instance_key = f"instance_{instance_id}"
        if instance_key in self.instances:
            del self.instances[instance_key]
            self.save_multi_instance_config()
    
    def update_instance_config(self, instance_id, config_type, config_data):
        """更新实例配置"""
        instance_key = f"instance_{instance_id}"
        if instance_key in self.instances:
            self.instances[instance_key][config_type] = config_data
            self.save_multi_instance_config()
    
    def get_instance_config(self, instance_id, config_type):
        """获取实例配置"""
        instance_key = f"instance_{instance_id}"
        if instance_key in self.instances:
            return self.instances[instance_key].get(config_type, {})
        return {}
    
    def get_all_instance_ids(self):
        """获取所有实例ID（只返回多开实例，排除主实例0）"""
        instance_ids = []
        for instance_key in self.instances.keys():
            if instance_key.startswith("instance_"):
                try:
                    id_num = int(instance_key.replace("instance_", ""))
                    if id_num > 0:  # 只返回 id > 0 的实例
                        instance_ids.append(id_num)
                except:
                    continue
        return sorted(instance_ids)

# 全局多开管理器
multi_instance_manager = MultiInstanceManager()

# ADB配置管理函数
def load_adb_config(instance_id=0):
    """加载ADB配置"""
    # 如果是多开模式，从多开管理器加载
    if instance_id > 0:
        device_config = multi_instance_manager.get_instance_config(f"instance_{instance_id}", 'device_config')
        return device_config or {}
    else:
        # 单开模式，从文件加载
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                return config
            except Exception as e:
                print(f"加载配置失败: {e}")
                return {}
        return {}

def save_adb_config(config, instance_id=0):
    """保存ADB配置"""
    try:
        # 确保只保存可序列化的数据，将 WindowsPath 转换为字符串
        serializable_config = {
            'adb_address': str(config.get('adb_address', '')),
            'adb_path': str(config.get('adb_path', ''))  # 转换为字符串
        }
        
        # 如果是多开模式，保存到多开管理器
        if instance_id > 0:
            multi_instance_manager.update_instance_config(f"instance_{instance_id}", 'device_config', serializable_config)
        else:
            # 单开模式，保存到文件
            with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
                json.dump(serializable_config, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        print(f"保存配置失败: {e}")
        return False

# 修改获取已保存设备的函数
def get_saved_adb_device(adb_devices, instance_id=0):
    """获取已保存的ADB设备"""
    config = load_adb_config(instance_id)
    saved_address = config.get('adb_address')
    
    if saved_address:
        # 确保地址是字符串
        saved_address = str(saved_address)
        for device in adb_devices:
            if device.address == saved_address:
                return device
    return None

# 显示设备选择窗口
def show_adb_devices(allow_saved_device=True, instance_id=0):
    adb_devices = Toolkit.find_adb_devices()
    if not adb_devices:
        messagebox.showinfo("No Devices", "No ADB device found.")
        return None

    # 尝试获取已保存的设备
    saved_device = None
    if allow_saved_device:
        saved_device = get_saved_adb_device(adb_devices, instance_id)
    
    # 如果有保存的设备且找到匹配，直接返回
    if saved_device:
        return saved_device

    # 创建窗口
    window = tk.Tk()
    window.title("Select ADB Device")
    
    # 创建标签
    tk.Label(window, text="请选择ADB设备:", font=("Arial", 12)).pack(pady=10)

    # 创建一个列表框来显示设备
    listbox = tk.Listbox(window, height=10, width=50, font=("Arial", 10))
    for device in adb_devices:
        listbox.insert(tk.END, f"{device.address} ({device.adb_path})")
    listbox.pack(pady=20, padx=20)
    listbox.select_set(0)  # 默认选择第一项

    selected_device = None

    # 确认按钮
    def on_select():
        nonlocal selected_device
        selection = listbox.curselection()
        if selection:
            selected_device = adb_devices[selection[0]]
            window.destroy()
        else:
            messagebox.showwarning("No Selection", "Please select a device.")

    confirm_button = tk.Button(window, text="Select", command=on_select, font=("Arial", 12), padx=20)
    confirm_button.pack(pady=10)

    # 阻塞直到窗口关闭
    window.mainloop()
    return selected_device

# 定义超链接函数
def open_url(url):
    import webbrowser
    webbrowser.open(url)

#迷宫运行函数
def move(pos,tasker):
    if pos == "leftup":
        pos1 = [200, 583, 67, 42]
        pipeline_override = {
            "MazeMove": {"target":pos1},
            "IfMazeMoveNow": {"target":pos1}
        }
        tasker.post_task("MazeMove",pipeline_override)
    elif pos == "leftdown":
        pos1 = [189, 706, 82, 52]
        pipeline_override = {
            "MazeMove": {"target":pos1},
            "IfMazeMoveNow": {"target":pos1}
        }
        tasker.post_task("MazeMove",pipeline_override)
    elif pos == "rightup":
        pos1 = [449, 568, 85, 56]
        pipeline_override = {
            "MazeMove": {"target":pos1},
            "IfMazeMoveNow": {"target":pos1}
        }
        tasker.post_task("MazeMove",pipeline_override)
    elif pos == "rightdown":
        pos1 = [448, 707, 85, 52]
        pipeline_override = {
            "MazeMove": {"target":pos1},
            "IfMazeMoveNow": {"target":pos1}
        }
        tasker.post_task("MazeMove",pipeline_override)
    else:
        pos1 = pos
        pipeline_override = {
            "MazeMove": {"target":pos1},
            "IfMazeMoveNow": {"target":pos1}
        }
        tasker.post_task("MazeMove",pipeline_override) 


def FirstFloor(tasker):
    move("rightdown", tasker)
    move("rightdown", tasker)
    move("rightup", tasker)
    move("rightdown", tasker)
    move("rightdown", tasker)
    move("rightup", tasker)
    move("rightdown", tasker)
    move("rightdown", tasker)
    move("rightup", tasker)
    move("rightup", tasker)
    move("rightdown", tasker)
    move("rightdown", tasker)

def SecondFloor(tasker):
    move("leftup", tasker)
    move("leftup", tasker)
    move("rightup", tasker)
    move("rightup", tasker)
    move("leftup", tasker)
    move("leftup", tasker)
    move("rightup", tasker)
    move("leftup", tasker)
    move("leftup", tasker)
    move("rightup", tasker)
    move("leftup", tasker)

def ThirdFloor(tasker):
    move("leftup", tasker)
    move("leftup", tasker)
    move("leftup", tasker)
    move("leftdown", tasker)  
    move("leftdown", tasker)
    move("leftup", tasker)
    move("leftdown", tasker)
    move("rightdown", tasker)
    move("rightdown", tasker)
    move("rightup", tasker)
    move([449, 449, 71, 35], tasker)
    move("leftup", tasker)
    move("leftup", tasker)
    move("leftup", tasker)
    move("leftup", tasker)
    move("leftdown", tasker)
    move("leftdown", tasker)
    move("leftup", tasker)
    move("leftdown", tasker)
    move("rightdown", tasker)
    move("rightdown", tasker)
    move("rightup", tasker)
    move([449, 449, 71, 35], tasker)
    move("leftup", tasker)
    move("leftup", tasker)
    move("leftup", tasker)
    move("leftup", tasker)
    move("leftup", tasker)
    move("rightup", tasker)
    move("rightup", tasker)
    move("rightdown", tasker)
    move("rightup", tasker)
    move("leftup", tasker)
    move("leftup", tasker)
    move("leftdown", tasker)
    move([202, 863, 59, 38],tasker)
    move("leftup",tasker)

# 实例管理类
class InstanceTab:
    def __init__(self, notebook, instance_id=0):
        self.notebook = notebook
        self.instance_id = instance_id
        self.tab_frame = ttk.Frame(notebook)
        self.tasker = None
        self.resource   = None
        self.controller = None
        self.selected_device = None
        self.if_running = True
        self.toggle_state = True
        self.is_executing = False  # 新增：标记是否正在执行任务
        
        # 初始化标签页UI
        self.init_tab_ui()
        
        # 添加到notebook，主实例没有关闭按钮，其他实例有
        tab_text = "主实例" if instance_id == 0 else f"实例 {instance_id} ❌"
        notebook.add(self.tab_frame, text=tab_text)
        
        # 如果是新实例，自动选择设备
        if instance_id > 0:
            self.auto_select_device()
        else:
            # 主实例尝试加载已保存的设备
            self.load_saved_device()
    
    def load_saved_device(self):
        """加载已保存的设备"""
        adb_devices = Toolkit.find_adb_devices()
        if adb_devices:
            saved_device = get_saved_adb_device(adb_devices, self.instance_id)
            if saved_device:
                self.selected_device = saved_device
                self.update_adb_status()
                self.init_maa_connection()
    
    def auto_select_device(self):
        """为新实例自动选择设备"""
        adb_devices = Toolkit.find_adb_devices()
        if adb_devices:
            # 获取已使用的设备
            used_devices = []
            for tab in instance_tabs.values():
                if tab.selected_device and tab != self:
                    used_devices.append(tab.selected_device.address)
            
            # 查找未使用的设备
            for device in adb_devices:
                if device.address not in used_devices:
                    self.selected_device = device
                    # 保存设备配置
                    config = {
                        'adb_address': str(device.address),
                        'adb_path': str(getattr(device, 'adb_path', ''))
                    }
                    save_adb_config(config, self.instance_id)
                    self.update_adb_status()
                    
                    # 初始化MAA连接
                    self.init_maa_connection()
                    break
            
            if not self.selected_device:
                messagebox.showwarning("警告", "所有可用设备都已被其他实例使用")
    
    def init_maa_connection(self):
        """初始化MAA连接"""
        if not self.selected_device:
            return
            
        try:
            # 如果已有连接，先关闭
            if self.tasker:
                self.tasker.post_stop()
                self.tasker = None
            
            user_path = "./"
            Toolkit.init_option(user_path)
            
            resource = Resource()
            resource.post_bundle("./resource")
            
            controller = AdbController(
                adb_path=self.selected_device.adb_path,
                address=self.selected_device.address,
                screencap_methods=self.selected_device.screencap_methods,
                input_methods=self.selected_device.input_methods,
                config=self.selected_device.config,
            )
            
            connection_job = controller.post_connection()
            connection_job.wait()
            if not connection_job.status:
                messagebox.showerror("连接失败", f"无法连接到设备: {self.selected_device.address}")
                return
            
            self.tasker = Tasker()
            self.tasker.bind(resource, controller)
            
            if self.tasker.inited:
                print(f"实例 {self.instance_id} 已连接到设备: {self.selected_device.address}")
                # 更新状态显示
                self.update_adb_status()
            else:
                messagebox.showerror("错误", "MAA初始化失败")
                
        except Exception as e:
            messagebox.showerror("错误", f"连接时发生错误: {str(e)}")
    
    def init_tab_ui(self):
        """初始化标签页UI"""
        # 创建顶部框架，包含标题和关闭按钮（仅非主实例）
        top_frame = tk.Frame(self.tab_frame)
        top_frame.grid(row=0, column=0, columnspan=4, sticky="ew", padx=10, pady=5)
        
        # 欢迎标签
        welcome_label = tk.Label(top_frame, text=f"欢迎使用MAADuelinks - 实例 {self.instance_id}", 
                                font=("Arial", 16), fg="black")
        welcome_label.pack(side=tk.LEFT)
        
        # 如果不是主实例，添加关闭按钮
        if self.instance_id > 0:
            close_button = tk.Button(top_frame, text="×", font=("Arial", 16, "bold"), 
                                   command=self.close_instance, bg="red", fg="white", 
                                   width=3, height=1)
            close_button.pack(side=tk.RIGHT)

        # 添加ADB状态显示和重新选择按钮
        adb_frame = tk.Frame(self.tab_frame)
        adb_frame.grid(row=1, column=0, columnspan=4, padx=10, pady=5, sticky="ew")
        
        self.adb_status_label = tk.Label(adb_frame, text="当前设备: 未连接", font=("Arial", 10), fg="blue")
        self.adb_status_label.pack(side=tk.LEFT, padx=(0, 10))
        
        reselect_button = tk.Button(adb_frame, text="重新选择ADB设备", 
                                command=lambda: self.reselect_adb_device(), 
                                font=("Arial", 10), bg="lightblue")
        reselect_button.pack(side=tk.RIGHT)

        # 任务列表

        # self.tasks = [
        #     "清战队任务加战队副本",
        #     "刷主页人机直到体力清空",
        #     "清自动传送门",
        #     "手动清传送门（不装卡垫，顶部视角）",
        #     "刷活动",
        #     "每日决斗回放",
        #     "领任务",
        #     "自动龙崎迷宫"
        # ]

        self.tasks = [
            "清战队任务加战队副本",
            "刷主页人机直到体力清空",
            "清自动传送门",
            "手动清传送门（不装卡垫，顶部视角）",
            "刷活动",
            "领任务",
            "每日决斗回放",
            "自动龙崎迷宫"
        ]

        # 世界选项
        world_options = [
            "DM世界", "DSOD世界", "GX世界", "5Ds世界", "Z4世界", "A5世界", "V6世界"
        ]

        # 传送门等级选项
        portal_level_options = ["10级", "20级", "30级", "40级"]

        # 活动种类选项
        activity_type_options = ["转轮活动","骰子活动","组队决斗活动","DD城堡","波动决斗","周年庆活动2025（需手动点进活动区域）","征服决斗"]

        # 传送门钥匙种类选项
        portal_key_options = [
            "迷宫兄弟（绿钥匙）", "天上院明日香（青色钥匙）", "丸藤翔（黄色钥匙）",
            "暗貘良（黑色钥匙）", "帕伽索斯·J·克劳福德（白色钥匙）", "基斯·霍华德（红色钥匙）",
            "默认传送门", "征服决斗"  # 添加在这里
        ]

        # 龙崎迷宫自动任务的楼层选项
        maze_floor_options = ["第一层", "第二层", "第三层"]

        # 创建队列存储勾选的任务编号和参数
        self.TaskList = []

        # 创建勾选框变量列表 - 改为实例变量
        self.check_vars = []

        # 存储选择框的当前值 - 改为实例变量
        self.selected_world = tk.StringVar(self.tab_frame)
        self.selected_world.set(world_options[0])
        self.selected_portal_level = tk.StringVar(self.tab_frame)
        self.selected_portal_level.set(portal_level_options[0])
        self.selected_activity_type = tk.StringVar(self.tab_frame)
        self.selected_activity_type.set(activity_type_options[0])
        self.selected_portal_key = tk.StringVar(self.tab_frame)
        self.selected_portal_key.set(portal_key_options[0])

        self.manual_portal_input_var = tk.IntVar(self.tab_frame)

        # 在主界面中添加下拉框
        self.maze_floor_var = tk.StringVar(self.tab_frame)
        self.maze_floor_var.set(maze_floor_options[0])

        # 创建输入框对应的变量 - 改为实例变量
        self.manual_entry_var = tk.StringVar(self.tab_frame)
        self.manual_entry_var.set("0")
        self.use_duelist_beads_var = tk.BooleanVar(self.tab_frame)
        self.activity_reverse_var = tk.BooleanVar(self.tab_frame)
        self.clan_copy_var = tk.BooleanVar(self.tab_frame)
        self.key_vars = []

        # 初始化当前行号
        current_row = 2

        # 创建任务复选框和选项
        for i, task_name in enumerate(self.tasks, start=1):
            var = tk.BooleanVar()
            check_button = tk.Checkbutton(self.tab_frame, text=task_name, variable=var)
            check_button.grid(row=current_row, column=0, sticky="w", padx=10, pady=5)
            
            self.check_vars.append(var)
            
            # 为每个任务创建附加选项
            if task_name == "刷主页人机直到体力清空":
                tk.Label(self.tab_frame, text="使用决斗珠次数：").grid(row=current_row, column=1, sticky="e", padx=4, pady=2)
                manual_entry = tk.Entry(self.tab_frame, textvariable=self.manual_entry_var, width=5)
                manual_entry.grid(row=current_row, column=2, padx=2, pady=2, sticky='ew')
                
                tk.Label(self.tab_frame, text="循环执行间隔（分钟）：").grid(row=current_row, column=3, sticky="e", padx=4, pady=2)
                self.cycle_time_entry = tk.Entry(self.tab_frame, width=5)
                self.cycle_time_entry.insert(0, "0")
                self.cycle_time_entry.grid(row=current_row, column=4, padx=2, pady=2, sticky='ew')
                
                current_row += 1
            elif task_name == "清自动传送门":
                current_row += 1
                portal_level_menu = tk.OptionMenu(self.tab_frame, self.selected_portal_level, *portal_level_options)
                portal_level_menu.grid(row=current_row, column=0, padx=4, pady=5, sticky='ew')
                current_row += 1
            elif task_name == "手动清传送门（不装卡垫，顶部视角）":
                current_row += 1
                portal_key_menu = tk.OptionMenu(self.tab_frame, self.selected_portal_key, *portal_key_options)
                portal_key_menu.grid(row=current_row, column=0, padx=4, pady=5, sticky='ew')
                tk.Label(self.tab_frame, text="手动次数：").grid(row=current_row, column=1, sticky="e")
                manual_portal_entry = tk.Entry(self.tab_frame, textvariable=self.manual_portal_input_var, width=5)
                manual_portal_entry.grid(row=current_row, column=2, padx=4, pady=5, sticky='ew')
                current_row += 1
            elif task_name == "刷活动":
                current_row += 1
                activity_type_menu = tk.OptionMenu(self.tab_frame, self.selected_activity_type, *activity_type_options)
                activity_type_menu.grid(row=current_row, column=0, padx=4, pady=5, sticky='ew')
                activity_reverse_check = tk.Checkbutton(self.tab_frame, text="特殊选项", variable=self.activity_reverse_var)
                activity_reverse_check.grid(row=current_row, column=1, padx=4, pady=5, sticky='ew')
                current_row += 1
            elif task_name == "清战队任务加战队副本":
                key_frame = tk.Frame(self.tab_frame, borderwidth=2, relief="groove")
                key_frame.grid(row=current_row, column=1, columnspan=2, padx=10, pady=5, sticky="nsew")
                
                key_options = ["普通钥匙", "红钥匙", "绿钥匙", "白钥匙", "黑钥匙", "蓝钥匙", "黄钥匙"]
                for j, key_name in enumerate(key_options):
                    key_var = tk.BooleanVar()
                    key_check_button = tk.Checkbutton(key_frame, text=key_name, variable=key_var)
                    key_check_button.grid(row=j // 3, column=j % 3, padx=5, pady=5, sticky="w")
                    self.key_vars.append(key_var)
                clan_copy_check_button = tk.Checkbutton(self.tab_frame, text="战队副本", variable=self.clan_copy_var)
                clan_copy_check_button.grid(row=current_row, column=3, padx=5, pady=5, sticky="w")
                
                current_row += 1
            else:
                current_row += 1

        # 龙崎迷宫选项
        maze_floor_label = tk.Label(self.tab_frame, text="龙崎迷宫自动开始楼层：")
        maze_floor_label.grid(row=current_row, column=1, sticky="e")
        maze_floor_menu = tk.OptionMenu(self.tab_frame, self.maze_floor_var, *maze_floor_options)
        maze_floor_menu.grid(row=current_row, column=2, padx=4, pady=5, sticky='ew')
        current_row += 1

        # 按钮
        confirm_button_row = current_row + 1
        stop_button_row = current_row + 1

        self.confirm_button = tk.Button(self.tab_frame, text="确认", 
                                    command=lambda: self.on_confirm(), 
                                    padx=40, font=("Arial", 12), bg="green", fg="white")
        self.confirm_button.grid(row=confirm_button_row, column=3, padx=10, pady=10, sticky='ew')

        self.stop_button = tk.Button(self.tab_frame, text="停止", 
                                    command=lambda: self.stop_task(), 
                                    font=("Arial", 12), padx=40, bg="red", fg="white")
        self.stop_button.grid(row=stop_button_row, column=2, padx=10, pady=10, sticky="ew")

        # 当前任务标签
        self.current_task_label = tk.Label(self.tab_frame, text="", font=("Arial", 12), fg="black")
        self.current_task_label.grid(row=len(self.tasks) + 5, column=0, sticky="w")

        # 加载配置
        self.load_task_config()
        
        # 启动标签更新
        self.update_label()

    def close_instance(self):
        """关闭实例"""
        if messagebox.askyesno("确认", f"确定要关闭实例 {self.instance_id} 吗？"):
            # 停止任务
            self.if_running = False
            self.is_executing = False
            if self.tasker:
                self.tasker.post_stop()
            
            # 从多开管理器中移除
            multi_instance_manager.remove_instance(self.instance_id)
            
            # 从notebook中移除
            self.notebook.forget(self.tab_frame)
            
            # 从实例字典中移除
            if self.instance_id in instance_tabs:
                del instance_tabs[self.instance_id]

    def update_adb_status(self):
        """更新ADB状态显示"""
        if self.selected_device:
            self.adb_status_label.config(text=f"当前设备: {self.selected_device.address}")
        else:
            self.adb_status_label.config(text="当前设备: 未连接")

    def reselect_adb_device(self):
        """重新选择ADB设备"""
        # 停止当前任务
        self.stop_task()
        
        new_device = show_adb_devices(allow_saved_device=False, instance_id=self.instance_id)
        if new_device:
            # 保存设备配置
            config = {
                'adb_address': str(new_device.address),
                'adb_path': str(getattr(new_device, 'adb_path', ''))
            }
            save_adb_config(config, self.instance_id)
            
            # 更新选择的设备
            self.selected_device = new_device
            self.update_adb_status()
            
            # 重新初始化MAA连接
            self.init_maa_connection()

    def on_confirm(self):
        """确认按钮处理"""
        # 重置运行状态
        self.if_running = True
        self.is_executing = True
        
        self.save_task_config()
        self.TaskList.clear()
        
        # 定义你想要的执行顺序：任务编号列表
        # 1=清战队任务, 2=刷主页人机, 3=清自动传送门, 4=手动清传送门,
        # 5=刷活动, 6=领任务, 7=每日决斗回放, 8=自动龙崎迷宫
        execution_order = [1, 2, 3, 4, 5, 7, 6, 8]  # 将任务6（领任务）移到倒数第二
        
        # 按自定义顺序检查任务
        for task_id in execution_order:
            i = task_id - 1  # 转换为0-based索引，用于访问check_vars
            
            if i < len(self.check_vars) and self.check_vars[i].get():
                task = [task_id]
                
                if task_id == 2:  # 刷主页人机直到体力清空
                    bead_count = self.manual_entry_var.get()
                    if bead_count and bead_count.isdigit():
                        task.append(int(bead_count))
                    else:
                        task.append(0)
                    
                    cycle_time = self.cycle_time_entry.get()
                    if cycle_time and cycle_time.isdigit():
                        task.append(int(cycle_time))
                    else:
                        task.append(0)
                elif task_id == 3:  # 清自动传送门
                    task.append(self.selected_portal_level.get())
                elif task_id == 4:  # 手动清传送门
                    task.append(self.selected_portal_key.get())
                    if self.manual_portal_input_var.get() is not None:
                        task.append(str(self.manual_portal_input_var.get()))
                    else:
                        task.append(str(0))
                elif task_id == 5:  # 刷活动
                    task.append(self.selected_activity_type.get())
                    task.append(self.activity_reverse_var.get())
                elif task_id == 1:  # 清战队任务
                    selected_keys = []
                    for j, key_var in enumerate(self.key_vars):
                        if key_var.get():
                            selected_keys.append(j + 1)
                    if selected_keys:
                        task.append(selected_keys)
                    if self.clan_copy_var.get():
                        task.append("ClanCopy")
                elif task_id == 8:  # 自动龙崎迷宫
                    task.append(self.maze_floor_var.get())
                # 任务6（领任务）没有额外参数，直接添加
                
                self.TaskList.append(task)
        
        # 使用线程异步执行
        if self.tasker and self.TaskList:
            thread = Thread(target=self.run_start_pipeline, args=(self.TaskList.copy(),))
            thread.daemon = True
            thread.start()
        else:
            if not self.tasker:
                messagebox.showwarning("警告", "请先连接ADB设备")
            elif not self.TaskList:
                messagebox.showwarning("警告", "请选择要执行的任务")

    def stop_task(self):
        """停止按钮处理"""
        self.if_running = False
        self.is_executing = False
        if self.tasker:
            self.tasker.post_stop()
        self.current_task_label.config(text=f"实例 {self.instance_id} - 任务已停止")

    def save_task_config(self):
        """保存任务配置"""
        try:
            config = {
                'tasks': {},
                'options': {}
            }
            
            for i, var in enumerate(self.check_vars):
                config['tasks'][str(i)] = var.get()
            
            config['options']['selected_world'] = self.selected_world.get()
            config['options']['selected_portal_level'] = self.selected_portal_level.get()
            config['options']['selected_activity_type'] = self.selected_activity_type.get()
            config['options']['selected_portal_key'] = self.selected_portal_key.get()
            config['options']['maze_floor'] = self.maze_floor_var.get()
            config['options']['manual_entry'] = self.manual_entry_var.get()
            config['options']['cycle_time'] = self.cycle_time_entry.get() if hasattr(self, 'cycle_time_entry') else "0"
            config['options']['manual_portal_input'] = self.manual_portal_input_var.get()
            config['options']['activity_reverse'] = self.activity_reverse_var.get() if hasattr(self, 'activity_reverse_var') else False
            config['options']['clan_copy'] = self.clan_copy_var.get() if hasattr(self, 'clan_copy_var') else False
            
            if hasattr(self, 'key_vars'):
                config['options']['keys'] = [var.get() for var in self.key_vars]
            
            multi_instance_manager.update_instance_config(f"instance_{self.instance_id}", 'task_config', config)
            return True
        except Exception as e:
            print(f"保存任务配置失败: {e}")
            return False

    def load_task_config(self):
        """加载任务配置"""
        config = multi_instance_manager.get_instance_config(f"instance_{self.instance_id}", 'task_config')
        if not config:
            return False
        
        try:
            if 'tasks' in config:
                for i, var in enumerate(self.check_vars):
                    if str(i) in config['tasks']:
                        var.set(config['tasks'][str(i)])
            
            if 'options' in config:
                opts = config['options']
                if 'selected_world' in opts:
                    self.selected_world.set(opts['selected_world'])
                if 'selected_portal_level' in opts:
                    self.selected_portal_level.set(opts['selected_portal_level'])
                if 'selected_activity_type' in opts:
                    self.selected_activity_type.set(opts['selected_activity_type'])
                if 'selected_portal_key' in opts:
                    self.selected_portal_key.set(opts['selected_portal_key'])
                if 'maze_floor' in opts:
                    self.maze_floor_var.set(opts['maze_floor'])
                if 'manual_entry' in opts:
                    self.manual_entry_var.set(opts['manual_entry'])
                if 'cycle_time' in opts and hasattr(self, 'cycle_time_entry'):
                    self.cycle_time_entry.delete(0, tk.END)
                    self.cycle_time_entry.insert(0, opts['cycle_time'])
                if 'manual_portal_input' in opts:
                    self.manual_portal_input_var.set(opts['manual_portal_input'])
                if 'activity_reverse' in opts and hasattr(self, 'activity_reverse_var'):
                    self.activity_reverse_var.set(opts['activity_reverse'])
                if 'clan_copy' in opts and hasattr(self, 'clan_copy_var'):
                    self.clan_copy_var.set(opts['clan_copy'])
                if 'keys' in opts and hasattr(self, 'key_vars'):
                    for i, var in enumerate(self.key_vars):
                        if i < len(opts['keys']):
                            var.set(opts['keys'][i])
            
            return True
        except Exception as e:
            print(f"加载任务配置失败: {e}")
            return False

    def update_label(self):
        """更新标签显示"""
        if self.if_running and not self.is_executing:
            if self.toggle_state:
                self.current_task_label.config(text=f"   实例 {self.instance_id} - 右上角关注up主")
            else:
                self.current_task_label.config(text=f"   实例 {self.instance_id} - 挖矿虽好，可不要贪杯哦")
            self.toggle_state = not self.toggle_state
            self.tab_frame.after(10000, self.update_label)

    def run_start_pipeline(self, TaskList):
        """运行任务管道"""
        pipeline_override = {
            "BatterierEmpty": {"next": []},
            "ShutDownClan2": {"next": []}
        }
        
        while TaskList:  # 删除了 if_running 检查
            TaskNum = TaskList.pop(0)
            current_task_name = self.tasks[TaskNum[0] - 1]
            self.current_task_label.config(text=f"实例 {self.instance_id} - 当前任务: {current_task_name}")
            
            try:
                if TaskNum[0] == 2:  # 刷主页人机直到体力清空
                    self.handle_homepage_task(TaskNum, pipeline_override)
                    time.sleep(2)
                elif TaskNum[0] == 1:  # 清战队任务加战队副本
                    if len(TaskNum) > 1:
                        if isinstance(TaskNum[1], list):
                            pipeline_override["ShutDownClan2"]["next"] = ["ClanStoreFind"]
                            self.tasker.post_task("FindClan", pipeline_override)
                            i = int(len(TaskNum[1]))
                            ClanTaskList = TaskNum[1]
                            while ClanTaskList:  # 删除了 if_running 检查
                                ClanStoreTask = ClanTaskList.pop(0)
                                if ClanStoreTask == 1:
                                    pipeline_override = {"SelectKey":{"template":"OrKey.png"}}
                                elif ClanStoreTask == 2:
                                    pipeline_override = {"SelectKey":{"template":"RedKey.png"}}
                                elif ClanStoreTask == 3:
                                    pipeline_override = {"SelectKey":{"template":"GreenKey.png"}}
                                elif ClanStoreTask == 4:
                                    pipeline_override = {"SelectKey":{"template":"WhiteKey.png"}}
                                elif ClanStoreTask == 5:
                                    pipeline_override = {"SelectKey":{"template":"BlackKey.png"}}
                                elif ClanStoreTask == 6:    
                                    pipeline_override = {"SelectKey":{"template":"BlueKey.png"}}
                                elif ClanStoreTask == 7:
                                    pipeline_override = {"SelectKey":{"template":"YellowKey.png"}}
                                self.tasker.post_task("GotoSelectKey", pipeline_override)
                            self.tasker.post_task("ReturnClanHome")
                            if len(TaskNum) == 3:
                                if TaskNum[2] == "ClanCopy":
                                    self.tasker.post_task("ClanCopy")
                            else:
                                self.tasker.post_task("ReturnClanHome")
                        elif TaskNum[1] == "ClanCopy":
                            pipeline_override["ShutDownClan2"]["next"] = ["ClanCopy"]
                            self.tasker.post_task("FindClan", pipeline_override)
                    elif len(TaskNum) == 1:
                        pipeline_override["ShutDownClan2"]["next"] = ["ClanCopy"]
                        self.tasker.post_task("FindClan", pipeline_override)
                elif TaskNum[0] == 3:  # 清自动传送门
                    pipeline_override = {"SelectPortals":{"expected":TaskNum[1]}}
                    self.tasker.post_task("PortalsEntry", pipeline_override)
                elif TaskNum[0] == 4:  # 手动清传送门
                    if TaskNum[1] == "默认传送门":
                        self.tasker.post_task("ManualPortalsFind2")
                    elif TaskNum[1] == "征服决斗":  # 新增：征服决斗处理
                        self.tasker.post_task("ZhengfuDuel")
                        i = 1
                        while i < int(TaskNum[2]):  # 删除了 if_running 检查
                            self.tasker.post_task("ZhengfuDuel", pipeline_override)
                            i += 1
                    else:
                        Expected = ""
                        Template = ""
                        if TaskNum[1] == "迷宫兄弟（绿钥匙）":
                            Expected = data["迷宫兄弟（绿钥匙）"]["expected"]
                            Template = data["迷宫兄弟（绿钥匙）"]["template"]
                        elif TaskNum[1] == "天上院明日香（青色钥匙）":
                            Expected = data["天上院明日香（青色钥匙）"]["expected"]
                            Template = data["天上院明日香（青色钥匙）"]["template"]
                        elif TaskNum[1] == "丸藤翔（黄色钥匙）":
                            Expected = data["丸藤翔（黄色钥匙）"]["expected"]
                            Template = data["丸藤翔（黄色钥匙）"]["template"]
                        elif TaskNum[1] == "暗貘良（黑色钥匙）":
                            Expected = data["暗貘良（黑色钥匙）"]["expected"]
                            Template = data["暗貘良（黑色钥匙）"]["template"]
                        elif TaskNum[1] == "帕伽索斯·J·克劳福德（白色钥匙）":
                            Expected = data["帕伽索斯·J·克劳福德（白色钥匙）"]["expected"]
                            Template = data["帕伽索斯·J·克劳福德（白色钥匙）"]["template"]
                        elif TaskNum[1] == "基斯·霍华德（红色钥匙）":
                            Expected = data["基斯·霍华德（红色钥匙）"]["expected"]
                            Template = data["基斯·霍华德（红色钥匙）"]["template"]
                        pipeline_override = {
                            "SelectManualPortalsWorld2": {"expected": Expected},
                            "SelectManualPortalsRole": {"template": Template}
                        }
                        self.tasker.post_task("ManualPortalsEntry", pipeline_override)
                    i = 1
                    while i < int(TaskNum[2]):  # 删除了 if_running 检查
                        if TaskNum[1] == "征服决斗":
                            # self.tasker.post_task("ZhengfuDuel", pipeline_override)
                            pass
                        else:
                            self.tasker.post_task("ManualPortalsFind2", pipeline_override)
                        i += 1
                elif TaskNum[0] == 6:  # 领任务
                    self.tasker.post_task("HomePageReward")
                elif TaskNum[0] == 5:  # 刷活动
                    activity_type = TaskNum[1]
                    if len(TaskNum) > 2:
                        reverse_order = TaskNum[2]
                    
                    # 根据活动类型设置任务参数
                    if activity_type == "转轮活动":
                        Taskpar = "WheelActivityEntry"
                    elif activity_type == "传送门活动":
                        Taskpar = ""
                    elif activity_type == "骰子活动":
                        Taskpar = "DiceActivityEntry"
                    elif activity_type == "组队决斗活动":
                        Taskpar = "TeamActivityEntry"
                    elif activity_type == "周年庆活动2025（需手动点进活动区域）":
                        Taskpar = "NewYearActivity2025"
                    elif activity_type == "DD城堡":
                        Taskpar = "DDActivityEntry"
                    elif activity_type == "波动决斗":
                        Taskpar = "WaveActivityEntry"
                    elif activity_type == "征服决斗":
                        Taskpar = "StartManualDuelPortals"

                    # 判断是否需要反序执行
                    if activity_type == "DD城堡" and reverse_order:
                        # DD城堡反序逻辑
                        pipeline_override = {
                            "StartDDActivity":{"index": -1},
                            "ActivityEntry": {"next": Taskpar}
                        }
                    elif activity_type == "周年庆活动2025（需手动点进活动区域）" and reverse_order:
                        # 周年庆活动反序逻辑（这里需要您根据实际需要添加具体执行内容）
                        pipeline_override = {
                            "IfNewYearActivityNow":{"next":["SelectActivityBot2","UseRefresh"]},  # 从最后一个开始
                            "UseRefresh":{"next":["SelectActivityBot2"]},
                            "ActivityEntry": {"next": Taskpar}
                        }
                        # 注意：您需要根据实际MAA任务配置来修改这个逻辑
                    else:
                        # 正常顺序执行
                        pipeline_override = {
                            "ActivityEntry": {"next": Taskpar}
                        }
                    
                    self.tasker.post_task("ActivityEntry", pipeline_override)
                elif TaskNum[0] == 7:  # 每日回放
                    pipeline_override = {}
                    self.tasker.post_task("VideoReview", pipeline_override)
                elif TaskNum[0] == 8:  # 自动龙崎迷宫
                    start_floor = TaskNum[1]
                    self.tasker.post_task("Mazeauto")
                    if start_floor == "第一层":
                        FirstFloor(self.tasker)
                        SecondFloor(self.tasker)
                        ThirdFloor(self.tasker)
                    elif start_floor == "第二层":
                        SecondFloor(self.tasker)
                        ThirdFloor(self.tasker)
                    elif start_floor == "第三层":
                        ThirdFloor(self.tasker)
            except Exception as e:
                print(f"实例 {self.instance_id} 任务执行失败: {e}")
        
        # 任务执行完成
        self.is_executing = False
        if self.if_running:
            self.current_task_label.config(text=f"实例 {self.instance_id} - 所有任务已完成")

    def handle_homepage_task(self, TaskNum, pipeline_override):
        """处理刷主页人机任务"""
        import time
        
        cycle_time_minutes = 0
        if len(TaskNum) > 2 and TaskNum[2]:
            cycle_time_minutes = int(TaskNum[2])
        
        bead_count = 0
        if len(TaskNum) > 1 and TaskNum[1]:
            bead_count = int(TaskNum[1])
        
        def execute_homepage_cycle():
            nonlocal bead_count
            
            def update_ui():
                self.current_task_label.config(text=f"实例 {self.instance_id} - 正在执行刷主页人机任务...")
            
            self.tab_frame.after(0, update_ui)
            
            if bead_count > 0:
                for i in range(bead_count):
                    self.tasker.post_task("NewHomePage", pipeline_override)
                    self.tasker.post_task("FindDuelBead")
                self.tasker.post_task("NewHomePage", pipeline_override)
            else:
                self.tasker.post_task("NewHomePage", pipeline_override)
        
        def run_cycle():
            cycle_count = 0
            
            while True:  # 删除了 if_running 检查
                cycle_count += 1
                
                def update_cycle_info():
                    if cycle_time_minutes > 0:
                        self.current_task_label.config(
                            text=f"实例 {self.instance_id} - 刷主页人机 - 第{cycle_count}次循环 (间隔{cycle_time_minutes}分钟)"
                        )
                    else:
                        self.current_task_label.config(text=f"实例 {self.instance_id} - 刷主页人机 - 单次执行")
                
                self.tab_frame.after(0, update_cycle_info)
                
                execute_homepage_cycle()
                
                if cycle_time_minutes <= 0:
                    break
                    
                if cycle_time_minutes > 0:  # 删除了 if_running 检查
                    def update_wait_info():
                        self.current_task_label.config(
                            text=f"实例 {self.instance_id} - 刷主页人机 - 等待中... ({cycle_time_minutes}分钟后开始下次循环)"
                        )
                    
                    self.tab_frame.after(0, update_wait_info)
                    
                    wait_seconds = cycle_time_minutes * 60
                    segment = 5
                    
                    for i in range(0, wait_seconds, segment):
                        time.sleep(min(segment, wait_seconds - i))

            def finish_ui():
                if self.if_running:
                    self.current_task_label.config(text=f"实例 {self.instance_id} - 刷主页人机任务完成")
                else:
                    self.current_task_label.config(text=f"实例 {self.instance_id} - 刷主页人机任务已停止")
            
            self.tab_frame.after(0, finish_ui)
        
        cycle_thread = threading.Thread(target=run_cycle)
        cycle_thread.daemon = True
        cycle_thread.start()

# 全局变量
instance_tabs = {}  # {instance_id: InstanceTab}
current_tab = None

def create_new_instance():
    """创建新实例"""
    # 获取可用的实例ID
    instance_id = multi_instance_manager.get_available_instance_id()
    add_tab(instance_id)

def add_tab(instance_id):
    """添加实例标签页"""
    tab = InstanceTab(notebook, instance_id)
    instance_tabs[instance_id] = tab
    
    # 切换到新标签页
    notebook.select(tab.tab_frame)

# 修改初始化主UI，加载所有保存的实例
def init_main_ui():
    global root, notebook
    
    # 初始化主窗口
    root = tk.Tk()
    root.title("MAADuelinks3.91")
    
    # 创建Notebook（标签页控件）
    notebook = ttk.Notebook(root)
    notebook.pack(fill='both', expand=True, padx=10, pady=10)
    
    # 添加主实例
    add_tab(0)
    
    # 加载所有保存的实例
    saved_instance_ids = multi_instance_manager.get_all_instance_ids()
    for instance_id in saved_instance_ids:
        add_tab(instance_id)
    
    # 添加"+"标签用于创建新实例
    add_button_tab()
    
    # 添加窗口关闭事件处理
    def on_closing():
        multi_instance_manager.save_multi_instance_config()
        root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    
    # 启动主事件循环
    root.mainloop()

def add_button_tab():
    """添加新建实例按钮标签页"""
    button_tab = ttk.Frame(notebook)
    notebook.add(button_tab, text="+")
    
    # 添加按钮到按钮标签页
    add_button = tk.Button(button_tab, text="新建实例", command=create_new_instance, 
                          font=("Arial", 16), bg="lightgreen", padx=20, pady=10)
    add_button.pack(expand=True)
    
    # 确保按钮标签页始终是最后一个
    def on_notebook_change(event):
        if event.widget == notebook:
            # 获取当前所有标签页
            tabs = notebook.tabs()
            button_tab_index = tabs.index(button_tab._w)
            # 如果按钮标签页不是最后一个，移动它到最后
            if button_tab_index != len(tabs) - 1:
                notebook.insert(len(tabs) - 1, button_tab)
    
    notebook.bind("<<NotebookTabChanged>>", on_notebook_change)

# 修改主函数
def main():
    # 直接初始化主UI，设备连接在实例中处理
    init_main_ui()

if __name__ == "__main__":
    main()
