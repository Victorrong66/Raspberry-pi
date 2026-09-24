# Raspberry Pi RGB Matrix Dashboard

A phone-connected dashboard for a Raspberry Pi + HUB75 RGB LED matrix panel.
Rotates through scenes: clock/date, weather, and Spotify now-playing, with
more app integrations (Messages, calendar, etc.) planned as follow-ups.

## Hardware

- Raspberry Pi 3 Model B+
- Adafruit RGB Matrix Bonnet
- 64x32 HUB75 RGB LED matrix panel, 4mm pitch
- 5V 4A switching power supply (5.5mm/2.1mm barrel jack)

Wire the panel to the Bonnet's ribbon cable, plug the Bonnet onto the Pi's
GPIO header, and feed the power supply into the Bonnet's barrel jack (it
powers both the panel and, via a jumper, the Pi itself). See
[Adafruit's RGB Matrix Bonnet guide](https://learn.adafruit.com/adafruit-rgb-matrix-bonnet-for-raspberry-pi)
for wiring photos and the power jumper setting.

## Setup on the Pi

```bash
git clone <this repo> ~/dashboard
cd ~/dashboard
./scripts/install_pi.sh
```

This builds [hzeller/rpi-rgb-led-matrix](https://github.com/hzeller/rpi-rgb-led-matrix)
(the driver library) from source, sets up a Python virtualenv, and installs
a systemd service.

Then:

1. Copy your API keys into `.env` (created from `.env.example` by the
   install script):
   - `OPENWEATHER_API_KEY` - free key from [openweathermap.org/api](https://openweathermap.org/api)
   - `LOCATION` - a city name like `Seattle,US`, or `lat,lon`
   - `SPOTIFY_CLIENT_ID` / `SPOTIFY_CLIENT_SECRET` - create an app at
     [developer.spotify.com/dashboard](https://developer.spotify.com/dashboard)
     (set its Redirect URI to match `SPOTIFY_REDIRECT_URI` in `.env`)
2. Run the one-time Spotify login: `.venv/bin/python scripts/spotify_auth.py`
   - This prints a URL to open on your phone/laptop and asks you to paste
     back the redirect URL. It then prints a `SPOTIFY_REFRESH_TOKEN` to add
     to `.env`. You only need to do this once - the token doesn't expire.
3. Start it: `sudo systemctl start dashboard`
   - Check logs: `journalctl -u dashboard -f`
   - Runs on boot automatically (`install_pi.sh` already enabled it)

Any scene whose API keys aren't set is skipped automatically - so you can
start with just the clock working and add weather/Spotify later.

## Local development (no hardware required)

`display/matrix.py` falls back to writing each frame to `preview.png`
instead of driving real hardware when the `rgbmatrix` bindings aren't
installed - which is the case on any machine other than the Pi. This lets
you iterate on layouts without the physical panel:

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
cp .env.example .env   # fill in whichever API keys you want to test
.venv/bin/python main.py
```

Open `preview.png` to see the current frame; it updates continuously while
the script runs.

## Project layout

```
main.py                 # scene rotation loop
config.py                # loads .env
display/matrix.py        # real hardware vs. PNG-preview abstraction
display/fonts.py         # shared font loader
display/icons.py         # small vector weather icons
widgets/base.py           # Scene base class
widgets/clock.py          # date/time scene
widgets/weather.py        # weather scene
widgets/spotify.py        # now-playing scene
services/weather_service.py   # OpenWeatherMap client
services/spotify_service.py   # Spotify Web API client (via spotipy)
scripts/install_pi.sh     # one-shot setup script for the Pi
scripts/spotify_auth.py   # one-time Spotify OAuth helper
scripts/dashboard.service # systemd unit
```

## Adding a new scene

Subclass `widgets.base.Scene`:

- `refresh()` - called once when the scene becomes active; do network calls
  here, not in `render()`.
- `is_available()` - return `False` to have the rotation skip this scene
  (e.g. Spotify when nothing is playing).
- `render(image, draw)` - draw onto the 64x32 PIL image using `draw`.

Then add an instance to `build_scenes()` in `main.py`.

## Troubleshooting

- **Flicker/ghosting**: try raising `MATRIX_GPIO_SLOWDOWN` in `.env` (1-4).
- **Nothing lights up**: double check the power jumper on the Bonnet and
  that `MATRIX_HARDWARE_MAPPING=adafruit-hat` matches your board.
- **Permission errors**: the matrix library needs direct memory/GPIO
  access, which is why the systemd service and any manual run need to be
  as root (`sudo .venv/bin/python main.py` for manual testing).

## Planned / not yet built

- iPhone Messages/notifications via a Shortcuts automation posting to a
  small webhook on the Pi (Apple has no direct notification API, unlike
  Android).
- Calendar, transit, and other scene ideas discussed but not yet scaffolded.
