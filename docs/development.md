# Development and testing

[Back to README](../README.md)

## Structure

```
esphome/
├── ha-remote.yaml            ← the only file to edit: pages and entities
├── secrets.yaml.example
└── remote/                   ← the building blocks, no need to touch them
    ├── core.yaml             (board, battery, deep sleep, bottom bar)
    ├── connection_status.h   (connection and TV availability logic)
    ├── settings.yaml
    ├── lang/       en.yaml, bg.yaml
    ├── lights/     page.yaml, light.yaml
    ├── led/        page.yaml, zone.yaml
    ├── tv/         google_tv.yaml
    ├── appliances/ page.yaml, appliance.yaml
    └── power/      page.yaml
```

## How it works (for those who want to modify it)

Each building block is an [ESPHome package](https://esphome.io/components/packages/) with variables. The files append their own actions to a few shared scripts defined in `core.yaml`, using `id: !extend`:

- `build_ui`: on boot, moves buttons, tiles and cards into their containers (bottom bar, lights grid, zone row, appliance list);
- `refresh_all`: on connection to HA, syncs everything with the real state;
- `nav_refresh`: on page change, highlights the right button in the bar.
- `refresh_connection`: every second, updates connection warnings and TV control availability.

To create a new page, start from `power/page.yaml`, which is the simplest.

## Configuration checks

With ESPHome installed and `esphome/secrets.yaml` configured:

```sh
esphome config esphome/ha-remote.yaml
esphome compile esphome/ha-remote.yaml
```

To run the automated tests (Python 3.12):

```sh
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-dev.txt
make test
```

Tests cover Google TV button commands and hold bindings, translation completeness, native C++ connection-state checks, and ESPHome validation and C++ source generation for both languages and each page on its own. A C++ compiler (`c++`) is required. They use a temporary copy with generated test credentials, so your local `secrets.yaml` is never read or changed. Internet access is required to download fonts.

To additionally compile full firmware for English and Bulgarian:

```sh
make test-full
```

GitHub Actions runs the same `make test-full` command on pushes and pull requests, and can also be started manually. Use `make test` during development for faster checks, and `make test-full` before pushing to match CI. You can select a Python interpreter with `make test PYTHON=/path/to/python`. The first full build downloads the ESP32 toolchain and can take considerably longer than the source-generation checks.

Physical display, touch calibration, battery readings and communication with a real Home Assistant / TV require the [hardware validation protocol](hardware-validation.md). The protocol includes a results sheet; hardware checks remain **not run** until measurements are recorded.
