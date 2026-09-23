"""One database engine per application; a fresh transaction per request/job."""

from sqlalchemy import create_engine, event, inspect, text
from sqlalchemy.orm import sessionmaker

from .models import Base


class Database:
    def __init__(self, url: str):
        options = {"check_same_thread": False, "timeout": 20} if url.startswith("sqlite") else {}
        self.engine = create_engine(url, connect_args=options)
        if url.startswith("sqlite"):

            @event.listens_for(self.engine, "connect")
            def configure_sqlite(connection, _):
                connection.execute("PRAGMA foreign_keys=ON")
                connection.execute("PRAGMA journal_mode=WAL")

        self.session = sessionmaker(self.engine, expire_on_commit=False)

    def initialize(self):
        Base.metadata.create_all(self.engine)
        # The demo uses SQLite without a migration package. Keep existing local
        # databases usable when a new JSON field is added to the inspection record.
        columns = {column["name"] for column in inspect(self.engine).get_columns("inspections")}
        if "applicability" not in columns:
            with self.engine.begin() as connection:
                connection.execute(text("ALTER TABLE inspections ADD COLUMN applicability JSON"))
