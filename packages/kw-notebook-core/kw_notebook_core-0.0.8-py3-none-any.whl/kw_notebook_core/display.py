from IPython.core.display import display, HTML, Markdown

def md(*paragraphs):
  for p in paragraphs:
    display(Markdown(p + '\n\n'))

def notebook_caution():
  md('''## 超重要：落とし穴に注意

  ほかのひとから共有されたノートブックの所有権は共有してくれた人にあります。そういうノートブックも一時的に修正できそうに見えるので、あたかも所有権が自分にあるかのように錯覚します。でも、所有権がほかの人にあるノートブックは保存することができません。

  せっかく編集して、自分好みの内容になっても保存できなければ困ります。そこで、ノートブックを共有されたら、なにはともかくそれを**自分のノートブックとして保存**しましょう。

  いったん自分のノートブックとして保存してしまえば、それを自分の好きに編集し、保存できるようになります。
  ''')

notebook_caution()

# @title 実装コード { run: "auto", vertical-output: true, display-mode: "form" }

from IPython.display import HTML, Markdown, display

# Admonition枠のスタイルの雛形
#   color: 枠の色のプレイスホルダー
ADMONITION_STYLE_TEMPLATE = '''
<style>
div.admonition {
    border-radius: 5px;
    border: 5px solid {color};
}

div.admonition-title {
    color: #fffff8;
    background-color: {color};
    padding: 0.5em 1em 0.5em 1em;
    font-size: larger;
    font-weight: bold;
}

div.admonition-message { padding: 1em; }
</style>'''


def new_admonition(category, default_title, color='#dfb5b4'):
    '''新しい Admonition のスタイルを定義する

    Args:
        category(str): Admonition の種別を表す名前
        default_title(str): Admonition 枠内に表示する標題
        color(str): Admonition枠の色の RGB を与えるオプショナル引数。デフォルトでピンク。

    Returns:
        (str) -> (): admonition 表示のための関数。この関数の引数は `message :: str`。
        Admonition 枠に表示する標題を `title :: str` オプションで取ることもできる。
    '''

    style = ADMONITION_STYLE_TEMPLATE.replace('{color}', color)

    def admonition(message, title=None):
        # Admonition の内容の HTML 表現
        content = f'''
<div class="admonition admonition-{category}">
    <div class="admonition-title admonition-title-{category}">{title or default_title}</div>
    <div class="admonition-message admonition-message-{category}">{message}</div>
</div>'''

        display(HTML(f'{style}\n{content}'))  # セルへの Admonition の埋め込み

    return admonition

warn = new_admonition('warn', '警告')
hint = new_admonition('hint', 'ヒント', '#94b6e2')


from bokeh.plotting import output_notebook, show, figure
from bokeh.models import *
from bokeh.layouts import *

output_notebook()
