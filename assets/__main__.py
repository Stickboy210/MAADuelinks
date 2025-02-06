# python -m pip install maafw
import maa.library
from maa.resource import Resource
from maa.controller import AdbController
from maa.tasker import Tasker
from maa.toolkit import Toolkit

from maa.custom_recognition import CustomRecognition
from maa.custom_action import CustomAction
from maa.notification_handler import NotificationHandler, NotificationType
from maa.job import Job, JobWithResult
import time

import tkinter as tk
import threading



# 定义一个字典来存储name和对应的expected与template值
data = {
    "迷宫兄弟（绿钥匙）": {"expected": "DM", "template": "迷宫兄弟.png"},
    "天上院明日香（青色钥匙）": {"expected": "GX", "template": "天上院明日香.png"},
    "丸藤翔（黄色钥匙）": {"expected": "GX", "template": "丸藤翔.png"},
    "暗貘良（黑色钥匙）": {"expected": "DM", "template": "暗貘良.png"},
    "帕伽索斯·J·克劳福德（白色钥匙）": {"expected": "DM", "template": "帕伽索斯·J·克劳福德.png"},
    "基斯·霍华德（红色钥匙）": {"expected": "DM", "template": "基斯·霍华德.png"}
}

# 初始化主窗口
root = tk.Tk()
root.title("MAADuelinks3.0")

# 创建欢迎标签
welcome_label = tk.Label(root, text="欢迎使用MAADuelinks！", font=("Arial", 16), fg="black")
welcome_label.grid(row=0, column=0, columnspan=4, pady=10, sticky="ew")

#任务列表
tasks = [
    "清战队任务加战队副本",
    "刷主页人机直到体力清空",
    "清自动传送门",
    "手动清传送门（不装卡垫，顶部视角）",
    "刷活动",
    "领任务",
    "每日决斗回放",
    "自动龙崎迷宫"  # 添加新任务
]

# 世界选项
world_options = [
    "DM世界", "DSOD世界", "GX世界", "5Ds世界", "Z4世界", "A5世界", "V6世界"
]

# 传送门等级选项
portal_level_options = ["10级", "20级", "30级", "40级"]

# 活动种类选项
activity_type_options = ["转轮活动","骰子活动","组队决斗活动","周年庆活动2025（需手动点进活动区域）"]

# 传送门钥匙种类选项
portal_key_options = [
    "迷宫兄弟（绿钥匙）", "天上院明日香（青色钥匙）", "丸藤翔（黄色钥匙）",
    "暗貘良（黑色钥匙）", "帕伽索斯·J·克劳福德（白色钥匙）", "基斯·霍华德（红色钥匙）"
]

# 龙崎迷宫自动任务的楼层选项
maze_floor_options = ["第一层", "第二层", "第三层"]

# 创建队列存储勾选的任务编号和参数
TaskList = []

# 创建勾选框变量列表
check_vars = []

# 存储选择框的当前值
selected_world = tk.StringVar(root)
selected_world.set(world_options[0])  # 默认选择第一个选项
selected_portal_level = tk.StringVar(root)
selected_portal_level.set(portal_level_options[0])  # 默认选择第一个选项
selected_activity_type = tk.StringVar(root)
selected_activity_type.set(activity_type_options[0])  # 默认选择第一个选项
selected_portal_key = tk.StringVar(root)
selected_portal_key.set(portal_key_options[0])  # 默认选择第一个选项

manual_portal_input_var = tk.IntVar(root)

# 在主界面中添加下拉框
maze_floor_var = tk.StringVar(root)
maze_floor_var.set(maze_floor_options[0])  # 默认选择第一层



# 创建输入框对应的变量
manual_entry_var = tk.StringVar(root)  # 刷主页人机直到体力清空的输入框变量
manual_entry_var.set(0) #默认不使用决斗珠
use_duelist_beads_var = tk.BooleanVar(root)  # 是否1体力用决斗珠的变量，默认为False

