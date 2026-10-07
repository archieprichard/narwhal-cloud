"""Tests for deriving the current room from the robot pose."""

from __future__ import annotations

import importlib.util
import sys
import zlib
from pathlib import Path

import test_live_map  # noqa: F401 - registers narwal_cloud.map_renderer
from test_auth import API  # noqa: F401 - registers the narwal_cloud package

PROTOCOL = sys.modules["narwal_cloud.protocol"]
ROOT = Path(__file__).parents[1] / "custom_components" / "narwal_cloud"


def _load_locator():
    spec = importlib.util.spec_from_file_location(
        "narwal_cloud.room_locator", ROOT / "room_locator.py"
    )
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


LOCATOR = _load_locator()


def _varint(value: int) -> bytes:
    out = bytearray()
    while value > 0x7F:
        out.append(value & 0x7F | 0x80)
        value >>= 7
    out.append(value)
    return bytes(out)


def _grid(width: int, height: int) -> tuple[bytes, list[int]]:
    """Left half room 1 (Kitchen), right half room 2 (Hallway), wall at x=5."""
    values: list[int] = []
    for _y in range(height):
        for x in range(width):
            if x == 5:
                values.append(0x20)
            elif x < 5:
                values.append((1 << 8) | 0x01)
            else:
                values.append((2 << 8) | 0x01)
    return zlib.compress(b"".join(_varint(v) for v in values)), values


def _map(x: float, y: float):
    compressed, _ = _grid(10, 6)
    return PROTOCOL.NarwalMap(
        width=10,
        height=6,
        rooms=(
            PROTOCOL.NarwalRoom(room_id=1, name="Kitchen"),
            PROTOCOL.NarwalRoom(room_id=2, name="Hallway"),
        ),
        compressed_grid=compressed,
        robot_pose=PROTOCOL.NarwalPose(x=x, y=y),
    )


def test_room_under_robot() -> None:
    assert LOCATOR.current_room(_map(2.5, 3.0)).name == "Kitchen"
    assert LOCATOR.current_room(_map(7.2, 1.0)).name == "Hallway"


def test_robot_on_wall_uses_nearest_room() -> None:
    room = LOCATOR.current_room(_map(5.1, 3.0))
    assert room is not None and room.name in {"Kitchen", "Hallway"}


def test_no_pose_or_off_map_returns_none() -> None:
    m = _map(2.0, 2.0)
    assert LOCATOR.current_room(
        PROTOCOL.NarwalMap(**{**m.__dict__, "robot_pose": None})
    ) is None
    assert LOCATOR.current_room(_map(50.0, 50.0)) is None
