#!/usr/bin/env python3
"""GitHub status for Waybar — official API: githubstatus.com/api/v2/summary.json"""

import json
import urllib.error
import urllib.request

API = "https://www.githubstatus.com/api/v2/summary.json"

ICONS = {
    "none": "\uf058",
    "minor": "\uf071",
    "major": "\uf06a",
    "critical": "\uf0e7",
}

STATUS = {
    "degraded_performance": "degraded",
    "partial_outage": "partial outage",
    "major_outage": "major outage",
}


def waybar(data: dict) -> dict:
    indicator = data["status"]["indicator"]
    css = indicator if indicator in ICONS else "error"
    icon = ICONS.get(indicator, "\uf057")

    tooltip = [f"GitHub: {data['status']['description']}"]

    bad = [
        f"  • {c['name']}: {STATUS.get(c['status'], c['status'].replace('_', ' '))}"
        for c in data.get("components", [])
        if not c.get("group") and c["status"] != "operational"
    ]
    if bad:
        tooltip += ["", "Affected components:", *bad]

    for title, key in (("Incidents", "incidents"), ("Maintenance", "scheduled_maintenances")):
        items = data.get(key, [])
        if items:
            tooltip += ["", f"{title}:"] + [
                f"  • {i['name']} ({i['status'].replace('_', ' ')})" for i in items
            ]

    if updated := data.get("page", {}).get("updated_at"):
        tooltip += ["", f"Updated: {updated}"]

    tooltip.append("\nClick → githubstatus.com")

    label = "OK" if indicator == "none" else indicator.upper()
    return {
        "text": f"{icon} {label}",
        "tooltip": "\n".join(tooltip),
        "class": css,
        "alt": css,
    }


def main() -> None:
    try:
        req = urllib.request.Request(API, headers={"User-Agent": "waybar-github-status"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            out = waybar(json.load(resp))
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError, KeyError) as err:
        out = {
            "text": "\uf057 ERR",
            "tooltip": f"Could not reach GitHub\n{err}",
            "class": "error",
            "alt": "error",
        }

    print(json.dumps(out, ensure_ascii=False))


if __name__ == "__main__":
    main()
