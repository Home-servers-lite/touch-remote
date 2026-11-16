#pragma once

#include <string>

namespace remote_status {

inline std::string connection_message(bool wifi, bool ha, const char *no_wifi, const char *no_ha) {
  if (!wifi) return no_wifi;
  if (!ha) return no_ha;
  return "";
}

inline bool tv_available(bool connected, const std::string &state) {
  return connected && (state == "on" || state == "off");
}

}  // namespace remote_status
