# ESPHome touch remote for your smart home - Home Assistant

A battery-powered touch remote built with **ESPHome** and **LVGL** on a Freenove ESP32-S3 2.8" display. Choose the pages and entities you need. The remote sleeps when idle and wakes with a touch.

The interface supports **English and Bulgarian**.

## Features

| Page | Controls |
|---|---|
| Google TV | Power, navigation, volume, play/pause, Back and Home; hold arrows or volume to repeat |
| Lights | Individual lights and all on/off |
| LED | Zones, colours and brightness |
| Appliances | Remaining time and pause/resume where supported |
| Power | Current home power consumption |
| Settings | Screen brightness and Stay awake for updates |

Battery indication and connection warnings are available on screen.

## Hardware

- Freenove ESP32-S3 Display 2.8" (FNK0104), 240×320 with capacitive touch.
- LiPo 102050 1000 mAh battery with JST 1.25 connector.
- Optional USB-C Qi charging receiver.

## Quick start

1. Copy [`esphome/`](esphome/) into your ESPHome configuration directory.
2. Create `secrets.yaml` from [`secrets.yaml.example`](esphome/secrets.yaml.example) and set your credentials.
3. Edit [`ha-remote.yaml`](esphome/ha-remote.yaml): choose English or Bulgarian and replace the example entity IDs. Pair Google TV through Home Assistant's **Android TV Remote** integration.
4. Flash over USB, add the device to Home Assistant, and enable **Allow the device to perform Home Assistant actions**.

See the [installation guide](docs/setup.md) for pairing, connection status, sleep and OTA updates.

## Documentation

- [Customisation](docs/configuration.md) — pages, entities, languages and icons.
- [Development and testing](docs/development.md) — project structure, local tests and GitHub Actions.
- [Hardware validation](docs/hardware-validation.md) — display, touch, battery, wake and TV checks.

## License

[MIT](LICENSE).
