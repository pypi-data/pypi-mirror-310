# imports
from shiny import ui, render, reactive, module

from dkdc_todo import Todo
from dkdc_util import uuid_parts
from dkdc_state import ibis

# global state
todo = Todo()


# individual todo card
@module.ui
def todo_card(header, body, priority):
    return ui.card(
        ui.card_header(header),
        ui.layout_columns(
            ui.markdown(body),
            ui.input_slider("priority", "priority", value=priority, min=0, max=100),
        ),
        ui.layout_columns(
            ui.input_action_button("done", "done", class_="btn-primary"),
            ui.input_action_button("delete", "delete", class_="btn-danger"),
        ),
    )


@module.server
def todo_card_server(input, output, session, todos_modified):
    def _get_id(session):
        # TODO: this isn't ideal
        return str(session.ns).split("-")[-1]

    @reactive.Effect
    @reactive.event(input.priority, ignore_init=True)
    def _update_priority():
        id = _get_id(session)
        t = todo.get_todo(id=id)
        todo.update_todo(
            id=id,
            user_id=t["user_id"],
            subject=t["subject"],
            body=t["body"],
            priority=input.priority(),
            status=t["status"],
            description=t["description"],
            labels=t["labels"],
        )
        todos_modified()

    @reactive.Effect
    @reactive.event(input.done, ignore_init=True)
    def _done():
        id = _get_id(session)
        t = todo.get_todo(id=id)
        todo.update_todo(
            id=id,
            user_id=t["user_id"],
            subject=t["subject"],
            body=t["body"],
            priority=t["priority"],
            status="done",
            description=t["description"],
            labels=t["labels"],
        )
        todos_modified()

    @reactive.Effect
    @reactive.event(input.delete, ignore_init=True)
    def _delete():
        id = _get_id(session)
        t = todo.get_todo(id=id)
        todo.update_todo(
            id=id,
            user_id=t["user_id"],
            subject=t["subject"],
            body=t["body"],
            priority=t["priority"],
            status="deleted",
            description=t["description"],
            labels=t["labels"],
        )
        todos_modified()


# page of todos
@module.ui
def todo_page():
    return ui.page_fluid(
        ui.layout_columns(
            ui.card(
                ui.card_header("add todo"),
                ui.layout_columns(
                    ui.input_text("todo", "todo"),
                    ui.input_slider("priority", "priority", value=0, min=0, max=100),
                ),
                ui.layout_columns(
                    ui.input_action_button("add", "add", class_="btn-primary"),
                    ui.input_action_button("clear", "clear all", class_="btn-danger"),
                ),
            ),
            ui.card(
                ui.card_header("todos stats"),
                ui.output_ui("stats"),
            ),
        ),
        ui.card(
            ui.card_header("todos"),
            ui.output_ui("todos_list"),
        ),
    )


@module.server
def todo_server(input, output, session):
    # reactive values
    todo_modified = reactive.Value(0)

    # servers
    [
        todo_card_server(
            t["id"], todos_modified=lambda: todo_modified.set(todo_modified.get() + 1)
        )
        for t in todo.get_todos()
    ]

    # effects
    @render.ui
    def stats():
        _ = todo_modified.get()
        return ui.markdown(
            f"total todos: {todo.t().filter(ibis._["status"].isnull()).count().to_pyarrow().as_py()}"
        )

    @reactive.Effect
    @reactive.event(input.add, ignore_init=True)
    def _add():
        _, id = uuid_parts()
        todo_text = input.todo()
        todo_priority = input.priority()
        todo.append_todo(
            id=id,
            user_id=None,
            subject=None,
            body=todo_text,
            priority=todo_priority,
        )
        todo_card_server(
            id, todos_modified=lambda: todo_modified.set(todo_modified.get() + 1)
        )
        todo_modified.set(todo_modified.get() + 1)

    @reactive.Effect
    @reactive.event(input.clear, ignore_init=True)
    def _clear():
        for t in todo.t().filter(ibis._["status"].isnull()).to_pyarrow().to_pylist():
            todo.update_todo(
                id=t["id"],
                user_id=t["user_id"],
                subject=t["subject"],
                body=t["body"],
                priority=t["priority"],
                status="deleted",
                description=t["description"],
                labels=t["labels"],
            )
        todo_modified.set(todo_modified.get() + 1)

    @render.ui
    def todos_list():
        _ = todo_modified.get()
        return (
            ui.layout_column_wrap(
                *[
                    todo_card(t["id"], t["id"], t["body"], t["priority"])
                    for t in todo.t()
                    .filter(ibis._["status"].isnull())
                    .to_pyarrow()
                    .to_pylist()
                ]
            ),
        )
