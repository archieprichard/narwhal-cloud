"""Work out which saved-map room the robot is currently in.

The saved map grid stores one value per cell: ``value >> 8`` is the room id
(0 for unassigned floor), and the low byte is the cell type. The robot pose
is converted to grid cells exactly as the map renderer places the robot
marker, so the room shown under the marker is the room reported here.
"""

from __future__ import annotations

from .map_renderer import _pixels, _pose_pixel
from .protocol import NarwalMap, NarwalRoom

# Cells to search outward when the robot sits on a wall/door/unassigned cell.
SEARCH_RADIUS = 4

_cache_key: bytes | None = None
_cache_values: list[int] = []


def _grid_values(map_data: NarwalMap) -> list[int]:
    """Decode the grid once per map revision; poses update every second."""
    global _cache_key, _cache_values
    if map_data.compressed_grid is not _cache_key:
        expected = map_data.width * map_data.height
        values = _pixels(map_data.compressed_grid)
        _cache_values = (values + [0] * expected)[:expected]
        _cache_key = map_data.compressed_grid
    return _cache_values


def _room_id_at(values: list[int], width: int, height: int, x: int, y: int) -> int:
    if not (0 <= x < width and 0 <= y < height):
        return 0
    value = values[y * width + x]
    if value in (0, 0x20, 0x28):
        return 0
    return value >> 8


def current_room(map_data: NarwalMap) -> NarwalRoom | None:
    """Return the room under the robot, or None when it can't be determined."""
    if (
        not map_data.compressed_grid
        or map_data.width <= 0
        or map_data.height <= 0
        or not map_data.rooms
    ):
        return None
    pixel = _pose_pixel(map_data)
    if pixel is None:
        return None
    try:
        values = _grid_values(map_data)
    except Exception:  # noqa: BLE001 - corrupt grid must not break updates
        return None
    width, height = map_data.width, map_data.height
    cx, cy = int(pixel[0]), int(pixel[1])
    rooms = {room.room_id: room for room in map_data.rooms}

    room_id = _room_id_at(values, width, height, cx, cy)
    if room_id not in rooms:
        # Nearest assigned cell within the search radius (ring by ring).
        room_id = 0
        for radius in range(1, SEARCH_RADIUS + 1):
            counts: dict[int, int] = {}
            for dx in range(-radius, radius + 1):
                for dy in range(-radius, radius + 1):
                    if max(abs(dx), abs(dy)) != radius:
                        continue
                    found = _room_id_at(values, width, height, cx + dx, cy + dy)
                    if found in rooms:
                        counts[found] = counts.get(found, 0) + 1
            if counts:
                room_id = max(counts, key=counts.get)
                break
    return rooms.get(room_id)
