import base64
import os
from pathlib import Path
import secrets
import shutil
import subprocess
import sys
import tempfile
import unittest

from esphome.yaml_util import dump, load_yaml


ROOT = Path(__file__).resolve().parents[1]


class ConfigurationTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        workspace = tempfile.TemporaryDirectory(prefix="touch-remote-tests-")
        cls.addClassCleanup(workspace.cleanup)
        cls.directory = Path(workspace.name) / "esphome"
        shutil.copytree(
            ROOT / "esphome",
            cls.directory,
            ignore=shutil.ignore_patterns("secrets.yaml", ".esphome"),
        )
        (cls.directory / "secrets.yaml").write_text(dump({
            "wifi_ssid": "test-network",
            "wifi_password": "test-password",
            "ap_password": "test-fallback-password",
            "api_encryption_key": base64.b64encode(secrets.token_bytes(32)).decode(),
        }))

    def generate(self, config, full_build=False):
        command = [sys.executable, "-m", "esphome", "compile"]
        if not (full_build and os.environ.get("TOUCH_REMOTE_FULL_BUILD") == "1"):
            command.append("--only-generate")
        result = subprocess.run(
            [*command, str(config)],
            capture_output=True,
            text=True,
            timeout=1800 if full_build else 120,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertNotRegex(result.stdout + result.stderr, r"Font .+ is missing \d+ glyph")

    def test_full_english_configuration(self):
        self.generate(self.directory / "ha-remote.yaml", full_build=True)

    def test_full_bulgarian_configuration(self):
        config = self.directory / "ha-remote.yaml"
        bulgarian = self.directory / "bulgarian.yaml"
        bulgarian.write_text(config.read_text().replace("remote/lang/en.yaml", "remote/lang/bg.yaml"))
        self.generate(bulgarian, full_build=True)

    def generate_page(self, *prefixes):
        config = load_yaml(self.directory / "ha-remote.yaml")
        config["packages"] = {
            key: value for key, value in config["packages"].items()
            if key in ("language", "core", "settings") or key.startswith(prefixes)
        }
        path = self.directory / "single-page.yaml"
        path.write_text(dump(config))
        self.generate(path)

    def test_tv_alone(self):
        self.generate_page("tv")

    def test_lights_alone(self):
        self.generate_page("lights", "light_")

    def test_led_alone(self):
        self.generate_page("led")

    def test_appliances_alone(self):
        self.generate_page("appliances", "appliance_")

    def test_power_alone(self):
        self.generate_page("power")