# 创建一个列表框来显示任务列表状态
# task_listbox = tk.Listbox(root)
# task_listbox.grid(row=len(tasks) + 4, column=0, columnspan=4, pady=5, sticky='ew')



# 打印任务列表函数
# def print_task_list():
#     print("当前任务列表:")
#     for task in TaskList:
#         task_name = tasks[task[0] - 1]  # 根据任务编号找到任务名称
#         if len(task) > 1:
#             task_details = [task_name] + [str(item) for item in task[1:]]  # 确保所有项都是字符串
#             print(f"任务 {task[0]}: {', '.join(task_details)}")
#         else:
#             print(f"任务 {task[0]}: {task_name}")
#终止按钮
def Stop_Button(tasker):
    global running
    running = False  # 设置停止标志
    tasker.post_stop()

# 创建打印任务列表按钮
# print_task_list_button = tk.Button(root, text="打印任务列表", command=print_task_list)
# print_task_list_button.grid(row=len(tasks) + 5, column=0, padx=10, pady=5, sticky='ew')

# 定义超链接函数
def open_url(url):
    import webbrowser
    webbrowser.open(url)

# 初始化当前行号
current_row = 1

# 在“刷主页人机直到体力清空”任务后面添加“使用决斗珠次数”和“循环执行时间”选项
for i, task_name in enumerate(tasks, start=1):
    var = tk.BooleanVar()
    check_button = tk.Checkbutton(root, text=task_name, variable=var)
    check_button.grid(row=current_row, column=0, sticky="w", padx=10, pady=5)
    
    check_vars.append(var)
    
    # 为每个任务创建附加选项
    if task_name == "刷主页人机直到体力清空":
        # “使用决斗珠次数”输入框
        tk.Label(root, text="使用决斗珠次数：").grid(row=current_row, column=1, sticky="e")
        manual_entry = tk.Entry(root, textvariable=manual_entry_var, width=5)
        manual_entry.grid(row=current_row, column=2, padx=4, pady=5, sticky='ew')
        
        # “循环执行时间”输入框
        tk.Label(root, text="循环执行时间（分钟）：").grid(row=current_row, column=3, sticky="e")
        cycle_time_entry = tk.Entry(root, width=5)
        cycle_time_entry.grid(row=current_row, column=4, padx=4, pady=5, sticky='ew')
        
        current_row += 1  # 增加行号，为下一个选项腾出空间
    elif task_name == "清自动传送门":
        current_row += 1  # 增加额外的行间距
        portal_level_menu = tk.OptionMenu(root, selected_portal_level, *portal_level_options)
        portal_level_menu.grid(row=current_row, column=0, padx=4, pady=5, sticky='ew')
        current_row += 1  # 增加行号，为下一个选项腾出空间
    elif task_name == "手动清传送门（不装卡垫，顶部视角）":
        current_row += 1
        portal_key_menu = tk.OptionMenu(root, selected_portal_key, *portal_key_options)
        portal_key_menu.grid(row=current_row, column=0, padx=4, pady=5, sticky='ew')
        tk.Label(root, text="手动次数：").grid(row=current_row, column=1, sticky="e")  # 添加输入框标签
        manual_portal_entry = tk.Entry(root, textvariable=manual_portal_input_var, width=5)  # 设置宽度为5
        manual_portal_entry.grid(row=current_row, column=2, padx=4, pady=5, sticky='ew')
        current_row += 1  # 增加行号，为下一个选项腾出空间
    elif task_name == "刷活动":
        current_row += 1
        activity_type_menu = tk.OptionMenu(root, selected_activity_type, *activity_type_options)
        activity_type_menu.grid(row=current_row, column=0, padx=4, pady=5, sticky='ew')
        current_row += 1  # 增加行号，为下一个选项腾出空间
    elif task_name == "清战队任务加战队副本":
        key_frame = tk.Frame(root, borderwidth=2, relief="groove")  # 创建一个矩形框
        key_frame.grid(row=current_row, column=1, columnspan=2, padx=10, pady=5, sticky="nsew")
        
        key_options = ["普通钥匙", "红钥匙", "绿钥匙", "白钥匙", "黑钥匙", "蓝钥匙", "黄钥匙"]
        key_vars = []
        for j, key_name in enumerate(key_options):
            key_var = tk.BooleanVar()
            key_check_button = tk.Checkbutton(key_frame, text=key_name, variable=key_var)
            key_check_button.grid(row=j // 3, column=j % 3, padx=5, pady=5, sticky="w")
            key_vars.append(key_var)
        
        clan_copy_var = tk.BooleanVar()
        clan_copy_check_button = tk.Checkbutton(root, text="战队副本", variable=clan_copy_var)
        clan_copy_check_button.grid(row=current_row, column=3, padx=5, pady=5, sticky="w")
        
        current_row += 1
    else:
        current_row += 1


# 更新任务列表显示的函数
# def update_task_list_display(TaskList):
#     task_listbox.delete(0, tk.END)  # 清空列表框
#     for task in sorted(TaskList, key=lambda x: tasks.index(tasks[x[0] - 1])):
#         task_name = tasks[task[0] - 1]  # 根据任务编号找到任务名称
#         if len(task) > 1:
#             task_details = [task_name] + [str(item) for item in task[1:]]  # 确保所有项都是字符串
#             task_listbox.insert(tk.END, f"任务 {task[0]}: {', '.join(task_details)}")
#         else:
#             task_listbox.insert(tk.END, f"任务 {task[0]}: {task_name}")

# # 添加每日决斗回放选项
# tasks.append("每日决斗回放")
# var = tk.BooleanVar()
# check_button = tk.Checkbutton(root, text="每日决斗回放", variable=var)
# check_button.grid(row=current_row, column=0, sticky="w", padx=10, pady=5)
# check_vars.append(var)
# current_row += 1

# # 添加自动求卡册点赞功能选项
# tasks.append("自动求卡册点赞（还用不了）")
# var = tk.BooleanVar()
# check_button = tk.Checkbutton(root, text="自动求卡册点赞（还用不了）", variable=var)
# check_button.grid(row=current_row, column=0, sticky="w", padx=10, pady=5)
# check_vars.append(var)
# current_row += 1

# # 添加战队副本选项
# clan_copy_var = tk.BooleanVar()
# clan_copy_check_button = tk.Checkbutton(key_frame, text="战队副本", variable=clan_copy_var)
# clan_copy_check_button.grid(row=len(key_options) // 3 + 1, column=0, padx=5, pady=5, sticky="w")


# 在“龙崎迷宫自动”任务后面添加下拉框
maze_floor_label = tk.Label(root, text="龙崎迷宫自动开始楼层：")
maze_floor_label.grid(row=current_row, column=1, sticky="e")
maze_floor_menu = tk.OptionMenu(root, maze_floor_var, *maze_floor_options)
maze_floor_menu.grid(row=current_row, column=2, padx=4, pady=5, sticky='ew')
current_row += 1  # 增加行号，为下一个选项腾出空间

#迷宫运行函数
def move(pos,tasker):
    # pipeline_override = {
    #     "MazeMove": {"target":[]},
    #     "IfMazeMoveNow": {"target":[]}
    # }
    if pos == "leftup":
        pos1 = [200, 583, 67, 42]
        pipeline_override = {
            "MazeMove": {"target":pos1},
            "IfMazeMoveNow": {"target":pos1}
        }
        tasker.post_pipeline("MazeMove",pipeline_override)
    elif pos == "leftdown":
        pos1 = [189, 706, 82, 52]
        pipeline_override = {
            "MazeMove": {"target":pos1},
            "IfMazeMoveNow": {"target":pos1}
        }
        tasker.post_pipeline("MazeMove",pipeline_override)
    elif pos == "rightup":
        pos1 = [449, 568, 85, 56]
        pipeline_override = {
            "MazeMove": {"target":pos1},
            "IfMazeMoveNow": {"target":pos1}
        }
        tasker.post_pipeline("MazeMove",pipeline_override)
    elif pos == "rightdown":
        pos1 = [448, 707, 85, 52]
        pipeline_override = {
            "MazeMove": {"target":pos1},
            "IfMazeMoveNow": {"target":pos1}
        }
        tasker.post_pipeline("MazeMove",pipeline_override)
    else:
        pos1 = pos
        pipeline_override = {
            "MazeMove": {"target":pos1},
            "IfMazeMoveNow": {"target":pos1}
        }
        tasker.post_pipeline("MazeMove",pipeline_override) 

def FourthFloor(tasker):
    move("rightdown", tasker)
    move("leftdown", tasker)
    move("rightdown", tasker)
    move("leftdown", tasker)
    move("rightdown", tasker)
    move("leftdown", tasker)
    move("rightdown", tasker)
    move("rightdown", tasker)
    move("rightdown", tasker)
    move("rightup", tasker)
    move("rightup", tasker)
    move("rightup", tasker)
    move("leftup", tasker)
    move("rightdown", tasker)
    
    move("rightup", tasker)
    move("rightup", tasker)
    move("leftdown", tasker)
    move("leftdown", tasker)
    
    move("rightdown", tasker)
    move("rightdown", tasker)
    move("rightdown", tasker)
    move("rightdown", tasker)
    move("rightdown", tasker)
    move("leftdown", tasker)
    move("rightdown", tasker)
    move("rightup", tasker)

def FirstFloor(tasker):
    move("rightdown", tasker)
    move("rightup", tasker)
    move("rightup", tasker)
    move("leftup", tasker)
    move("leftup", tasker)
    move("rightup", tasker)
    move("rightup", tasker)
    move("rightdown", tasker)
    move("rightdown", tasker)
    move("rightdown", tasker)
    move("leftdown", tasker)
    move("rightdown", tasker)
    move("leftdown", tasker)
    move("leftdown", tasker)
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
    move("leftdown", tasker)  
    move("leftup", tasker)
    move("leftdown", tasker)
    move("leftup", tasker)
    move("leftup", tasker)
    # if exists(Template(r"tpl1653800261462.png", threshold=0.95, record_pos=(-0.282, -0.337), resolution=(900, 1600))):
    #     move("leftup", tasker)
    # else:
    #     move("leftup", tasker)
    move("leftup", tasker) #just kankan xingbuxing
    move("rightup", tasker)
    move("rightup", tasker)
    move("rightdown", tasker)
    move("rightdown", tasker)
    move("rightup", tasker)
    move("rightdown", tasker)
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
    move("rightup", tasker)
    move("rightup", tasker)
    move("rightdown", tasker)
    move("rightup", tasker)
    move("leftup", tasker)
    move("leftup", tasker)
    move("leftdown", tasker)
    move([202, 863, 59, 38],tasker)
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
    move("rightup", tasker)
    move("rightup", tasker)
    move("rightdown", tasker)
    move("rightup", tasker)
    move("leftup", tasker)
    move("leftup", tasker)
    move("leftdown", tasker)
    move([202, 863, 59, 38],tasker)
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
    move("rightup", tasker)
    move("rightup", tasker)
    move("rightdown", tasker)
    move("rightup", tasker)
    move("leftup", tasker)
    move("leftup", tasker)
    move("leftdown", tasker)
    move([202, 863, 59, 38],tasker)
    move("leftup",tasker)



# 修改 on_confirm 函数
def on_confirm(tasker, TaskList):
    TaskList.clear()  # 清空TaskList
    for i, var in enumerate(check_vars):
        if var.get():  # 如果勾选框被勾选
            task = [i + 1]
            if i + 1 == 2:  # 刷主页人机直到体力清空
                if manual_entry_var.get():
                    task.append(manual_entry_var.get())  # 添加刷主页人机的输入
                cycle_time = cycle_time_entry.get()  # 获取循环执行时间
                if cycle_time.isdigit():  # 确保是整数
                    task.append(int(cycle_time))  # 添加循环时间
            elif i + 1 == 3:  # 清自动传送门
                task.append(selected_portal_level.get())
            elif i + 1 == 4:  # 手动清传送门（不装卡垫，顶部视角）
                task.append(selected_portal_key.get())
                if manual_portal_input_var.get() is not None:
                    task.append(str(manual_portal_input_var.get()))  # 确保是字符串
                else:
                    task.append(str(0))
            elif i + 1 == 5:  # 刷活动
                task.append(selected_activity_type.get())
            elif i + 1 == 1:  # 清战队任务加战队副本
                # 如果勾选了清战队任务加战队副本，则检查钥匙选项和战队副本选项
                selected_keys = []
                for j, key_var in enumerate(key_vars):
                    if key_var.get():
                        selected_keys.append(j + 1)  # 添加钥匙的序号
                if selected_keys:
                    task.append(selected_keys)  # 将选中的钥匙序号列表添加到任务中
                if clan_copy_var.get():
                    task.append("ClanCopy")  # 添加战队副本选项
            elif i + 1 == 8:  # 自动龙崎迷宫
                # 添加自动龙崎迷宫任务的参数（如果有）
                task.append(maze_floor_var.get())  # 添加龙崎迷宫自动任务的楼层选项
            TaskList.append(task)
    run_start_pipeline(tasker, TaskList)


# 勾选框点击事件处理函数
def on_check_button_click(task_num, var):
    # 这里可以添加勾选框状态改变时的处理逻辑
    pass

# 更新任务列表显示
# update_task_list_display(TaskList)



def run_home_page(tasker):
    # 这里执行 HomePage 任务
    tasker.post_pipeline("HomePage")

def run_Clan(tasker):
    tasker.post_pipeline("FindClan")

def run_PortalsEntry(tasker, portal_level):
    # 这里执行清自动传送门任务
    pipeline_override = {"SelectPortals": {"expected": portal_level}}
    tasker.post_pipeline("PortalsEntry", pipeline_override)

def run_ManualPortalsEntry(tasker, key_type):
    # 这里执行手动清传送门任务
    pipeline_override = {
        "SelectManualPortalsRoleWorld2": {"expected": key_type},
    }
    tasker.post_pipeline("ManualPortalsEntry", pipeline_override)

def run_HomePageReward(tasker):
    # 这里执行领任务任务
    tasker.post_pipeline("HomePageReward")

def run_ActivityEntry(tasker, activity_type):
    # 这里执行刷活动任务
    pipeline_override = {"ActivityEntry": {"next": [activity_type]}}
    tasker.post_pipeline("ActivityEntry", pipeline_override)

# 在窗口左下角添加一个标签，用于显示当前执行的任务名称
current_task_label = tk.Label(root, text="", font=("Arial", 12), fg="black")
# 使用grid布局管理器将标签放置在左下角
current_task_label.grid(row=len(tasks) + 5, column=0, sticky="w")


def update_label():
    global toggle_state, running
    if running:
        if toggle_state:
            current_task_label.config(text=f"   右上角关注up主")
        else:
            current_task_label.config(text=f"   挖矿虽好，可不要贪杯哦")
        toggle_state = not toggle_state
        root.after(10000, update_label)  # 5秒后再次调用 toggle_label 函数

#这里开始执行pipeline任务
def run_start_pipeline(tasker,TaskList):
    pipeline_override = {
        #"HomePageDuelList": {"template": []},
        #"HomePageBot": {"template": []},
        "BatterierEmpty": {"next": []},
        "ShutDownClan2": {"next": []}
    }
    while TaskList:
        TaskNum = TaskList.pop(0)
        current_task_name = tasks[TaskNum[0] - 1]  # 获取当前任务名称
        current_task_label.config(text=f"   挖矿虽好，可不要贪杯哦")  # 更新显示当前任务名称
        root.after(5000, update_label)
        if(TaskNum[0] == 2):
            
            world_name = TaskNum[1]  # 获取世界名称
            cycle_time = TaskNum[2]  # 获取循环执行时间（分钟）
            # 根据世界名称选择对应的图片列表
            i=int(TaskNum[1])
            while i>=0:
                if(i>0):
                    tasker.post_pipeline("NewHomePage",pipeline_override)
                    tasker.post_pipeline("FindDuelBead")
                    i-=1
                else:
                    tasker.post_pipeline("NewHomePage",pipeline_override)
                    i-=1
            while True:
                # 等待循环时间
                time.sleep(cycle_time * 60)  # 转换为秒
                tasker.post_pipeline("HomePage")  # 回到主页
        elif(TaskNum[0] == 1):
            if(len(TaskNum)>1):
                if isinstance(TaskNum[1], list):
                    pipeline_override["ShutDownClan2"]["next"] = ["ClanStoreFind"]
                    tasker.post_pipeline("FindClan",pipeline_override)
                    i = int(len(TaskNum[1]))
                    ClanTaskList = TaskNum[1]
                    while ClanTaskList:
                        ClanStoreTask = ClanTaskList.pop(0)
                        if(ClanStoreTask == 1):
                            pipeline_override = {"SelectKey":{"template":"OrKey.png"}}
                        elif(ClanStoreTask == 2):
                            pipeline_override = {"SelectKey":{"template":"RedKey.png"}}
                        elif(ClanStoreTask == 3):
                            pipeline_override = {"SelectKey":{"template":"GreenKey.png"}}
                        elif(ClanStoreTask == 4):
                            pipeline_override = {"SelectKey":{"template":"WhiteKey.png"}}
                        elif(ClanStoreTask == 5):
                            pipeline_override = {"SelectKey":{"template":"BlackKey.png"}}
                        elif(ClanStoreTask == 6):    
                            pipeline_override = {"SelectKey":{"template":"BlueKey.png"}}
                        elif(ClanStoreTask == 7):
                            pipeline_override = {"SelectKey":{"template":"YellowKey.png"}}
                        tasker.post_pipeline("GotoSelectKey",pipeline_override)
                    tasker.post_pipeline("ReturnClanHome")
                    #tasker.post_pipeline("ClanCopy")
                    if len(TaskNum) == 3:
                        if TaskNum[2] == "ClanCopy":
                            tasker.post_pipeline("ClanCopy")
                    else:
                        tasker.post_pipeline("ReturnClanHome")
                elif(TaskNum[1] == "ClanCopy"):
                    pipeline_override["ShutDownClan2"]["next"] = ["ClanCopy"]
                    tasker.post_pipeline("FindClan",pipeline_override)
            elif(len(TaskNum) == 1):
                pipeline_override["ShutDownClan2"]["next"] = ["ClanCopy"]
                tasker.post_pipeline("FindClan",pipeline_override)
        elif(TaskNum[0] == 3):
            pipeline_override = {"SelectPortals":{"expected":TaskNum[1]}}
            tasker.post_pipeline("PortalsEntry",pipeline_override)
        elif(TaskNum[0] == 4):
            # 定义一个字典来存储name和对应的expected与template值
            data = {
                "迷宫兄弟（绿钥匙）": {"expected": "DM", "template": "迷宫兄弟.png"},
                "天上院明日香（青色钥匙）": {"expected": "GX", "template": "天上院明日香.png"},
                "丸藤翔（黄色钥匙）": {"expected": "GX", "template": "丸藤翔.png"},
                "暗貘良（黑色钥匙）": {"expected": "DM", "template": "暗貘良.png"},
                "帕伽索斯·J·克劳福德（白色钥匙）": {"expected": "DM", "template": "帕伽索斯·J·克劳福德.png"},
                "基斯·霍华德（红色钥匙）": {"expected": "DM", "template": "基斯·霍华德.png"}
            }

            # 初始化Expected和Template变量
            Expected = ""
            Template = ""

            # 使用if-elif-else结构来判断TaskNum[1]并赋值
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
            else:
                print("未找到匹配的name")
            pipeline_override = {
                "SelectManualPortalsWorld2": {"expected": Expected},
                "SelectManualPortalsRole": {"template": Template} # 以前是f"{TaskNum[2]}"
            }
            i = 1
            tasker.post_pipeline("ManualPortalsEntry",pipeline_override)
            while i < int(TaskNum[2]):
                tasker.post_pipeline("ManualPortalsFind2",pipeline_override)
                i+=1

        elif TaskNum[0] == 6:  # 领任务
            Job_Result = tasker.post_pipeline("HomePageReward")
            # if Job_Result.succeeded:
            #     print("任务成功完成")
            #     # 获取任务的详细结果
            #     task_detail = Job_Result.get_task_detail(Job_Result.taskid)
            #     print(task_detail)
            # else:
            #     print("任务未完成或失败")
        elif TaskNum[0] == 5:  # 刷活动
            activity_type = TaskNum[1]  # 获取活动种类
            if (activity_type == "转轮活动"):
                Taskpar = "WheelActivityEntry"
            elif(activity_type == "传送门活动"):
                Taskpar = ""
            elif(activity_type == "骰子活动"):
                Taskpar = "DiceActivityEntry"
            elif(activity_type == "组队决斗活动"):
                Taskpar = "TeamActivityEntry"
            elif(activity_type == "周年庆活动2025（需手动点进活动区域）"):
                Taskpar = "NewYearActivity2025"
            pipeline_override = {
                "ActivityEntry": {"next": Taskpar}
            }
            tasker.post_pipeline("ActivityEntry", pipeline_override)
        elif TaskNum[0] == 7:  # 每日回放
            pipeline_override = {}
            tasker.post_pipeline("VideoReview", pipeline_override)
        elif TaskNum[0] == 8:  # 自动龙崎迷宫
            # 自动龙崎迷宫
            start_floor = TaskNum[1]  # 获取开始楼层
            tasker.post_pipeline("Mazeauto")
            if start_floor == "第一层":
                FirstFloor(tasker)
                SecondFloor(tasker)
                ThirdFloor(tasker)
            if start_floor =="第二层":
                SecondFloor(tasker)
                ThirdFloor(tasker)
            if start_floor =="第三层":
                ThirdFloor(tasker)


def run_OneKeyDaily(tasker, world):
    # 这里执行一键日常任务
    pipeline_override = {
        "ShutDownClan3": {"next": ["PortalsEntry"]},
        "ShutDownClanCopy": {"next": ["PortalsEntry"]},
        "SelectPortals": {"expected": "10级"},
        "PortalsBackToHomePage": {"next": ["HomePage"]},
        "Stop": {"next": ["HomePageReward"]},
    }
    tasker.post_pipeline("FindClan", pipeline_override)

def main():
    user_path = "./"
    Toolkit.init_option(user_path)
    global toggle_state, running
    running = True  # 初始化运行标志
    toggle_state = True  # 初始化切换状态
    
    # # 确保在调用其他功能之前初始化库
    # from maa.library import Library

    # # 假设您的库文件位于当前工作目录的 "lib" 子目录中
    # Library.open("./")  # 调用库的初始化函数

    resource = Resource()
    res_job = resource.post_path("./resource")
    res_job.wait()

    adb_devices = Toolkit.find_adb_devices()
    if not adb_devices:
        print("No ADB device found.")
        exit()

    # for demo, we just use the first device
    device = adb_devices[0]
    controller = AdbController(
        adb_path=device.adb_path,
        address=device.address,
        screencap_methods=device.screencap_methods,
        input_methods=device.input_methods,
        config=device.config,
    )
    controller.post_connection().wait()
    global tasker
    tasker = Tasker()
    # tasker = Tasker(notification_handler=MyNotificationHandler())
    tasker.bind(resource, controller)

    if not tasker.inited:
        print("Failed to init MAA.")
        exit()

    resource.register_custom_recognition("MyRec", MyRecongition())
    # # 创建一个线程来运行 HomePage 任务
    # home_page_thread = threading.Thread(target=run_home_page, args=(tasker,))
    # home_page_thread.start()

    #需要将TaskParameter写入TaskList中，一同传输进函数里
    TaskList = []

    # #创建一个线程来执行Pipeline任务
    # Start_thread = threading.Thread(target=run_start_pipeline, args=(tasker,TaskList))
    
    # 更新确认按钮和停止按钮的行号
    confirm_button_row = current_row + 1
    stop_button_row = current_row + 1

    # 创建确认按钮
    confirm_button = tk.Button(root, text="确认", command=lambda: on_confirm(tasker, TaskList), padx=40,font=("Arial", 12),bg="green",fg="white")
    confirm_button.grid(row=confirm_button_row, column=3, padx=10, pady=10, sticky='ew')

    # 创建停止按钮
    stop_button = tk.Button(root, text="停止", command=lambda: Stop_Button(tasker), font=("Arial", 12),padx=40,bg="red",fg="white")
    stop_button.grid(row=stop_button_row, column=2, padx=10, pady=10, sticky="ew")

    # 创建超链接标签
    link_label = tk.Label(root, text="关注B站翻弄杂鱼卡片的亡灵", font=("Arial", 10), fg="blue", cursor="hand2")
    link_label.grid(row=0, column=3, padx=10, pady=10, sticky='ew')

    # 为标签添加超链接功能
    link_label.bind("<Button-1>", lambda e: open_url("https://space.bilibili.com/3546639744633147"))

    root.mainloop()  # 启动 Tkinter 的主事件循环

    # 等待 HomePage 线程结束
    # home_page_thread.join()
    # do something with task_detail


class MyRecongition(CustomRecognition):

    def analyze(
        self,
        context,
        argv: CustomRecognition.AnalyzeArg,
    ) -> CustomRecognition.AnalyzeResult:
        reco_detail = context.run_recognition(
            "MyCustomOCR",
            argv.image,
            pipeline_override={"MyCustomOCR": {"roi": [100, 100, 200, 300]}},
        )

        # context is a reference, will override the pipeline for whole task
        context.override_pipeline({"MyCustomOCR": {"roi": [1, 1, 114, 514]}})
        # context.run_recognition ...

        # make a new context to override the pipeline, only for itself
        new_context = context.clone()
        new_context.override_pipeline({"MyCustomOCR": {"roi": [100, 200, 300, 400]}})
        reco_detail = new_context.run_recognition("MyCustomOCR", argv.image)

        click_job = context.tasker.controller.post_click(10, 20)
        click_job.wait()

        context.override_next(argv.current_task_name, ["TaskA", "TaskB"])

        return CustomRecognition.AnalyzeResult(
            box=(0, 0, 100, 100), detail="Hello World!"
        )


class MyNotificationHandler(NotificationHandler):
    def on_resource_loading(
        self,
        noti_type: NotificationType,
        detail: NotificationHandler.ResourceLoadingDetail,
    ):
        print(f"on_resource_loading: {noti_type}, {detail}")

    def on_controller_action(
        self,
        noti_type: NotificationType,
        detail: NotificationHandler.ControllerActionDetail,
    ):
        print(f"on_controller_action: {noti_type}, {detail}")

    def on_tasker_task(
        self, noti_type: NotificationType, detail: NotificationHandler.TaskerTaskDetail
    ):
        print(f"on_tasker_task: {noti_type}, {detail}")

    def on_task_next_list(
        self,
        noti_type: NotificationType,
        detail: NotificationHandler.TaskNextListDetail,
    ):
        print(f"on_task_next_list: {noti_type}, {detail}")

    def on_task_recognition(
        self,
        noti_type: NotificationType,
        detail: NotificationHandler.TaskRecognitionDetail,
    ):
        print(f"on_task_recognition: {noti_type}, {detail}")

    def on_task_action(
        self, noti_type: NotificationType, detail: NotificationHandler.TaskActionDetail
    ):
        print(f"on_task_action: {noti_type}, {detail}")


if __name__ == "__main__":
    main()
