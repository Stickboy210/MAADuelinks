import sys
import random
import math
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QFont, QPainter, QColor, QPen
from PyQt5.QtCore import Qt, QTimer, QRect

class HeartRateDisplay(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.start_heart_rate_simulation()
        self.is_dragging = False
        self.offset = None
        self.forced_adjust_count = 0  # 用于强制调整的计数器
        self.close_button_visible = False  # 关闭按钮是否可见
        self.close_button_timer = QTimer(self)  # 关闭按钮计时器
        self.close_button_timer.timeout.connect(self.hide_close_button)
        self.close_button_timer.setSingleShot(True)  # 设置为单次触发

    def init_ui(self):
        # 设置窗口透明
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)

        # 设置字体和初始心率值
        self.setFont(QFont("Arial", 24))
        self.heart_rate = random.randint(75, 83)  # 初始心率

        # 设置窗口大小
        self.setFixedSize(200, 70)

    def paintEvent(self, event):
        # 绘制爱心和心率数字
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # 绘制爱心
        painter.setPen(QPen(QColor(255, 0, 0)))  # 红色
        painter.drawText(QRect(10, 10, 50, 50), Qt.AlignCenter, "❤")

        # 绘制心率数字
        painter.setPen(QPen(QColor(0, 0, 0)))  # 黑色
        painter.drawText(QRect(60, 10, 130, 50), Qt.AlignLeft | Qt.AlignVCenter, str(self.heart_rate))

        # 绘制关闭按钮（如果可见）
        if self.close_button_visible:
            painter.setPen(QPen(QColor(255, 255, 255)))  # 白色
            painter.drawText(QRect(170, 10, 20, 20), Qt.AlignCenter, "X")

    def start_heart_rate_simulation(self):
        # 启动定时器
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_heart_rate)
        self.timer.start()

    def update_heart_rate(self):
        # 计算时间间隔
        interval = random.uniform(1.5, 2.5)
        self.timer.setInterval(int(interval * 1000))  # 转换为毫秒

        # 检查是否需要强制调整
        if self.forced_adjust_count > 0:
            if self.heart_rate == 66:
                self.heart_rate += 1
            elif self.heart_rate == 92:
                self.heart_rate -= 1
            self.forced_adjust_count -= 1
        else:
            # 计算心率变化
            change = self.calculate_change_probability(self.heart_rate)
            if random.random() < change:
                self.heart_rate += 1
            else:
                self.heart_rate -= 1

            # 检查是否触碰边界
            if self.heart_rate == 66 or self.heart_rate == 92:
                self.forced_adjust_count = 3  # 触碰边界后强制调整3次

        # 限制心率范围
        self.heart_rate = max(66, min(self.heart_rate, 92))

        # 更新显示
        self.update()

    def calculate_change_probability(self, heart_rate):
        """
        使用Sigmoid函数计算心率变化的概率
        当心率在75到85之间时，以0.5的概率增加或减少
        当心率在75到85之外时，越远离这个范围，概率越高地向75到85调整
        """
        # 当心率在75到85之间时，概率为0.5
        if 75 <= heart_rate <= 85:
            return 0.5
        else:
            # 计算心率与目标范围中心的偏差
            center = 80
            deviation = heart_rate - center

            # 使用Sigmoid函数计算概率
            k = 0.2  # 调整参数，控制Sigmoid曲线的陡峭程度
            sigmoid_value = 1 / (1 + math.exp(-k * deviation))

            # 当心率高于85时，概率向减少方向倾斜
            # 当心率低于75时，概率向增加方向倾斜
            if heart_rate > 85:
                return 1 - sigmoid_value
            else:
                return sigmoid_value

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            # 检查是否点击了关闭按钮
            if self.close_button_visible and QRect(170, 10, 20, 20).contains(event.pos()):
                self.close()
            else:
                self.is_dragging = True
                self.offset = event.globalPos() - self.pos()

    def mouseMoveEvent(self, event):
        if self.is_dragging:
            self.move(event.globalPos() - self.offset)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.is_dragging = False

    def enterEvent(self, event):
        # 鼠标进入窗口时显示关闭按钮
        self.close_button_visible = True
        self.update()
        # 如果计时器已经启动，则停止并重新启动
        if self.close_button_timer.isActive():
            self.close_button_timer.stop()
        self.close_button_timer.start(1000)  # 1秒后隐藏

    def leaveEvent(self, event):
        # 鼠标离开窗口时不立即隐藏关闭按钮
        pass

    def hide_close_button(self):
        # 隐藏关闭按钮
        self.close_button_visible = False
        self.update()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    display = HeartRateDisplay()
    display.show()
    sys.exit(app.exec_())