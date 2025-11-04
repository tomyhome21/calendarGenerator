
## 📅 Python Calendar Generator

### 概要

このプロジェクトは、Pythonの**Pillow**ライブラリを使用して、指定されたフォント、年、カラースキームに基づき、月単位の**透過PNGカレンダー画像**を自動生成するスクリプトです。日本の祝日情報を外部APIから取得し、祝日の色分けにも対応しています。

-----

### 必須環境

  * Python 3.x
  * **Pillow** (PIL Fork)
  * **requests** (祝日APIの利用に必要)
  * **日本語TrueTypeフォントファイル（.ttf）**
      * `FONT_SETTINGS_JSON`に定義されているパス（例: `ttf/NotoSansJP-Regular.ttf`）に配置する必要があります。

-----

### セットアップ

#### 1\. ライブラリのインストール

```bash
pip install Pillow requests
```

#### 2\. フォントファイルの準備

スクリプト内で定義されているパスに合わせて、日本語フォントファイル（例：`NotoSansJP-Regular.ttf`）をプロジェクトルートの\*\*`ttf`\*\*ディレクトリ内に配置してください。

```
/ (プロジェクトルート)
├── calendar_generator.py (このスクリプト)
└── ttf/
    ├── NotoSansJP-Regular.ttf
    ├── Murecho-Regular.ttf
    └── ...
```

-----

### 使い方

スクリプトの末尾にある`if __name__ == '__main__':`ブロック内で、`generate_calendar`関数を呼び出して実行します。

#### `generate_calendar`関数

```python
generate_calendar(
    font_name: str, 
    target_year: int, 
    color_scheme: str = "black", 
    enable_holiday_color: bool = True
)
```

| パラメータ | 型 | 説明 |
| :--- | :--- | :--- |
| `font_name` | `str` | 使用するフォント名（**FONT\_SETTINGS\_JSONに定義されているもの**）。 |
| `target_year` | `int` | カレンダーを生成する年。 |
| `color_scheme` | `str` | テキストの色スキーム（`"black"` または `"white"`）。 |
| `enable_holiday_color`| `bool` | 祝日を特別な色で表示するかどうか。 |

#### 実行例

```python
if __name__ == '__main__':
    # 例: Kaisei Decol, 2027年, whiteスキームで生成
    generate_calendar(
        font_name="Kaisei Decol",
        target_year=2027,
        color_scheme="white",
        enable_holiday_color=True
    )
```

-----

### 出力ファイル 📂

カレンダー画像は、実行環境の**ホームディレクトリ**直下にある\*\*`Documents/CalendarFont`\*\*フォルダ内に、フォント名、カラースキーム、年の階層で自動生成されます。

#### フォルダ構造

| OS | 出力ベースパスの例 |
| :--- | :--- |
| **Windows** | `C:\Users\[ユーザー名]\Documents\CalendarFont` |
| **macOS/Linux** | `/Users/[ユーザー名]/Documents/CalendarFont` |

**最終的な出力パスの例:**

```
[ホームディレクトリ]/Documents/CalendarFont/
├── Kaisei Decol/
│   └── white/
│       └── 2027/
│           ├── 2027_01_KaiseiDecol_white_calendar.png
│           └── ...
└── Zen Kurenaido/
    └── black/
        └── 2026/
            └── ...
```

#### ファイル名規則

`[年]_[月(2桁)]_[フォント名(スペースなし)]_[カラースキーム]_calendar.png`

例: `2027_01_KaiseiDecol_white_calendar.png`

-----

### 💡 設定の詳細

#### 1\. フォント設定 (`FONT_SETTINGS_JSON`)

フォントごとの文字間調整などが定義されています。新しいフォントを追加する際は、ここに追記が必要です。

#### 2\. 色設定プリセット (`COLOR_PRESETS`)

デフォルトで`black`と`white`が定義されています。

-----

### 祝日情報の取得

祝日情報は [Nager.at Public Holidays API](https://date.nager.at/) を利用して取得しています。インターネット接続が必要です。

