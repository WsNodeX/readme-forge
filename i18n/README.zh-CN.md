<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="../assets/logo-dark.svg">
    <img src="../assets/logo.svg" width="440" alt="readme-forge">
  </picture>
</p>

<p align="center">
  <em>你的模型写了一篇 README。其中一半是写给它自己看的。</em>
</p>

<p align="center"><a href="../README.md">English</a></p>

---

一个 Agent Skill：审计 GitHub README，然后按「给读者看」而不是「给作者看」重写。

## 它针对的问题

让模型写 README，它经常一次交付两份文档。第一份是 README，第二份是它写给自己的
发布计划：

```markdown
## 如何把本文扩展成一篇发布稿

- 标题建议：《我用 600 行纯 Python 手写了 PyTorch 的内核》
- 配图建议：复用上面的架构图
- 发布平台：掘金 / 知乎 / Hacker News
```

两个问题：它是写给作者的；它声称存在一张从来没画过的图。访问者读到这段，判断
「机器产物」，然后关掉页面。

这个 skill 跑 13 条检查，把每一条违规原文引出来，然后按固定骨架重写：
**正文字数 300–800**，一张真图，三个动态徽章，以及前 20 行内能跑起来的上手示例。

## 安装

```bash
git clone https://github.com/WsNodeX/readme-forge ~/.claude/skills/readme-forge
```

Claude Code 也可以用插件方式：

```bash
/plugin marketplace add WsNodeX/readme-forge
/plugin install readme-forge
```

纯 Markdown，所以 Codex、Cursor、Cline、Gemini CLI、Kiro 同样可用。

## 快速开始

```bash
python scripts/readme-audit.py --dir path/to/repo
```

```text
WsNodeX/ember     11540 字符   6 个徽章   0 张图   9 种问题   FAIL
    x 面向作者的文本：标题建议
    x 零真实图片，且声称存在一张实际没有的图
    x 首个代码块在第 81 行，上限 40
```

然后把结果交给你的 agent：`用 readme-forge skill 处理 WsNodeX/ember。`

## 检查什么

| 规则 | 判定失败的条件 |
|---|---|
| 面向作者的文本 | 含发布计划、标题清单或配图说明 |
| 平台引流 | 写明文章发到哪里 |
| 徽章节制 | 超过 3 个，或全是静态字符串 |
| 真实图片 | 非徽章的图片数量为 0 |
| 幽灵资产 | 描述了一张 `git ls-files` 找不到的图 |
| 无证据的数字 | 测试数量背后没有对应命令 |
| 长度 | 超过 4,000 字符 |
| 首个代码块 | 在第 40 行之后才出现 |

## 为什么做这个

大部分 README 建议在优化文笔。文笔不是问题所在——写给错误读者的 README，写得
再好也是失败的。

真正干活的是「幽灵资产」那一条。模型写「复用上面的架构图」时，它在描述一个自己
没创建的文件。这是可以机械检查的，所以就该被检查。

最难的部分是区分「使用」和「引用」：一份讲反例的 README 必须引用那些坏词。所以
文本规则只在正文上跑——围栏代码块、行内代码和 HTML 属性先被剥离。没有这条规则，
本项目自己的 README 都过不了自己的审计。

## 局限

- **救不了空项目。** 代码没东西可说，审计会直说然后停下。
- **不能涨 star。** 干净的 README 只是去掉了访客离开的理由，它不制造访客到来的
  理由——那是分发问题，见 `references/distribution.md`。
- **远程审计需要 `api.github.com`**，无 token 时限 60 个仓库/小时。

## 许可证

MIT
