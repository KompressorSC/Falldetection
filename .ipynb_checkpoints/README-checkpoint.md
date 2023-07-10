## Falldetection_Group_2
# 更新
更换数据集为自己制作的版本，并用不同的lr下降率分别训练了三次，每次100个epoch。之前模型的召回率不高疑似过拟合导致。

# 安装
1、安装anaconda(推荐)或者python

https://www.anaconda.com/

https://www.python.org/

2、安装pytorch框架

https://pytorch.org/

3、安装yolov8
***
pip install ultralytics
***
# 运行
1、在当前路径打开命令行

2、训练
***
yolo cfg=train.yaml
***
3、验证
***
yolo cfg=val.yaml
***
# 查看结果
结果存于当前目录的results下

