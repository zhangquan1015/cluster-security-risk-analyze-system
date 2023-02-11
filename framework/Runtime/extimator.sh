cd ..
ESTIMATOR_PATH=$PWD"/Estimator"

# 评估集群漏洞
echo "准备进行集群风险分析"
cd $ESTIMATOR_PATH
python3 run.py
