import itertools
import os
from pathlib import Path
from typing import Iterator

from dotenv import find_dotenv, load_dotenv
from lawsql_utils.trees import data_tree_walker
from sqlite_utils import Database

load_dotenv(find_dotenv())


def get_db() -> Database:
    l = os.getenv("PATH_TO_LAWSQL").split("/") + ["index.db"]
    p = Path.home().joinpath(*l)
    return Database(p)


sql = """--sql
    select
        d.rowid,
        d.source,
        d.pk,
        d.date_prom date_promulgated,
        snippet(
            fts_result.Decisions_fts,
            3,
            '_',
            '_',
            '...',
            64
        ) search_result
    from Decisions_fts fts_result
    join Decisions d on d.rowid = fts_result.rowid
    where Decisions_fts match ?
    order by date_promulgated desc;
"""


def get_rows_with_key_from_dict(data: dict, key: str) -> Iterator[dict]:
    def extract_queries(data: dict, key: str):
        yield from data_tree_walker(data, key)

    db: Database = get_db()
    queries = itertools.chain(*extract_queries(data, key))
    joined_text = '" OR "'.join(queries)
    rows = db.execute(sql, (f'"{joined_text}"',))  # note extra double quote
    for row in rows:
        yield {
            "rowid": row[0],
            "source": row[1],
            "pk": row[2],
            "date": row[3],
            "snippet": row[4],
        }
    return rows
