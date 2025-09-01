import random
import tkinter as tk
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import math
from matplotlib.font_manager import FontProperties
from matplotlib.patches import Polygon, Circle
import numpy as np
import pathlib

# macOS 专用字体加载
def get_chinese_font():
    try:
        font_path = '/System/Library/Fonts/Hiragino Sans GB.ttc'
        if pathlib.Path(font_path).exists():
            return FontProperties(fname=font_path)
        else:
            print("警告：Hiragino Sans GB 字体不存在，尝试使用 PingFang SC")
            return FontProperties(family='PingFang SC')
    except Exception as e:
        print(f"字体加载失败：{e}，使用默认字体")
        return FontProperties()

# 奖品和颜色（可动态配置，例如添加新奖品）
prizes = ["谢谢参与", "七等奖", "六等奖", "五等奖", "四等奖", "三等奖", "二等奖", "一等奖"]
# 示例：添加新奖品测试通用性
# prizes = ["谢谢参与", "四等奖", "三等奖", "二等奖", "一等奖", "特等奖"]
#colors = ["#FF6666", "#FFCC66", "#66CC66", "#66CCCC", "#9999FF"]
# colors = ["#FF6666", "#FFCC66", "#66CC66", "#66CCCC", "#9999FF", "#FF66FF"]  # 对应添加

# Tk 窗口
root = tk.Tk()
root.title("转盘抽奖")

# 创建画布
fig, ax = plt.subplots(figsize=(5, 5), subplot_kw=dict(aspect="equal"))
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack()

# 全局状态
current_angle = 0
spinning = False
velocity = 0
chinese_font = get_chinese_font()

def draw_pointer(angle):
    """绘制更精致的箭头指针"""
    ax.set_xlim(-1.5, 1.5)
    ax.set_ylim(-1.5, 1.5)

    # 角度转弧度
    rad = math.radians(angle)

    # 箭头长度和宽度
    length = 1.3
    width = 0.1

    # 箭头顶点
    tip_x = length * math.cos(rad)
    tip_y = length * math.sin(rad)

    # 箭头底边两个点（垂直方向偏移）
    left_x = 0.2 * math.cos(rad - math.pi/2)
    left_y = 0.2 * math.sin(rad - math.pi/2)
    right_x = 0.2 * math.cos(rad + math.pi/2)
    right_y = 0.2 * math.sin(rad + math.pi/2)

    # 拼成三角形箭头
    arrow_coords = [
        (tip_x, tip_y),
        (left_x, left_y),
        (right_x, right_y)
    ]
    arrow = Polygon(arrow_coords, closed=True, color="red")
    ax.add_patch(arrow)

    # 中心小圆点（装饰）
    center = Circle((0, 0), 0.05, color="black", zorder=10)
    ax.add_patch(center)

def update_wheel(angle):
    """更新转盘显示"""
    ax.clear()
    wedges, texts = ax.pie(
        [1] * len(prizes),
        labels=prizes,
        startangle=90,  # 从 90 度（12点钟方向）开始逆时针排列
        wedgeprops=dict(edgecolor='white', linewidth=1),
        radius=1.5
    )
    for text in texts:
        text.set_fontproperties(chinese_font)
    draw_pointer(angle)
    canvas.draw()

def animate_spin():
    """动画逻辑"""
    global current_angle, velocity, spinning
    if not spinning:
        return
    
    if velocity > 0.1:  # 减速停止阈值
        current_angle += velocity
        velocity *= 0.98  # 平滑减速
        update_wheel(current_angle)
        root.after(20, animate_spin)
    else:
        spinning = False
        button.config(state="normal")  # 恢复按钮
        # 计算中奖结果（优化逻辑，确保通用性）
        sector_size = 360 / len(prizes)
        pointer_angle = current_angle % 360
        angle_diff = (pointer_angle - 90) % 360
        idx = int(angle_diff // sector_size)  # 修正为 floor division
        print(f"调试：current_angle={current_angle % 360:.2f}, pointer_angle={pointer_angle:.2f}, angle_diff={angle_diff:.2f}, idx={idx}, prize={prizes[idx]}")  # 调试信息
        result_label.config(text=f"抽中的结果是：{prizes[idx]}")

def spin():
    """开始旋转"""
    global spinning, velocity, current_angle
    if spinning:
        return
    spinning = True
    button.config(state="disabled")  # 禁用按钮
    current_angle = 0  # 重置角度
    velocity = random.uniform(20, 30)  # 随机初速度
    animate_spin()

# 按钮
button = tk.Button(root, text="开始抽奖", command=spin, font=("Arial", 14))
button.pack(pady=10)

# 结果显示
result_label = tk.Label(root, text="点击开始抽奖！", font=("Arial", 16))
result_label.pack(pady=10)

# 初始转盘
update_wheel(0)

# 错误处理
try:
    root.mainloop()
except Exception as e:
    print(f"程序运行错误：{e}")