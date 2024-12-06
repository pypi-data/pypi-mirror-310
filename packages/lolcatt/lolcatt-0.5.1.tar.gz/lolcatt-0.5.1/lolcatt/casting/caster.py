#!/usr/bin/env python3
import subprocess
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Dict
from typing import List
from typing import Optional

from catt.api import CattDevice
from catt.api import discover
from catt.cli import get_config_as_dict
from catt.error import CastError

from .youtube_playlist_handler import YoutubePlaylistHandler


@dataclass
class CastState:
    """Dataclass for cast state, encapsulating info dictionaries of a catt controller."""

    cast_info: dict
    info: dict
    is_loading: bool = False
    loading_failed: bool = False
    queue_len: int = 0


class Caster:
    """
    Class encapsulating the catt.api.CattDevice.

    Provides a simple interface and enables exchange of the CattDevice on the fly.
    """

    CATT_ARGS = []
    CAST_ARGS = ['--force-default']

    def __init__(
        self,
        name_or_alias: Optional[str] = 'default',
        update_interval: float = 0.5,
        autoplay: bool = True,
        config: Dict = None,
    ):
        self._config = config if config is not None else {}
        self._yt_playlist_handler = YoutubePlaylistHandler(
            cookies_file=self._config.get('options', {}).get('youtube_cookies_file')
        )
        self._device = None
        self._queue = []
        self._current_item = None
        self._played_queue = []
        self._well_known_devices = {}
        self._available_devices = None
        self._catt_call = None
        self._catt_config = get_config_as_dict()
        self._loading_started = time.time()
        self._is_loading_cast = True
        self._media_loading_failed = False
        self._loading_timeout = 8
        self._update_interval = update_interval
        self._autoplay = autoplay
        self._state_last_updated = time.time()
        self._init_well_known_devices()
        self.change_device(name_or_alias)

    def _build_cast_args(self) -> List[str]:
        catt_cast_args = self.CAST_ARGS[:]

        # if we have a cookies file for youtube, attempt to mark videos as watched
        if self._config.get('options', {}).get('youtube_mark_watched', False):
            cookies_file = self._config.get('options', {}).get('youtube_cookies_file')
            if cookies_file is not None:
                cookies_file = str(Path(cookies_file).expanduser().resolve())
                catt_cast_args += [
                    '--ytdl-option=mark_watched=true',
                    f'--ytdl-option=cookiefile={cookies_file}',
                ]

        return catt_cast_args

    def _init_well_known_devices(self):
        for _, device_name in self._catt_config['aliases'].items():
            try:
                self._well_known_devices[device_name] = CattDevice(device_name)
            except Exception:
                pass

    def cast(self, url_or_path: str):
        """
        Casts the given url or path to the currently active device.

        :param url_or_path: The url or path to cast.
        """
        if self._catt_call is not None:
            self._catt_call.kill()
        if self._device is None:
            raise ValueError('Can\'t cast: No device selected.')
        full_catt_args = [
            'catt',
            *self.CATT_ARGS,
            '-d',
            self._device_name,
            'cast',
            *self._build_cast_args(),
            url_or_path,
        ]
        self._catt_call = subprocess.Popen(
            full_catt_args,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        self._trigger_is_loading()

    def cast_next(self):
        """
        Casts the next item in the queue to the currently active device.
        """
        if self._current_item is not None:
            self._played_queue.append(self._current_item)
            self._current_item = None
        if len(self._queue) > 0:
            self._current_item = self._queue.pop(0)
            self.cast(self._current_item)
        else:
            try:
                self._device.stop()
            except CastError:
                pass

    def cast_previous(self):
        """
        Casts the previous item in the queue to the currently active device.
        """
        if self._current_item is not None:
            self._queue.insert(0, self._current_item)
            self._current_item = None
        if len(self._played_queue) > 0:
            self._current_item = self._played_queue.pop()
            self.cast(self._current_item)

    def cast_at_idx(self, idx: int):
        """
        Skips to the item at the given index in the queues.
        """
        if idx == 0:
            return
        if idx < 0:
            prev_idx = len(self._played_queue) + idx
            if prev_idx < 0:
                return
            self._queue.insert(0, self._current_item)
            self._queue = self._played_queue[prev_idx + 1 :] + self._queue
            self._played_queue = self._played_queue[: prev_idx + 1]
            self._current_item = self._played_queue.pop(-1)
        else:
            if idx > len(self._queue):
                return
            self._played_queue.append(self._current_item)
            self._played_queue += self._queue[: idx - 1]
            self._current_item = self._queue.pop(idx - 1)
            self._queue = self._queue[idx - 1 :]
        self.cast(self._current_item)

    def stop_cast(self):
        """
        Stops the current cast.
        """
        if self._current_item is not None:
            self._played_queue.append(self._current_item)
            self._current_item = None
        if self._catt_call is not None:
            self._catt_call.kill()
        if self._device is not None:
            self._device.stop()

    def enqueue(self, url_or_path: str, front: bool = False):
        """
        Enqueues the given url or path to the queue.

        :param url_or_path: The url or path to enqueue.
        :param front: If True, the url or path is added to the front of the queue.
        """
        if 'youtube' in url_or_path and 'playlist?' in url_or_path:
            self._trigger_is_loading()
            all_new_urls = self._yt_playlist_handler.resolve_playlist(url_or_path)
            self._queue = all_new_urls + self._queue if front else self._queue + all_new_urls
        else:
            self._queue.append(url_or_path) if not front else self._queue.insert(0, url_or_path)

    def clear_queue(self):
        """
        Clears the queue.
        """
        self._queue = []

    def get_queue(self) -> List[str]:
        """
        Returns the current queue.

        :return: The current queue.
        """
        return self._queue

    def get_current_item(self) -> Optional[str]:
        """
        Returns the currently playing item.

        :return: The currently playing item.
        """
        return self._current_item

    def get_played_queue(self) -> List[str]:
        """
        Returns the played queue.

        :return: The played queue.
        """
        return self._played_queue

    def get_well_known_devices(self) -> Dict[str, CattDevice]:
        """
        Returns well known devices which have aliases set.

        :return: Well known devices.
        """
        return self._well_known_devices

    def get_available_devices(self) -> List[CattDevice]:
        """
        Runs Chromecast discovery and returns a list of available CattDevices.

        :return: A list of available CattDevices.
        """
        self._available_devices = discover()
        return self._available_devices

    def _get_device_name(self, name_or_alias: Optional[str]) -> Optional[str]:
        """
        Returns the device name for the given device name or alias.
        """
        if name_or_alias == 'default':
            device_name = self._catt_config['options'].get('device')
            if device_name is None:
                print(
                    'No default device set. '
                    'Scanning for all available devices and picking first...'
                )
                print(
                    'To skip this in the future, either pass a device name '
                    'or set a default device in the catt config file.'
                )
                possible_devices = self.get_available_devices()
                if len(possible_devices) > 0:
                    device_name = possible_devices[0].name
        elif name_or_alias == 'None':
            device_name = None
        elif name_or_alias is not None:
            device_name = self._catt_config['aliases'].get(name_or_alias, name_or_alias)
        else:
            device_name = None
        return device_name

    def change_device(self, name_or_alias: Optional[str] = None):
        """
        Changes the currently active device to the given name or alias. If the device is not
        available, a ValueError is raised.

        :param name_or_alias: The name or alias of the device to change to.
        """
        self._device_name = self._get_device_name(name_or_alias)

        if self._device_name is not None:
            if self._device_name in self._well_known_devices:
                self._device = self._well_known_devices[self._device_name]
            else:
                try:
                    self._device = CattDevice(self._device_name)
                except CastError as e:
                    print(f'Selected device "{self._device_name}" was not found on this network.')
                    print('Scan for available devices using "lolcatt --scan".')
                    raise ValueError(f'No device with name or alias "{name_or_alias}" found: {e}')
        self._loading_started = None
        self._is_loading_cast = False

    def get_device(self) -> Optional[CattDevice]:
        """
        Returns the currently active CattDevice.

        :return: The currently active CattDevice.
        """
        return self._device

    def get_device_name(self) -> Optional[str]:
        """
        Returns the name of the currently active CattDevice.

        :return: The name of the currently active CattDevice.
        """
        return self._device_name

    def get_update_interval(self) -> float:
        """
        Returns the update interval of the CastState. Determines how often UI elements are need to
        be updated.

        :return: The update interval of the CastState.
        """
        return self._update_interval

    def _trigger_is_loading(self):
        self._loading_started = time.time()
        self._is_loading_cast = True

    def _tick(self):
        """
        Internal method that is called on every call to update the CastState.
        """
        if self._device is None:
            return

        if (
            self._autoplay
            and self._device.controller.info.get('idle_reason') == 'FINISHED'
            and len(self._queue) > 0
        ):
            self.cast_next()

        if time.time() - self._state_last_updated > self._update_interval:
            self._device.controller._update_status()
            self._state_last_updated = time.time()

        if self._is_loading_cast and time.time() - self._loading_started > self._loading_timeout:
            self._loading_started = None
            self._is_loading_cast = False
            self._media_loading_failed = True

        if self._device.controller.cast_info.get('player_state') in [
            'PLAYING',
            'BUFFERING',
            'PAUSED',
        ]:
            self._loading_started = None
            self._is_loading_cast = False

    def get_cast_state(self) -> CastState:
        """
        Returns a CastState object encapsulating the info dictionaries of the currently active
        CattDevice.

        :return: A CastState object
        """
        self._tick()
        if self._device is None:
            cs = CastState({}, {}, False, False, 0)
        else:
            cs = CastState(
                self._device.controller.cast_info,
                self._device.controller.info,
                is_loading=self._is_loading_cast,
                loading_failed=self._media_loading_failed,
                queue_len=len(self._queue),
            )
            self._media_loading_failed = False
        return cs
