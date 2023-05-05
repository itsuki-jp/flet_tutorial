import flet
from flet import (
    Checkbox,
    Column,
    FloatingActionButton,
    IconButton,
    Page,
    Row,
    Tab,
    Tabs,
    TextField,
    UserControl,
    colors,
    icons,
)
from tinydb import TinyDB, Query


class TodoApp(UserControl):
    def __init__(self, db):
        super().__init__()
        self.db = db

    def show_db(self):
        for item in self.db:
            id = item.doc_id
            t_name = item["name"]
            t_status = item["completed"]
            task = Task(
                t_name,
                self.task_status_change,
                self.task_delete,
                self.task_change_db,
                id,
                t_status,
            )
            self.tasks.controls.append(task)
            self.new_task.value = ""

    def build(self):
        self.new_task = TextField(hint_text="Whats needs to be done?", expand=True)
        self.tasks = Column()
        self.filter = Tabs(
            selected_index=0,
            on_change=self.tabs_changed,
            tabs=[Tab(text="all"), Tab(text="active"), Tab(text="completed")],
        )
        self.show_db()

        # application's root control (i.e. "view") containing all other controls
        return Column(
            width=600,
            controls=[
                Row(
                    controls=[
                        self.new_task,
                        FloatingActionButton(icon=icons.ADD, on_click=self.add_clicked),
                    ],
                ),
                Column(
                    spacing=25,
                    controls=[
                        self.filter,
                        self.tasks,
                    ],
                ),
            ],
        )

    def add_clicked(self, e):
        id = self.db.insert({"name": self.new_task.value, "completed": False})
        task = Task(
            self.new_task.value,
            self.task_status_change,
            self.task_delete,
            self.task_change_db,
            id,
        )
        self.tasks.controls.append(task)
        self.new_task.value = ""
        self.update()

    def task_status_change(self, task):
        self.update()

    def task_delete(self, task):
        self.db.remove(doc_ids=[task.get_id()])
        self.tasks.controls.remove(task)
        self.update()

    def task_change_db(self, task_name, completed, id):
        self.db.update({"name": task_name, "completed": completed}, doc_ids=[id])

    def update(self):
        status = self.filter.tabs[self.filter.selected_index].text
        for task in self.tasks.controls:
            task.visible = (
                status == "all"
                or (status == "active" and task.completed == False)
                or (status == "completed" and task.completed)
            )
        super().update()

    def tabs_changed(self, e):
        self.update()


class Task(UserControl):
    def __init__(
        self,
        task_name,
        task_status_change,
        task_delete,
        task_change_db,
        id,
        completed=False,
    ):
        super().__init__()
        self.completed = completed
        self.task_name = task_name
        self.task_status_change = task_status_change
        self.task_delete = task_delete
        self.task_change_db = task_change_db
        self.id = id

    def build(self):
        self.display_task = Checkbox(
            value=False, label=self.task_name, on_change=self.status_changed
        )
        self.edit_name = TextField(expand=1)

        self.display_view = Row(
            alignment="spaceBetween",
            vertical_alignment="center",
            controls=[
                self.display_task,
                Row(
                    spacing=0,
                    controls=[
                        IconButton(
                            icon=icons.CREATE_OUTLINED,
                            tooltip="Edit To-Do",
                            on_click=self.edit_clicked,
                        ),
                        IconButton(
                            icons.DELETE_OUTLINE,
                            tooltip="Delete To-Do",
                            on_click=self.delete_clicked,
                        ),
                    ],
                ),
            ],
        )

        self.edit_view = Row(
            visible=False,
            alignment="spaceBetween",
            vertical_alignment="center",
            controls=[
                self.edit_name,
                IconButton(
                    icon=icons.DONE_OUTLINE_OUTLINED,
                    icon_color=colors.GREEN,
                    tooltip="Update To-Do",
                    on_click=self.save_clicked,
                ),
            ],
        )
        self.display_task.value = self.completed
        return Column(controls=[self.display_view, self.edit_view])

    def edit_clicked(self, e):
        self.edit_name.value = self.display_task.label
        self.display_view.visible = False
        self.edit_view.visible = True
        self.update()

    def save_clicked(self, e):
        self.task_change_db(self.edit_name.value, self.completed, self.id)
        self.display_task.label = self.edit_name.value
        self.display_view.visible = True
        self.edit_view.visible = False
        self.update()

    def status_changed(self, e):
        self.completed = self.display_task.value
        self.task_change_db(self.display_task.label, self.completed, self.id)
        self.task_status_change(self)

    def delete_clicked(self, e):
        self.task_delete(self)

    def get_id(self):
        return self.id


def main(page: Page):
    page.title = "ToDo App"
    page.horizontal_alignment = "center"
    page.update()

    # read/ create database
    db = TinyDB("./todo_app/db.json")

    # create application instance
    app = TodoApp(db)

    # add application's root control to the page
    page.add(app)


flet.app(target=main)
