from IPython.core.display import display, HTML, Markdown

def md(*paragraphs):
  for p in paragraphs:
    display(Markdown(p + '\n\n'))
