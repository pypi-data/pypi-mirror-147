from IPython.display import display, HTML

# Admonition枠のスタイルの雛形
#   color: 枠の色のプレイスホルダー
ADMONITION_STYLE = '''
<style>
div.admonition {
    border-radius: 5px;
    margin-bottom: 10px;
}
div.admonition-{category} { border: 5px solid {color}; }

div.admonition-title {
    color: #fffff8;
    padding: 0.5em 1em 0.5em 1em;
    font-size: larger;
    font-weight: bold;
}
div.admonition-title-{category} { background-color: {color}; }

div.admonition-message {}
div.admonition-message-{category} { padding: 1em; }
</style>'''

ADMONITION_CONTENT = '''
<div class="admonition admonition-{category}">
    <div class="admonition-title admonition-title-{category}">{title}</div>
    <div class="admonition-message admonition-message-{category}">{message}</div>
</div>'''

def new_admonition(category, default_title, color='#ccc'):
    '''新しい Admonition のスタイルを定義する

    Args:
        category(str): Admonition の種別を表す名前
        default_title(str): Admonition 枠内に表示する標題
        color(str): Admonition枠の色の RGB を与えるオプショナル引数。デフォルトでピンク。

    Returns:
        (str) -> (): admonition 表示のための関数。この関数の引数は `message :: str`。
        Admonition 枠に表示する標題を `title :: str` オプションで取ることもできる。
    '''

    _style   = ADMONITION_STYLE.replace('{category}', category).replace('{color}', color)
    _content = ADMONITION_CONTENT.replace('{category}', category)

    def admonition(message, title=None):
      content = _content.replace('{title}', title or default_title).replace('{message}', message)
      display(HTML(f'{_style}\n{content}'))

    return admonition

################################################################################

warn = new_admonition('warn', '警告', color='#f99')
hint = new_admonition('hint', 'ヒント', color='#9be')

def notebook_caution():
    warn('''<p>ほかのひとから共有されたノートブックの所有権は共有してくれた人に属します。そういうノートブックも編集できるので、あたかも所有権が自分にあるかのように錯覚します。でも、せっかく作業した結果を保存しようとしても、所有権がほかの人にあるノートブックは保存できず、エラーになってしまいます。

    <p>せっかく編集して自分好みの内容になっても、保存できなければ意味がありません。そこで、ノートブックを共有されたら、作業を始める前に<strong>自分が所有するノートブックとしてDropboxにコピーを保存</strong>しましょう。コピーを保存する方法は初回の資料を見て下さい。

    <p>いったん自分のノートブックとして保存すれば、それを自分の好きに編集し、保存できるようになります。自分のノートブックは Google Drive の <code>Colab Notebooks</code>にフォルダーに保存されます。

    <p>以前に作業したノートブックは、<code>Colab Notebooks</code>フォルダから該当するノートブックを探して開けば、作業を継続できます。''',
        title='超重要：落とし穴に注意')
warn = new_admonition('warn', '警告', color='#f99')
hint = new_admonition('hint', 'ヒント', color='#9be')
quiz = new_admonition('quiz', 'クイズ', color='purple')
why  = new_admonition('why', 'なんでだろう？', color='#8d8')
column = new_admonition('column', 'コラム', color='#88d')
_english_ = new_admonition('words_and_phrases', '英語の語義', color='#aaa')
def english(word, definition):
    _english_(definition, f'"{word}" の意味')

def notebook_caution():
    warn('''<p>ほかのひとから共有されたノートブックの所有権は共有してくれた人に属します。そういうノートブックも編集できるので、あたかも所有権が自分にあるかのように錯覚します。でも、せっかく作業した結果を保存しようとしても、所有権がほかの人にあるノートブックは保存できず、エラーになってしまいます。

    <p>せっかく編集して自分好みの内容になっても、保存できなければ意味がありません。そこで、ノートブックを共有されたら、作業を始める前に<strong>自分が所有するノートブックとしてDropboxにコピーを保存</strong>しましょう。コピーを保存する方法は初回の資料を見て下さい。

    <p>いったん自分のノートブックとして保存すれば、それを自分の好きに編集し、保存できるようになります。自分のノートブックは Google Drive の <code>Colab Notebooks</code>にフォルダーに保存されます。

    <p>以前に作業したノートブックは、<code>Colab Notebooks</code>フォルダから該当するノートブックを探して開けば、作業を継続できます。''',
        title='超重要：落とし穴に注意')
