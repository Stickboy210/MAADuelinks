import PyInstaller.__main__
import os
import sys

def build():
    # 定义图标文件路径
    icon_path = os.path.abspath("heart.ico")
    
    # 检查图标文件是否存在
    if not os.path.exists(icon_path):
        print(f"Error: Icon file '{icon_path}' not found.")
        sys.exit(1)
    else :
        print(f"Icon file '{icon_path}' found.")
    
    # # 定义打包命令
    # command = f"pyinstaller --onefile --noconsole --icon={icon_path} show_my_heart.py"
    
    # 打印正在执行的命令
    # print(f"Executing command: {command}")
    
    # 运行 PyInstaller
    PyInstaller.__main__.run([
        'show_my_heart.py',
        '--onefile',
        '--noconsole',
        '--name=show_my_heart',
        f'--icon={icon_path}',  # 添加图标参数
    ])


    print("Build completed. Check the 'dist' folder for the executable.")

if __name__ == "__main__":
    build()