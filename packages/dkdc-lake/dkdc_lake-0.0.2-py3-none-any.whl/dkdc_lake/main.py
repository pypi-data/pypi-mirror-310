import os

from dkdc_util import now, uuid, get_dkdc_dir
from dkdc_state import State, ibis, dt


# class
class Lake(State):
    def __init__(self, dbpath: str = None):
        if dbpath is None:
            dbpath = os.path.join(get_dkdc_dir(), "lake.db")
        super().__init__(dbpath=dbpath)

    def _cons(self) -> (ibis.BaseBackend, ibis.BaseBackend):
        # create write connection
        wcon = ibis.sqlite.connect(self.dbpath)

        # create tables in write connection
        ## lake data
        self.lake_table_name = "lake"
        schema = ibis.schema(
            {
                "idx": dt.timestamp,
                "id": str,
                "user_id": str,
                "path": str,
                "filename": str,
                "filetype": str,
                "data": dt.binary,
                "version": int,
                "status": str,
                "description": str,
                "labels": str,  # comma-separated list of labels
            }
        )
        if self.lake_table_name not in wcon.list_tables():
            wcon.create_table(self.lake_table_name, schema=schema)

        # create read connection
        rcon = ibis.duckdb.connect()

        # create tables in read connection
        for table_name in wcon.list_tables():
            rcon.read_sqlite(self.dbpath, table_name=table_name)

        return wcon, rcon

    # tables
    def lake_t(self, user_id: str = None):
        # get lake data
        t = self.rcon.table(self.lake_table_name)

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
        t = t.order_by(ibis.desc("idx"))

        # return the data
        return t

    # contains
    def contains_path(self, path: str, user_id: str = None) -> bool:
        t = self.lake_t(user_id=user_id)
        return t.filter(t["path"] == path).count().to_pyarrow().as_py() > 0

    def contains_file(
        self, filename: str, path: str = None, user_id: str = None
    ) -> bool:
        t = self.lake_t(user_id=user_id)
        return (
            t.filter((t["path"] == path) & (t["filename"] == filename))
            .count()
            .to_pyarrow()
            .as_py()
            > 0
        )

    # get record
    def get_file(self, filename: str, path: str = None, user_id: str = None):
        if not self.contains_file(filename=filename, path=path, user_id=user_id):
            raise ValueError(f"File {filename} does not exist")

        t = self.lake_t(user_id=user_id)
        return (
            t.filter((t["path"] == path) & (t["filename"] == filename))
            .to_pyarrow()
            .to_pylist()[0]
        )

    # append record
    def append_file(
        self,
        user_id: str = None,
        path: str = None,
        filename: str = None,
        filetype: str = None,
        data: bytes = None,
        version: int = None,
        status: str = None,
        description: str = None,
        labels: list[str] = None,
    ):
        assert (filename is not None) and (
            data is not None
        ), "user_id, filename, and data are required"

        if self.contains_file(filename=filename, path=path, user_id=user_id):
            raise ValueError(f"File {filename} already exists")

        data = {
            "idx": [now()],
            "id": [uuid()],
            "user_id": [user_id],
            "path": [path],
            "filename": [filename],
            "filetype": [filetype],
            "data": [data],
            "version": [version],
            "status": [status],
            "description": [description],
            "labels": [",".join(labels) if labels else None],
        }
        self.wcon.insert(self.lake_table_name, data)

        return self.get_file(filename=filename, path=path, user_id=user_id)

    # update record
    def update_file(
        self,
        user_id: str,
        path: str,
        filename: str,
        filetype: str,
        data: bytes,
        version: int,
        status: str,
        description: str,
        labels: list[str] = None,
    ):
        if not self.contains_file(filename=filename, path=path, user_id=user_id):
            raise ValueError(f"File {filename} does not exist")

        f = self.get_file(filename=filename, path=path, user_id=user_id)
        id = f["id"]

        data = {
            "idx": [now()],
            "id": [id],
            "user_id": [user_id],
            "path": [path],
            "filename": [filename],
            "filetype": [filetype],
            "data": [data],
            "version": [version],
            "status": [status],
            "description": [description],
            "labels": [",".join(labels) if labels else None],
        }
        self.wcon.insert(self.lake_table_name, data)

        return self.get_file(filename=filename, path=path, user_id=user_id)

    # aliases
    __call__ = get_file
    t = lake_t
