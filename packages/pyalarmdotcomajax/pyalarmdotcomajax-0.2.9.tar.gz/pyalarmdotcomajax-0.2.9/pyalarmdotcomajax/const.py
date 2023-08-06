"""Constants."""
from __future__ import annotations

from datetime import datetime
from enum import Enum
from enum import IntEnum
from typing import Any
from typing import TypedDict

TWO_FACTOR_COOKIE_NAME = "twoFactorAuthenticationId"


class AuthResult(Enum):
    """Standard for reporting results of login attempt."""

    SUCCESS = "success"
    OTP_REQUIRED = "otp_required"
    ENABLE_TWO_FACTOR = "enable_two_factor"


class ExtendedEnumMixin(Enum):
    """Search and export-list functions to enums."""

    @classmethod
    def has_value(cls, value: str) -> bool:
        """Return whether value exists in enum."""
        return value in cls._value2member_map_

    @classmethod
    def list(cls) -> list:
        """Return list of all enum members."""

        def get_enum_value(enum_class: Enum) -> Any:
            """Mypy choked when this was expressed as a lambda."""
            return enum_class.value

        return list(map(get_enum_value, cls))


class ADCOtpType(Enum):
    """Alarm.com two factor authentication type."""

    # https://www.alarm.com/web/system/assets/customer-ember/enums/TwoFactorAuthenticationType.js

    DISABLED = 0
    APP = 1
    SMS = 2
    EMAIL = 4


class ADCTroubleCondition(TypedDict):
    """Alarm.com alert / trouble condition."""

    message_id: str
    title: str
    body: str
    device_id: str


class ADCRelationshipType(Enum):
    """Library of identified ADC device families."""

    SYSTEM = "systems/system"
    SENSOR = "devices/sensor"
    PARTITION = "devices/partition"
    LOCK = "devices/lock"
    GARAGE_DOOR = "devices/garage-door"
    IMAGE_SENSOR_IMAGE = "image-sensor/image-sensor"
    LIGHT = "devices/light"

    # Not Supported
    # THERMOSTAT = "devices/thermostat"
    # CONFIGURATION = "systems/configuration"
    # LIGHT = "devices/light"
    # CAMERA = "video/camera"
    # GEO_DEVICE = "geolocation/geo-device"
    # GEO_FENCE = "geolocation/fence"
    # SCENE = "automation/scene"


class ADCDeviceType(ExtendedEnumMixin):
    """Enum of SUPPORTED devices using ADC ids."""

    SYSTEM = "systems"
    SENSOR = "sensors"
    PARTITION = "partitions"
    LOCK = "locks"
    GARAGE_DOOR = "garageDoors"
    IMAGE_SENSOR = "imageSensors"
    LIGHT = "lights"

    # Not Supported
    # THERMOSTAT = "thermostats"
    # CONFIGURATION = "configuration"
    # CAMERA = "camera"
    # GEO_DEVICE = "geo-device"
    # GEO_FENCE = "fence"
    # SCENE = "scene"


class ADCSensorSubtype(IntEnum):
    """Library of identified ADC device types."""

    CONTACT_SENSOR = 1
    MOTION_SENSOR = 2
    SMOKE_DETECTOR = 5
    FREEZE_SENSOR = 8
    CO_DETECTOR = 6
    PANIC_BUTTON = 9
    GLASS_BREAK_DETECTOR = 19
    PANEL_MOTION_SENSOR = 89
    PANEL_GLASS_BREAK_DETECTOR = 83
    PANEL_IMAGE_SENSOR = 68
    MOBILE_PHONE = 69


class ADCPartitionCommand(Enum):
    """Commands for ADC partitions."""

    DISARM = "disarm"
    ARM_STAY = "armStay"
    ARM_AWAY = "armAway"


class ADCLockCommand(Enum):
    """Commands for ADC locks."""

    LOCK = "lock"
    UNLOCK = "unlock"


class ADCGarageDoorCommand(Enum):
    """Commands for ADC garage doors."""

    OPEN = "open"
    CLOSE = "close"


class ADCLightCommand(Enum):
    """Commands for ADC lights."""

    ON = "turnOn"
    OFF = "turnOff"


class ADCImageSensorCommand(Enum):
    """Commands for ADC image sensors."""

    PEEK_IN = "doPeekInNow"


class ElementSpecificData(TypedDict, total=False):
    """Hold entity-type-specific metadata."""

    images: list[ImageData] | None


class ImageData(TypedDict):
    """Holds metadata for image sensor images."""

    id_: str
    image_b64: str
    image_src: str
    description: str
    timestamp: datetime
