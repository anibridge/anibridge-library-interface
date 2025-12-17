"""Anibridge library provider interfaces package."""

from anibridge.library.interfaces import (
    HistoryEntry,
    LibraryEntity,
    LibraryEpisode,
    LibraryMedia,
    LibraryMovie,
    LibraryProvider,
    LibraryProviderT,
    LibrarySeason,
    LibrarySection,
    LibraryShow,
    LibraryUser,
    MediaKind,
)
from anibridge.library.registry import (
    LibraryProviderRegistry,
    library_provider,
    provider_registry,
)

__all__ = [
    "HistoryEntry",
    "LibraryEntity",
    "LibraryEpisode",
    "LibraryMedia",
    "LibraryMovie",
    "LibraryProvider",
    "LibraryProviderRegistry",
    "LibraryProviderT",
    "LibrarySeason",
    "LibrarySection",
    "LibraryShow",
    "LibraryUser",
    "MediaKind",
    "library_provider",
    "provider_registry",
]
