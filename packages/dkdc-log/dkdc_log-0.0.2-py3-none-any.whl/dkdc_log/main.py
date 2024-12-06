import os

from dkdc_util import now, uuid, get_dkdc_dir
from dkdc_state import State, ibis, dt


# class
class Log(State):
    def __init__(self, dbpath: str = None):
        if dbpath is None:
            dbpath = os.path.join(get_dkdc_dir(), "log.db")
        super().__init__(dbpath=dbpath)

    def _cons(self) -> (ibis.BaseBackend, ibis.BaseBackend):
        # create write connection
        wcon = ibis.sqlite.connect(self.dbpath)

        # create tables in write connection
        ## logs data
        self.logs_table_name = "logs"
        schema = ibis.schema(
            {
                "idx": dt.timestamp,
                "id": str,
                "value": str,
                "log_level": str,
                "source": str,
                "status": str,
                "description": str,
                "labels": str,  # comma-separated list of labels
            }
        )
        if self.logs_table_name not in wcon.list_tables():
            wcon.create_table(self.logs_table_name, schema=schema)

        # create read connection
        rcon = ibis.duckdb.connect()

        # create tables in read connection
        for table_name in wcon.list_tables():
            rcon.read_sqlite(self.dbpath, table_name=table_name)

        return wcon, rcon

    # tables
    def logs_t(self, id: str = None):
        # get logs data
        t = self.rcon.table(self.logs_table_name)

        # filter by id
        if id:
            t = t.filter(t["id"] == id)

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
    def contains_log(self, id: str = None) -> bool:
        assert id, "id must be provided"

        t = self.logs_t()
        return t.filter(t["id"] == id).count().to_pyarrow().as_py() > 0

    # get record
    def get_log(self, id: str):
        if not self.contains_log(id=id):
            raise ValueError(f"Log {id} does not exist")

        t = self.logs_t(id=id)
        return t.to_pyarrow().to_pylist()[0]

    # append record
    def log(
        self,
        value: str,
        log_level: str = "info",
        source: str = None,
        status: str = None,
        description: str = None,
        labels: list[str] = None,
    ):
        # insert log data
        id = uuid()
        data = {
            "idx": [now()],
            "id": [id],
            "log_level": [log_level],
            "value": [value],
            "status": [status],
            "description": [description],
            "labels": [",".join(labels) if labels else None],
        }
        self.wcon.insert(self.logs_table_name, data)

        return self.get_log(id=id)

    # aliases
    __call__ = log
    t = logs_t
