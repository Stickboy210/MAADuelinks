# python -m pip install maafw
from maa.resource import Resource
from maa.controller import AdbController
from maa.tasker import Tasker
from maa.toolkit import Toolkit

from maa.custom_recognition import CustomRecognition
from maa.custom_action import CustomAction
from maa.notification_handler import NotificationHandler, NotificationType

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
root.title("任务勾选框")

# 创建欢迎标签
welcome_label = tk.Label(root, text="欢迎使用MAADuelinks！", font=("Arial", 16), fg="black")
welcome_label.grid(row=0, column=0, columnspan=4, pady=10, sticky="ew")


# 根据您提供的顺序重新排列任务名称
tasks = [
    "清战队任务加战队副本",
    "刷主页人机直到体力清空",
    "清自动传送门",
    "手动清传送门（不装卡垫，顶部视角）",
    "刷活动",
    "领任务"
]

# 世界选项
world_options = [
    "DM世界", "DSOD世界", "GX世界", "5Ds世界", "Z4世界", "A5世界", "V6世界"
]

# 传送门等级选项
portal_level_options = ["10级", "20级", "30级", "40级"]

# 活动种类选项
activity_type_options = ["转轮活动"]

# 传送门钥匙种类选项
portal_key_options = [
    "迷宫兄弟（绿钥匙）", "天上院明日香（青色钥匙）", "丸藤翔（黄色钥匙）",
    "暗貘良（黑色钥匙）", "帕伽索斯·J·克劳福德（白色钥匙）", "基斯·霍华德（红色钥匙）"
]

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


# 创建输入框对应的变量
manual_entry_var = tk.StringVar(root)  # 刷主页人机直到体力清空的输入框变量
manual_entry_var.set(0) #默认不使用决斗珠

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
    tasker.post_stop()

# 创建打印任务列表按钮
# print_task_list_button = tk.Button(root, text="打印任务列表", command=print_task_list)
# print_task_list_button.grid(row=len(tasks) + 5, column=0, padx=10, pady=5, sticky='ew')


# 创建勾选框并使用grid布局管理器进行布局
for i, task_name in enumerate(tasks, start=1):
    var = tk.BooleanVar()
    check_button = tk.Checkbutton(root, text=task_name, variable=var)
    check_button.grid(row=i, column=0, sticky="w", padx=10, pady=5)
    
    check_vars.append(var)
    
    # 为每个任务创建附加选项
    if task_name == "刷主页人机直到体力清空":
        world_menu = tk.OptionMenu(root, selected_world, *world_options)
        world_menu.grid(row=i, column=1, padx=10, pady=5, sticky='ew')
        tk.Label(root, text="使用决斗珠次数：").grid(row=i, column=2, sticky="e")  # 添加输入框标签
        manual_entry = tk.Entry(root, textvariable=manual_entry_var)
        manual_entry.grid(row=i, column=3, padx=10, pady=5, sticky='ew')
    elif task_name == "清自动传送门":
        portal_level_menu = tk.OptionMenu(root, selected_portal_level, *portal_level_options)
        portal_level_menu.grid(row=i, column=1, padx=10, pady=5, sticky='ew')
    elif task_name == "手动清传送门（不装卡垫，顶部视角）":
        portal_key_menu = tk.OptionMenu(root, selected_portal_key, *portal_key_options)
        portal_key_menu.grid(row=i, column=1, padx=10, pady=5, sticky='ew')
        tk.Label(root, text="手动次数：").grid(row=i, column=2, sticky="e")  # 添加输入框标签
        manual_portal_entry = tk.Entry(root, textvariable=manual_portal_input_var)
        manual_portal_entry.grid(row=i, column=3, padx=10, pady=5, sticky='ew')
    elif task_name == "刷活动":
        activity_type_menu = tk.OptionMenu(root, selected_activity_type, *activity_type_options)
        activity_type_menu.grid(row=i, column=1, padx=10, pady=5, sticky='ew')

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



# 确认按钮事件处理函数
def on_confirm(tasker,TaskList):
    TaskList.clear()  # 清空TaskList
    for i, var in enumerate(check_vars):
        if var.get():  # 如果勾选框被勾选
            task = [i + 1]
            if i + 1 == 2 and selected_world.get():
                task.append(selected_world.get())
                if manual_entry_var.get():
                    task.append(manual_entry_var.get())  # 添加刷主页人机的输入
            if i + 1 == 3 and selected_portal_level.get():
                task.append(selected_portal_level.get())
            if i + 1 == 4:
                task.append(selected_portal_key.get())
                if manual_portal_input_var.get() is not None:
                    task.append(str(manual_portal_input_var.get()))  # 确保是字符串
                else:
                    task.append(str(0))
            if i + 1 == 5 and selected_activity_type.get():
                task.append(selected_activity_type.get())
            TaskList.append(task)
    run_start_pipeline(tasker,TaskList)
    #update_task_list_display(TaskList)  # 更新显示



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

