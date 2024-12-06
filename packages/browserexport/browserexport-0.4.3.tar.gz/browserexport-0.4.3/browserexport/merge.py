"""
Merges multiple history sqlite databases into one
"""

from datetime import datetime
from typing import Iterator, Iterable, Sequence, Set, Tuple, List

from .log import logger
from .model import Visit
from .common import PathIsh, expand_path
from .parse import read_visits


def read_and_merge(paths: Sequence[PathIsh]) -> Iterator[Visit]:
    """
    Receives any amount of Path-like databases as input,
    reads Visits from each of those databases,
    and merges them together (removing duplicates)
    """
    pths = [expand_path(p) for p in paths]
    hst: List[Iterator[Visit]] = list(map(read_visits, pths))
    yield from merge_visits(hst)


def merge_visits(sources: Sequence[Iterable[Visit]]) -> Iterator[Visit]:
    """
    Removes duplicate Visit items from multiple sources
    """
    logger.debug(f"merging information from {len(sources)} source(s)...")
    # use combination of URL, visit date and visit type to uniquely identify visits
    emitted: Set[Tuple[str, datetime]] = set()
    duplicates = 0
    for src in sources:
        for vs in src:
            key = (vs.url, vs.dt)
            if key in emitted:
                # logger.debug(f"skipping {key} => {vs}")
                duplicates += 1
                continue
            yield vs
            emitted.add(key)
    logger.debug("Summary: removed {} duplicates...".format(duplicates))
    logger.info("Summary: returning {} visit entries...".format(len(emitted)))
