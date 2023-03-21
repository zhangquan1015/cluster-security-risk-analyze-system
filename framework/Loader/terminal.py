import os

# 删除非空路径
def remove_dir(dir):
    dir = dir.replace('\\', '/')
    if(os.path.isdir(dir)):
        for p in os.listdir(dir):
            remove_dir(os.path.join(dir,p))
        if(os.path.exists(dir)):
            os.rmdir(dir)
    else:
        if(os.path.exists(dir)):
            os.remove(dir)
# 初始化文件夹
def existsHelper(path):
    if os.path.exists(path):
        remove_dir(path)
    os.mkdir(path)