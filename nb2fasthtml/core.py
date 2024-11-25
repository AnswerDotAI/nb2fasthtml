"""Create FastHTML from a NB"""

# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/00_core.ipynb.

# %% auto 0
__all__ = ['hdrs', 'get_frontmatter_raw', 'get_frontmatter_md', 'strip_list', 'get_nb_lang', 'render_md', 'render_code_source',
           'render_code_output', 'get_frontmatter', 'render_frontmatter', 'render_nb']

# %% ../nbs/00_core.ipynb
from fasthtml.common import *
from pathlib import Path
import json, yaml
from execnb.nbio import *
from execnb.shell import render_outputs
from typing import Callable
from functools import partial

# %% ../nbs/00_core.ipynb
hdrs = (MarkdownJS(), HighlightJS(langs=['python', 'javascript', 'html', 'css']))

# %% ../nbs/00_core.ipynb
def strip_list(l, val='\n'):
    start, end = 0, len(l)
    while start < end and l[start] == val: start += 1
    while end > start and l[end - 1] == val: end -= 1
    return l[start:end]

# %% ../nbs/00_core.ipynb
def get_nb_lang(nb):
    "Get the language of `nb`"
    return nb['metadata']['kernelspec']['language']

# %% ../nbs/00_core.ipynb
def render_md(c, container=Div):
    "Default rendering function; adds class 'marked' for use with highlight-js"
    return container(c, cls="marked")

# %% ../nbs/00_core.ipynb
def render_code_source(cell, lang='python', render_md=render_md):
    if not cell.source: return ''
    return render_md(f'''\n```{lang}\n{cell.source}\n```\n''')

# %% ../nbs/00_core.ipynb
def render_code_output(cell, lang='python', pygments=False, wrapper=Footer):
    if not cell.outputs: return ''
    res = render_outputs(cell.outputs, pygments=pygments)
    if res: return wrapper(NotStr(res))

# %% ../nbs/00_core.ipynb
_RE_FM_BASE=r'''^---\s*
(.*?\S+.*?)
---\s*'''

# %% ../nbs/00_core.ipynb
_re_fm_nb = re.compile(_RE_FM_BASE+'$', flags=re.DOTALL)
_re_fm_md = re.compile(_RE_FM_BASE, flags=re.DOTALL)

# %% ../nbs/00_core.ipynb
def _fm2dict(s:str, nb=True):
    "Load YAML frontmatter into a `dict`"
    re_fm = _re_fm_nb if nb else _re_fm_md
    match = re_fm.search(s.strip())
    return yaml.safe_load(match.group(1)) if match else {}

# %% ../nbs/00_core.ipynb
def _md2dict(s:str):
    "Convert H1 formatted markdown cell to frontmatter dict"
    if '#' not in s: return {}
    m = re.search(r'^#\s+(\S.*?)\s*$', s, flags=re.MULTILINE)
    if not m: return {}
    res = {'title': m.group(1)}
    m = re.search(r'^>\s+(\S.*?)\s*$', s, flags=re.MULTILINE)
    if m: res['description'] = m.group(1)
    r = re.findall(r'^-\s+(\S.*:.*\S)\s*$', s, flags=re.MULTILINE)
    if r:
        try: res.update(yaml.safe_load('\n'.join(r)))
        except Exception as e: warn(f'Failed to create YAML dict for:\n{r}\n\n{e}\n')
    return res

# %% ../nbs/00_core.ipynb
def get_frontmatter(source,     # metatadata source (jupyter cell or md content)
                    nb_file=True,    # Is jupyter nb or qmd file
                    md_fm=False # md or raw style frontmatter
                   ):
    if not nb_file: return _fm2dict(source)
    if md_fm:       return _md2dict(source.source)
    return _fm2dict(source.source, nb_file)    

get_frontmatter_raw = partial(get_frontmatter, md_fm=False)
get_frontmatter_md =  partial(get_frontmatter, md_fm=True)

# %% ../nbs/00_core.ipynb
def render_frontmatter(fm):
    desc = P(fm['description']) if 'description' in fm else ()
    return Div(cls='frontmatter')(
        H1(fm['title']), desc
    )

# %% ../nbs/00_core.ipynb
def render_nb(fpath, # Path to Jupyter Notebook
              wrapper=Main, #Wraps entire rendered NB, default is for pico
              cls='container', # cls to be passed to wrapper, default is for pico
              md_cell_wrapper=Div, # Wraps markdown cell
              md_fn=render_md, # md -> rendered html
              code_cell_wrapper=Card, # Wraps Source Code (body) + Outputs (footer)
              cd_fn=render_code_source, # code cell -> code source rendered html
              out_fn=render_code_output, # code cell -> code output rendered html
              get_fm=get_frontmatter_md, # How to read frontmatter cell
              fm_fn:None|Callable=render_frontmatter, # Frontmatter -> FT components
              **kwargs # Passed to wrapper
             ): 
    nb = read_nb(fpath)
    res, content_start_idx = [], 0
    if fm_fn: 
        content_start_idx = 1
        fm = get_fm(nb.cells[0])
        res.append(fm_fn(fm))
    for cell in nb.cells[content_start_idx:]:
        if   cell['cell_type']=='code'    : res.append(code_cell_wrapper(cd_fn(cell), out_fn(cell)))
        elif cell['cell_type']=='markdown': res.append(md_cell_wrapper(md_fn(cell.source)))
    return wrapper(cls=cls, **kwargs)(*res)
