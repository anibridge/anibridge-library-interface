# anibridge-library-interface

anibridge-library-interface provides a set of protocols and utilities to implement and register media library providers for the [AniBridge](https://github.com/anibridge/anibridge) project.

> [!IMPORTANT]
> This package is a definition-only interface library. It does not include any concrete provider implementations. Provider implementations should be created in separate packages that depend on this interface library.

## Installation

```shell
pip install anibridge-library-interface
# pip install git+https://github.com/anibridge/anibridge-library-interface.git
```

## API reference

The package exposes two main modules:

- `anibridge.library.interfaces`: provider and entity protocols
- `anibridge.library.registry`: registration helpers and `provider_registry`

Key types and protocols (from `anibridge.library.interfaces`):

- `MediaKind` (StrEnum): High-level kinds: `MOVIE`, `SHOW`, `SEASON`, `EPISODE`.

- `LibraryEntity` (Protocol): Base protocol with `key`, `media_kind`, `title`, and helpers `provider()`.

- `LibrarySection` (Protocol): Represents a logical collection/section in a library.

- `LibraryMedia` (Protocol): Base media item protocol exposing:

  - `on_watching` and `on_watchlist` properties
  - `poster_image`, `user_rating` (0–100 or None), and `view_count`
  - Async `history() -> Sequence[HistoryEntry]`
  - `ids() -> dict[str,str]` for external identifiers
  - Async `review() -> str | None`
  - `section() -> LibrarySection`

- `LibraryMovie`, `LibraryShow`, `LibrarySeason`, `LibraryEpisode` (Protocols):

  - `LibraryShow` adds `ordering` ("tmdb"|"tvdb"|"") and `episodes()`/`seasons()` helpers.
  - `LibrarySeason` has an `index` and `episodes()`/`show()` helpers.
  - `LibraryEpisode` has `index`, `season_index`, and `season()`/`show()` helpers.

- `HistoryEntry` (dataclass): `library_key: str`, `viewed_at: datetime` (timezone-aware).

- `LibraryUser` (dataclass): `key: str`, `title: str`.

Core provider protocol (`LibraryProvider`):

- Class attribute: `NAMESPACE: ClassVar[str]`: Provider namespace identifier.
- Constructor: `__init__(*, config: dict | None = None)`: Receives provider-scoped config.
- `async initialize() -> None`: Async setup hook.
- `user() -> LibraryUser | None`: Return associated user info.
- `async clear_cache() -> None` and `async close() -> None`: Lifecycle helpers.
- `async get_sections() -> Sequence[LibrarySection[Self]]`: List available sections.
- `async list_items(section, *, min_last_modified: datetime | None = None, require_watched: bool = False, keys: Sequence[str] | None = None) -> Sequence[LibraryMedia[Self]]`: List items for a section with optional filters.
- `async parse_webhook(request: starlette.requests.Request) -> tuple[bool, Sequence[str]]`: Parse incoming webhooks and return whether it's relevant plus media keys to sync.

Registry utilities (from `anibridge.library.registry`):

- `LibraryProviderRegistry`: Registry class with:

  - `create(namespace, *, config=None) -> LibraryProvider`: Instantiate registered provider
  - `get(namespace) -> type[LibraryProvider]`: Lookup provider class
  - `namespaces() -> tuple[str,...]`: Registered namespaces
  - `register(cls, *, namespace: str | None = None)`: Register as decorator or direct call
  - `unregister(namespace)` / `clear()` / `__contains__` / `__iter__`

- `provider_registry`: Module-level `LibraryProviderRegistry` instance.
- `library_provider`: Decorator/helper that registers a provider class in `provider_registry` (accepts `namespace=` and `registry=` overrides).

Refer to the module docstrings and the `src/anibridge/library` sources for method signatures and usage examples.

## Examples

You can view the following built-in provider implementations as examples of how to implement the interface:

- [anibridge-provider-template](https://github.com/anibridge/anibridge-provider-template)
- [anibridge-plex-provider](https://github.com/anibridge/anibridge-plex-provider)
