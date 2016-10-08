# server-hud

Status display running on an old LG netbook. Shows the status of the firewall 
and the web server.

![Screenshot](docs/images/screenshot.png)

The WebSocket daemon depends on the `tornado`and `watchdog` python packages.

## Security
**server-hud communicates in clear text over WebSocket connections. There is no
inherit security at all.** 
