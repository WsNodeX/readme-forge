# This file is deliberately a bad README. It is the input to the audit, not a
# document that should pass. Named `ember.md` and not `README.md` on purpose:
# the audit walks all `README.md` files, and this one is meant to fail.

<div align="center">

# Ember

### A from-scratch autograd engine and neural-network library — written in pure Python, with **zero runtime dependencies**.

[![Python](https://img.shields.io/badge/python-3.9%2B-3776AB?logo=python&logoColor=white)](https://www.python.org)
[![License: MIT](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![Dependencies](https://img.shields.io/badge/dependencies-0-blue)](requirements.txt)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey)](https://github.com/WsNodeX/ember)
[![Tests](https://img.shields.io/badge/tests-60%20passing-brightgreen)](tests)
[![Pure Python](https://img.shields.io/badge/implementation-pure%20Python-orange)](ember)

</div>

---

## ✨ 为什么

Every deep-learning framework rests on the same two ideas: a tensor that remembers
how it was built, and a reverse-mode differentiation pass. Ember is a small,
readable implementation of exactly those two ideas.

Why build one by hand?

- **Understanding.** Reading a 3,000-line autograd implementation teaches you more
  about backpropagation in an afternoon than a semester of treating `.backward()`
  as magic.
- **Zero dependencies.** It runs on a bare Python interpreter.
- **A real résumé artifact.**

## 🚀 特性

- Reverse-mode autograd over scalars, vectors and matrices
- A pure-Python tensor backend implementing matmul, broadcasting, softmax
- Neural-network blocks: Linear, ReLU, Sigmoid, Tanh, Softmax, Sequential
- Tested with 60 unit tests

## 📦 安装

```bash
git clone https://github.com/WsNodeX/ember.git
cd ember
python -c "import ember; print(ember.__version__)"
```

## 三、关键实现点（面试常问）

**1. 矩阵乘法的反向。** 前向是 `C = A @ B`，反向要算两个梯度。

**2. 广播（broadcasting）的反向是"求和归约"。**

## 五、如何扩展这个项目

- 把张量从 0/1/2 维扩到 N 维，支持图像卷积；
- 实现 RNN / LSTM，做序列建模；

## 六、如何把本文扩展成一篇发布稿

- **标题建议**：《我用 600 行纯 Python 手写了 PyTorch 的内核》
- **配图建议**：Ember 的 README 里已经有一张分层架构图，可直接引用或重绘
- **钩子开头**：从"你真的懂 loss.backward() 吗"这种反问切入
- **发布平台**：适合掘金 / 知乎；B 站讲"手写框架"系列非常有受众
