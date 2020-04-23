"""Fully Kiosk Browser media_player entity."""
import json
import logging

from homeassistant.components.media_player import (
    DEVICE_CLASS_SPEAKER,
    SUPPORT_PLAY_MEDIA,
    MediaPlayerDevice,
)
from homeassistant.helpers.dispatcher import async_dispatcher_connect

from .const import DOMAIN, COORDINATOR, CONTROLLER

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up the Fully Kiosk Browser media player."""
    coordinator = hass.data[DOMAIN][config_entry.entry_id][COORDINATOR]
    controller = hass.data[DOMAIN][config_entry.entry_id][CONTROLLER]

    device_info = {
        "identifiers": {(DOMAIN, coordinator.data["deviceID"])},
        "name": coordinator.data["deviceName"],
        "manufacturer": coordinator.data["deviceManufacturer"],
        "model": coordinator.data["deviceModel"],
        "sw_version": coordinator.data["appVersionName"],
    }

    async_add_entities([FullyMediaPlayer(coordinator, controller, device_info)], False)


class FullyMediaPlayer(MediaPlayerDevice):
    def __init__(self, coordinator, controller, device_info):
        self._name = f"{coordinator.data['deviceName']} Media Player"
        self._device_info = device_info
        self.coordinator = coordinator
        self.controller = controller
        self._unique_id = f"{coordinator.data['deviceID']}-mediaplayer"

    @property
    def name(self):
        return self._name

    @property
    def supported_features(self):
        return SUPPORT_PLAY_MEDIA

    @property
    def device_info(self):
        return self._device_info

    @property
    def unique_id(self):
        return self._unique_id

    def play_media(self, media_type, media_id, **kwargs):
        _LOGGER.warning("play media: %s :: %s", media_type, media_id)
        self.controller.playSound(media_id)

    async def async_added_to_hass(self):
        """Connect to dispatcher listening for entity data notifications."""
        self.async_on_remove(
            self.coordinator.async_add_listener(self.async_write_ha_state)
        )

    async def async_update(self):
        """Update Fully Kiosk Browser entity."""
        await self.coordinator.async_request_refresh()