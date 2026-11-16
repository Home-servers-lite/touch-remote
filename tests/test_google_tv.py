from pathlib import Path
import unittest

from esphome.yaml_util import load_yaml


ROOT = Path(__file__).resolve().parents[1] / "esphome"


class GoogleTVTest(unittest.TestCase):
    def test_button_actions(self):
        config = load_yaml(ROOT / "remote/tv/google_tv.yaml")
        buttons = {
            widget["button"]["id"]: widget["button"]
            for widget in config["lvgl"]["pages"][0]["widgets"]
            if "button" in widget
        }
        commands = {
            "btn_tv_power": None,
            "k_up": "DPAD_UP",
            "k_down": "DPAD_DOWN",
            "k_left": "DPAD_LEFT",
            "k_right": "DPAD_RIGHT",
            "k_ok": "DPAD_CENTER",
            "k_volup": "VOLUME_UP",
            "k_voldn": "VOLUME_DOWN",
            "k_playpause": "MEDIA_PLAY_PAUSE",
            "k_back": "BACK",
            "k_home": "HOME",
        }
        self.assertEqual(set(buttons), set(commands))
        repeating = {"k_up", "k_down", "k_left", "k_right", "k_volup", "k_voldn"}
        for button_id, command in commands.items():
            with self.subTest(button=button_id):
                button = buttons[button_id]
                event = "on_press" if button_id in repeating else "on_click"
                if command:
                    self.assertEqual(button[event], [{"script.execute": {
                        "id": "send_tv_command", "command": command,
                    }}])
                else:
                    action = button[event][0]["if"]["then"][0]["homeassistant.action"]
                    self.assertEqual(action, {
                        "action": "remote.toggle", "data": {"entity_id": "${remote}"},
                    })
                if button_id in repeating:
                    self.assertEqual(button["on_long_press_repeat"], button["on_press"])
                    self.assertNotIn("on_click", button)
                else:
                    self.assertNotIn("on_long_press_repeat", button)
        self.assertEqual(config["text_sensor"][0]["entity_id"], "${remote}")

    def test_commands_are_gated_by_tv_availability(self):
        config = load_yaml(ROOT / "remote/tv/google_tv.yaml")
        send_command = next(script for script in config["script"] if script["id"] == "send_tv_command")
        guarded = send_command["then"][0]["if"]
        condition = guarded["condition"]["lambda"]
        self.assertIn("remote_status::tv_available", condition)
        self.assertIn("id(ha_connected)", condition)
        action = guarded["then"][0]["homeassistant.action"]
        self.assertEqual(action["action"], "remote.send_command")
        self.assertEqual(action["data"]["entity_id"], "${remote}")
        self.assertEqual(action["data"]["command"].value, "return command;")
        reset = config["api"]["on_client_disconnected"][0]["lambda"]
        self.assertIn('id(ts_tv).publish_state("")', reset)

    def test_back_label_in_both_languages(self):
        for language, label in (("en", "Back"), ("bg", "Назад")):
            config = load_yaml(ROOT / f"remote/lang/{language}.yaml")
            self.assertEqual(config["substitutions"]["txt_tv_back"], label)

    def test_languages_have_the_same_translation_keys(self):
        english = load_yaml(ROOT / "remote/lang/en.yaml")["substitutions"]
        bulgarian = load_yaml(ROOT / "remote/lang/bg.yaml")["substitutions"]
        self.assertEqual(set(english), set(bulgarian))
        for language in (english, bulgarian):
            for key, value in language.items():
                with self.subTest(key=key):
                    self.assertIsInstance(value, str)
                    self.assertTrue(value.strip())


if __name__ == "__main__":
    unittest.main()
