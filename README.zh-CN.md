# RL-CS

**历史游戏智能体与优化实验。** 自建 Python 游戏环境旁包含神经进化、遗传算法、粒子群及监督学习练习。

[English](README.md) · [历史](docs/README-history.md)

## 仓库索引

| 路径 | 材料 |
|---|---|
| `Game/`、`Object/`、`map/` | 自建游戏规则、对象与地图 |
| `Neuron_Network/`、`neat/` | 神经网络集成与内置 NEAT 源码 |
| [Algorithm/](Algorithm/) | GA、PSO、贝叶斯等优化实验 |
| [SL/](SL/) | 独立监督学习练习及样例资源 |
| `main_neat.py`、`main_opt.py`、`main_gui.py` | 历史训练、优化和 GUI 入口 |
| `CSDeepLearing_v*.zip` | 保留的历史版本包 |

## 状态与使用

这是学习／实验档案，不是接入实时 Counter-Strike 的智能体。仓库名不表示所有内容都属于强化学习，源码实际包含多种优化及监督学习方法。

没有统一锁定环境、持续维护的安装器或本次重现的训练结果。重建隔离环境前，应先阅读选定实验及其导入；入口可能立即开始训练或打开窗口。已有 winner／检查点与旧版本包不是当前基准。本次没有运行应用、加载序列化检查点或训练智能体。

## 归属与许可

保留原模块名称与贡献历史。内置 `neat/` 继续适用其 [独立许可](neat/LICENSE) 和归属，该许可不自动覆盖其他部分。仓库整体未声明开源许可证。[文档历史](docs/README-history.md) 指向原版本说明。
