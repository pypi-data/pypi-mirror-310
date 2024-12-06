from typing import Any, Optional
import os
import json


def _read_icons() -> dict[str, Any]:
    try:
        with open(os.path.join(os.path.dirname(__file__), "data.json")) as f:
            return json.load(f)
    except Exception as e:
        print("Error reading octicons", e)
        return {}


_octicons = _read_icons()


def octicon(name: str, size: int | str) -> Optional[str]:
    icon = _octicons.get(name)
    if not icon:
        return None

    closest_size = find_closest_size(int(size), icon["heights"].keys())
    sized_icon = icon["heights"].get(closest_size)

    classes = ["octicon", f"octicon-{name}"]

    attributes = sized_icon["ast"]["attributes"] | {
        "class": " ".join(classes),
        "width": size,
        "height": size,
    }

    attributes_str = " ".join(f"{k}='{v}'" for k, v in attributes.items())

    return f"<svg {attributes_str}>{sized_icon['path']}</svg>"


def find_closest_size(requested_size: int, icon_sizes: list[str]) -> str:
    available_sizes = [int(size) for size in icon_sizes]
    return str(min(available_sizes, key=lambda size: abs(size - requested_size)))
