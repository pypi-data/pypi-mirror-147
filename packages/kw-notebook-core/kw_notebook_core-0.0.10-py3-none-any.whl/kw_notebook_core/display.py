from IPython.core.display import display, HTML, Markdown

def md(*paragraphs):
  for p in paragraphs:
    display(Markdown(p + '\n\n'))

# @title 実装コード { run: "auto", vertical-output: true, display-mode: "form" }

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

def notebook_caution():
    warn('''<p>ほかのひとから共有されたノートブックの所有権は共有してくれた人に属します。そういうノートブックも編集できるので、あたかも所有権が自分にあるかのように錯覚します。でも、せっかく作業した結果を保存しようとしても、所有権がほかの人にあるノートブックは保存できず、エラーになってしまいます。

    <p>せっかく編集して自分好みの内容になっても、保存できなければ意味がありません。そこで、ノートブックを共有されたら、作業を始める前に<strong>自分が所有するノートブックとしてDropboxにコピーを保存</strong>しましょう。コピーを保存する方法は初回の資料を見て下さい。

    <p>いったん自分のノートブックとして保存すれば、それを自分の好きに編集し、保存できるようになります。自分のノートブックは Google Drive の <code>Colab Notebooks</code>にフォルダーに保存されます。

    <p>以前に作業したノートブックは、<code>Colab Notebooks</code>フォルダから該当するノートブックを探して開けば、作業を継続できます。''',
        title='超重要：落とし穴に注意')


from bokeh.plotting import output_notebook, show, figure
from bokeh.models import *
from bokeh.layouts import *

output_notebook()
