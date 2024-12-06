import os

from dkdc_util import now, uuid, get_dkdc_dir
from dkdc_state import State, ibis, dt

from dkdc_user import User
from dkdc_lake import Lake
from dkdc_lake.file import File


# class
class Chat(State):
    def __init__(self, dbpath: str = None):
        if dbpath is None:
            dbpath = os.path.join(get_dkdc_dir(), "chat.db")
        super().__init__(dbpath=dbpath)

        # other states
        self.user = User()
        self.lake = Lake()

    def _cons(self) -> (ibis.BaseBackend, ibis.BaseBackend):
        # create write connection
        wcon = ibis.sqlite.connect(self.dbpath)

        # create tables in write connection
        ## messages data
        self.messages_table_name = "messages"
        schema = ibis.schema(
            {
                "idx": dt.timestamp,
                "id": str,
                "to": str,
                "from": str,
                "convo_id": str,
                "thread_id": str,
                "subject": str,
                "body": str,
                "attachments": str,  # comma-separated list of attachment ids
                "version": int,
                "status": str,
                "description": str,
                "labels": str,  # comma-separated list of labels
            }
        )
        if self.messages_table_name not in wcon.list_tables():
            wcon.create_table(self.messages_table_name, schema=schema)

        # create read connection
        rcon = ibis.duckdb.connect()

        # create tables in read connection
        for table_name in wcon.list_tables():
            rcon.read_sqlite(self.dbpath, table_name=table_name)

        return wcon, rcon

    # tables
    def messages_t(self, user_id: str = None):
        # get messages data
        t = self.rcon.table(self.messages_table_name)

        # filter by user_id
        if user_id:
            t = t.filter((t["to"] == user_id) | (t["from"] == user_id))

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
        t = t.mutate(attachments=t["attachments"].split(","))
        t = t.mutate(labels=t["labels"].split(","))

        # order
        t = t.order_by(ibis.desc("idx"))

        # return the data
        return t

    # contains
    def contains_message(self, id: str, user_id: str = None) -> bool:
        t = self.messages_t(user_id=user_id)
        return t.filter(t["id"] == id).count().to_pyarrow().as_py() > 0

    # get record
    def get_messages(
        self, user_id: str = None, convo_id: str = None, thread_id: str = None
    ):
        t = self.messages_t(user_id=user_id)

        if convo_id:
            t = t.filter(t["convo_id"] == convo_id)
        if thread_id:
            t = t.filter(t["thread_id"] == thread_id)

        return t.to_pyarrow().to_pylist()

    def get_message(self, id: str, user_id: str = None):
        t = self.messages_t(user_id=user_id)
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
        attachments: list[File] = None,
        version: int = None,
        status: str = None,
        description: str = None,
        labels: list[str] = None,
    ):
        assert (to is not None) and (from_ is not None), "to and from_ are required"
        assert all(
            isinstance(a, File) for a in attachments
        ), "attachments must be a list of File objects"

        # message id
        id = uuid()

        # TODO: bad idea? easier for testing for now
        if not self.user.contains_user(username=from_):
            self.user.append_user(username=from_)

        # TODO: should users go in the vault?
        u = self.user.get_user(username=from_)
        user_id = u["id"]

        # append attachments to lake
        attachment_ids = []
        for file in attachments:
            f = self.lake.append_file(
                user_id=user_id,
                path=id,
                filename=str(file.filename),
                data=bytes(file.data),
                description="dkdc-chat attachment",
                labels=["attachment"],
            )
            attachment_ids.append(f["id"])

        # append message
        data = {
            "idx": [now()],
            "id": [id],
            "to": [to],
            "from": [from_],
            "convo_id": [convo_id],
            "thread_id": [thread_id],
            "subject": [subject],
            "body": [body],
            "attachments": [",".join(attachment_ids) if attachments else None],
            "version": [version],
            "status": [status],
            "description": [description],
            "labels": [",".join(labels) if labels else None],
        }
        self.wcon.insert(self.messages_table_name, data)

        return self.get_message(id=data["id"][0])

    # update record
    def update_message(
        self,
        id: str,
        to: str,
        from_: str,
        convo_id: str,
        thread_id: str,
        subject: str,
        body: str,
        attachments: list[str],
        version: int = None,
        status: str = None,
        description: str = None,
        labels: list[str] = None,
    ):
        if not self.contains_message(id=id):
            raise ValueError(f"Message {id} does not exist")

        data = {
            "idx": [now()],
            "id": [id],
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
        self.wcon.insert(self.messages_table_name, data)

        return self.get_message(id=id)

    # aliases
    __call__ = get_messages
    t = messages_t
