from nb2fasthtml.core import *
from fasthtml.common import *

hdrs = [
    MarkdownJS(),
    HighlightJS(langs=['python', 'javascript', 'html', 'css',]),    
]

app, rt = fast_app(hdrs=hdrs)

@rt
def index():
    return render_nb('demo.ipynb')

serve()
