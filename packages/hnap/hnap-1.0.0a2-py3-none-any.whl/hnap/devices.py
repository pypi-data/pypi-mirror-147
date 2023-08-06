# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Luis López <luis@cuarentaydos.com>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301,
# USA.


import functools
import logging
from datetime import datetime
from enum import Enum

from .soapclient import MethodCallError, SoapClient

_LOGGER = logging.getLogger(__name__)


def auth_required(fn):
    @functools.wraps(fn)
    def _wrap(device, *args, **kwargs):
        if not device.client.authenticated:
            device.client.authenticate()
            _LOGGER.debug("Device authenticated")
        return fn(device, *args, **kwargs)

    return _wrap


def DeviceFactory(
    *, client=None, hostname=None, password=None, username="Admin", port=80
):
    client = client or SoapClient(
        hostname=hostname, password=password, username=username, port=port
    )
    info = client.device_info()

    module_types = info["ModuleTypes"]
    if not isinstance(module_types, list):
        module_types = [module_types]

    if "Audio Renderer" in module_types:
        cls = Siren
    # 'Optical Recognition', 'Environmental Sensor', 'Camera']
    elif "Camera" in module_types:
        cls = Camera
    elif "Motion Sensor" in module_types:
        cls = Motion
    else:
        raise TypeError(module_types)

    return cls(client=client)


class Device:
    MODULE_TYPE: str

    def __init__(
        self,
        *,
        client=None,
        hostname=None,
        password=None,
        username="Admin",
        port=80,
    ):
        self.client = client or SoapClient(
            hostname=hostname, password=password, username=username, port=port
        )
        self._info = None
        self._module_id = None
        self._controller = None

    @property
    def info(self):
        if not self._info:
            self._info = self.client.device_info()

        return self._info

    @property
    def module_id(self):
        if not self._module_id:
            self._module_id = self.info["ModuleTypes"].find(self.MODULE_TYPE) + 1

        return self._module_id

    @property
    def controller(self):
        # NOTE: not sure about this
        return self.module_id

    def call(self, *args, **kwargs):
        kwargs["ModuleID"] = kwargs.get("ModuleID") or self.module_id
        kwargs["Controller"] = kwargs.get("Controller") or self.controller

        return self.client.call(*args, **kwargs)

    # def get_info(self):
    #     info = self.client.device_info()

    #     if isinstance(info["ModuleTypes"], str):
    #         info["ModuleTypes"] = [info["ModuleTypes"]]

    #     dev = set(info["ModuleTypes"])
    #     req = set(self.REQUIRED_MODULE_TYPES)
    #     if not req.issubset(dev):
    #         raise TypeError(
    #             f"device '{self.client.hostname}' is not a "
    #             f"{self.__class__.__name__}",
    #         )

    #     return info


class Camera(Device):
    MODULE_TYPE = "Camera"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._base_url = (
            "http://"
            + f"{self.client.username.lower()}:{self.client.password}@"
            + f"{self.client.hostname}:{self.client.port}"
        )

    @property
    def stream_url(self):
        return f"{self._base_url}/play1.sdp"

    @property
    def picture_url(self):
        return f"{self._base_url}/image/jpeg.cgi"


class Motion(Device):
    MODULE_TYPE = "Motion Sensor"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._backoff = None

    @property
    def backoff(self):
        if self._backoff is None:
            resp = self.call("GetMotionDetectorSettings")
            try:
                self._backoff = int(resp["Backoff"])
            except (KeyError, ValueError, TypeError):
                # Return the default value for tested devices but don't store
                # to force retry
                return 30

        return self._backoff

    # @backoff.setter
    # def backoff(self, seconds):
    #     self.client.call(
    #         "SetMotionDetectorSettings", ModuleID=1, Backoff=self._backoff
    #     )
    #     _LOGGER.warning("set backoff property has no effect")

    # def authenticate(self):
    #     super().authenticate()

    #     res = self.client.call("GetMotionDetectorSettings", ModuleID=1)
    #     try:
    #         self._backoff = int(res["Backoff"])
    #     except (ValueError, TypeError, KeyError):
    #         _LOGGER.warning("Unable to get delta from device")

    @auth_required
    def get_latest_detection(self):
        res = self.call("GetLatestDetection")
        return datetime.fromtimestamp(float(res["LatestDetectTime"]))

    @auth_required
    def is_active(self):
        now = datetime.now()
        diff = (now - self.get_latest_detection()).total_seconds()

        return diff <= self.backoff


class Router(Device):
    # NOT tested
    # See https://github.com/waffelheld/dlink-device-tracker/blob/master/custom_components/dlink_device_tracker/dlink_hnap.py#L95  # noqa: E501
    MODULE_TYPE = "check-module-types-for-router"

    @auth_required
    def get_clients(self):
        res = self.call("GetClientInfo")
        clients = res["ClientInfoLists"]["ClientInfo"]

        # Filter out offline clients
        # clients = [x for x in clients if x["Type"] != "OFFLINE"]

        ret = [
            {
                "name": client["DeviceName"],
                "nickName": client["NickName"],
                "is_connected": client["Type"] == "OFFLINE" and 0 or 1,
                "mac": client["MacAddress"],
            }
            for client in clients
        ]
        return ret


class SirenSound(Enum):
    EMERGENCY = 1
    FIRE = 2
    AMBULANCE = 3
    POLICE = 4
    DOOR_CHIME = 5
    BEEP = 6

    @classmethod
    def fromstring(cls, s):
        s = s.upper()
        for c in ["-", " ", "."]:
            s = s.replace(c, "_")

        return getattr(cls, s)


class Siren(Device):
    MODULE_TYPE = "Audio Renderer"

    @auth_required
    def is_playing(self):
        res = self.call("GetSirenAlarmSettings")
        return res["IsSounding"] == "true"

    @auth_required
    def play(self, sound=SirenSound.EMERGENCY, volume=100, duration=60):
        ret = self.call(
            "SetSoundPlay",
            SoundType=sound.value,
            Volume=volume,
            Duration=duration,
        )
        if ret["SetSoundPlayResult"] != "OK":
            raise MethodCallError(f"Unable to play. Response: {ret}")

    @auth_required
    def beep(self, volume=100, duration=1):
        return self.play(sound=SirenSound.BEEP, duration=duration, volume=volume)

    @auth_required
    def stop(self):
        ret = self.call("SetAlarmDismissed")

        if ret["SetAlarmDismissedResult"] != "OK":
            raise MethodCallError(f"Unable to stop. Response: {ret}")


class Water(Device):
    # NOT tested
    MODULE_TYPE = "check-module-types-for-water-detector"

    @auth_required
    def is_active(self):
        ret = self.call("GetWaterDetectorState")
        return ret.get("IsWater") == "true"
