from nb2fasthtml.core import *
from fasthtml.common import *

hdrs = (Script(type="module", src="https://cdn.jsdelivr.net/npm/zero-md@3?register"),
        Script(src="https://cdn.tailwindcss.com"),
        Script(src="https://cdn.jsdelivr.net/npm/uikit@3.21.6/dist/js/uikit.min.js"),
        Script(src="https://cdn.jsdelivr.net/npm/uikit@3.21.6/dist/js/uikit-icons.min.js"),
        Script(type="module", src="https://unpkg.com/franken-wc@0.0.6/dist/js/wc.iife.js"),
        Link(rel="stylesheet", href="https://unpkg.com/franken-wc@0.0.6/dist/css/blue.min.css"))

app = FastHTML(hdrs=hdrs)

nbs_dir = Path('example_nbs/')


def CodeCard(s,o):
    return Card(s, footer=o, cls='mx-20')

def create_route(file_path):
    def route_handler():
        nb = render_nb(file_path, code_cell_wrapper=CodeCard, cls='mx-20 space-y-6')
        return nb
    return route_handler

def index_route():
    links = []
    for file_path in nbs_dir.rglob('*.ipynb'):
        if '.ipynb_checkpoints' not in file_path.parts:
            relative_path = file_path.relative_to(nbs_dir)
            route = f'/{relative_path.with_suffix("")}'
            links.append(Li(A(str(relative_path), href=route)))
    return Div(Ul(*links))

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
