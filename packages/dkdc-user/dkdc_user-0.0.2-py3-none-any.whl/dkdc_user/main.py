import os

from dkdc_util import now, uuid, get_dkdc_dir
from dkdc_state import State, ibis, dt


# class
class User(State):
    def __init__(self, dbpath: str = None):
        if dbpath is None:
            dbpath = os.path.join(get_dkdc_dir(), "user.db")
        super().__init__(dbpath=dbpath)

    def _cons(self) -> (ibis.BaseBackend, ibis.BaseBackend):
        # create write connection
        wcon = ibis.sqlite.connect(self.dbpath)

        # create tables in write connection
        ## users data
        self.users_table_name = "users"
        schema = ibis.schema(
            {
                "idx": dt.timestamp,
                "id": str,
                "username": str,
                "status": str,
                "description": str,
                "labels": str,  # comma-separated list of labels
            }
        )
        if self.users_table_name not in wcon.list_tables():
            wcon.create_table(self.users_table_name, schema=schema)

        # create read connection
        rcon = ibis.duckdb.connect()

        # create tables in read connection
        for table_name in wcon.list_tables():
            rcon.read_sqlite(self.dbpath, table_name=table_name)

        return wcon, rcon

    # tables
    def users_t(self, username: str = None):
        # get users data
        t = self.rcon.table(self.users_table_name)

        # filter by username
        if username:
            t = t.filter(t["username"] == username)

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
        t = t.order_by(ibis.desc("idx"))

        # return the data
        return t

    # contains
    def contains_user(self, id: str = None, username: str = None) -> bool:
        assert id or username, "id or username must be provided"
        assert not (id and username), "only one of id or username must be provided"

        t = self.users_t()
        if id:
            return t.filter(t["id"] == id).count().to_pyarrow().as_py() > 0
        else:
            return t.filter(t["username"] == username).count().to_pyarrow().as_py() > 0

    # get record
    def get_user(self, username: str):
        if not self.contains_user(username=username):
            raise ValueError(f"User {username} does not exist")

        t = self.users_t(username=username)
        return t.to_pyarrow().to_pylist()[0]

    # append record
    def append_user(
        self,
        username: str,
        status: str = None,
        description: str = None,
        labels: list[str] = None,
    ):
        # check if user already exists
        if self.contains_user(username=username):
            raise ValueError(f"User {username} already exists")

        # insert user data
        data = {
            "idx": [now()],
            "id": [uuid()],
            "username": [username],
            "status": [status],
            "description": [description],
            "labels": [",".join(labels) if labels else None],
        }
        self.wcon.insert(self.users_table_name, data)

        return self.get_user(username=username)

    # update record
    def update_user(
        self, username: str, status: str, description: str, labels: list[str] = None
    ):
        if not self.contains_user(username=username):
            raise ValueError(f"User {username} does not exist")

        u = self.get_user(username=username)
        id = u["id"]

        data = {
            "idx": [now()],
            "id": [id],
            "username": [username],
            "status": [status],
            "description": [description],
            "labels": [",".join(labels) if labels else None],
        }
        self.wcon.insert(self.users_table_name, data)

        return self.get_user(username=username)

    # aliases
    __call__ = get_user
    t = users_t
