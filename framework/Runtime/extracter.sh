cd ..
EXTRACTER_PATH=$PWD"/Extracter"
# 提取漏洞特征（漏洞特征）
echo "准备提取漏洞特征（漏洞特征）"
cd $EXTRACTER_PATH
python3 run.py
