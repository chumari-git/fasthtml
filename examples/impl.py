# AUTOGENERATED! DO NOT EDIT! File to edit: impl.ipynb.

# %% auto 0
__all__ = ['id_curr', 'id_list', 'TODO_LIST', 'tid', 'TodoItem', 'mk_input', 'get_card', 'find_todo', 'get_editform']

# %% impl.ipynb 2
from dataclasses import dataclass
from typing import Any,Union,Tuple,List

from fastcore.utils import *
from fastcore.xml import *
from fastcore.xtras import hl_md
from fasthtml import *

# %% impl.ipynb 7
id_curr = 'current-todo'
id_list = 'todo-list'
def tid(id): return f'todo-{id}'

# %% impl.ipynb 8
@dataclass
class TodoItem():
    title: str; id: int = -1; done: bool = False

    def __xt__(self):
        show = AX(self.title, f'/todos/{self.id}', id_curr)
        edit = AX('edit',     f'/edit/{self.id}' , id_curr)
        dt = ' (done)' if self.done else ''
        return Li(show, dt, ' | ', edit, id=tid(self.id))

    _repr_html_ = showtags

#|export
TODO_LIST = [TodoItem(id=0, title="Start writing todo list", done=True),
             TodoItem(id=1, title="???", done=False),
             TodoItem(id=2, title="Profit", done=False)]

# %% impl.ipynb 12
def mk_input(**kw): return Input(id="new-title", name="title", placeholder="New Todo", **kw)

def get_card(todos):
    add = Form(Group(mk_input(), Button("Add")),
               hx_post="/", target_id=id_list, hx_swap="beforeend")
    return Card(Ul(*todos, id=id_list),
                header=add, footer=Div(id=id_curr))

# %% impl.ipynb 14
def find_todo(id):
    try: return next(o for o in TODO_LIST if o.id==id)
    except: raise NotFoundException(f'Todo #{id}') from None

# %% impl.ipynb 16
def get_editform(id):
    todo = find_todo(id)
    res = Form(Group(Input(id="title"), Button("Save")),
        Hidden(id="id"), Checkbox(id="done", label='Done'),
        hx_put="/", target_id=tid(id), id="edit")
    fill_form(res, todo)
    return res