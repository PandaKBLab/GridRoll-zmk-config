# SPDX-License-Identifier: MIT
zephyr_library()
zephyr_library_sources_ifdef(CONFIG_GRIDROLL_STUDIO_BLE_DISCOVERY drivers/studio/discovery.c)
zephyr_library_sources_ifdef(CONFIG_GRIDROLL_PRECISION drivers/input/precision.c)
zephyr_library_sources_ifdef(CONFIG_GRIDROLL_STATUS_LED drivers/status/status_led.c)
zephyr_library_sources_ifdef(CONFIG_GRIDROLL_WHEEL_STEP drivers/input/wheel_step.c)
zephyr_library_sources_ifdef(CONFIG_GRIDROLL_USB_AUTO_OUTPUT drivers/usb/usb_output.c)
zephyr_library_sources_ifdef(CONFIG_GRIDROLL_PAW3222 drivers/input/paw3222.c drivers/input/paw3222_sdio.c)
if(CONFIG_GRIDROLL_PAW3222 OR CONFIG_GRIDROLL_USB_AUTO_OUTPUT OR CONFIG_GRIDROLL_STATUS_LED OR CONFIG_GRIDROLL_PRECISION OR CONFIG_GRIDROLL_STUDIO_BLE_DISCOVERY)
  # The module reads the selected USB/BLE endpoint. ZMK's app-private include
  # directory is not otherwise inherited by a Zephyr module library.
  zephyr_library_include_directories(${APPLICATION_SOURCE_DIR}/include)
endif()
zephyr_library_sources_ifdef(CONFIG_NEWLIB_LIBC drivers/compat/newlib_fini.c)

# Pinned runtime-input/ZMK revisions use printf functions without stdio.h
# in several Studio sources. Supply declarations without editing fetched code.
if(CONFIG_ZMK_RUNTIME_INPUT_PROCESSOR_STUDIO_RPC)
  target_compile_options(app PRIVATE -include stdio.h)
endif()
