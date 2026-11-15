# 原材料审计与自学修订

[返回主线](../system_identification_learning_plan.md) · [全部文件覆盖](resources_and_coverage.md)

核对日期 2026-11-10。已清点 46 个原文件并记录 SHA-256；本计划不修改它们。PDF 页码均指阅读器页码，区别于页脚印刷页码。这里的修订是自学建议，不是原教师发布的勘误。

## 材料齐备程度

三个 Project、课程 slides、完整 S&S 教材、43 道题及答案、6 份历年试卷都在目录中。P1/P2 要求学生编写的函数没有提供成品，这是作业本身，不是资料损坏。Canvas 自动评分和教师反馈没有取得；本地样例、合成真值、独立验证及报告关卡代替在线评分。

S&S 为经典版本，涵盖回归、输入、模型结构、PEM、IV、递推、闭环和验证；本计划用 Freiburg 的公开材料补足非线性优化和 KF/EKF 的连续叙述。不会因教材较早而跳过噪声模型、可辨识性和实验设计。

<a id="ridge"></a>
## Project 1：岭回归增广矩阵

[原题 PDF 第 2 页](../Projects/project_1.pdf#page=2) 的示意写法对一般 N×p 的 X 与 N×m 的 Y 维度不成立。标准的“惩罚全部 p 个系数”形式是：

$$
\widetilde X=\begin{bmatrix}X\\ \sqrt{\lambda}I_p\end{bmatrix},\qquad
\widetilde Y=\begin{bmatrix}Y\\0_{p\times m}\end{bmatrix}.
$$

MATLAB 对应：

~~~matlab
p = size(X,2);
Xaug = [X; sqrt(lambda)*eye(p)];
Yaug = [Y; zeros(p,size(Y,2))];
theta = Xaug \ Yaug;
~~~

若不惩罚截距，应改正则项矩阵，而不是默认上述公式会自动排除截距。增广的零行不是新独立测量，不能把它们计入 OLS 噪声方差的样本数。Ridge 有偏，其协方差和均方误差需区分。

## Project 1：函数名与区间

原题的自定义 polyfit 接口与 MATLAB 内置 polyfit 不一致。建议自己的实现命名 polyModelFit，必要时在独立作业路径下做兼容包装；用 which polyfit -all 检查实际调用者。不要在系统路径覆盖内置函数。

附录的参数置信集合及采样所得曲线，与“新观测的预测区间”不同；有限次采样形成的包络也不能自动解释为精确的 95% 同时置信带。图中需说明覆盖对象和假设。

<a id="poly"></a>
## poly_x2 的适用范围

[poly_x2.m](../Projects/MatlabFiles/poly_x2.m) 的实现包含单变量幂与两变量交叉项，不能作为任意维数完整多项式基的通用生成器。二维三次基可以使用；十维总次数不超过 3 的完整基应有 $\binom{13}{3}=286$ 列（含常数），该辅助函数只生成 166 列，缺少三个不同变量相乘的 120 项。

十维选修任务可保留其有限基，但报告必须写明；若声称完整三次基，则自行生成指数集合并核对列数。原题样本量列表有重复的 1000；若增加 10000，属于本计划扩展，不是原题原文。

<a id="interfaces"></a>
## Project 2：统一接口与符号

[题面](../Projects/project_2.pdf) 和 [student_test_pr2.m](../Projects/MatlabFiles/student_test_pr2.m) 存在命名/参数顺序差异：

|项目|题面或其他项目|本地测试脚本|自学约定|
|---|---|---|---|
|仿真|idsimulate(model,z)|idsim(model,u)|内部统一 simulate_model(model,u)；两种外部接口做薄包装|
|比较|idcompare(z,model,horizon)|idcompare(model,z,horizon)|按本地测试顺序，另提供清晰包装，不同时猜测两种参数|
|类型字段|P1 使用 model.model|P2 使用 model.type|各项目保留兼容字段；内部统一并写入说明|

uy2phi 返回 [当前 y，历史 y，历史 u]；测试用的历史 y 列是正号。若 θ 中前 na 项记为 a，则差分式为 $y_k=\sum a_i y_{k-i}+\sum b_j u_{k-n_k-j+1}+e_k$，传递函数分母为 $1-\sum a_iq^{-i}$。教材若使用 $A(q)=1+\sum \bar a_iq^{-i}$，需要 $\bar a_i=-a_i$。

P2 §2 是以高阶 ARX 为中介的两阶段 OE 近似，不应称为通用非线性 OE/PEM 的精确优化解。题中的 Ah 滤波是 FIR 多项式滤波，不是其逆。

<a id="datasets"></a>
## 本地数据与划分

已实际读取 MAT 文件：

|文件|变量|形状|已知信息|缺失信息|
|---|---|---|---|---|
|exercise1.mat|u / y|各 300×1|有限数值；u 为 ±1|无 Ts、物理单位、测量设备元数据|
|exercise2.mat|z1 / z2|各 200×2|每行 [y,u]；原题说明至少一拍延迟|无 Ts、物理单位|

不要把采样索引人为设为 1 后宣称 Ts=1 秒。可在代码中使用归一化 Ts=1，但图轴标“样本/归一化时间”。

主线建议的 exercise1 180/60/60 与 exercise2 的 z1 140/60、z2 最终测试，是自学划分方案，不是原题新发现的元数据。训练/验证太短时可做受限的滚动验证，但不可利用最终测试反复选择模型。

## Slides、题集和试卷

- lect9 的 103 个 PDF 页面包含动画展开，约 30 个逻辑页；读主题即可，不按总页数估工作量。
- lect1 与 lect1-present 是概览的不同呈现；introduction-handout 是统计学习背景。无需逐页重复。
- 两个 lect13 分别是神经网络和自适应控制，不是同一讲的重复文件。
- Ljung99_chap5 是扫描的时变/非线性模型章节，已经查看页面确认；不能仅凭搜索提取为空就判断缺页，也不要把它误当成预测误差章节。
- SSY230Problems 的题面为 PDF 第 1–25 页，解答从第 26 页开始。见 [43 题索引](problem_index.md)。
- tenta_240530 虽文件名没有 solutions，PDF 第 6–11 页实际上含答案。自测先只看第 1–5 页。2025 卷保留到末期。
- EC21、EC3 和 ec12 图片是局部补充，不能替代完整题集。Simulink 模型留给自适应控制选修；本次未执行。

## 外部资源的边界

Freiburg 的讲义和 5 张题面已下载，但 Classroom 模板及相关数据没有取得；[本计划生成器](tools/generate_practice_data.py) 提供明确标注的合成替代，不能称为官方代码复现。Sheet 10 标头沿用较早学年，保留原文件不更改。

MIT 三个 notebook 已下载并检查 JSON 结构，未执行；其 underactuated / Drake / 自动评分依赖不属于 MATLAB 必修环境。按需在官方推荐的 Colab 入口运行，或只实现等价的 NumPy 数学练习。

Cascaded Tanks 的实测数据及基准说明已下载并读入核对，变量名 uVal/yVal 在本计划中保留为最终测试。其初态、单位及测试规则见 [数据卡](resources/cascaded_tanks/README.md)。
