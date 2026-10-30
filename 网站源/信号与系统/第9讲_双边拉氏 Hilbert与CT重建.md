---
edit_url: https://github.com/yunbianmailang/university-course-materials/edit/main/%E5%86%85%E5%AE%B9%E6%BA%90/%E5%A4%A7%E4%BA%8C%E4%B8%8A/%E4%BF%A1%E5%8F%B7%E4%B8%8E%E7%B3%BB%E7%BB%9F/%E7%AC%AC09%E8%AE%B2.md
---

# 第9讲 双边拉氏 Hilbert与CT重建

**V3.0 · 核对日期 2026-10-30**

[PDF 阅读](<../文件/信号与系统_第9讲_学习讲义_V3重制版.pdf>) · [Word 下载](<../文件/信号与系统_第9讲_学习讲义_V3重制版.docx>) · [报告本讲问题](https://github.com/yunbianmailang/university-course-materials/issues/new?template=note-error.yml&title=%5B%E7%BA%A0%E9%94%99%5D%20%E4%BF%A1%E5%8F%B7%E4%B8%8E%E7%B3%BB%E7%BB%9F%20%E7%AC%AC9%E8%AE%B2%20)

网页与下载版依据同一份定稿整理；网页省略印刷页码，按章节导航阅读。来源和原图说明保留在正文。

## 第一层 课堂核心速览

### 本节课的核心问题

负时间信号怎样作拉氏变换？拉氏边界何时给出傅里叶谱？Hilbert、二维变换与投影切片怎样联系CT重建？

### 必要先修知识

指数积分、部分分式、傅里叶对、冲激筛选和卷积；电路关系、主值和坐标代换随题补足。

### 核心知识结构

双边拉氏与ROC → 傅里叶边界 → Hilbert与解析信号 → 二维FT和Radon → 切片与滤波反投影。

### 重要结论与条件

双边反演须同时给F与ROC；虚轴在通常ROC内才可直接取 $s=j\omega$。CT采用空间周频率 $\nu$，ramp与求导后Hilbert之间的系数为 $1/(2\pi)$。

### 课堂听讲重点

【重点】左右信号的同一分式如何区分？虚轴冲激权重从何而来？解析信号怎样抵消负频率？切片方向与反投影系数如何核对？

## 第二层 引导式学习正文

### 1 本课入口与正弦稳态回顾

**【必须掌握】** 知道本课由单边走向双边，再由一维走向二维；区分完整响应与正弦稳态。

资料内容｜讲义第 1—3 页。本课沿两条线展开：补全拉氏变换对负时间信号的处理；用积分变换把移相、投影与重建问题变成频域关系。

必要回顾｜对稳定的实 LTI 系统，输入 $E_m\sin(\omega_0t)u(t)$ 的启动瞬态消退后，有

$$
r_{ss}(t)=E_m|H(j\omega_0)|\sin[\omega_0t+\arg H(j\omega_0)].
$$

来源是 $R_{zs}(s)=H(s)E(s)$：输入的 $\pm j\omega_0$ 极点留下同频项，系统的严格左半平面模态衰减。频率响应须在相应变换存在时由 $s=j\omega$ 得到；它只给正弦稳态，不是全部启动响应。

<a id="error-1"></a>

!!! warning "资料校核"

    第 2 页以 $h(t)\to0$ 概括稳定，是本课因果适当有理模型下的简化。一般 LTI 系统的 BIBO 判据是冲激响应绝对可积（直接传递项另计），仅趋零不充分；非因果系统还须结合 ROC，不能只看极点位置。

符号约定｜$s=\sigma+j\omega$，$\omega$ 为角频率（rad/s）；$\mathcal L_B$ 为双边拉氏变换，$\mathcal H$ 为 Hilbert 变换，$\hat f=\mathcal Hf$。一维时间傅里叶采用核 $e^{-j\omega t}$、逆变换系数 $1/(2\pi)$。二维与 CT 部分采用课件的 $e^{-j2\pi(ux+vy)}$；$u,v,\nu$ 是空间周频率，不沿用角频率的求导系数。

### 2 双边拉普拉斯变换与收敛域

**【必须掌握】** 【重点】把象函数和 ROC 看成一组信息，能判断左右信号的收敛方向。

资料内容｜讲义第 4—6、9 页。单边变换围绕 $0^-$ 处理初始状态，双边变换把整个时间轴纳入，适合描述负时间输入、双侧信号及与傅里叶变换的联系。

#### 2.1 定义与两端的共同约束

**【必须掌握】** 按正、负时间分段积分，并取收敛条件的交集。

$$
F_B(s)=\mathcal L_B\{f(t)\}=\int_{-\infty}^{\infty}f(t)e^{-st}\,dt.
$$

（9-1）

通常以绝对收敛定义 ROC：$\int|f(t)|e^{-\sigma t}dt$ 有限的 $\sigma$ 范围。对常见有理象函数，它是竖直半平面或带状区域，内部不能含极点。反变换沿 ROC 内一条竖直线积分：

$$
f(t)=\frac1{2\pi j}\int_{\sigma-j\infty}^{\sigma+j\infty}F_B(s)e^{st}\,ds.
$$

!!! info "理解提示"

    增大 $\sigma$ 会压低正时间尾部，却放大负时间尾部。两端条件须同时成立，没有交集便没有通常意义下的双边变换。

<a id="error-2"></a>

!!! warning "资料校核"

    第 4、9 页以“两端乘衰减因子后趋零”帮助判断常见指数信号，不是一般收敛的充分条件。例如 $1/(1+|t|)$ 两端趋零，但在 $\sigma=0,\omega=0$ 的积分发散。ROC 应从积分判断，不能只查端点极限。

#### 2.2 同一分式的不同反变换

**【必须掌握】** 用 ROC 决定每个极点项向左还是向右延伸。

右侧阶跃给出 $\int_0^\infty e^{-st}dt=1/s$，要求 $\sigma>0$。左侧负阶跃则给

$$
\int_{-\infty}^{0}[-e^{-st}]dt=\frac1s,\qquad \sigma<0.
$$

因此仅有 $1/s$ 不能区分 $u(t)$ 与 $-u(-t)$；ROC 补足了时域支持方向。

![图 1 依据讲义第 4—6 页重绘 同一象函数与不同 ROC](<插图/第9讲/roc_compare.png>){ loading=lazy }

*图 1 依据讲义第 4—6 页重绘 同一象函数与不同 ROC*

读图：先看波形位于原点哪侧，再看极点所在边界。右侧信号的 ROC 向右，左侧信号向左；边界极点不属于 ROC。

| 时域信号 | 双边象函数 | ROC |
|---|---|---|
| $\delta(t)$ | 1 | 全部有限 s |
| $u(t)$ | $1/s$ | $\sigma>0$ |
| $-u(-t)$ | $1/s$ | $\sigma<0$ |
| $e^{-at}u(t)$ | $1/(s+a)$ | $\sigma>-a$ |
| $-e^{-at}u(-t)$ | $1/(s+a)$ | $\sigma<-a$ |
| $\frac{t^{n-1}e^{-at}}{(n-1)!}u(t)$ | $\frac1{(s+a)^n}$ | $\sigma>-a$ |
| $-\frac{t^{n-1}e^{-at}}{(n-1)!}u(-t)$ | $\frac1{(s+a)^n}$ | $\sigma<-a$ |

表中 $n=1,2,\ldots$；a 为实数时边界为 $-a$，为复数时换为 $-\operatorname{Re}a$。时间幂来自 $\mathcal L_B\{t^mf\}=(-1)^m d^mF_B/ds^m$。左侧公式的负号和 t 的幂次必须保留，不能把 t 任意换成 $|t|$。

教师例题｜第 5 页：求 $f(t)=u(t)+e^tu(-t)$ 的双边变换。先分段：

$$
F_B(s)=\int_{-\infty}^0e^{(1-s)t}dt+\int_0^\infty e^{-st}dt.
$$

左端要求 $1-\sigma>0$，右端要求 $\sigma>0$，共同 ROC 为 $0<\sigma<1$，得

$$
F_B(s)=\frac1{1-s}+\frac1s,\qquad 0<\operatorname{Re}s<1.
$$

核验：极点 0、1 均在带状 ROC 的边界上；第一项来自负时间，第二项来自正时间。

单边与双边的微分性质不能混用。两端边界项消失时，分部积分给 $\mathcal L_B\{f'\}=sF_B$；单边则为 $\mathcal L\{f'\}=sF-f(0^-)$。双边式已包含整个历史，不自动另带 $0^-$ 初值项；单边初值定理也不能不加条件地照搬到任意双边信号。

### 3 教师换路 RC 电路例题

**【必须掌握】** 【重点】用 ROC 逐项反演，与单边初始状态法交叉核验。

资料例题｜讲义第 7—8 页。开关在 $t<0$ 的全部过去接 1 端，电容由直流源 E 充电；$t=0$ 转至 2 端，电容经 R 放电。理想 $R,C>0$，求完整的 $v_C(t)$。

![图 2 依据讲义第 7—8 页重绘 换路电路 等效输入与电容电压](<插图/第9讲/rc_switch.png>){ loading=lazy }

*图 2 依据讲义第 7—8 页重绘 换路电路 等效输入与电容电压*

读图：先认开关 1、2 端及参考节点，再看等效输入 $e(t)=Eu(-t)$。电路是因果系统，输入在负时间已有作用不代表电路非因果；电容电压从 E 连续接到指数放电。

!!! info "必要先修"

    串联 R、C 流过同一电流，KVL 为 $e=v_R+v_C$，且 $v_R=Ri,\ i=Cv_C'$。零状态传递函数由 $Z_C=1/(sC)$ 分压得到；这是全时间输入输出规律，不能把已经充电的 $v_C(0^-)$ 强行设零。

第一步，建模。记 $a=1/(RC)>0$：

$$
H(s)=\frac{V_C(s)}{E(s)}=\frac{1/(sC)}{R+1/(sC)}=\frac{a}{s+a},\qquad \sigma>-a.
$$

第二步，负时间阶跃的双边变换为 $E(s)=-E/s$、ROC 为 $\sigma<0$；乘积取共同区域：

$$
V_C(s)=-\frac{Ea}{s(s+a)}=-\frac E s+\frac E{s+a},\qquad -a<\sigma<0.
$$

第三步，按这个带状 ROC 反演：$-E/s$ 取左侧支撑，$E/(s+a)$ 取右侧支撑，故

$$
v_C(t)=Eu(-t)+Ee^{-at}u(t),\qquad a=\frac1{RC}.
$$

（9-2）

即 $t<0$ 为 E，$t>0$ 为 $Ee^{-t/(RC)}$，边界连续取 $v_C(0)=E$。

核验一｜$t<0$ 时稳态电流为零、电容电压为 E；$t>0$ 时满足 $RCv_C'+v_C=0$。电容电压没有跳变，导数中没有由电压跳变产生的冲激。

核验二｜仅研究 $t\ge0$ 时，单边法使用 $e=0$、$v_C(0^-)=E$：

$$
RC[sV_+(s)-E]+V_+(s)=0,\qquad V_+(s)=\frac E{s+a}.
$$

它只给右半段放电，与双边结果一致。双边历史输入 $Eu(-t)$ 已负责预充电，不能再重复叠加一次相同的初始状态响应。

### 4 拉氏变换与傅里叶变换的关系

**【必须掌握】** 【重点】先查 ROC 与虚轴的关系，再决定直接代入还是作广义边界处理。

资料内容｜讲义第 10—14 页。把 $s=\sigma+j\omega$ 代入定义，直接得

$$
F_B(\sigma+j\omega)=\mathcal F\{f(t)e^{-\sigma t}\}(\omega).
$$

拉氏变换是“指数加权后的傅里叶变换”。因果信号的单边、双边变换在共同收敛处一致；非因果信号的单边变换只保留右半段，不能代替完整双边变换。

#### 4.1 虚轴在 ROC 内与边界上的区别

**【必须掌握】** 知道令 s=jω 的前提，区分普通频谱与广义频谱。

虚轴位于通常绝对收敛域内时，

$$
F(\omega)=F_B(j\omega).
$$

（9-3）

例如 $a>0$ 时，$e^{-at}u(t)$ 的 ROC 为 $\sigma>-a$，傅里叶谱为 $1/(a+j\omega)$。而 $e^{at}u(t)$ 的 ROC 为 $\sigma>a>0$，普通傅里叶变换不存在，不能只把分式中的 s 换成 $j\omega$。

<a id="error-3"></a>

!!! warning "资料校核"

    第 11 页按收敛边界作三类讨论，针对这里的因果有理示例。双侧信号还须看完整带状 ROC；边界在虚轴上也不保证任意信号都存在带冲激的频谱。以下边界公式用于所述虚轴极点、可作广义变换的因果信号。

对 $u(t)$，从右侧加微小衰减 $\epsilon>0$，再取 $\epsilon\to0^+$，得分布边界值

$$
\mathcal F\{u(t)\}=\operatorname{PV}\frac1{j\omega}+\pi\delta(\omega).
$$

（9-4）

PV 为柯西主值：对称避开奇点后取极限。$\pi\delta$ 记录零频成分，不能因形式代入 $1/s$ 而漏掉；此式也不是给 $\omega=0$ 赋一个普通数值。来源见 A1。

#### 4.2 虚轴简单极点的冲激权重

**【必须掌握】** 按每个极点的留数与位置，写齐主值项与冲激项。

资料内容｜讲义第 12 页。设因果信号满足：

$$
F(s)=F_a(s)+\sum_{n=1}^N\frac{K_n}{s-j\omega_n},
$$

其中 $F_a$ 的普通傅里叶边界存在，例如为极点严格位于左半平面的严格真有理部分。每项对应 $K_ne^{j\omega_nt}u(t)$，由频移得

$$
F(\omega)=F_a(j\omega)+\sum_{n=1}^N K_n\left[\operatorname{PV}\frac1{j(\omega-\omega_n)}+\pi\delta(\omega-\omega_n)\right].
$$

（9-5）

“直接代入再加冲激”的简写中，奇异部分须按主值解释；每个冲激权重是 $\pi K_n$。本式仅处理简单虚轴极点，重极点用广义导数，见 A1。

教师例题｜第 13 页：求 $\sin(\omega_0t)u(t)$ 的傅里叶谱，$\omega_0>0$。先写清部分分式：

$$
F(s)=\frac{\omega_0}{s^2+\omega_0^2}=\frac{j/2}{s+j\omega_0}-\frac{j/2}{s-j\omega_0}.
$$

在 $-j\omega_0$ 的留数为 $j/2$，在 $+j\omega_0$ 为 $-j/2$，逐项使用式（9-5），得

$$
F(\omega)=\operatorname{PV}\frac{\omega_0}{\omega_0^2-\omega^2}+\frac{j\pi}{2}[\delta(\omega+\omega_0)-\delta(\omega-\omega_0)].
$$

第一项按两个简单极点分别定义主值。核验：实信号频谱共轭对称，实部偶、虚部奇。第 13 页中间通式的移位须逐项写 $\omega_n$，不能把所有冲激写在同一个 $\omega_0$。

| 原信号 | 单边拉氏 | 傅里叶谱 |
|---|---|---|
| $\delta(t)$ | 1 | 1 |
| $u(t)$ | $1/s$ | $\operatorname{PV}\frac1{j\omega}+\pi\delta(\omega)$ |
| $e^{-at}u(t)$ | $\frac1{s+a}$ | $\frac1{a+j\omega}$ |
| $\sin(\omega_0t)u(t)$ | $\frac{\omega_0}{s^2+\omega_0^2}$ | $\operatorname{PV}\frac{\omega_0}{\omega_0^2-\omega^2}+\frac\pi{2j}[\delta(\omega-\omega_0)-\delta(\omega+\omega_0)]$ |
| $\cos(\omega_0t)u(t)$ | $\frac s{s^2+\omega_0^2}$ | $\operatorname{PV}\frac{j\omega}{\omega_0^2-\omega^2}+\frac\pi2[\delta(\omega-\omega_0)+\delta(\omega+\omega_0)]$ |

表中依照第 14 页约定，把省写的因果因子 $u(t)$ 显式补回；$a>0,\omega_0>0$。另有 $n=0,1,\ldots$ 的时间幂：

$$
\mathcal L\{t^nu(t)\}=\frac{n!}{s^{n+1}},\qquad \sigma>0,
$$

$$
\mathcal F\{t^nu(t)\}=\frac{n!}{(j\omega)^{n+1}}+j^n\pi\delta^{(n)}(\omega).
$$

其中 $n=0$ 的第一项为 PV，$n\ge1$ 按有限部分 Fp 解释；不能把它当普通反常积分。推导见 A1。

### 5 积分变换与傅里叶家族

**【建议理解】** 用核函数观点定位各工具，不混淆周期性和频率单位。

资料内容｜讲义第 15—17 页。积分变换的一般形式是 $F(s)=\int_a^b f(t)K(s,t)dt$。核 K 决定怎样提取信息：傅里叶核提取振荡分量，拉氏核再加指数权重；Hilbert 取得正交分量，Radon 取得沿线投影。

| 形式 | 时域基本结构 | 频域基本结构 |
|---|---|---|
| FT | 连续时间，通常非周期 | 连续，通常非周期 |
| FS | 连续时间，周期信号 | 离散谐波系数，一般不周期 |
| DTFT | 离散时间，一般非周期 | 连续频率，周期 $2\pi$ |
| DFS / DFT | 离散周期序列 / N个数及其周期延拓 | 离散频率，索引按N周期延拓 |

读表｜时域周期化使频域离散化，时域采样使频域周期化。DFT 本身处理 N 个数；与 DFS 联系时采用长度 N 的周期延拓，不能认定实际有限记录本来就周期。

连续时间对应 FT 与拉氏变换；离散时间有 $X(z)=\sum_nx[n]z^{-n}$，在单位圆 $z=e^{j\Omega}$ 上才与 DTFT 联系，也须检查存在域。这里只定位课件的“亲戚”，不展开 z 变换计算。

### 6 Hilbert 变换的模型与直觉

**【必须掌握】** 【重点】正频率减90度、负频率加90度，理解主值核与理想模型的条件。

资料内容｜讲义第 18—20 页。为在不改变各非零频率幅度的情况下取得正交分量，定义理想 Hilbert 变换器：

$$
H_H(j\omega)=-j\operatorname{sgn}(\omega),\qquad \omega\ne0.
$$

（9-6）

正频率乘 $-j$、相位减 $90^\circ$；负频率乘 $+j$、相位加 $90^\circ$。约定 $\operatorname{sgn}(0)=0$，直流单独处理。

来源｜由 $\operatorname{sgn}(t)\leftrightarrow2/(j\omega)$，应用傅里叶对偶性，得 $\operatorname{PV}[1/(\pi t)]\leftrightarrow-j\operatorname{sgn}\omega$。因此

$$
h_H(t)=\operatorname{PV}\frac1{\pi t},\qquad \hat f(t)=\mathcal H\{f\}(t)=f*h_H.
$$

主值存在时，积分式为

$$
\hat f(t)=\frac1\pi\operatorname{PV}\int_{-\infty}^{\infty}\frac{f(\tau)}{t-\tau}\,d\tau.
$$

（9-7）

PV 同时删去 $\tau=t$ 左右等长的小区间再取极限，不是分别求两个发散积分后相减。一般有限能量信号可用 $L^2$ 极限定义。

![图 3 依据讲义第 18—20 页重绘 Hilbert 核与非零频率幅相](<插图/第9讲/hilbert_response.png>){ loading=lazy }

*图 3 依据讲义第 18—20 页重绘 Hilbert 核与非零频率幅相*

读图：正、负频率的模均为 1，相位符号相反；原点值另约定。时域核在正负时间都有值，零点有主值奇性。

<a id="error-4"></a>

!!! warning "易错提醒"

    保幅是保持幅度谱，不是每一时刻 $|\hat f(t)|=|f(t)|$。理想 Hilbert 核非因果、不绝对可积，不能当成普通 BIBO 稳定、能精确实时实现的有限阶全通电路；它在 $L^2$ 能量范数中有界。工程实现须近似与延迟。

连续作两次，非零频率上 $(-j\operatorname{sgn}\omega)^2=-1$，因此适当信号类中 $\mathcal H^2f=-f$，逆变换为

$$
f=-\mathcal H\hat f=-\frac1\pi\operatorname{PV}\int_{-\infty}^{\infty}\frac{\hat f(\tau)}{t-\tau}\,d\tau.
$$

这适用于 $L^2$ 信号，或另行排除直流的相应信号类；常数的 Hilbert 变换取零，不能通过再变换恢复这个常数。

### 7 教师余弦例题与 Hilbert 性质

**【必须掌握】** 会在频域处理符号和冲激权重，知道正交性、卷积性质的条件。

资料例题｜讲义第 21—23 页。求 $\cos(\omega_0t)$ 的 Hilbert 变换，$\omega_0>0$。直接主值积分较繁，先用两个冲激谱：

$$
F(\omega)=\pi\delta(\omega-\omega_0)+\pi\delta(\omega+\omega_0).
$$

正频率权重乘 $-j$，负频率乘 $+j$：

$$
\hat F(\omega)=-j\pi\delta(\omega-\omega_0)+j\pi\delta(\omega+\omega_0).
$$

逆变换保留 $1/(2\pi)$ 系数：

$$
\hat f(t)=\frac{-j\pi e^{j\omega_0t}+j\pi e^{-j\omega_0t}}{2\pi}=\sin(\omega_0t).
$$

这是完整时间余弦，没有乘 $u(t)$。因果截断余弦的频谱与 Hilbert 结果不同，不能套用同一变换对。

| 原函数（ω₀>0） | Hilbert 结果 |
|---|---|
| $\cos(\omega_0t)$ | $\sin(\omega_0t)$ |
| $\sin(\omega_0t)$ | $-\cos(\omega_0t)$ |
| $e^{j\omega_0t}$ | $-je^{j\omega_0t}$ |
| $e^{-j\omega_0t}$ | $+je^{-j\omega_0t}$ |

![图 4 依据讲义第 21—22 页补充绘制 正余弦与正交分量](<插图/第9讲/hilbert_quadrature.png>){ loading=lazy }

*图 4 依据讲义第 21—22 页补充绘制 正余弦与正交分量*

读图：同频的 $\cos$ 经 Hilbert 变成 $\sin$，$\sin$ 经 Hilbert 变成 $-\cos$。按波形的相位移动核对符号，而不是把所有信号都统一乘一个普通复数。

性质一｜非零频率 $|\hat F|=|F|$；对 $L^2$ 信号，Parseval 关系给出能量不变。

性质二｜对实值有限能量信号，$\int f(t)\hat f(t)dt=0$，称正交。周期正余弦改用一周期平均或积分表述，不能把全轴能量积分当有限数。证明见 A2。

性质三｜卷积存在、允许结合时，

录音补充｜A 02:04—03:29：先把 Hilbert 看成与同一个核的卷积，再用交换、结合律理解为什么可以对任一因子先作变换。

$$
\mathcal H\{f_1*f_2\}=\hat f_1*f_2=f_1*\hat f_2.
$$

（9-8）

来源是同一个核 $h_H$ 可与任一因子先卷积；频域乘积 $F_1F_2$ 只乘一次 $-j\operatorname{sgn}\omega$。两个因子都先 Hilbert 会多乘一次，通常得到相反号，不能写成同一性质。

### 8 解析信号怎样去掉负频率

**【必须掌握】** 【重点】逐项解释正频率加倍、负频率抵消和直流例外。

资料内容｜讲义第 25 页。对实信号 x，定义复解析信号

录音补充｜A 04:54—06:57：课堂逐项比较正负频率的符号；正频率同号相加、负频率相消，是解析信号构造的关键。

$$
z(t)=x(t)+j\hat x(t),\qquad \hat x=\mathcal Hx.
$$

（9-9）

代入频域乘子：

$$
Z(\omega)=X(\omega)+j[-j\operatorname{sgn}\omega]X(\omega)=[1+\operatorname{sgn}\omega]X(\omega).
$$

$\omega>0$ 时为 $2X$，$\omega<0$ 时为 0；若有直流冲激，按上述约定保留原直流、不加倍。原实信号为 $\operatorname{Re}z$。

![图 5 依据讲义第 25 页重绘 解析信号三格频谱](<插图/第9讲/analytic_spectrum.png>){ loading=lazy }

*图 5 依据讲义第 25 页重绘 解析信号三格频谱*

读图：逐个频率比较 X、$j\hat X$ 与 Z。正频率同号相加，负频率反号抵消；不要把 $\hat X$ 和 $j\hat X$ 当成同一幅谱。

补充讲解｜$x=\cos\omega_0t$ 时，$z=\cos\omega_0t+j\sin\omega_0t=e^{j\omega_0t}$，正好只含正频率。对复信号不能直接套实信号的负频率共轭冗余解释。

<a id="error-5"></a>

!!! warning "资料校核"

    第 25 页引出“降低抽样率”，需要额外条件。单纯从实 x 构成复 z 不会把最高频率减半，也不意味着样本数据量不变。应结合带通搬移、复基带与具体采样方案讨论，不能无条件承诺抽样率减半。

### 9 因果性怎样约束频响实部和虚部

**【必须掌握】** 知道实虚部不能任意独立给定，理解直通常数与模相唯一性的边界。

资料内容｜讲义第 24、26—27 页。因果性是实时实现的必要条件，但不保证稳定、有限带宽或精确实现。对普通因果冲激响应 $h(t)=h(t)u(t)$；时域支撑限制会转为频域 Hilbert 约束。

录音补充｜A 06:57—12:40：由 h=hu 出发，先转成频域卷积，再分别比较实部和虚部；课堂强调二者并非独立任取。

设 $H(j\omega)=R(\omega)+jX(\omega)$。H 有足够衰减、相关主值存在时：

$$
R=\mathcal H_\omega X,\qquad X=-\mathcal H_\omega R.
$$

（9-10）

下标 $\omega$ 表示这次在频率变量上作 Hilbert 变换，例如

$$
X(\omega)=-\frac1\pi\operatorname{PV}\int_{-\infty}^{\infty}\frac{R(\lambda)}{\omega-\lambda}\,d\lambda.
$$

来源是时域乘积转频域卷积：

$$
H=\frac1{2\pi}H*\left[\pi\delta+\operatorname{PV}\frac1{j\omega}\right].
$$

代入 $R+jX$，分别比较实、虚部并移项即得式（9-10），完整代数见 A3。

<a id="error-6"></a>

!!! warning "资料校核"

    第 27 页的“互相唯一确定”须有衰减或已知直通项等条件。若 $H=D+H_0$，D 为实常数，应对 $H_0$ 用衰减关系；未知 D 不能由虚部确定。H=1 的虚部恒零，就不能由它区分不同实常数增益。

因果也不等于幅频唯一决定相频：同幅频系统可另乘稳定全通因子，改变相位。由模恢复相位还需最小相移、归一化及适当渐近条件；第 24 页提到联系，并未给一般模相恢复算法。

### 10 二维傅里叶变换与旋转

**【必须掌握】** 掌握二维核与归一化，区分逐维变换和变量可分离，读懂旋转图。

资料内容｜讲义第 28—31 页。图像 $f(x,y)$ 依赖两个位置，频谱 $F(u,v)$ 描述两个方向的空间起伏。先从课件的一维例子理解这种对应。

引入｜第 28 页用一维矩形及其 Sa 谱，对照二维照片及其空间谱。对幅值 E、宽度 $\tau$、关于原点对称的矩形，

$$
F(\omega)=\int_{-\tau/2}^{\tau/2}Ee^{-j\omega t}dt=E\tau\operatorname{Sa}(\omega\tau/2).
$$

这里 $\operatorname{Sa}z=\sin z/z$，零点处连续取 1。二维图像同样能展开为不同方向的空间振荡分量；以下方形示例保留这种图像与频谱的对应，便于核对旋转。

二维定义采用课件的周频率规范：

录音补充｜A 12:40—15:29：二维变换可沿两轴依次做一维变换；把 2π 放进指数，是后续各式归一化必须一致的约定。

$$
F(u,v)=\int_{-\infty}^{\infty}\int_{-\infty}^{\infty}f(x,y)e^{-j2\pi(ux+vy)}\,dx\,dy.
$$

（9-11）

$$
f(x,y)=\int_{-\infty}^{\infty}\int_{-\infty}^{\infty}F(u,v)e^{j2\pi(ux+vy)}\,du\,dv.
$$

x、y 用米时，u、v 为 cycles/m。逆变换前没有 $1/(2\pi)^2$，因为 $2\pi$ 已放进指数；改用角空间频率时必须一并改核与逆变换系数。

“2D=1D+1D”是允许交换积分时，先对 x 作一维 FT、再对 y 作 FT，不是相加。只有 $f=f_1(x)f_2(y)$ 等可分离函数，频谱才分解为 $F_1(u)F_2(v)$。

![图 6 依据讲义第 30—31 页重绘 方形与旋转后的频谱](<插图/第9讲/rotation_2d.png>){ loading=lazy }

*图 6 依据讲义第 30—31 页重绘 方形与旋转后的频谱*

读图：比较方形方向与频谱主轴。图像转动时频谱随同转动，并非频谱在原坐标上完全不变；亮度是便于观察的幅值显示。

补充讲解｜令 $R_\theta$ 为平面旋转矩阵，$f_\theta(\boldsymbol r)=f_0(R_{-\theta}\boldsymbol r)$。作替换 $\boldsymbol r=R_\theta\boldsymbol r'$，面积雅可比为 1、内积保持，得到

$$
F_\theta(\boldsymbol k)=F_0(R_{-\theta}\boldsymbol k).
$$

这就是课件“旋转不变性”的具体含义：变换与旋转相容，两幅图一起转。

### 11 Radon 变换与 CT 投影

**【必须掌握】** 【重点】明确投影角、探测器位置和积分直线，会算点对象的正弦图。

资料内容｜讲义第 32—35 页。Radon 变换沿一条条直线累加，回答“从一个方向观察，对象的投影是多少”；从多方向投影恢复物体是反问题。

录音补充｜A 16:57—19:51：先用角度和偏移选定积分直线，再问多方向的测量怎样恢复原物体。

![图 7 依据讲义第 32、35 页绘制 投影角与探测器坐标](<插图/第9讲/radon_geometry.png>){ loading=lazy }

*图 7 依据讲义第 32、35 页绘制 投影角与探测器坐标*

读图：$\theta$ 为直线法向量与 x 轴夹角，t 为探测器轴上的有符号偏移；同一 t 对应一条积分直线。此处 t 是空间位置，不是前半课的时间。

取 $\boldsymbol n_\theta=(\cos\theta,\sin\theta)$，切向量 $\boldsymbol l_\theta=(-\sin\theta,\cos\theta)$，Radon 变换为

$$
g(\theta,t)=\int_{-\infty}^{\infty}\int_{-\infty}^{\infty}f(x,y)\delta(t-x\cos\theta-y\sin\theta)\,dx\,dy.
$$

（9-12）

换到正交坐标 $\boldsymbol r=t'\boldsymbol n_\theta+\ell\boldsymbol l_\theta$，雅可比为 1，冲激将 $t'$ 筛到 t，故也可写成

$$
g(\theta,t)=\int_{-\infty}^{\infty}f(t\cos\theta-\ell\sin\theta,\ t\sin\theta+\ell\cos\theta)\,d\ell.
$$

前式便于频域推导，后式便于几何理解。法向量长度为 1，这里没有额外的线积分缩放系数。

![图 8 教师原图 讲义第 33 页 CT 应用示例](<插图/第9讲/ct_application.png>){ loading=lazy }

*图 8 教师原图 讲义第 33 页 CT 应用示例*

读图：设备从多个方向采集投影，再重建截面。补充讲解｜理想单能、忽略散射的衰减模型中，对透射强度取 $-\ln(I/I_0)$ 才得到衰减系数线积分，不能把原始探测器强度直接等同于 g。

教师例题｜第 34 页：点对象 $f(x,y)=\delta(x-a)\delta(y-b)$。代入式（9-12），先对 x、y 筛选：

$$
g(\theta,t)=\delta(t-a\cos\theta-b\sin\theta).
$$

（9-13）

冲激权重仍为 1；每个角度的亮点位于 $t(\theta)=a\cos\theta+b\sin\theta$。固定空间点随角度描出的轨迹，就是正弦图中的点迹。

![图 9 依据讲义第 34 页重绘 点对象与正弦图](<插图/第9讲/point_sinogram.png>){ loading=lazy }

*图 9 依据讲义第 34 页重绘 点对象与正弦图*

读图：$\theta=0$ 时 t=a，$\theta=\pi/2$ 时 t=b，可用这两个位置核对方向和符号；正弦图不是原图像。

### 12 投影切片定理与频域重建

**【必须掌握】** 【重点】从投影的一维 FT 得到二维频谱径线，理解反演的绝对值雅可比。

资料内容｜讲义第 36—39 页。固定角度，把投影对探测器位置 t 作一维 FT。以下用 $\nu$ 替代课件 CT 式中的 $\omega$，仍保留其 $2\pi$ 指数：

$$
G_\theta(\nu)=\int_{-\infty}^{\infty}g(\theta,t)e^{-j2\pi\nu t}\,dt.
$$

代入式（9-12），交换积分并使用冲激筛选：

$$
G_\theta(\nu)=\int\int f(x,y)\left[\int\delta(t-x\cos\theta-y\sin\theta)e^{-j2\pi\nu t}\,dt\right]dx\,dy,
$$

$$
G_\theta(\nu)=\int\int f(x,y)e^{-j2\pi\nu(x\cos\theta+y\sin\theta)}dx\,dy,
$$

$$
G_\theta(\nu)=F(\nu\cos\theta,\nu\sin\theta).
$$

（9-14）

一个方向的投影，经一维 FT 后，给出二维频谱中沿同一法向方向、穿过原点的一条径线。

![图 10 教师原图 讲义第 37 页 圆盘投影与频谱切片核验](<插图/第9讲/disk_slice.png>){ loading=lazy }

*图 10 教师原图 讲义第 37 页 圆盘投影与频谱切片核验*

读图：圆盘的投影宽度对应穿过圆盘的弦长；投影的一维频谱与二维频谱中心径线相符。这里对照的是变换后的频谱，不是拿投影曲线直接与二维频谱比较。

![图 11 依据讲义第 38 页绘制 图像 投影与频谱径线](<插图/第9讲/slice_theorem.png>){ loading=lazy }

*图 11 依据讲义第 38 页绘制 图像 投影与频谱径线*

读图：固定角度的一条投影曲线，经 1D FT 对应二维频谱的一条中心径线；不是从原图直接截一条线。多个方向补充不同频谱径线。

另一推导入口｜第 36 页把 $\delta(\rho)=\int e^{j2\pi\nu\rho}d\nu$ 代入投影式，整理积分得

录音补充｜A 23:40—31:44：遇到冲激，尝试写成傅里叶积分；交换次序后先找指数中的 x、y 系数，识别二维频谱，再认出剩余的一维逆变换。

$$
g(\theta,t)=\int F(\nu\cos\theta,\nu\sin\theta)e^{j2\pi\nu t}d\nu.
$$

再对 t 作 FT 得到同一结果。冲激表示按广义函数理解，不能把未收敛的普通积分任意交换。

反演关键｜二维逆 FT 中取 $u=\nu\cos\theta,\ v=\nu\sin\theta$。以 $\nu\in\mathbb R,\ 0\le\theta<\pi$ 覆盖平面，除原点外恰一次；面积元为 $du\,dv=|\nu|d\nu d\theta$，故

$$
f(x,y)=\int_0^\pi\left[\int_{-\infty}^{\infty}|\nu|G_\theta(\nu)e^{j2\pi\nu(x\cos\theta+y\sin\theta)}d\nu\right]d\theta.
$$

（9-15）

<a id="error-7"></a>

!!! warning "易错提醒"

    $|\nu|$ 来自雅可比，不是可删的经验权重。若角度取 $0$ 到 $2\pi$、半径仍取正负全轴，会重复覆盖，系数必须相应修正。

### 13 滤波反投影与教师推导任务

**【必须掌握】** 【重点】把二维反演改成一维滤波再回填，核对求导与 Hilbert 表示的系数。

资料内容｜讲义第 39—42 页。式（9-15）的内层积分只沿 $\nu$ 进行，可先看作一维滤波：

录音补充｜A 34:02—38:44：把直接二维反演改写为一维滤波加反投影，关键是认出频域乘积对应时域卷积。

$$
q_\theta(t)=\mathcal F_\nu^{-1}\{|\nu|G_\theta(\nu)\}(t)=(g_\theta*h_r)(t),\qquad \mathcal F_\nu\{h_r\}=|\nu|.
$$

（9-16）

再把滤波后的值沿对应直线放回图像并累加：

$$
f(x,y)=\int_0^\pi q_\theta(x\cos\theta+y\sin\theta)\,d\theta.
$$

（9-17）

这就是滤波反投影 FBP。“投影”沿线积分，“反投影”沿线回填，不是把正投影逐点相除。直接反投影而不滤波会模糊。

求导加 Hilbert 的等价形式｜本节周频率规范下，$\mathcal F_\nu\{\partial_tg_\theta\}=j2\pi\nu G_\theta$，Hilbert 乘子仍为 $-j\operatorname{sgn}\nu$，因此

$$
q_\theta(t)=\frac1{2\pi}\mathcal H_t\{\partial_tg_\theta\}(t).
$$

（9-18）

因为 $(j2\pi\nu)(-j\operatorname{sgn}\nu)=2\pi|\nu|$，须除回 $2\pi$ 才与式（9-16）一致。两条完整推导见 A4。

<a id="error-8"></a>

!!! warning "资料校核"

    第 40 页频域乘积 $j\omega G_\theta(-j\operatorname{sgn}\omega)=|\omega|G_\theta$ 本身正确；但沿用该页 $e^{j2\pi\omega t}$ 的核时，下方直接标 $g_\theta'*1/(\pi t)$ 少了 $1/(2\pi)$。本文以 $\nu$ 明确空间周频率，按式（9-18）统一归一化。

![图 12 依据讲义第 41—42 页原理补充绘制 滤波与反投影对照](<插图/第9讲/fbp_demo.png>){ loading=lazy }

*图 12 依据讲义第 41—42 页原理补充绘制 滤波与反投影对照*

读图：先看补充示例对象及正弦图，再比较未滤波与滤波反投影。教师 PDF 两页是演示的静态帧；本图用另一个明确数值对象展示前后效果，不冒充教师原始影像或完整动画。

结果解释｜ramp 按 $|\nu|$ 增强高空间频率，抵消直接反投影的频率偏重，也会增强噪声。离散重建还涉及有限带宽、角度采样、插值和滤波窗；连续公式假定足够投影数据及相应可逆条件，有限数据的数值结果只是近似。

录音补充｜A 42:33—43:33：ramp 随频率绝对值上升，增强高频也增强噪声；最终还要按各角度反投影并累加。

### 14 核心回顾与正式作业

**【必须掌握】** 按支持、ROC、频率规范与几何关系选择工具，明确本课方法的联系。

!!! abstract "知识回顾"

    双边反演需要“分式＋ROC”；虚轴在 ROC 内才可直接取傅里叶边界。简单虚轴极点产生主值项与 $\pi$ 倍留数的冲激。Hilbert 对正频率减90度、负频率加90度；解析信号去掉负频率。切片定理把一维投影谱接到二维径线，FBP 再用 ramp 与反投影重建。

方法回顾｜负时间输入先分段积分求交集；虚轴极点先检查因果性和广义频谱；Hilbert 题逐个频率乘符号；CT 题先定 $\theta,t$ 几何意义与 $2\pi$ 规范，再用冲激筛选、坐标替换和卷积。

<a id="error-9"></a>

!!! warning "易错回顾"

    左侧 $1/s$ 对应负阶跃；历史输入与同一初始状态不能重复计数；Hilbert 保幅不等于逐时刻等幅；直流影响反演边界；因果不保证幅频决定相频；CT 不能丢 $|\nu|$ 与 $2\pi$。

资料内容｜第 44 页作业：教材 4-50；“推导证明：37页公式中的内层积分等效为特殊的时域卷积”。复习第 4 章，预习第 5 章。教材题面未随本课件提供，以教材为准，不另编题面。

资料校核｜课末原文写“37页公式”；本 PDF 第 37 页为投影傅里叶关系，含 $|\nu|$ 的反演内层积分及两种作业表示在第 39—40 页。A4 对应这两条推导，保留原任务并给当前 PDF 定位。

## 第三层 详细参考与拓展

### A1 广义傅里叶边界与高阶极点

**【建议理解】** 追溯冲激系数和高阶有限部分，理解边界极限的思路。

补充讲解｜$\epsilon>0$ 时，$e^{-\epsilon t}u(t)$ 的普通傅里叶谱为

$$
\frac1{\epsilon+j\omega}=\frac{\epsilon}{\epsilon^2+\omega^2}-j\frac{\omega}{\epsilon^2+\omega^2}.
$$

第一项面积为 $\pi$，$\epsilon\to0^+$ 时集中到零点，按分布趋于 $\pi\delta(\omega)$；第二项以对称主值趋于 $1/(j\omega)$，得到式（9-4）。从左侧逼近对应不同支持，不能照抄冲激符号组合。

对 $n=0,1,\ldots$，时间乘幂对应频域微分：

$$
\mathcal F\{t^nu(t)\}=j^n\frac{d^n}{d\omega^n}\left[\operatorname{PV}\frac1{j\omega}+\pi\delta(\omega)\right].
$$

课件第 14 页通式为

$$
\mathcal F\{t^nu(t)\}=\frac{n!}{(j\omega)^{n+1}}+j^n\pi\delta^{(n)}(\omega),
$$

第一项按上式分布导数定义；$n\ge1$ 时是 Hadamard 有限部分 Fp，不是普通对称删除奇点就能收敛的积分。例如 $tu(t)$ 的谱为 $-\operatorname{Fp}(1/\omega^2)+j\pi\delta'(\omega)$。

在 $t^nu(t)$ 上再乘 $e^{j\omega_ct}$，整个谱移到 $\omega_c$。所以重虚轴极点会产生冲激的导数，不只是多加一个普通冲激；这些式子不用于给奇点赋有限数值。

### A2 Hilbert 保能 正交与逆变换

**【建议理解】** 把性质与频域乘子相连，避免把能量结论误用到直流或无限能量信号。

资料内容与补充证明｜讲义第 23 页。取实值 $f\in L^2$。除零点外几乎处处 $|\hat F|^2=|F|^2$，由 Parseval 得

$$
\int|\hat f(t)|^2dt=\frac1{2\pi}\int|\hat F(\omega)|^2d\omega=\int|f(t)|^2dt.
$$

正交性先用带共轭的 Parseval 内积，再利用 $\hat f$ 实值：

$$
\int f(t)\hat f(t)dt=\frac1{2\pi}\int F(\omega)\hat F^*(\omega)d\omega,
$$

$$
\int f(t)\hat f(t)dt=\frac j{2\pi}\int\operatorname{sgn}(\omega)|F(\omega)|^2d\omega=0.
$$

因为实信号的 $|F|^2$ 为偶函数，乘符号函数后为奇函数；可积性来自有限能量。不是对任意复信号的共轭内积都断言为零。

同一 $L^2$ 口径下，零频单点不改变等价类，因此 $\mathcal H^2=-I$、$\mathcal H^{-1}=-\mathcal H$。含直流冲激的周期或广义信号需先剔除或另存直流，不能套无条件反演。

### A3 因果实虚部约束的代数来源

**【建议理解】** 看清关系来自因果支撑，而非凭空规定的相位经验式。

补充讲解｜以普通因果 $h\in L^1$ 为基础，并要求相关频率主值存在；$h=hu$ 不受单点 $u(0)$ 影响。时域乘积的傅里叶变换给

$$
H=\frac12H+\frac1{2\pi}H*\operatorname{PV}\frac1{j\omega}.
$$

记 $\mathcal H_\omega R=R*\operatorname{PV}[1/(\pi\omega)]$，代入 $H=R+jX$：

$$
R+jX=\frac12(R+jX)+\frac12\mathcal H_\omega X-\frac j2\mathcal H_\omega R.
$$

实部给 $R=R/2+\mathcal H_\omega X/2$，虚部给 $X=X/2-\mathcal H_\omega R/2$；移项即为 $R=\mathcal H_\omega X,\ X=-\mathcal H_\omega R$。

含 $D\delta(t)$ 时不能机械地对冲激作普通 $h=hu$ 单点论证。先写 $H=D+H_0$，对衰减部分 $H_0$ 用上述关系，另给 D；更一般的色散关系可能需要减项，不把无衰减的所有函数纳入本式。

### A4 两种 FBP 等价表示的完整推导

**【必须掌握】** 理解教师布置的两条推导，按频率规范核对卷积核与常数。

资料内容与补充推导｜讲义第 39—40、44 页。固定 $\theta$，以 $g_\theta(t)$ 表示该角投影。目标是把式（9-15）内层积分写成一维运算，再反投影。

录音补充｜A 38:52—41:13：课堂将 ramp 拆为求导因子和 Hilbert 乘子，并明确称上述两条等价表示的证明为“两项作业”；准确系数仍须按变换规范核对。

#### A4.1 ramp 乘法等价于卷积

**【必须掌握】** 从频域乘积识别卷积，知道理想核是分布而非普通可积函数。

取 $h_r=\mathcal F_\nu^{-1}\{|\nu|\}$，卷积定理给 $q_\theta=g_\theta*h_r$；在 $t=x\cos\theta+y\sin\theta$ 取值，就是反演内层积分，得到式（9-16）和（9-17）。

求核不能直接把 $\int|\nu|e^{j2\pi\nu t}d\nu$ 当普通收敛积分。先加 Abel 衰减：

$$
h_\epsilon(t)=\int_{-\infty}^{\infty}|\nu|e^{-\epsilon|\nu|}e^{j2\pi\nu t}d\nu,
$$

$$
h_\epsilon(t)=2\int_0^\infty\nu e^{-\epsilon\nu}\cos(2\pi\nu t)d\nu.
$$

先积 $\int_0^\infty e^{-\epsilon\nu}\cos(b\nu)d\nu=\epsilon/(\epsilon^2+b^2)$，对 $\epsilon$ 求负导数，取 $b=2\pi t$：

$$
h_\epsilon(t)=\frac{2(\epsilon^2-4\pi^2t^2)}{(\epsilon^2+4\pi^2t^2)^2}.
$$

当 $t\ne0$，趋于 $-1/(2\pi^2t^2)$；全轴上的正确极限是

$$
h_r=-\frac1{2\pi^2}\operatorname{Fp}\frac1{t^2}=\frac1{2\pi}\frac d{dt}\left(\operatorname{PV}\frac1{\pi t}\right).
$$

有限部分要连同奇点附近的发散项一起扣除。例如对光滑衰减的 g，

$$
\operatorname{Fp}\int\frac{g(\tau)}{(t-\tau)^2}d\tau=\lim_{\eta\to0^+}\left[\int_{|t-\tau|>\eta}\frac{g(\tau)}{(t-\tau)^2}d\tau-\frac{2g(t)}{\eta}\right].
$$

不能仅避开原点就把 $1/t^2$ 当普通卷积核；数值实现也不按此发散积分直接逐点求和。

#### A4.2 ramp 等价于求导后作 Hilbert

**【必须掌握】** 把 j2πν 与符号函数相乘，正确得到 1/(2π)。

投影足够光滑衰减、或相应广义运算成立时，

$$
\mathcal F_\nu\{\mathcal H_t(\partial_tg_\theta)\}=(-j\operatorname{sgn}\nu)(j2\pi\nu)G_\theta=2\pi|\nu|G_\theta.
$$

除以 $2\pi$ 并逆变换：

$$
q_\theta=\frac1{2\pi}\mathcal H_t(\partial_tg_\theta)=\frac1{2\pi}\left[g_\theta'*\operatorname{PV}\frac1{\pi t}\right].
$$

相应条件下可把求导移到卷积核，与 A4.1 的核导数式一致。代回角度积分，两条路线给同一个 f，核验了系数。

改用角空间频率 $\Omega=2\pi\nu$，导数乘子虽变为 $j\Omega$，二维逆变换前系数和面积元也须相应改变；不能只删除这里的 $2\pi$ 而保持其余式子不动。

### A5 人物背景与其他积分变换

**【拓展阅读】** 认识课件列出的工具，不增加本课之外的计算任务。

资料内容｜讲义第 24、43 页。David Hilbert（1862—1943）是德国数学家，课件以希尔伯特空间、公理化几何和 23 个问题介绍背景；这里只联系变换名称。

Hartley 变换使用实的余弦与正弦组合核；Hankel 变换常联系圆对称问题及 Bessel 函数；Mellin 变换常联系正变量的尺度分析；Abel 变换联系轴对称投影。课件只列名称，没有要求本讲逐一计算。

资料来源｜高河伟《信号与系统 第 4 章 拉普拉斯变换 IV 及其他积分变换》，PDF《Ch4_4》45 页，封面标注 2026 年秋季。第 45 页注明基于邢宇翔、赵自然老师原讲稿并参考其他教师课件修改。文中页码均指该 PDF；教师原图与重绘、补充图在图注中区分。
