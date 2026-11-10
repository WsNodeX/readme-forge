<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="../assets/logo-dark.svg">
    <img src="../assets/logo.svg" width="440" alt="readme-forge">
  </picture>
</p>

<p align="center">
  <em>あなたのモデルは README を書いた。その半分は、自分自身へのメモだった。</em>
</p>

<p align="center"><a href="../README.md">English</a> · <a href="README.zh-CN.md">简体中文</a></p>

---

GitHub の README を監査し、「作者のため」ではなく「読者のため」に書き直す
Agent Skill です。

## 対象とする失敗

モデルに README を書かせると、しばしば二つの文書を一度に納品します。一つ目は
README。二つ目は、モデルが自分のために書いたローンチ計画です。

```markdown
## この記事をローンチ記事に拡張する方法

- 見出し案：「PyTorch の autograd を 600 行で書いた」
- 画像指示：上記のアーキテクチャ図を再利用する
- 投稿先：dev.to / r/Python / Hacker News
```

問題は二つ。作者に向けて書かれていること、そして存在しない図を参照していること。
訪問者はこれを「機械の出力」と判断して離脱します。

この skill は 13 項目を監査し、違反した行をそのまま引用したうえで、固定の骨格に
書き直します：**本文 300〜800 文字**、実画像 1 枚、ライブバッジ 3 個、そして
最初の 20 行以内に動くクイックスタート。

## インストール

```bash
git clone https://github.com/WsNodeX/readme-forge ~/.claude/skills/readme-forge
```

Claude Code のプラグインとしても使えます：

```bash
/plugin marketplace add WsNodeX/readme-forge
/plugin install readme-forge
```

プレーンな Markdown なので、Codex / Cursor / Cline / Gemini CLI / Kiro でも動作します。

## クイックスタート

```bash
python scripts/readme-audit.py --dir path/to/repo
```

```text
WsNodeX/ember     11540 文字   バッジ 6   画像 0   問題 9 種   FAIL
    x 作者向けのテキスト：見出し案
    x 実画像ゼロ、かつ存在しない図を参照
    x 最初のコードブロックが 81 行目、上限は 40
```

その後エージェントに渡します：`readme-forge skill を使って WsNodeX/ember を処理して。`

## 検査項目

| ルール | 失敗条件 |
|---|---|
| 作者向けテキスト | ローンチ計画・見出し案・画像指示を含む |
| プラットフォーム誘導 | 記事の投稿先を明記している |
| バッジの節度 | 3 個を超える、または全て静的文字列 |
| 実画像 | バッジ以外の画像が 0 枚 |
| 幽霊アセット | `git ls-files` で見つからない図を説明している |
| 裏付けのない数値 | テスト数の背後にコマンドがない |
| 長さ | 4,000 文字を超える |
| 最初のコード | 40 行目より後に出現する |

## なぜ作ったか

README の助言はたいてい文章を最適化します。文章は問題ではありません。誤った読者に
向けて書かれた README は、どれだけ上手に書かれても失敗します。

最も効くのは「幽霊アセット」の検査です。モデルが「上記のアーキテクチャ図を再利用」
と書くとき、それは自分が作っていないファイルを説明しています。これは機械的に
検査できるので、検査しています。

最も難しかったのは「使用」と「言及」の区別です。悪い例を説明する README は、それを
引用しなければなりません。そのためテキスト規則は本文にのみ適用し、コードブロック・
インラインコード・HTML 属性は事前に除去します。この規則がなければ、本プロジェクト
自身の README が自身の監査に落ちます。

## 制限

- **空のプロジェクトは救えません。** コードに語ることがなければ、監査はそう告げて
  停止します。
- **star は増やしません。** きれいな README は訪問者が離脱する理由を消すだけで、
  訪問者が訪れる理由は作りません。それは配布の問題です。
- **リモート監査には `api.github.com` が必要**で、トークンなしでは 1 時間 60 リポジトリまでです。

## ライセンス

MIT
