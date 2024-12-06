import os

from dkdc_util import now, uuid, get_dkdc_dir
from dkdc_state import State, ibis, dt


# class
class Vault(State):
    def __init__(self, dbpath: str = None):
        if dbpath is None:
            dbpath = os.path.join(get_dkdc_dir(), "vault.db")
        super().__init__(dbpath=dbpath)

    def _cons(self) -> (ibis.BaseBackend, ibis.BaseBackend):
        # create write connection
        wcon = ibis.sqlite.connect(self.dbpath)

        # create tables in write connection
        ## sessions data
        self.sessions_table_name = "sessions"
        schema = ibis.schema(
            {
                "idx": dt.timestamp,
                "id": str,
                "user_id": str,
                "status": str,
                "description": str,
                "labels": str,  # comma-separated list of labels
            }
        )
        if self.sessions_table_name not in wcon.list_tables():
            wcon.create_table(self.sessions_table_name, schema=schema)

        ## secrets data
        self.secrets_table_name = "secrets"
        schema = ibis.schema(
            {
                "idx": dt.timestamp,
                "user_id": str,
                "key": str,
                "value": bytes,
                "salt": bytes,
                "pepper": bytes,
                "cayenne": bytes,
                "status": str,
                "description": str,
                "labels": str,  # comma-separated list of labels
            }
        )
        if self.secrets_table_name not in wcon.list_tables():
            wcon.create_table(self.secrets_table_name, schema=schema)

        ## tokens data
        self.tokens_table_name = "tokens"
        schema = ibis.schema(
            {
                "idx": dt.timestamp,
                "user_id": str,
                "key": str,
                "value": bytes,
                "salt": bytes,
                "pepper": bytes,
                "cayenne": bytes,
                "expires_at": dt.timestamp,
                "status": str,
                "description": str,
                "labels": str,  # comma-separated list of labels
            }
        )
        if self.tokens_table_name not in wcon.list_tables():
            wcon.create_table(self.tokens_table_name, schema=schema)

        # create read connection
        rcon = ibis.duckdb.connect()

        # create tables in read connection
        for table_name in wcon.list_tables():
            rcon.read_sqlite(self.dbpath, table_name=table_name)

        return wcon, rcon

    # tables
    def sessions_t(self, user_id: str = None):
        # get sessions data
        t = self.rcon.table(self.sessions_table_name)

        # filter by user_id
        if user_id:
            t = t.filter(t["user_id"] == user_id)

        # get only the latest metadata
        t = (
            t.mutate(
                rank=ibis.row_number().over(
                    ibis.window(
                        group_by=["id", "user_id"],
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

    def secrets_t(self, user_id: str = None):
        # get secrets data
        t = self.rcon.table(self.secrets_table_name)

        # filter by user_id
        if user_id:
            t = t.filter(t["user_id"] == user_id)

        # get only the latest metadata
        t = (
            t.mutate(
                rank=ibis.row_number().over(
                    ibis.window(
                        group_by=["user_id", "key"],
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

    def tokens_t(self, user_id: str = None):
        # get tokens data
        t = self.rcon.table(self.tokens_table_name)

        # filter by user_id
        if user_id:
            t = t.filter(t["user_id"] == user_id)

        # get only the latest metadata
        t = (
            t.mutate(
                rank=ibis.row_number().over(
                    ibis.window(
                        group_by=["user_id", "key"],
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
    def contains_session(self, user_id: str, id: str) -> bool:
        t = self.sessions_t(user_id=user_id)
        return t.filter(t["id"] == id).count().to_pyarrow().as_py() > 0

    def contains_secret(self, user_id: str, key: str) -> bool:
        t = self.secrets_t(user_id=user_id)
        return t.filter(t["key"] == key).count().to_pyarrow().as_py() > 0

    def contains_token(self, user_id: str, key: str) -> bool:
        t = self.tokens_t(user_id=user_id)
        return t.filter(t["key"] == key).count().to_pyarrow().as_py() > 0

    # get record
    def get_session(self, user_id: str, id: str):
        if not self.contains_session(user_id=user_id, id=id):
            raise ValueError(f"Session {id} for user {user_id} does not exist")

        t = self.sessions_t(user_id=user_id)
        return t.filter(t["id"] == id).to_pyarrow().to_pylist()[0]

    def get_secret(self, user_id: str, key: str):
        if not self.contains_secret(user_id=user_id, key=key):
            raise ValueError(f"Secret {key} for user {user_id} does not exist")

        t = self.secrets_t(user_id=user_id)
        return t.filter(t["key"] == key).to_pyarrow().to_pylist()[0]

    def get_token(self, user_id: str, key: str):
        if not self.contains_token(user_id=user_id, key=key):
            raise ValueError(f"Token {key} for user {user_id} does not exist")

        t = self.tokens_t(user_id=user_id)
        return t.filter(t["key"] == key).to_pyarrow().to_pylist()[0]

    # append record
    def append_session(
        self, user_id: str, id: str = None, status: str = None, description: str = None
    ):
        id = id or uuid()

        # check if session already exists
        if self.contains_session(user_id=user_id, id=id):
            raise ValueError(f"Session {id} for user {user_id} already exists")

        # insert session data
        data = {
            "idx": [now()],
            "id": [id],
            "user_id": [user_id],
            "status": [status],
            "description": [description],
        }
        self.wcon.insert(self.sessions_table_name, data)

        return self.get_session(user_id=user_id, id=id)

    def append_secret(
        self,
        user_id: str,
        key: str,
        value: str,
        salt: str = None,
        pepper: str = None,
        cayenne: str = None,
        status: str = None,
        description: str = None,
    ):
        # check if secret already exists
        if self.contains_secret(user_id=user_id, key=key):
            raise ValueError(f"Secret {key} for user {user_id} already exists")

        # insert secret data
        data = {
            "idx": [now()],
            "user_id": [user_id],
            "key": [key],
            "value": [value],
            "salt": [salt],
            "pepper": [pepper],
            "cayenne": [cayenne],
            "status": [status],
            "description": [description],
        }
        self.wcon.insert(self.secrets_table_name, data)

        return self.get_secret(user_id=user_id, key=key)

    def append_token(
        self,
        user_id: str,
        key: str,
        value: bytes,
        salt: str = None,
        pepper: str = None,
        cayenne: str = None,
        status: str = None,
        expires_at: str = None,
        description: str = None,
    ):
        # check if token already exists
        if self.contains_token(user_id=user_id, key=key):
            raise ValueError(f"Token {key} for user {user_id} already exists")

        # insert token data
        data = {
            "idx": [now()],
            "user_id": [user_id],
            "key": [key],
            "value": [value],
            "salt": [salt],
            "pepper": [pepper],
            "cayenne": [cayenne],
            "status": [status],
            "expires_at": [expires_at],
            "description": [description],
        }
        self.wcon.insert(self.tokens_table_name, data)

        return self.get_token(user_id=user_id, key=key)

    # update record
    def update_session(self, id: str, user_id: str, status: str, description: str):
        if not self.contains_session(id=id, user_id=user_id):
            raise ValueError(f"Session {id} for user {user_id} does not exist")

        data = {
            "idx": [now()],
            "id": [id],
            "user_id": [user_id],
            "status": [status],
            "description": [description],
        }
        self.wcon.insert(self.sessions_table_name, data)

        return self.get_session(id)

    def update_secret(
        self, user_id: str, key: str, value: str, status: str, description: str
    ):
        if not self.contains_secret(user_id=user_id, key=key):
            raise ValueError(f"Secret {key} for user {user_id} does not exist")

        data = {
            "idx": [now()],
            "user_id": [user_id],
            "key": [key],
            "value": [value],
            "status": [status],
            "description": [description],
        }
        self.wcon.insert(self.secrets_table_name, data)

        return self.get_secret(key)

    def update_token(
        self,
        user_id: str,
        key: str,
        value: str,
        status: str = None,
        expires_at: str = None,
        description: str = None,
    ):
        if not self.contains_token(user_id=user_id, key=key):
            raise ValueError(f"Token {key} for user {user_id} does not exist")

        data = {
            "idx": [now()],
            "user_id": [user_id],
            "key": [key],
            "value": [value],
            "status": [status],
            "expires_at": [expires_at],
            "description": [description],
        }
        self.wcon.insert(self.tokens_table_name, data)

        return self.get_token(user_id=user_id, key=key)

    # aliases
