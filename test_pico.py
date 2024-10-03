from nb2fasthtml.core import *
from fasthtml.common import *

hdrs = [
    MarkdownJS(),
    HighlightJS(langs=['python', 'javascript', 'html', 'css',]),    
]

app, rt = fast_app(hdrs=hdrs)

nbs_dir = Path('example_nbs/')



def create_route(file_path):
    def route_handler():
        nb = render_nb(file_path)
        return nb
    return route_handler

def index_route():
    links = []
    for file_path in nbs_dir.rglob('*.ipynb'):
        if '.ipynb_checkpoints' not in file_path.parts:
            relative_path = file_path.relative_to(nbs_dir)
            route = f'/{relative_path.with_suffix("")}'
            links.append(Li(A(str(relative_path), href=route)))
    return Main(Ul(*links))

app.add_route('/', index_route)

for file_path in nbs_dir.rglob('*.ipynb'):
    if '.ipynb_checkpoints' not in file_path.parts:
        relative_path = file_path.relative_to(nbs_dir)
        route = f'/{relative_path.with_suffix("")}'
        app.add_route(route, create_route(file_path))


# def hw():
#     nb = render_nb(nbs_dir/'00_core.ipynb')
#     return nb
# app.add_route('/', hw)
serve()
