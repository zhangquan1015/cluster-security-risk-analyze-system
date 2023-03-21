import subprocess
import os

current_dir = os.path.dirname(os.path.abspath(__file__))

eval_method = input("请输入要选择的评估方法（BSC 或者 Cost）：")

if eval_method == "BSC":
    # 执行 script_BSC.py
    print("正在执行 BSC 评估方法...")
    # 这里插入执行 script_BSC.py 的代码
    script_path = os.path.join(current_dir, "script_BSC.py")
elif eval_method == "Cost":
    # 执行 script.py
    print("正在执行 Cost 评估方法...")
    # 这里插入执行 script.py 的代码
    script_path = os.path.join(current_dir, "script.py")
else:
    print("无效的评估方法。请输入 BSC 或 Cost。")

subprocess.call(["python3", script_path])