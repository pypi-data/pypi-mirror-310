"""
A namedtuple representaton for the extracted info
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Optional, NamedTuple, Dict, Any


Second = int


class Metadata(NamedTuple):
    """
    typically isn't used completely by one browser, includes
    partial information from browsers which supply the information
    """

    title: Optional[str] = None
    description: Optional[str] = None
    preview_image: Optional[str] = None
    duration: Optional[Second] = None

    @classmethod
    def make(
        cls,
        title: Optional[str] = None,
        description: Optional[str] = None,
        preview_image: Optional[str] = None,
        duration: Optional[Second] = None,
    ) -> Optional[Metadata]:
        """
        Alternate constructor; only make the Metadata object if the user
        supplies at least one piece of data
        """
        if (
            title is None
            and description is None
            and preview_image is None
            and duration is None
        ):
            return None
        return cls(
            title=title,
            description=description,
            preview_image=preview_image,
            duration=duration,
        )


def test_make_metadata() -> None:
    assert Metadata.make(None, None, None, None) is None
    assert Metadata.make(title="webpage title", duration=5) is not None


class Visit(NamedTuple):
    url: str
    dt: datetime
    # hmm, does this being optional make it more annoying to consume
    # by other programs? reduces the amount of data that other programs
    # need to consume, so there's a tradeoff...
    metadata: Optional[Metadata] = None

    def serialize(self) -> Dict[str, Any]:
        return {
            "url": self.url,
            "dt": self.dt.timestamp(),
            "metadata": self.metadata._asdict() if self.metadata is not None else None,
        }

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> Visit:
        md = d.get("metadata")
        metadata = Metadata.make(**md) if md is not None else None
        return cls(
            url=d["url"],
            dt=datetime.fromtimestamp(d["dt"], tz=timezone.utc),
            metadata=metadata,
        )
