import os

from datetime import datetime

from dkdc_util import now, get_dkdc_dir
from dkdc_state import State, ibis, dt

from dkdc_lake import Lake


# class
class Calendar(State):
    def __init__(self, dbpath: str = None):
        if dbpath is None:
            dbpath = os.path.join(get_dkdc_dir(), "calendar.db")
        super().__init__(dbpath=dbpath)

        # other states
        self.lake = Lake()

    def _cons(self) -> (ibis.BaseBackend, ibis.BaseBackend):
        # create write connection
        wcon = ibis.sqlite.connect(self.dbpath)

        # create tables in write connection
        ## events data
        self.events_table_name = "events"
        schema = ibis.schema(
            {
                "idx": dt.timestamp,
                "id": str,
                "user_id": str,
                "required": str,  # comma-separated list of user_ids
                "optional": str,  # comma-separated list of user_ids
                "start": dt.timestamp,
                "end": dt.timestamp,
                "all_day": bool,
                "subject": str,
                "body": str,
                "attachments": str,  # comma-separated list of attachment_ids
                "accepted": str,  # comma-separated list of user_ids
                "maybe": str,  # comma-separated list of user_ids
                "declined": str,  # comma-separated list of user_ids
                "priority": int,
                "status": str,
                "description": str,
                "labels": str,  # comma-separated list of labels
            }
        )
        if self.events_table_name not in wcon.list_tables():
            wcon.create_table(self.events_table_name, schema=schema)

        # create read connection
        rcon = ibis.duckdb.connect()

        # create tables in read connection
        for table_name in wcon.list_tables():
            rcon.read_sqlite(self.dbpath, table_name=table_name)

        return wcon, rcon

    # tables
    def events_t(self, user_id: str = None):
        # get events data
        t = self.rcon.table(self.events_table_name)

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
        t = t.mutate(required=t["required"].split(","))
        t = t.mutate(optional=t["optional"].split(","))
        t = t.mutate(labels=t["labels"].split(","))
        t = t.mutate(attachments=t["attachments"].split(","))
        t = t.mutate(accepted=t["accepted"].split(","))
        t = t.mutate(maybe=t["maybe"].split(","))
        t = t.mutate(declined=t["declined"].split(","))

        # order
        t = t.order_by(ibis.asc("priority"), ibis.desc("idx"))

        # return the data
        return t

    # contains
    def contains_event(self, id: str, user_id: str = None) -> bool:
        t = self.events_t(user_id=user_id)
        return t.filter(t["id"] == id).count().to_pyarrow().as_py() > 0

    # get record
    def get_event(self, id: str, user_id: str = None):
        t = self.events_t(user_id=user_id)
        return t.filter(t["id"] == id).to_pyarrow().to_pylist()[0]

    # append record
    def append_event(
        self,
        id: str,
        user_id: str,
        required: list[str],
        optional: list[str],
        start: datetime,
        end: datetime,
        all_day: bool,
        subject: str,
        body: str,
        attachments: list[str],
        accepted: list[str],
        maybe: list[str],
        declined: list[str],
        priority: int = 100,
        status: str = None,
        description: str = None,
        labels: list[str] = None,
    ):
        data = {
            "idx": [now()],
            "id": [id],
            "user_id": [user_id],
            "required": [",".join(required) if required else None],
            "optional": [",".join(optional) if optional else None],
            "start": [start],
            "end": [end],
            "all_day": [all_day],
            "subject": [subject],
            "body": [body],
            "attachments": [",".join(attachments) if attachments else None],
            "accepted": [",".join(accepted) if accepted else None],
            "maybe": [",".join(maybe) if maybe else None],
            "declined": [",".join(declined) if declined else None],
            "priority": [priority],
            "status": [status],
            "description": [description],
            "labels": [",".join(labels) if labels else None],
        }
        self.wcon.insert(self.events_table_name, data)

        return self.get_event(id=id)

    # update record
    def update_event(
        self,
        id: str,
        user_id: str,
        required: list[str],
        optional: list[str],
        start: datetime,
        end: datetime,
        all_day: bool,
        subject: str,
        body: str,
        attachments: list[str],
        accepted: list[str],
        maybe: list[str],
        declined: list[str],
        priority: int = 100,
        status: str = None,
        description: str = None,
        labels: list[str] = None,
    ):
        if not self.contains_event(id=id):
            raise ValueError(f"event {id} does not exist")

        data = {
            "idx": [now()],
            "id": [id],
            "user_id": [user_id],
            "required": [",".join(required) if required else None],
            "optional": [",".join(optional) if optional else None],
            "start": [start],
            "end": [end],
            "all_day": [all_day],
            "subject": [subject],
            "body": [body],
            "attachments": [",".join(attachments) if attachments else None],
            "accepted": [",".join(accepted) if accepted else None],
            "maybe": [",".join(maybe) if maybe else None],
            "declined": [",".join(declined) if declined else None],
            "priority": [priority],
            "status": [status],
            "description": [description],
            "labels": [",".join(labels) if labels else None],
        }
        self.wcon.insert(self.events_table_name, data)

        return self.get_event(id=id)

    # aliases
    __call__ = get_event
    t = events_t
