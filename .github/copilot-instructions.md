# Instructions for AI Agents (Copilot, Claude, Codex)

## Repository context
- This repository is a Python async wrapper for the IMGW-PIB public API (weather + hydrological data)
- The publishable package is `imgw_pib` (PyPI name: `imgw-pib`)
- The public API surface is the `ImgwPib` class in `imgw_pib/__init__.py` and the models in `imgw_pib/model.py`

## Project layout
```
imgw_pib/
├── __init__.py        # Main client (ImgwPib)
├── const.py           # Endpoints, headers, timeouts, maps
├── exceptions.py      # ApiError + base error types
├── model.py           # Dataclasses + enums
├── utils.py           # Parsing helpers
├── data/              # Packaged JSON data files
└── py.typed           # Type hint marker
```

## Python and environment
- Target Python: >=3.13
- Preferred setup: `./scripts/setup-local-env.sh` (creates `./venv`, installs deps with `uv`, runs `prek install`)
- Local venv: `./venv` (activate with `source venv/bin/activate`)

## Linting, formatting, typing
- Lint: `ruff check <files> --fix`
- Format: `ruff format <files>`
- Types: `ty check <files>`
- Avoid silencing rules unless there is a strong reason

## Testing
- Run with `pytest` (async tests use `pytest-asyncio`)
- Mock HTTP via `aioresponses`; do not hit real endpoints in tests
- Time-based logic uses `freezegun` and snapshots use `syrupy` (`tests/snapshots/`)
- When output structures change, update snapshots and fixtures together

## Implementation guidelines
- Keep all I/O async; use `aiohttp.ClientSession` from the caller, and `aiofiles` for local file reads
- Use `orjson` for JSON parsing/serialization and `yarl.URL` for endpoint construction
- Keep endpoints/constants in `imgw_pib/const.py` and avoid scattering URLs
- Preserve the public API and model shapes; breaking changes require explicit discussion
- Prefer `ApiError` for API-level failures and use lazy logging (`_LOGGER.debug("msg %s", value)`)
