# Customising pages and entities

[Back to README](../README.md)

## Customisation

Everything happens in the `packages:` section of `ha-remote.yaml`. The included file uses example entities; replace them with your Home Assistant entity IDs.

**Language:** keep one of the two `language:` lines (`en.yaml` or `bg.yaml`). To add a language, copy `remote/lang/en.yaml`, translate it and include your copy.

For Bulgarian, comment out the English include and enable `remote/lang/bg.yaml`. Text fonts include Cyrillic characters. Entity names and custom appliance state labels come from the values you set in `ha-remote.yaml`.

**Removing a page:** comment out or delete the page line and the lines of its entities. For example, without a Google TV you delete the `tv:` block.

**Adding an item:** copy an existing block, give it a unique package name and change the variables. For example, a fifth light:

```yaml
  light_bathroom: !include
    file: remote/lights/light.yaml
    vars:
      key: bathroom              # short unique name (lowercase, digits, _)
      name: Bathroom             # text on the tile
      entity: light.bathroom
      icon: "\U000F0335"         # optional
```

**Order:** the order of the packages is the order of the buttons in the bottom bar, and the first page is the one shown at power-on. Keep `language` and `core` first and `settings` last.

The variables of each building block (required and optional, with defaults) are described at the top of its file in `remote/`. A few special cases:

- **LED zones with several strips:** `entity` is the light whose state and brightness are shown; with `extra_entities` you add more lights controlled together.
- **Appliances:** states depend on the integration. By default the machine is "stopped" when the state is `idle` and "paused" when it is `pause`. If your integration has many different states, use `active_states` to list the ones in which it is running and `state_labels` to give a text to the others. The dishwasher in the example file shows how.
- **Without pause/resume buttons** the appliance card is information only.

### Icons

Icons are [Material Design Icons](https://pictogrammers.com/library/mdi/). Find the icon, copy its code (e.g. `F0335`) and write it like this: `"\U000F0335"`, i.e. `\U000` followed by the code.

A few icons used in the example: `F0335` light bulb, `F0769` ceiling light, `F04B9` sofa, `F072A` washing machine, `F0917` tumble dryer, `F0502` television, `F0241` lightning bolt.
