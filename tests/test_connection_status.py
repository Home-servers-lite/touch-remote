from pathlib import Path
import subprocess
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]


class ConnectionStatusTest(unittest.TestCase):
    def test_connection_and_tv_states(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "status.cpp"
            binary = Path(directory) / "status"
            source.write_text(r'''
#include "esphome/remote/connection_status.h"
#include <cassert>

int main() {
  for (bool wifi : {false, true}) {
    for (bool ha : {false, true}) {
      const char *expected = !wifi ? "No Wi-Fi" : !ha ? "No HA" : "";
      assert(remote_status::connection_message(wifi, ha, "No Wi-Fi", "No HA") == expected);
    }
  }
  for (const std::string state : {"on", "off", "unknown", "unavailable", "", "playing"}) {
    assert(!remote_status::tv_available(false, state));
    assert(remote_status::tv_available(true, state) == (state == "on" || state == "off"));
  }
  assert(remote_status::connection_message(false, true, "Няма Wi-Fi", "Няма HA") == "Няма Wi-Fi");
}
''')
            compile_result = subprocess.run(
                ["c++", "-std=c++17", "-Wall", "-Wextra", "-Werror", "-I", str(ROOT), str(source), "-o", str(binary)],
                capture_output=True, text=True, timeout=60,
            )
            self.assertEqual(compile_result.returncode, 0, compile_result.stderr)
            result = subprocess.run([str(binary)], capture_output=True, text=True, timeout=10)
            self.assertEqual(result.returncode, 0, result.stderr)
