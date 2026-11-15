# 环境、数据与复现

[返回主线](../system_identification_learning_plan.md)

用户已选择：**MATLAB 完成 SSY230 原生项目，Python 用于补充练习。** 不要求把同一算法重复实现两遍。

## MATLAB 主路线

P1/P2 的回归、递推、滤波和绘图可用 MATLAB 基础功能自己实现。P3 原题的 GUI、iddata/arx/oe/n4sid 等现成估计命令需要 System Identification Toolbox；Simulink 只在自适应控制选修中使用。非线性优化可用有相应许可证的优化工具箱，或 Python/SciPy。

本次没有替你运行 MATLAB、核验许可证或执行原生项目答案。第一周在 MATLAB 运行：

~~~matlab
version
ver
which polyfit -all
~~~

为自己的代码建立 submissions/A1 等目录，只添加需要的源码路径。保留原 Projects/MatlabFiles，不在其中保存会覆盖题目函数的修改。缺少 LinRegress/arxfit 等是待完成作业。

## Python 补充路线

建议独立虚拟环境，Python 3.10 或更新版本；所提供生成器也兼容常见较新版本。核心依赖只有 NumPy、SciPy；绘图使用 Matplotlib，notebook 按需安装 Jupyter。安装版本以实际环境记录为准，不要求最新版本。

在课程根目录打开 PowerShell：

~~~powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install numpy scipy matplotlib
.\.venv\Scripts\python.exe self_study\tools\check_course_data.py
.\.venv\Scripts\python.exe self_study\tools\generate_practice_data.py --output self_study\practice_data
.\.venv\Scripts\python.exe -m pip freeze > self_study\python_environment.txt
~~~

这是你之后复现时的命令。本次已使用当前机器已有运行时及隔离依赖执行生成/检查，未为你安装或修改系统 Python，也未建立上述 .venv。已生成的 practice_data 可直接使用。

MATLAB 读取合成练习：

~~~matlab
d = load('self_study/practice_data/differential_drive_train.mat');
plot(d.t, d.y);
~~~

Python 读取：

~~~python
import numpy as np
d = np.load("self_study/practice_data/differential_drive_train.npz")
print(d.files, d["u"].shape, d["y"].shape, d["Ts"])
~~~

## 合成数据契约

[生成器](tools/generate_practice_data.py) 使用固定种子，输出同内容的 NPZ/MAT 及 dataset_manifest.json。所有 truth 字段仅用于评分/研究可辨识性，不能作为待估参数的拟合输入。train/validation/test 的随机性与轨迹不同；不要合并后再随机打乱。

|前缀|任务|内容|性质|
|---|---|---|---|
|resistance|A2|电流、带异方差噪声的电压，已知噪声标准差|自编 WLS 题，替代 Sheet 4 缺失数据|
|rls|E1|一阶 ARX，半程系数变化|自编递推题|
|differential_drive|E2|左右轮速输入、二维位置观测、真值姿态|借用 Sheet 8 结构，独立合成；RK4 生成|
|differential_drive_degenerate|E2|左右等轮速|可辨识性退化对照|
|two_state_kf|G1|位置/速度状态、已知输入、位置观测|自编二维 KF/创新似然题；不是官方六状态数据|
|torque_robot|G2|左右轮转矩、位置与轮速观测、五状态真值|借用 Sheet 10 结构，独立合成；Euler 生成|

矩阵每行一个时间点；u 为当前区间输入，x[k+1] 由 x[k]、u[k] 推进；y[k] 对应 x[k]，最后一个 u 仅保留接口一致。具体列名、Ts、单位、噪声与积分方法见 manifest。真值均非实测，不代表某台实际机器人/车辆。

G1 的 q 是每个采样区间加速度扰动的方差，过程噪声矩阵为 q ggᵀ；不是连续白噪声谱密度。G2 的过程噪声为每步对 v、ω 的离散加性扰动。滤波时应使用与该定义一致的 Q。

## 验证范围

已验证：46 个原文件哈希、下载文件哈希、PDF/Notebook 可读取、本地 MAT 数据形状与有限性、生成器执行、固定种子重现、数学公式语法、课程内部文件链接及任务覆盖。实际执行结果见 [course_validation.json](course_validation.json)。

未执行：MATLAB 原生项目、MIT notebook、Simulink 模型；未获取 Freiburg Classroom 资料；没有实车验证。课程包提供任务和数据，不提供所有项目的已完成答案。
