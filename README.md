# GitHub Status for Waybar

Shows GitHub system status in Waybar using the official API: `https://www.githubstatus.com/api/v2/summary.json`

## Setup

```bash
chmod +x scripts/github-status.py
```

Add to `~/.config/waybar/config.jsonc`:

```jsonc
"custom/github-status": {
  "exec": "/path/to/github-status/scripts/github-status.py",
  "return-type": "json",
  "interval": 300,
  "tooltip": true,
  "on-click": "xdg-open https://www.githubstatus.com/"
}
```

Copy `waybar/style.css` into your Waybar config. It uses FontAwesome Icons.

Reload: `killall -SIGUSR2 waybar`