def on_task_completed(task_name):
    # 这个函数在任务完成后被调用，用于更新UI
    current_task_label.config(text=f"任务 {task_name} 执行完毕")

#这里开始执行pipeline任务
def run_start_pipeline(tasker,TaskList):
    pipeline_override = {
        "HomePageDuelList": {"template": []},
        "HomePageBot": {"template": []},
        "BatterierEmpty": {"next": []}
    }
    while TaskList:
        TaskNum = TaskList.pop(0)
        current_task_name = tasks[TaskNum[0] - 1]  # 获取当前任务名称
        current_task_label.config(text=f"当前执行的任务: {current_task_name}")  # 更新显示当前任务名称
        if(TaskNum[0] == 2):
            
            world_name = TaskNum[1]  # 获取世界名称
            # 根据世界名称选择对应的图片列表
            if world_name == "DM世界":
                pipeline_override["HomePageDuelList"]["template"] = [
                    "伊西斯·伊修达尔.png",
                    "光与暗之假面.png",
                    "利希德.png",
                    "城之内克也.png",
                    "基斯·霍华德.png",
                    "天才吕场.png",
                    "孔雀舞.png",
                    "帕伽索斯·J·克劳福德.png",
                    "御伽龙儿.png",
                    "恐龙龙崎.png",
                    "昆虫羽蛾.png",
                    "暗游戏.png",
                    "暗貘良.png",
                    "暗马利克.png",
                    "梶木渔太.png",
                    "武藤游戏.png",
                    "海马圭平.png",
                    "海马濑人.png",
                    "潘多拉.png",
                    "真崎杏子.png",
                    "迷宫兄弟.png",
                    "鬼谷冢.png"
                ]
                pipeline_override["HomePageBot"]["template"] = [
                    "Bot8.png",
                    "Bot11.png",
                    "Bot13.png",
                    "Bot9.png",
                    "Bot5.png",
                    "Bot4.png",
                    "Bot17.png",
                    "Bot15.png",
                    "Bot16.png",
                    "Bot17.png",
                    "Bot18.png",
                    "Bot19.png",
                    "Bot20.png",
                    "Bot21.png",
                    "Bot14.png",
                    "Bot2.png"
                ]
            elif world_name == "DSOD世界":
                pipeline_override["HomePageDuelList"]["template"] = [
                    "海马濑人（DSOD）.png",
                    "海马圭平（DSOD）.png",
                    "武藤游戏（DSOD）.png",
                    "真崎杏子（DSOD）.png",
                    "塞拉.png"
                ]
                pipeline_override["HomePageBot"]["template"] = [
                    "Bot1.png",
                    "Bot11.png",
                    "Bot8.png",
                    "Bot5.png",
                    "Bot15.png",
                    "Bot19.png",
                    "Bot13.png",
                    "Bot9.png",
                    "Bot16.png",
                    "Bot21.png",
                    "Bot14.png",
                    "Bot17.png",
                    "Bot4.png"
                ]
            elif world_name == "GX世界":
                pipeline_override["HomePageDuelList"]["template"] = [
                    "万丈目准.png",
                    "三则大地.png",
                    "丸藤翔.png",
                    "凯撒亮.png",
                    "吉姆·克劳戴尔·库克.png",
                    "天上院明日香.png",
                    "尤贝尔.png",
                    "尤贝尔十代.png",
                    "库洛诺斯·德·梅迪契.png",
                    "斋王琢磨.png",
                    "早乙女礼.png",
                    "游城十代.png",
                    "约翰·安德森.png",
                    "艾德·菲尼克斯.png",
                    "迪拉诺剑山.png",
                    "霸王.png"
                ]
                pipeline_override["HomePageBot"]["template"] = [
                    "Bot8.png",
                    "Bot16.png",
                    "Bot11.png",
                    "Bot13.png",
                    "Bot9.png",
                    "Bot5.png",
                    "Bot4.png",
                    "Bot17.png",
                    "Bot22.png",
                    "Bot23.png",
                    "Bot24.png",
                    "Bot25.png",
                    "Bot26.png",
                    "Bot39.png"
                ]
            elif world_name == "5Ds世界":
                pipeline_override["HomePageDuelList"]["template"] = [
                    "不动游星.png",
                    "杰克·亚特拉斯.png",
                    "乌鸦·霍根.png",
                    "十六夜亚纪.png",
                    "龙亚.png",
                    "龙可.png",
                    "卡利渚.png",
                    "暗印者鬼柳京介.png",
                    "暗印者卡利渚.png",
                    "暗印者雷克斯·戈德温.png",
                    "帕拉多格斯.png",
                    "普拉西多.png",
                    "安提诺米.png"
                ]
                pipeline_override["HomePageBot"]["template"] = [
                    "Bot1.png",
                    "Bot2.png",
                    "Bot3.png",
                    "Bot4.png",
                    "Bot5.png",
                    "Bot6.png",
                    "Bot7.png",
                    "Bot8.png",
                    "Bot9.png",
                    "Bot10.png",
                    "Bot11.png",
                    "Bot12.png",
                    "Bot16.png",
                    "Bot13.png",
                    "Bot17.png"
                ]
            elif world_name == "Z4世界":
                pipeline_override["HomePageDuelList"]["template"] = [
                    "Ⅲ.png",
                    "Ⅳ.png",
                    "天城快斗.png",
                    "武田铁男.png",
                    "游马和星光体.png",
                    "神代凌牙.png",
                    "神代璃绪.png",
                    "神月安奈.png",
                    "观月小鸟.png"
                ]
                pipeline_override["HomePageBot"]["template"] = [
                    "Bot8.png",
                    "Bot16.png",
                    "Bot11.png",
                    "Bot13.png",
                    "Bot9.png",
                    "Bot5.png",
                    "Bot4.png",
                    "Bot17.png",
                    "Bot21.png",
                    "Bot27.png",
                    "Bot28.png",
                    "Bot29.png",
                    "Bot30.png"
                ]
            elif world_name == "A5世界":
                pipeline_override["HomePageDuelList"]["template"] = [
                    "塞瑞娜.png",
                    "权现坂升.png",
                    "柊柚子.png",
                    "榊游矢.png",
                    "泽渡慎吾.png",
                    "游斗.png",
                    "赤马零儿.png",
                    "黑咲隼.png"
                ]
                pipeline_override["HomePageBot"]["template"] = [
                    "Bot8.png",
                    "Bot16.png",
                    "Bot11.png",
                    "Bot13.png",
                    "Bot9.png",
                    "Bot5.png",
                    "Bot4.png",
                    "Bot17.png",
                    "Bot31.png",
                    "Bot32.png",
                    "Bot33.png",
                    "Bot34.png"
                ]
            elif world_name == "V6世界":
                pipeline_override["HomePageDuelList"]["template"] = [
                    "Go鬼塚.png",
                    "Playnaker和Ai.png",
                    "左轮.png",
                    "焚魂烈火.png",
                    "蓝色天使.png"
                ]
                pipeline_override["HomePageBot"]["template"] = [
                    "Bot8.png",
                    "Bot16.png",
                    "Bot11.png",
                    "Bot13.png",
                    "Bot9.png",
                    "Bot5.png",
                    "Bot4.png",
                    "Bot17.png",
                    "Bot35.png",
                    "Bot36.png",
                    "Bot37.png",
                    "Bot38.png"
                ]
            if(int(TaskNum[2])>0):
                pipeline_override["BatterierEmpty"]["next"] = ["FindDuelBead"]
            i=int(TaskNum[2])
            while i>=0:
                if(i>0):
                    tasker.post_pipeline("HomePage",pipeline_override)
                    i-=1
                else:
                    pipeline_override["BatterierEmpty"]["next"] = ["Stop"]
                    tasker.post_pipeline("HomePage",pipeline_override)
                    i-=1
        elif(TaskNum[0] == 1):
            tasker.post_pipeline("FindClan")
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
                "SelectManualPortalsRoleWorld2": {"expected": Expected},
                "SelectManualPortalsRole": {"template": Template} # 以前是f"{TaskNum[2]}"
            }
            i = 1
            tasker.post_pipeline("ManualPortalsEntry",pipeline_override)
            while i < int(TaskNum[2]):
                tasker.post_pipeline("ManualPortalsFind2",pipeline_override)
                i+=1

        elif TaskNum[0] == 6:  # 领任务
            tasker.post_pipeline("HomePageReward")
        elif TaskNum[0] == 5:  # 刷活动
            activity_type = TaskNum[1]  # 获取活动种类
            if (activity_type == "转轮活动"):
                Taskpar = "WheelActivityEntry"
            pipeline_override = {
                "ActivityEntry": {"next": Taskpar}
            }
            tasker.post_pipeline("ActivityEntry", pipeline_override)
        elif TaskNum[0] == 7:  # 一键日常
            pipeline_override = {
                "ShutDownClan3": {"next": ["PortalsEntry"]},
                "ShutDownClanCopy": {"next": ["PortalsEntry"]},
                "SelectPortals": {"expected": "10级"},
                "PortalsBackToHomePage": {"next": ["HomePage"]},
                "Stop": {"next": ["HomePageReward"]}
            }
            tasker.post_pipeline("FindClan", pipeline_override)


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
    
    # 创建确认按钮
    confirm_button = tk.Button(root, text="确认", command=lambda: on_confirm(tasker, TaskList), padx=40,font=("Arial", 12),bg="green",fg="white")
    confirm_button.grid(row=len(tasks) + 5, column=3, padx=10, pady=10, sticky='ew')
        
    # 创建停止按钮
    stop_button = tk.Button(root, text="停止", command=lambda: Stop_Button(tasker), font=("Arial", 12),padx=40,bg="red",fg="white")
    stop_button.grid(row=len(tasks) + 5, column=2, padx=10, pady=10, sticky="ew")



    #root.protocol("WM_DELETE_WINDOW", lambda: Stop_Button(tasker))
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
