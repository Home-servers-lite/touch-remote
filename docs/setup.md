# Installation and operation

[Back to README](../README.md)

## Installation

1. Copy the contents of the `esphome/` folder into your ESPHome configuration (for the Home Assistant add-on it is `/config/esphome/`), keeping the `remote/` subfolder.
2. Create `secrets.yaml` from [`secrets.yaml.example`](../esphome/secrets.yaml.example). If you already have a `secrets.yaml` for other devices, just add the missing keys.
3. Customise `ha-remote.yaml` using the [configuration guide](configuration.md).
4. Flash the first time over USB; after that, updates go over the air (OTA).
5. In Home Assistant, add the ESPHome device when it is discovered and enter the API key.
6. **Important:** in the ESPHome device options in HA, enable *"Allow the device to perform Home Assistant actions"*, otherwise the buttons won't control anything.

The first compile downloads the fonts (Montserrat from Google Fonts and Material Design Icons from GitHub), so an internet connection is needed.

## Google TV setup

1. In Home Assistant, add the [Android TV Remote](https://www.home-assistant.io/integrations/androidtv_remote/) integration and pair your Google TV using the code shown on the TV.
2. Find its `remote` entity and replace `remote.google_tv` in `esphome/ha-remote.yaml`. Use the Android TV Remote entity, not the Google Cast media player.
3. Enable **Allow the device to perform Home Assistant actions** in the ESPHome device options.

All TV buttons use that one remote entity: power uses `remote.toggle`; navigation, volume, play/pause, Back and Home use `remote.send_command` with Android key codes. The power indicator follows the remote's on/off state. Arrows and volume send one command on press, then repeat while held (500 ms hold threshold, 200 ms repeat interval). Releasing or moving off the button stops generating repeat events; commands already transmitted may still arrive.

The header shows **No Wi-Fi** or **No HA** when the corresponding connection is missing, and returns to the page title when connected. TV controls are disabled and show **TV unavailable** until Home Assistant reports a valid `on` or `off` remote state. Connection checks run every second; TV availability depends on Home Assistant publishing the state change. These messages are translated in Bulgarian. The HA indicator identifies the Home Assistant API client; it does not confirm permission to perform Home Assistant actions.

Volume and playback behavior depends on the TV and foreground app. Some TVs become unavailable when powered off and cannot be woken over this integration; enable network standby if the device supports it.

## Deep sleep and OTA updates

After 20 s without touches the board goes into deep sleep; a touch wakes it up (the first touch only wakes it; connection time depends on the network). While asleep it can't receive OTA updates, so before updating:

1. wake the remote;
2. open the gear and turn on **Stay awake** (or tap the battery indicator: a dot appears);
3. start the update. The option turns itself off on restart.

## Notes

- If the touch responds mirrored, see the comments in the `touchscreen` section of `core.yaml`.
- The board does not route the charging signal to the processor: the "charging" state is estimated from the battery voltage trend.
- GPIO45 and GPIO46 are strapping pins and ESPHome shows a warning: this is normal for this board.
