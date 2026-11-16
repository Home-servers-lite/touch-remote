# Hardware validation

[Back to README](../README.md)

Status: **not run on hardware**. Complete this protocol before treating a firmware build as validated for daily use. Automated tests cover configuration, source generation, connection-state logic and, with full-build mode, firmware compilation.

## Record the setup

| Item | Value |
|---|---|
| Date / tester | |
| Git commit | |
| ESPHome version | |
| Board / display revision | |
| Battery model / capacity | |
| TV model / firmware | |
| Home Assistant version | |
| Language | English / Bulgarian |
| Android TV Remote entity | |

Use your own `esphome/secrets.yaml` and entity IDs. Enable Home Assistant actions for the ESPHome device. Start at low TV volume. For network tests, enable **Stay awake** first so deep sleep does not interrupt the test. Open logs with `esphome logs esphome/ha-remote.yaml --no-states`.

## Display and touch — run in both languages

1. Open every page and Settings. Check that titles, buttons, state text and the settings note fit and that Bulgarian letters and icons render correctly.
2. Tap each corner and the center; check that the intended control reacts. Check sliders at their minimum and maximum. Record any offset or mirrored axis before changing touch calibration.
3. On the lights page, use more than four lights and scroll. On appliances, use more than three cards and scroll. Confirm scrolling does not trigger an unintended action.
4. Change screen brightness, reboot and wake from deep sleep; check that the selected brightness is restored.

Pass: readable text, no overlap or missing characters, correct touch targets and preserved brightness.

## TV taps and holds

1. Tap each arrow once. Each tap should move one item. Test OK, Back, Home, play/pause, volume and power.
2. Hold each arrow for two seconds. Repetition should begin after the hold threshold (500 ms), with repeat events every 200 ms. Record actual TV responsiveness; network latency can affect delivery.
3. Hold volume briefly, then release. Confirm volume stops changing after any command already in flight. Repeat for volume down.
4. Slide your finger outside a held button and release. Confirm no continuing commands. Repeat a hold while changing connection availability.
5. Tap power and play/pause briefly and hold them: these buttons should not repeat.

Pass: single taps do not double-fire; repetition ends on release or loss of press; unavailable TV controls do not dispatch commands. An already transmitted command cannot be cancelled.

## Connection loss and recovery

1. Boot with Wi-Fi unavailable: the header should show **No Wi-Fi / Няма Wi-Fi**.
2. Restore Wi-Fi while Home Assistant is stopped: the header should show **No HA / Няма HA**. A log-only API connection must not clear this warning.
3. Start Home Assistant: the warning should disappear after its API connection is established. Confirm real entity state updates and actions, not just the absence of a warning.
4. Make the TV remote entity unavailable (disconnect the TV from the network or temporarily disable its integration). The TV power label should show **TV unavailable / TV недостъпен** and TV controls should be disabled once HA publishes the new state. Normal `off` state must still allow power-on.
5. Restore the TV integration. Confirm controls recover when an `on` or `off` state arrives.
6. While holding a TV arrow, stop Home Assistant, then restore it. Confirm no old hold command resumes on reconnection and the TV waits for a fresh state.
7. Repeat Wi-Fi and HA recovery three times, both while awake and after a sleep/wake cycle. Inspect logs for resets or safe mode.

Pass: network warnings update within about one second after the device observes the change, TV status follows HA availability updates, and controls recover without rebooting. A connected HA client does not prove that Home Assistant actions are permitted; verify that setting separately.

## Sleep and wake

1. Disable **Stay awake**, then stop touching the screen. Confirm deep sleep after about 20 seconds.
2. Touch the screen: the first touch wakes the board. Time from touch to usable TV controls, including Wi-Fi, HA and TV-state synchronization. Repeat ten times.
3. Hold a control for over 20 seconds at a safe volume or in a harmless menu. Confirm the device does not sleep while it is being used.
4. Enable **Stay awake**: inactivity should turn off the backlight without entering deep sleep; touching should restore the screen. Reboot and confirm Stay awake resets.

Record all ten wake times, failures and any touch needed beyond the initial wake touch. Do not claim a wake-time target until measured on the actual network.

## Battery and charging

Disconnect USB and Qi charging when measuring battery runtime. USB power changes the result. Use suitable battery measurement equipment if measuring current; never short the battery or bypass its protection.

1. Compare reported battery voltage with a meter at several charge levels. Record both values before changing the ADC calibration factor.
2. Record current while awake, in deep sleep, and with Stay awake enabled/backlight off, if suitable equipment is available.
3. For a runtime test, record starting charge, brightness, Wi-Fi signal and a repeatable usage pattern (for example, ten 30-second sessions per day). Record runtime and ending charge. Do not infer runtime from percentage alone.
4. Connect and disconnect charging; check the charging indicator after waking and after at least 60 seconds awake. It is an estimate from voltage changes, not a hardware charging signal.
5. Observe low-battery behavior using normal discharge. Record unexpected resets and whether normal operation returns after recharging.

## Results

| Check | Pass / fail / not run | Measurements / issues |
|---|---|---|
| English layout and touch | Not run | |
| Bulgarian layout and touch | Not run | |
| TV taps and holds | Not run | |
| Connection loss and recovery | Not run | |
| Ten wake cycles | Not run | |
| Brightness persistence | Not run | |
| Battery voltage calibration | Not run | |
| Standby / active current | Not run | |
| Battery runtime | Not run | |
| Charging estimate | Not run | |

Attach measurements and relevant logs with credentials and network identifiers removed. A successful compilation is not a hardware pass.
