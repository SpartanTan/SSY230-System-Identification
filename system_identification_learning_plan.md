# 系统辨识自学主线：从回归、动态模型到车辆辨识与 EKF

> 目标：能够从有噪声的输入输出数据建立、选择、验证动态模型，解释什么时候参数无法被识别，并将可信模型用于车辆状态估计。
>
> 建议投入：每周 6–10 小时；A–G 核心主线约 18 周，H 车辆应用约 6 周。24 周是学习周，不绑定日历；另留 2–4 周缓冲。已有基础可通过诊断跳过重复内容。
>
> 状态：⬜ 未开始 · 🟨 进行中 · ✅ 完成。材料核对日期：2026-11-10。

本计划参考你的 SLAM 计划，保留“连续知识链 → 原生作业 → 自编补充 → 综合项目 → 验收”的组织方式。完成标准是能说明输入、输出、状态、参数、目标函数、噪声假设、数据划分和失效条件，并能在查资料或 AI 协助下实现与验证；不要求背完所有渐近证明。

## 从这里开始

1. 阅读 [材料审计与使用注意](self_study/source_audit.md)，先了解原题接口差异、缺失模板和数据限制。
2. 完成 [A0 环境与先修诊断](self_study/assignment_guide.md#a0)，决定是否压缩第 1–4 周。
3. 每周按下面日程只推进一个任务。任务细则、数据、失败实验和提交物见 [作业手册](self_study/assignment_guide.md)。
4. 第 16 周完成一次真实数据辨识，第 18 周完成辨识到 KF/EKF 的连接；再进入车辆 capstone。

主线：

**统计回归 → 采样与频域 → 激励和可辨识性 → ARX/预测/OE → 验证与闭环 → 状态空间/递推/灰箱 → 真实系统 → KF/EKF → 车辆模型。**

## 材料如何分工

|材料|角色|入口|
|---|---|---|
|本地 SSY230 slides|每周概念主轴，按主题重排而非机械按文件名排序|下方各阶段|
|Söderström & Stoica，简称 S&S|线性动态辨识、噪声、激励、闭环和验证的理论底座|[本地完整教材][SS]|
|本地三个 Project|主要编程链：静态回归 → 动态辨识 → 真实系统|[P1][P1] · [P2][P2] · [P3][P3]|
|SSY230Problems，简称 P|43 道题及其解答，用于手推和检查理解|[原题与解答][P] · [按题索引](self_study/problem_index.md)|
|Freiburg MSI 2025 讲义|最小二乘、非线性优化、RLS、KF/EKF 的连续补强|[已归档讲义][MSI] · [官网](https://www.syscop.de/teaching/ws2025/modelling-and-system-identification)|
|MIT Underactuated 的 System Identification|机械参数、方程误差与仿真误差、模型用于控制的语境|[章节](https://underactuated.mit.edu/sysid.html) · [公开 notebook 说明](self_study/resources_and_coverage.md#mit)|
|Cascaded Tanks 实测数据|P3 的默认真实系统，不依赖实验台或课程账号|[数据卡](self_study/resources/cascaded_tanks/README.md)|
|已整理的 MMF062 讲义|最后六周的车辆方程、传动约束与 EKF 背景|[车辆动力学主线][VME]|

资源下载、来源、版本与可访问性见 [资源及覆盖审计](self_study/resources_and_coverage.md)。已有材料保持原位；新材料位于 self_study。

**已确认的编程安排：** 原生 P1–P3 优先沿用 MATLAB；自编补充采用 Python/NumPy/SciPy，也可用 MATLAB 实现相同接口。无需每个算法做两遍。MATLAB 工具箱不可用时走手册内的 Python 路线，不让商业软件权限阻断学习。MIT 的 Drake notebook 是可选分支，不是 Windows 本机安装 Drake 的前置要求。

## 课程日程

“最晚完成”是缓冲建议：未通过上一任务的验收时，先补齐，不为了赶周数堆积新概念。表中时间包含阅读、推导、编程与短报告。

|状态|周|任务|主题与原作业|建议完成|最晚完成|用时|
|:---:|---:|---|---|---:|---:|---:|
|⬜|1|[A0](self_study/assignment_guide.md#a0)|环境、统计/线代/离散系统诊断、数据字典|W1|W2|4–6 h|
|⬜|2|[A1](self_study/assignment_guide.md#a1)|LS、协方差、Monte Carlo；P1 §1(a,b)、附录 A|W2|W3|6–8 h|
|⬜|3|[A2](self_study/assignment_guide.md#a2)|Ridge、WLS、多项式、置信区间；P1 §1(c–e)|W3|W4|8–10 h|
|⬜|4|[A3](self_study/assignment_guide.md#a3)|偏差/方差、KNN、维数与分布变化；完成 P1 必修部分|W4|W5|8–10 h|
|⬜|5|[B1](self_study/assignment_guide.md#b1)|采样、瞬态、相关与频率响应|W5|W6|6–8 h|
|⬜|6|[B2](self_study/assignment_guide.md#b2)|持续激励、实验设计、时延和预处理|W6|W7|6–8 h|
|⬜|7|[C1](self_study/assignment_guide.md#c1)|ARX 回归器与符号；P2 §1(a,b)|W7|W8|8–10 h|
|⬜|8|[C2](self_study/assignment_guide.md#c2)|一步、多步预测与自由仿真；P2 §1(c,d)|W8|W9|8–10 h|
|⬜|9|[C3](self_study/assignment_guide.md#c3)|噪声结构、PEM/ML、两阶段 OE；P2 §2|W9|W10|8–10 h|
|⬜|10|[C4](self_study/assignment_guide.md#c4)|模型阶次、残差与留出验证；P2 §3|W10|W11|8–10 h|
|⬜|11|[D1](self_study/assignment_guide.md#d1)|闭环辨识、IV、相关噪声与偏差|W11|W12|6–10 h|
|⬜|12|[D2](self_study/assignment_guide.md#d2)|状态空间、Markov 参数、Ho–Kalman 与子空间|W12|W13|8–10 h|
|⬜|13|[E1](self_study/assignment_guide.md#e1)|RLS、遗忘因子、参数漂移|W13|W14|6–8 h|
|⬜|14|[E2](self_study/assignment_guide.md#e2)|非线性/灰箱、输出误差优化、可辨识性|W14|W15|8–10 h|
|⬜|15|[F1](self_study/assignment_guide.md#f1)|真实双水箱：数据审计与线性基线；P3 第一阶段|W15|W16|8–10 h|
|⬜|16|[F2](self_study/assignment_guide.md#f2)|非线性比较、独立测试和演示；完成 P3|W16|W18|8–10 h|
|⬜|17|[G1](self_study/assignment_guide.md#g1)|KF、创新似然与噪声参数辨识|W17|W18|6–10 h|
|⬜|18|[G2](self_study/assignment_guide.md#g2)|EKF、测量模型、可观测性；主线综合检查|W18|W20|8–10 h|
|⬜|19|[H1](self_study/assignment_guide.md#h1)|车辆模型、参数与传感器配置契约|W19|W21|6–8 h|
|⬜|20|[H2](self_study/assignment_guide.md#h2)|纵向驱动响应：有效增益、延迟与可辨识组合|W20|W22|8–10 h|
|⬜|21|[H3](self_study/assignment_guide.md#h3)|横向灰箱：前后轴刚度、激励与工况覆盖|W21|W23|8–10 h|
|⬜|22|[H4](self_study/assignment_guide.md#h4)|固定辨识参数的车辆 EKF；参数误差消融|W22|W24|8–10 h|
|⬜|23|[H5](self_study/assignment_guide.md#h5)|传感器配置比较、偏置/时延/掉线与少量参数扩展|W23|W25|8–10 h|
|⬜|24|[H6](self_study/assignment_guide.md#h6)|可复现演示、失败案例、最终答辩|W24|W28|6–10 h|

若你的 SLAM 计划中 D0、E1、E2 已完成，A0/A1 和 G1/G2 可以做诊断后压缩，但仍要完成“参数可辨识性”和“创新用于模型验证”的新增部分。若只想先掌握 SSY230，可在 G2 后暂停 H；不要跳过 F 的真实数据项目。

## A：统计学习与回归

**先读：** [课程概览][L1] → [Statistical Learning][STAT] → [课程 Linear Regression][L5]。ISL 风格的 [linear_regression-handout][LR] 用于直观解释，不与 L5 重复逐页刷。

**教材：** S&S §2.5、§4.1–4.5；MSI §2.4、§4.1–4.7，ML/MAP 用 MSI §5.1–5.2。

|任务|原生任务与练习|必须掌握|完成线|
|---|---|---|---|
|A0|自编诊断；P 第 9 题作基础检查|矩阵维度、噪声、离散递推、数据单位|能从零复现小规模线性拟合，不依赖现成辨识命令|
|A1|P1 §1(a,b)、附录 A；P 1、9|LS 推导、残差方差、参数协方差|噪声为零恢复参数；Monte Carlo 方差与理论趋势一致|
|A2|P1 §1(c–e)；[Freiburg Sheet 4][F4] 题 1–2|正则化偏差、秩亏、加权、参数区间与预测区间|白化残差正确；不显式计算正规方程逆；解释错误模型也能给很窄区间|
|A3|P1 §2、§3.1–3.2、§4.1；P 2|KNN、模型复杂度、训练与测试分布|用独立数据选阶次/邻居数；保留最终测试集；完成 P1 报告|

P1 §3.3 chirpData 与 §4 的十维问题保留为选修；二维问题自学时做两个生成器中的一个，另一个作为额外留出分布。十维三次多项式先阅读 [辅助代码审计](self_study/source_audit.md#poly)。

## B：数据必须含有你想辨识的信息

**主材料：** [Non-parametric Identification][L4]、[Experiment Design slides][L9] 的输入、采样、预处理部分；S&S 第 3 章、§5.1–5.4、§6.3–6.4、§12.2–12.6。L9 的 103 个 PDF 页面含逐步动画展开，不代表 103 个独立知识点。

|任务|练习|产出|故意制造的失败|
|---|---|---|---|
|B1|P 4–6；P 3 暂留 D1|阶跃/脉冲/相关/频率响应的同系统对照图|截掉或保留瞬态、频率泄漏、激励不足频带的失真|
|B2|P 23、24、26、28，27 选做|输入频谱、回归矩阵奇异值、采样与时延实验|单一正弦拟合高阶模型，或错误对齐输入输出|

**完成线：** 能解释增加同一种无信息的数据为何不能解决不可辨识；把输入幅值、频带、记录长度、采样和工作点写成可执行实验计划。真实设备上另受执行器与运行边界限制，本课程先用仿真。

## C：动态辨识与验证

**主材料：** [Linear Black-Box Models][L6] → [PEM / ML][L7] → [Model Validation][L8]。S&S §6.1–6.2、§7.1–7.6、第 11 章；MSI 第 7 章用于对照 equation error 与 output error。

|任务|原生任务与练习|完成线|
|---|---|---|
|C1|P2 §1(a,b)；P 7、9、12|逐项对应数据列、延迟和参数符号；通过本地 student_test_pr2 数值样例|
|C2|P2 §1(c,d)；P 12、14、15|同一模型输出一步、五步和自由仿真；预测不得使用预测起点之后的真实输出|
|C3|P2 §2；P 13、16、18|区分 ARX 噪声模型与输出噪声；两阶段 OE 与真正非线性输出误差优化分开命名|
|C4|P2 §3；P 19、21、22，20 选做|两组数据都有阶次/延迟比较、残差检查、预测与仿真报告；完成 P2|

**重要：** 本地 exercise1 有 300 个样本，exercise2 的 z1、z2 各 200 行；文件中没有采样周期字段。缺少其他证据时使用“每采样点”的时间单位，不把自行设定的 Ts=1 声称为物理上的 1 秒。数据划分和原题接口修订见 [材料审计](self_study/source_audit.md#datasets)。

## D：反馈与状态空间

**主材料：** L9 的闭环部分；[State-Space / IV slides][L10]；[Subspace Chapter 10][SUB]。S&S 第 8 章先读 IV 原理、第 10 章读可辨识性与直接/间接方法。

|任务|材料与练习|完成线|
|---|---|---|
|D1|P 3、25、29；自编“反馈中加入独立参考激励”实验|区分反馈引起的相关性与信息不足；说明所用 IV 的相关/不相关条件|
|D2|P 30、32，31、33 选做；MIT 线性辨识题的最小二乘部分作为补充|从 Markov 参数构造 Hankel 并做 Ho–Kalman；用输入输出响应比较实现，不直接比较不同基底下的 A 元素|

Ho–Kalman 是教学起点，不等同于实现了完整的噪声鲁棒 N4SID。实际子空间模型可以用工具箱作对照，必须注明算法与估计阶次。[Tony Gustafsson 论文][TONY] 放在 D2 后选读，不作为入门前置。

## E：递推、非线性与灰箱

**主材料：** [Recursive Identification][L12]；[Ljung 第 5 章节选][LJUNG] 的时变/非线性模型；[Neural Networks][NN] 先看表示和泛化概念。S&S §9.1–9.3、§9.7；MSI §5.3、§5.5、第 7 章。

|任务|材料与练习|完成线|
|---|---|---|
|E1|P 38、39；[Freiburg Sheet 6][F6] 作思路补充|λ=1 的 RLS 与同先验批量 LS 一致；比较遗忘因子的跟踪速度与噪声|
|E2|P 34、35；[Freiburg Sheet 8][F8] 的差速机器人灰箱思路；P 37 选做|先拟合少量有物理意义的参数，检查 Jacobian、尺度、多初值与激励退化|

Freiburg 题面公开，但其 Classroom 模板和部分实测数据没有在本次获得。手册提供明确标注的自编等价练习和合成数据生成器，不把它们称作已完成官方原题复现。E2 中的差速机器人用于连接你的 SLAM 标定经验，与汽车转向模型分开。

## F：真实系统项目

按 [Project 3][P3] 完成一次完整辨识循环，默认使用已下载的 [Cascaded Tanks 数据卡](self_study/resources/cascaded_tanks/README.md)。它包含真实输入输出、未知初态、软非线性和溢出效应，适合检验简单模型何时不够。

|任务|内容|完成线|
|---|---|---|
|F1|数据字典、采样、缺失值、趋势、频谱、训练/验证/测试协议；ARX/OE 线性基线|先提交分析与建模理由，再开始批量调参|
|F2|增加一种非线性模型，比较误差、残差、复杂度与稳定性；完成 10 分钟演示|每张图回答一个问题；冻结选择后只使用一次官方测试集；清楚区分预测与自由仿真|

本科式“跑几十个模型挑最高 fit”不作为完成线。课程允许没有达到论文精度：只要方法、比较、误差和失败原因可解释。原 P3 推荐商业工具箱；自学的 Python 路线保留同一科学任务，并标明没有完成 MATLAB GUI 熟悉目标。

## G：把辨识和状态估计连接起来

**主材料：** MSI §8.1–8.3、§8.5、§8.7；[Freiburg Sheet 9][F9]、[Sheet 10][F10]。视频只补卡住的推导，入口与观看范围见 [资源表](self_study/resources_and_coverage.md#videos)。

|任务|内容|完成线|
|---|---|---|
|G1|固定模型运行 KF；用创新似然拟合一个受限噪声参数|区分参数协方差、过程噪声、测量噪声与创新协方差；报告留出序列结果|
|G2|非线性测量/运动模型、EKF Jacobian、状态与参数的不同角色|检查离散映射 Jacobian；比较已知参数与错误参数；不能用增大 Q 掩盖所有失配|

**主线关卡：** 用本地 2024 卷前 5 页做分两次、各 60–90 分钟的自测，再看该文件第 6 页起的解答。考试分数只是检查之一；同时必须通过 P1–P3 的实验验收。2025 卷留作完成 H 后复测，避免提前读答案。

## H：车辆辨识与 EKF 综合项目

这里是本计划自编的应用项目，使用你已整理的 MMF062 内容，不冒充 SSY230 原生作业。硬件尚未确定，始终保留差速器与传感器选项。先用合成实验完成方法链，真实车辆数据到位后再替换数据源。

|任务|核心工作|完成线|
|---|---|---|
|H1|选择二状态单轨作为辨识基线，七状态后驱作为集成目标；固定可测的质量和几何，列出未知参数|状态/参数/输入/观测/单位表，哪些量可辨识的论证|
|H2|纵向增益与驱动响应延迟；区别命令与实际转矩|至少两种激励、独立验证；说明效率、质量、半径等哪些只能识别组合|
|H3|拟合 Cf、Cr 等少量横向参数，比较多车速/多转向频带|参数敏感度与相关性，训练工况之外的误差，不凭单次优化收敛宣称唯一|
|H4|固定已辨识参数，比较“名义错误参数 / 辨识参数 / 合成真值参数”的 EKF|同数据划分、同测量与同调参预算；速度/侧偏角/横摆误差及创新|
|H5|比较轮速+IMU、加 GNSS、转矩未知三种配置；必要时只增加一个慢变参数或偏置|解释哪种激励/测量支持新增状态；保留失败分支|
|H6|统一数据接口、模型、配置、报告与演示|另一人按 README 能复现；分清合成自洽、模型失配验证与实车验证|

从 [车辆讲义第 08 章][RWD] 和 [第 09 章][EKF] 获取方程背景。现有七状态 EKF 示例可用作理解接口的参考，但不能把同模型产生数据、同模型估计的良好结果当作辨识验证。至少加入一种生成端与估计端不同的动力学或参数工况。

## 选修及有意延后

|选修|何时学习|具体入口与任务|
|---|---|---|
|X1 自适应控制|E1、D1 后|[Adaptive Control][ADAPT]；P 40–43；用仿真比较固定增益与在线更新，检查闭环稳定性|
|X2 学习型动力学|F2 后|MIT [glider notebook](self_study/resources/mit/glider_sysid.ipynb)；比较物理基函数与更复杂模型的独立仿真误差|
|X3 强化学习连接|核心主线后|[本地 RL slides][RL]，结合已学 02465；区分 model-based RL 中的辨识、策略学习与探索|
|X4 深入理论|有研究需求时|S&S 渐近分析、IV 最优性、CRLB；不以手抄全部证明作为入门关卡|
|X5 MHE / 联合辨识|G2、H4 后|MSI §8.6–8.7；先比较约束与计算成本，再决定是否替代 EKF|

## 每份任务的统一提交物

参考 [报告模板](self_study/report_template.md)。每份提交至少包括：

1. 输入、输出、状态、参数和单位；数据来源与划分。
2. 一条核心推导，以及公式到代码变量的对应。
3. 无噪声、正常噪声和一个故意失败实验。
4. 独立验证：指标、残差、参数不确定性与适用条件。
5. 一条可复现运行命令、依赖版本、随机种子和下一步决定。

完成原题前不看解答。卡住时先写下具体维度、符号或假设，再查对应最小片段。AI 可以帮你解释、调试和检查；最终应能不看代码讲清模型为什么可辨识、预测时用了哪些信息，以及实验结果能支持什么结论。

## 第一周的具体安排

- 第一次，约 2 小时：读 L1、S&S 第 1 章；运行数据检查脚本，填写材料和环境情况。
- 第二次，约 2 小时：完成 A0 的四个诊断，读取 exercise1/2，画输入输出，不拟合复杂模型。
- 第三次，约 1–2 小时：手推一个两参数 LS 例子，规划 P1 的函数接口；通过即进入 A1。

环境、生成器与依赖：[环境说明](self_study/environment.md)。课程全局自检与来源哈希：[核对记录](self_study/course_validation.json)。

[SS]: <slides/System%20Identification%20-%20Soderstrom%20and%20Stoica%20(searchable).pdf>
[P]: <ExercisesSolutions/SSY230Problems.pdf>
[P1]: <Projects/project_1.pdf>
[P2]: <Projects/project_2.pdf>
[P3]: <Projects/project_3.pdf>
[L1]: <slides/lect1.pdf>
[STAT]: <slides/statistical_learning-handout.pdf>
[LR]: <slides/linear_regression-handout.pdf>
[L5]: <slides/lect5LinearRegression_handhout.pdf>
[L4]: <slides/lect4nonparametric.pdf>
[L6]: <slides/lect6LinearBlackBoxModels_handout.pdf>
[L7]: <slides/lect7PredictingEstimate_PEM_handout.pdf>
[L8]: <slides/lect8ModelValidation_handouts.pdf>
[L9]: <slides/lect9ExperimentalDesignData_ClosedLoopID_Handhouts.pdf>
[L10]: <slides/lect10_State_space_Id_IV_methods_Handhouts.pdf>
[SUB]: <slides/SubSpace_ch10.pdf>
[TONY]: <slides/SubSpaceIdentificationTonyGustafsson.pdf>
[L12]: <slides/lect12_recurciveSI_handouts.pdf>
[LJUNG]: <slides/Ljung99_chap5.pdf>
[NN]: <slides/Lect13Neural%20Networks%20made%20simple.pdf>
[ADAPT]: <slides/lect13_adaptiveControl.pdf>
[RL]: <slides/lect14_Re-inforcement_Learning.pdf>
[MSI]: <self_study/resources/freiburg/msi.pdf>
[F4]: <self_study/resources/freiburg/exercise4.pdf>
[F6]: <self_study/resources/freiburg/exercise6.pdf>
[F8]: <self_study/resources/freiburg/exercise8.pdf>
[F9]: <self_study/resources/freiburg/exercise9.pdf>
[F10]: <self_study/resources/freiburg/exercise10.pdf>
[VME]: <C:/Users/zhicun/Documents/Obsidian/Onenote/笔记整理/硕士/Chalmers/SP2/MMF062%20Vehicle%20Motion%20Eng/教学讲义/00%20车辆动力学推导主线.md>
[RWD]: <C:/Users/zhicun/Documents/Obsidian/Onenote/笔记整理/硕士/Chalmers/SP2/MMF062%20Vehicle%20Motion%20Eng/教学讲义/08%20单电机后驱改写.md>
[EKF]: <C:/Users/zhicun/Documents/Obsidian/Onenote/笔记整理/硕士/Chalmers/SP2/MMF062%20Vehicle%20Motion%20Eng/教学讲义/09%20EKF状态估计.md>

## 后续课程

已设计的 [EEN050 鲁棒与非线性控制课程](<C:/Users/zhicun/Desktop/EEN050%20-%20Robust%20and%20nonlinear%20control/EEN050%20-%20Robust%20and%20nonlinear%20control/robust_nonlinear_control_learning_plan.md>) 接收本课程的名义模型、参数范围、残差与 EKF 结果。完成 A–G 后可先学该课程核心，再将两门车辆项目连接起来；具体见 [辨识—估计—控制衔接](<C:/Users/zhicun/Desktop/EEN050%20-%20Robust%20and%20nonlinear%20control/EEN050%20-%20Robust%20and%20nonlinear%20control/self_study/identification_to_control.md>)。
