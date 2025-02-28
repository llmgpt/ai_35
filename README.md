一些常用命令的汇总：
1.查看cuda版本
nvidia-smi
-监测GPU利用率,每5s
nvidia-smi -l

2.环境准备
conda create -n torch110 python=3.9
conda activate torch110
conda list torch
conda info --envs
conda remove -n torch110 --all

3.安装torch
pip install torch==1.10.0+cu113 torchvision==0.11.1+cu113 torchaudio==0.10.0+cu113 -f https://download.pytorch.org/whl/cu113/torch_stable.html
pip install torch==1.10.1+cu102 torchvision==0.11.2+cu102 torchaudio==0.10.1 -f https://download.pytorch.org/whl/cu102/torch_stable.html
conda install pytorch==1.10.0 torchvision==0.11.0 torchaudio==0.10.0 cudatoolkit=11.3

4.检查cuda是否可用
torch.cuda.is_available()

5.清华源
https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/pytorch/win-64/

6.conda换源
conda config --show channels  # 查看当前的channels
conda config --remove-key channels  # 恢复conda的官方默认源
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main # 添加清华源的四个通道
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/r
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/pytorch/

7.一次换清华源
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple matplotlib==3.5.2
pip install -i https://mirrors.aliyun.com/pypi/simple/ opencv-python==4.5.5.64

8.pip换源
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple

1.tensorboard载入权重
tensorboard --logdir=F:\workspace\ai_course\ai_35\day25_2\logs

2.git操作
-移除git跟踪，实现commit时不显示该文件夹(下面是强删)
git rm --cached -r day46/weights
git rm --cached -r -f day55/weights
-提交git跟踪
git commit -m "添加文件夹"
-使用.gitignore进行忽略，但要求是没有在commit中进行缓存
-本地项目克隆到gitee仓库
git init（初始化）
git remote add origin 仓库地址 （将远程代码仓库与本地仓库关联起来。"origin" 是一个远程仓库的别名）
git pull origin master （从远程仓库（origin）的主分支（master）拉取最新的代码更新到本地仓库,如果远程仓库有readme删除即可，保存空文件情况）
git add . （将当前目录下的所有文件和文件夹的更改添加到 Git 的暂存区）
git commit -m “XX” （将暂存区中的更改提交到 Git 仓库的版本历史记录中。"-m" 参数后面的 "XX" 是提交的消息或注释）
git push origin master （将本地仓库的更改推送到远程仓库（origin）的主分支（master））
-本地项目克隆到gitee仓库（简洁版）
git init # 初始化
git remote add origin https://gitee.com/wzhang-sanfeng/use_-yolov5_face.git # 本地仓库和云端仓库相连（创建仓库时不要新建任何东西）

3.运行过程中的问题
AttributeError: module 'distutils' has no attribute 'version'
pip install setuptools==59.5.0 -i https://pypi.tuna.tsinghua.edu.cn/simple
pip install setuptools==65.5.1 -i https://pypi.tuna.tsinghua.edu.cn/simple
CUDA_LAUNCH_BLOCKING=1
import os
os.environ["CUDA_VISIBLE_DEVICES"] = "1" # 当线程没有主函数支持时

4.标注分割
labelme

5.标注的分割json转化为yolo格式
labelme2yolo --json_dir path/json --val_size 0.1 --test_size 0.1

6.使用Jupyter Notebook
activate 环境名
pip install ipykernel
python -m ipykernel install --user --name 环境名 --display-name 环境名

7.pyqtui设计
anaconda3\Library\bin\designer.exe

8.安装tensorrt，先安装cuda，再安装cudnn，还需要安装pycuda,安装在base环境中
https://blog.csdn.net/m0_45447650/article/details/123704930
https://blog.csdn.net/KRISNAT/article/details/130789078
trtexec --onnx=sr.onnx --saveEngine=sr16.engine --fp16=True #转换成部署模型并量化

9.使用docker和代理和ssh
sudo docker run -it --shm-size=10g --gpus=all -v /usr/bin/docker/study_sl -p 40010:22 -p 40011:40011 -p 40012:40012 -p 40013:40013 --name study_sl nvidia/cuda:11.8.0-devel-ubuntu22.04
(--shm-size=10g ——> 共享内存设置成10G)
docker exec -it study_sl /bin/bash
passwd
conda activate py310
source /etc/profile.d/clash.sh #
proxy_off # 关闭代理
proxy_on
os.environ["CUDA_VISIBLE_DEVICES"] = "0"
vim /etc/ssh/sshd_config
service ssh restart
service ssh status

10. Jupyter notebook切换环境
pip install ipykernel
python -m ipykernel install --name yolov8
