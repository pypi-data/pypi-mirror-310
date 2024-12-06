import os

from dkdc_util import now, uuid, get_dkdc_dir
from dkdc_state import State, ibis, dt


# class
class Todo(State):
    def __init__(self, dbpath: str = None):
        if dbpath is None:
            dbpath = os.path.join(get_dkdc_dir(), "todo.db")
        super().__init__(dbpath=dbpath)

    def _cons(self) -> (ibis.BaseBackend, ibis.BaseBackend):
        # create write connection
        wcon = ibis.sqlite.connect(self.dbpath)

        # create tables in write connection
        ## todos data
        self.todos_table_name = "todos"
        schema = ibis.schema(
            {
                "idx": dt.timestamp,
                "id": str,
                "user_id": str,
                "subject": str,
                "body": str,
                "priority": int,
                "status": str,
                "description": str,
                "labels": str,  # comma-separated list of labels
            }
        )
        if self.todos_table_name not in wcon.list_tables():
            wcon.create_table(self.todos_table_name, schema=schema)

        # create read connection
        rcon = ibis.duckdb.connect()

        # create tables in read connection
        for table_name in wcon.list_tables():
            rcon.read_sqlite(self.dbpath, table_name=table_name)

        return wcon, rcon

    # tables
    def todos_t(self, user_id: str = None):
        # get todos data
        t = self.rcon.table(self.todos_table_name)

        # filter by user_id
        if user_id:
            t = t.filter(t["user_id"] == user_id)

        # get only the latest metadata
        t = (
            t.mutate(
                rank=ibis.row_number().over(
                    ibis.window(
                        group_by="id",
                        order_by=ibis.desc("idx"),
                    )
                )
            )
            .filter(ibis._["rank"] == 0)
            .drop("rank")
        )

        # comma-separated lists to arrays
        t = t.mutate(labels=t["labels"].split(","))

        # order
        t = t.order_by(ibis.asc("priority"), ibis.desc("idx"))

        # return the data
        return t

    # contains
    def contains_todo(self, id: str, user_id: str = None) -> bool:
        t = self.todos_t(user_id=user_id)
        return t.filter(t["id"] == id).count().to_pyarrow().as_py() > 0

    # get record
    def get_todos(self, user_id: str = None):
        t = self.todos_t(user_id=user_id)

        return t.to_pyarrow().to_pylist()

    def get_todo(self, id: str, user_id: str = None):
        t = self.todos_t(user_id=user_id)
        return t.filter(t["id"] == id).to_pyarrow().to_pylist()[0]

    # append record
    def append_message(
        self,
        to: str,
        from_: str,
        convo_id: str,
        thread_id: str,
        subject: str,
        body: str,
        attachments: list[str] = None,
        version: int = None,
        status: str = None,
        description: str = None,
        labels: list[str] = None,
    ):
        assert (to is not None) and (from_ is not None), "to and from_ are required"

        data = {
            "idx": [now()],
            "id": [uuid()],
            "to": [to],
            "from": [from_],
            "convo_id": [convo_id],
            "thread_id": [thread_id],
            "subject": [subject],
            "body": [body],
            "attachments": [",".join(attachments) if attachments else None],
            "version": [version],
            "status": [status],
            "description": [description],
            "labels": [",".join(labels) if labels else None],
        }
        self.wcon.insert(self.todos_table_name, data)

        return self.get_todo(id=data["id"][0])

    def append_todo(
        self,
        id: str,
        user_id: str,
        subject: str,
        body: str,
        priority: int = 100,
        status: str = None,
        description: str = None,
        labels: list[str] = None,
    ):
        data = {
            "idx": [now()],
            "id": [id],
            "user_id": [user_id],
            "subject": [subject],
            "body": [body],
            "priority": [priority],
            "status": [status],
            "description": [description],
            "labels": [",".join(labels) if labels else None],
        }
        self.wcon.insert(self.todos_table_name, data)

        return self.get_todo(id=id)

    # update record
    def update_todo(
        self,
        id: str,
        user_id: str,
        subject: str,
        body: str,
        priority: int = 100,
        status: str = None,
        description: str = None,
        labels: list[str] = None,
    ):
        if not self.contains_todo(id=id):
            raise ValueError(f"todo {id} does not exist")

        data = {
            "idx": [now()],
            "id": [id],
            "user_id": [user_id],
            "subject": [subject],
            "body": [body],
            "priority": [priority],
            "status": [status],
            "description": [description],
            "labels": [",".join(labels) if labels else None],
        }
        self.wcon.insert(self.todos_table_name, data)

        return self.get_todo(id=id)

    # aliases
    __call__ = get_todos
    t = todos_t
