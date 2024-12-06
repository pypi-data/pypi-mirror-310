from urllib.parse import unquote

from .common import (
    Iterator,
    Visit,
    Metadata,
    PathIshOrConn,
    Browser,
    Schema,
    Path,
    datetime,
    timezone,
    execute_query,
    handle_glob,
    handle_path,
    Paths,
)

# Referenced:
# https://github.com/karlicoss/promnesia/blob/0e1e9a1ccd1f07b2a64336c18c7f41ca24fcbcd4/src/promnesia/sources/browser.py#L222
# https://web.archive.org/web/20201026130310/http://fileformats.archiveteam.org/wiki/History.db


def _safari_date_to_utc(safari_time: int) -> datetime:
    ts = safari_time + 978307200
    return datetime.fromtimestamp(ts, tz=timezone.utc)


class Safari(Browser):
    detector = "history_tombstones"

    schema = Schema(
        cols=[
            "U.url",
            "V.visit_time",
            "V.title",
        ],
        where="FROM history_visits as V, history_items as U WHERE V.history_item = U.id",
        order_by="V.visit_time",
    )

    @classmethod
    def extract_visits(cls, path: PathIshOrConn) -> Iterator[Visit]:
        for row in execute_query(path, cls.schema.query):
            yield Visit(
                url=unquote(row["url"]),
                dt=_safari_date_to_utc(row["visit_time"]),
                metadata=Metadata.make(title=row["title"]),
            )

    @classmethod
    def data_directories(cls) -> Paths:
        return handle_path(
            {
                "darwin": "~/Library/Safari/",
            },
            browser_name=cls.__name__,
            default_behaviour="mac",
        )

    @classmethod
    def locate_database(cls, profile: str = "*") -> Path:
        dd = cls.data_directories()
        return handle_glob(dd, profile + "History.db")
