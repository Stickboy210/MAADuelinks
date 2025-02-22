# python -m pip install maafw PyQt5
import sys
import time
from threading import Thread
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QCheckBox, QLabel, QComboBox, QLineEdit, QPushButton,
                             QGroupBox, QScrollArea, QGridLayout, QFrame)
from PyQt5.QtCore import Qt, pyqtSignal, QObject, QTimer
import maa.library
from maa.resource import Resource
from maa.controller import AdbController
from maa.tasker import Tasker
from maa.toolkit import Toolkit

# 原始数据定义
data = {
    "迷宫兄弟（绿钥匙）": {"expected": "DM", "template": "迷宫兄弟.png"},
    "天上院明日香（青色钥匙）": {"expected": "GX", "template": "天上院明日香.png"},
    "丸藤翔（黄色钥匙）": {"expected": "GX", "template": "丸藤翔.png"},
    "暗貘良（黑色钥匙）": {"expected": "DM", "template": "暗貘良.png"},
    "帕伽索斯·J·克劳福德（白色钥匙）": {"expected": "DM", "template": "帕伽索斯·J·克劳福德.png"},
    "基斯·霍华德（红色钥匙）": {"expected": "DM", "template": "基斯·霍华德.png"}
}

tasks = [
    "清战队任务加战队副本",
    "刷主页人机直到体力清空",
    "清自动传送门",
    "手动清传送门（不装卡垫，顶部视角）",
    "刷活动",
    "领任务",
    "每日决斗回放",
    "自动龙崎迷宫"
]

world_options = ["DM世界", "DSOD世界", "GX世界", "5Ds世界", "Z4世界", "A5世界", "V6世界"]
portal_level_options = ["10级", "20级", "30级", "40级"]
activity_type_options = ["转轮活动","骰子活动","组队决斗活动","DD城堡","周年庆活动2025（需手动点进活动区域）"]
portal_key_options = [
    "迷宫兄弟（绿钥匙）", "天上院明日香（青色钥匙）", "丸藤翔（黄色钥匙）",
    "暗貘良（黑色钥匙）", "帕伽索斯·J·克劳福德（白色钥匙）", "基斯·霍华德（红色钥匙）"
]
maze_floor_options = ["第一层", "第二层", "第三层"]

class SignalEmitter(QObject):
    update_status = pyqtSignal(str)
    toggle_buttons = pyqtSignal(bool)
    task_finished = pyqtSignal()

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

class ModernUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.signal = SignalEmitter()
        self.tasker = None
        self.running = False
        self.task_thread = None
        self.init_ui()
        self.init_maa()
        self.setup_connections()

    def init_ui(self):
        self.setWindowTitle("MAADuelinks Pro 4.0")
        self.setGeometry(100, 100, 800, 600)
        self.setStyleSheet("""
            QMainWindow {
                background-color: #000000; /* 设置黑色背景 */
            }
            QGroupBox {
                color: #000000;
                font: bold 12px;
                border: 2px solid #3D3D3D;
                border-radius: 5px;
                margin-top: 10px;
            }
            QCheckBox, QLabel {
                color: #000000;
            }
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
            }
            QPushButton#stopBtn {
                background-color: #F44336;
            }
            QLineEdit, QComboBox {
                background-color: #FFFFFF;
                color: #000000;
                border: 1px solid #3D3D3D;
                padding: 4px;
            }
            QListWidget {
                background-color: #404040;
                color: #FFFFFF;
                border: none;
            }
        """)

        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout(main_widget)

        # 欢迎标题
        title_label = QLabel("欢迎使用MAADuelinks Pro 4.0")
        title_label.setStyleSheet("font: bold 18px; color: #4CAF50;")
        main_layout.addWidget(title_label)

        # 滚动区域
        scroll = QScrollArea()
        content_widget = QWidget()
        scroll.setWidget(content_widget)
        scroll.setWidgetResizable(True)
        main_layout.addWidget(scroll)

        layout = QVBoxLayout(content_widget)

        # 任务组
        task_group = QGroupBox("任务配置")
        task_layout = QVBoxLayout(task_group)
        
        self.checkboxes = []
        self.option_widgets = []

        # 创建任务项
        for i, task in enumerate(tasks):
            cb = QCheckBox(task)
            task_layout.addWidget(cb)
            self.checkboxes.append(cb)
            
            # 添加任务特定选项
            option_widget = QWidget()
            option_layout = QHBoxLayout(option_widget)
            option_layout.setContentsMargins(30, 0, 0, 0)
            
            if task == "刷主页人机直到体力清空":
                option_layout.addWidget(QLabel("使用决斗珠次数："))
                self.duel_beads_input = QLineEdit("0")
                option_layout.addWidget(self.duel_beads_input)
                option_layout.addWidget(QLabel("循环间隔（分钟）："))
                self.cycle_time_input = QLineEdit()
                option_layout.addWidget(self.cycle_time_input)
            elif task == "清自动传送门":
                self.portal_level_combo = QComboBox()
                self.portal_level_combo.addItems(portal_level_options)
                option_layout.addWidget(self.portal_level_combo)
            elif task == "手动清传送门（不装卡垫，顶部视角）":
                self.portal_key_combo = QComboBox()
                self.portal_key_combo.addItems(portal_key_options)
                option_layout.addWidget(self.portal_key_combo)
                option_layout.addWidget(QLabel("手动次数："))
                self.manual_portal_input = QLineEdit()
                option_layout.addWidget(self.manual_portal_input)
            elif task == "刷活动":
                self.activity_type_combo = QComboBox()
                self.activity_type_combo.addItems(activity_type_options)
                option_layout.addWidget(self.activity_type_combo)
                self.reverse_check = QCheckBox("是否反序")
                option_layout.addWidget(self.reverse_check)
            elif task == "清战队任务加战队副本":
                self.key_vars = []
                key_frame = QGroupBox("钥匙选择")
                key_layout = QVBoxLayout(key_frame)
                for j, key_name in enumerate(["普通钥匙", "红钥匙", "绿钥匙", "白钥匙", "黑钥匙", "蓝钥匙", "黄钥匙"]):
                    key_cb = QCheckBox(key_name)
                    key_layout.addWidget(key_cb)
                    self.key_vars.append(key_cb)
                option_layout.addWidget(key_frame)
                self.clan_copy_check = QCheckBox("战队副本")
                option_layout.addWidget(self.clan_copy_check)
            elif task == "自动龙崎迷宫":
                self.maze_floor_combo = QComboBox()
                self.maze_floor_combo.addItems(maze_floor_options)
                option_layout.addWidget(self.maze_floor_combo)
            
            self.option_widgets.append(option_widget)
            task_layout.addWidget(option_widget)
            option_widget.hide()

            # 绑定显示/隐藏选项
            cb.toggled.connect(lambda state, w=option_widget: w.setVisible(state))

        layout.addWidget(task_group)

        # 控制按钮
        btn_layout = QHBoxLayout()
        self.start_btn = QPushButton("开始执行")
        self.start_btn.clicked.connect(self.start_tasks)
        btn_layout.addWidget(self.start_btn)

        self.stop_btn = QPushButton("停止")
        self.stop_btn.setObjectName("stopBtn")
        self.stop_btn.clicked.connect(self.stop_tasks)
        btn_layout.addWidget(self.stop_btn)

        main_layout.addLayout(btn_layout)

        # 状态显示
        self.status_label = QLabel("就绪")
        self.status_label.setStyleSheet("color: #4CAF50; font: bold 12px;")
        main_layout.addWidget(self.status_label)

    def setup_connections(self):
        self.start_btn.clicked.connect(self.start_tasks)
        self.stop_btn.clicked.connect(self.stop_tasks)
        self.signal.update_status.connect(self.statusBar.setText)
        self.signal.toggle_buttons.connect(lambda x: (self.start_btn.setEnabled(not x), self.stop_btn.setEnabled(x)))
        self.signal.task_finished.connect(self.on_task_finished)

        for group, params in self.task_widgets:
            checkbox = group.findChild(QCheckBox)
            if checkbox:
                checkbox.toggled.connect(lambda state, p=params: p.setVisible(state))

    def init_maa(self):
        Toolkit.init_option("./")
        adb_devices = Toolkit.find_adb_devices()
        if not adb_devices:
            self.signal.update_status.emit("未找到ADB设备!")
            return

        device = adb_devices[0]
        self.controller = AdbController(
            adb_path=device.adb_path,
            address=device.address,
            screencap_methods=device.screencap_methods,
            config=device.config
        )
        self.controller.post_connection().wait()

        self.resource = Resource()
        self.resource.post_path("./resource").wait()

        self.tasker = Tasker()
        self.tasker.bind(self.resource, self.controller)

    def start_tasks(self):
        if not self.running and self.tasker:
            self.running = True
            self.signal.toggle_buttons.emit(True)
            self.task_thread = Thread(target=self.run_tasks)
            self.task_thread.start()

    def stop_tasks(self):
        if self.running:
            self.running = False
            self.tasker.post_stop()
            self.signal.update_status.emit("正在停止...")

    def on_task_finished(self):
        self.running = False
        self.signal.toggle_buttons.emit(False)
        self.signal.update_status.emit("任务完成")

    def collect_tasks(self):
        task_list = []
        for i, (group, _) in enumerate(self.task_widgets):
            checkbox = group.findChild(QCheckBox)
            if checkbox and checkbox.isChecked():
                task = [i+1]
                if i+1 == 2:  # 刷主页人机
                    task.append(int(self.beads_input.text()))
                    task.append(int(self.cycle_input.text()) if self.cycle_input.text() else 0)
                elif i+1 == 3:  # 清自动传送门
                    task.append(self.portal_level.currentText())
                elif i+1 == 4:  # 手动传送门
                    task.append(self.portal_key.currentText())
                    task.append(int(self.manual_count.text()))
                elif i+1 == 5:  # 刷活动
                    task.append(self.activity_type.currentText())
                    task.append(self.reverse_check.isChecked())
                elif i+1 == 1:  # 战队任务
                    keys = [j+1 for j, cb in enumerate(self.key_checks) if cb.isChecked()]
                    if keys: task.append(keys)
                    if self.clan_copy_check.isChecked(): task.append("ClanCopy")
                elif i+1 == 8:  # 迷宫
                    task.append(self.maze_floor.currentText())
                task_list.append(task)
        return task_list

    def run_tasks(self):
        task_list = self.collect_tasks()
        pipeline_override = {
            "BatterierEmpty": {"next": []},
            "ShutDownClan2": {"next": []}
        }
        while task_list and self.running:
            task = task_list.pop(0)
            self.signal.update_status.emit(f"执行中: {tasks[task[0]-1]}")
            
            try:
                if task[0] == 2:  # 主页人机
                    beads = task[1]
                    cycle = task[2]
                    # 原始执行逻辑...
                    i=int(beads)
                    while i>=0:
                        if(i>0):
                            self.tasker.post_pipeline("NewHomePage",pipeline_override)
                            self.tasker.post_pipeline("FindDuelBead")
                            i-=1
                        else:
                            self.tasker.post_pipeline("NewHomePage",pipeline_override)
                            i-=1
                elif task[0] == 1: #战队副本
                    if(len(task)>1):
                        if isinstance(task[1], list):
                            pipeline_override["ShutDownClan2"]["next"] = ["ClanStoreFind"]
                            self.tasker.post_pipeline("FindClan",pipeline_override)
                            i = int(len(task[1]))
                            ClanTaskList = task[1]
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
                                self.tasker.post_pipeline("GotoSelectKey",pipeline_override)
                            self.tasker.post_pipeline("ReturnClanHome")
                            #tasker.post_pipeline("ClanCopy")
                            if len(task) == 3:
                                if task[2] == "ClanCopy":
                                    self.tasker.post_pipeline("ClanCopy")
                            else:
                                self.tasker.post_pipeline("ReturnClanHome")
                        elif(task[1] == "ClanCopy"):
                            pipeline_override["ShutDownClan2"]["next"] = ["ClanCopy"]
                            self.tasker.post_pipeline("FindClan",pipeline_override)
                    elif(len(task) == 1):
                        pipeline_override["ShutDownClan2"]["next"] = ["ClanCopy"]
                        self.tasker.post_pipeline("FindClan",pipeline_override)
                elif task[0] == 3:  # 自动传送门
                    level = task[1]
                    # 执行传送门逻辑...
                    pipeline_override = {"SelectPortals":{"expected":task[1]}}
                    self.tasker.post_pipeline("PortalsEntry",pipeline_override)
                elif task[0] == 4: 
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

                    # 使用if-elif-else结构来判断task[1]并赋值
                    if task[1] == "迷宫兄弟（绿钥匙）":
                        Expected = data["迷宫兄弟（绿钥匙）"]["expected"]
                        Template = data["迷宫兄弟（绿钥匙）"]["template"]
                    elif task[1] == "天上院明日香（青色钥匙）":
                        Expected = data["天上院明日香（青色钥匙）"]["expected"]
                        Template = data["天上院明日香（青色钥匙）"]["template"]
                    elif task[1] == "丸藤翔（黄色钥匙）":
                        Expected = data["丸藤翔（黄色钥匙）"]["expected"]
                        Template = data["丸藤翔（黄色钥匙）"]["template"]
                    elif task[1] == "暗貘良（黑色钥匙）":
                        Expected = data["暗貘良（黑色钥匙）"]["expected"]
                        Template = data["暗貘良（黑色钥匙）"]["template"]
                    elif task[1] == "帕伽索斯·J·克劳福德（白色钥匙）":
                        Expected = data["帕伽索斯·J·克劳福德（白色钥匙）"]["expected"]
                        Template = data["帕伽索斯·J·克劳福德（白色钥匙）"]["template"]
                    elif task[1] == "基斯·霍华德（红色钥匙）":
                        Expected = data["基斯·霍华德（红色钥匙）"]["expected"]
                        Template = data["基斯·霍华德（红色钥匙）"]["template"]
                    else:
                        print("未找到匹配的name")
                    pipeline_override = {
                        "SelectManualPortalsWorld2": {"expected": Expected},
                        "SelectManualPortalsRole": {"template": Template} # 以前是f"{task[2]}"
                    }
                    i = 1
                    self.tasker.post_pipeline("ManualPortalsEntry",pipeline_override)
                    while i < int(task[2]):
                        self.tasker.post_pipeline("ManualPortalsFind2",pipeline_override)
                        i+=1

                elif task[0] == 5:
                    activity_type = task[1]  # 获取活动种类
                    if(len(task)>2):
                        reverse_order = task[2]
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
                    elif(activity_type == "DD城堡"):
                        Taskpar = "DDActivityEntry"
                    if activity_type == "DD城堡" and reverse_order:
                        pipeline_override = {
                            "StartDDActivity":{"index": -1},
                            "ActivityEntry": {"next": Taskpar}
                        }
                    else:
                        pipeline_override = {
                            "ActivityEntry": {"next": Taskpar}
                        }
                    self.tasker.post_pipeline("ActivityEntry", pipeline_override)
                elif task[0] == 6:
                    Job_Result = self.tasker.post_pipeline("HomePageReward")
                elif task[0] == 7:
                    self.tasker.post_pipeline("VideoReview", pipeline_override)
                elif task[0] == 8:
                    start_floor = task[1]
                    self.tasker.post_pipeline("Mazeauto")
                    if start_floor == "第一层":
                        FirstFloor(self.tasker)
                        SecondFloor(self.tasker)
                        ThirdFloor(self.tasker)
                    if start_floor =="第二层":
                        SecondFloor(self.tasker)
                        ThirdFloor(self.tasker)
                    if start_floor =="第三层":
                        ThirdFloor(self.tasker)
                # 其他任务分支处理...

                time.sleep(1)  # 模拟任务执行
            except Exception as e:
                self.signal.update_status.emit(f"错误: {str(e)}")
                break

        self.signal.task_finished.emit()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ModernUI()
    window.show()
    sys.exit(app.exec_())