# Narwal Cloud US for Home Assistant

An unofficial Home Assistant integration for Narwal robot vacuums on the **US**
Narwal Cloud (`us-app.narwaltech.com`), with room cleaning and a current-room
sensor.

> [!IMPORTANT]
> Not affiliated with Narwal. Narwal's cloud API is private and can change
> without notice.

## Status

Ported from the EU edition, which was live-tested on a Freo `YJCC012`. This US
build targets a Narwal Freo Z Ultra (product key `hEA7OEshlx`) on a US account
and is **under test**. It installs under the `narwal_cloud` domain, so it can sit
alongside the `narwal` integrations (nadavbau, sjmotew) without a HACS conflict.

## Examples

Clean the kitchen, then check a minute later that it's really there:

```yaml
actions:
  - action: narwal_cloud.clean_rooms
    target:
      entity_id: vacuum.zoomba
    data:
      rooms: [Kitchen]
  - delay: "00:01:00"
  - if:
      - condition: not
        conditions:
          - condition: state
            entity_id: vacuum.zoomba
            state: cleaning
          - condition: state
            entity_id: sensor.zoomba_current_room
            state: Kitchen
    then:
      - action: notify.notify
        data:
          message: "Zoomba isn't cleaning the kitchen ({{ states('sensor.zoomba_current_room') }})"
```

The robot drives from the dock first, so the current room may briefly be another
room on the way. Room names come from the Narwal app (the vacuum's `rooms`
attribute lists them).

## Features

- Narwal account login with automatic access/refresh-token renewal
- Manual app-token setup for existing installations
- Battery, movement, cleaning, fault, and turbo state
- Start, pause, resume, stop, and return to dock
- Cleaning modes: Freo Mind, vacuum, mop, vacuum-and-mop, and vacuum-then-mop
- Settings for suction, mop humidity, and cleaning cycles for the **next task**
- Saved map, rooms, robot position, live trajectory, and cleaning overlay
- Room/segment cleaning using Narwal's official per-room templates
- Persistent map and room-template cache across Home Assistant restarts
- Fail-closed room cleaning: no command is sent if a safe room template is missing
- Mop washing/drying controls and consumable remaining-time sensors
- Configurable state polling from 1 to 300 seconds (default: 1 second)
- **Current room** sensor (and `current_room` vacuum attribute), derived from the robot's live position on the saved map
- **`narwal_cloud.clean_rooms`** action that takes room names, e.g. `Kitchen`
- English and Danish Home Assistant translations

## Installation with HACS

1. Open HACS and choose **Custom repositories**.
2. Add `https://github.com/archieprichard/narwhal-cloud` as an
   **Integration** repository.
3. Install **Narwal Cloud US**.
4. Restart Home Assistant.
5. Go to **Settings → Devices & services → Add integration**.
6. Select **Narwal Cloud US (unofficial)** and sign in with your Narwal account.

Existing token-based entries can use **Reconfigure** to switch to automatic
account login. Manual token setup is documented in
[`docs/token_setup.md`](docs/token_setup.md).

## First-time map setup

Normally, you only need to open the official Narwal app **once after installing
the integration**. Open the map in the app and leave it open for approximately
**2 minutes**, even if the map appears sooner. This gives Home Assistant time to
receive both the map and the room-cleaning templates. Then close the app again.

Home Assistant saves the map and room-cleaning templates locally. They survive
normal Home Assistant restarts, integration updates, and Home Assistant Core
updates, so you do not need to open the Narwal app each time.

Open the app again only if:

- you change the map or room layout in the Narwal app;
- the integration is removed and installed again;
- Home Assistant reports that a room template is missing.

Until a valid room template is available, room cleaning is safely blocked rather
than risking a whole-home cleaning task.

## Important behavior and known limitations

- The vacuum card's fan-speed control selects suction for the **next cleaning
  task**. It does not currently change suction during an active task.
- Freo Mind uses Narwal's official automatic room plan; manual suction, humidity,
  and cycle choices are not applied to that mode.
- On the verified YJCC012 firmware, Narwal can report `in_station: false` while
  the robot is physically at the dock. Home Assistant may therefore show
  `idle` instead of `docked`; return-to-dock itself still works.
- A fresh cloud map request can time out while the app is closed. The last valid
  saved map remains available from the local cache.
- The detailed map-data camera exposes more raw map information than the normal
  rendered map camera. Keep it disabled unless you specifically need it.

## Privacy and security

Credentials are stored in Home Assistant's local config entry. They are not
written to this repository, diagnostics, or normal integration logs. Protect
your Home Assistant host and backups because they can contain local secrets.

Maps, room names, and robot positions describe a real home. Do not post raw MQTT
payloads, diagnostics containing identifiers, map geometry, broker addresses,
tokens, or unredacted logs in public issues.

## Documentation

- [`CHANGELOG.md`](CHANGELOG.md) — release history
- [`docs/discovered_features.md`](docs/discovered_features.md) — implemented and pending capabilities
- [`docs/protocol_yjcc012.md`](docs/protocol_yjcc012.md) — redacted protocol notes
- [`docs/token_setup.md`](docs/token_setup.md) — advanced manual-token setup

## Ownership, attribution, and license

Not affiliated with or endorsed by Narwal. This US edition is a fork of
[`madsah211/ha-narwal-cloud-eu`](https://github.com/madsah211/ha-narwal-cloud-eu),
itself a fork of [`mk0000001/ha-narwal-cloud`](https://github.com/mk0000001/ha-narwal-cloud).
The protocol work and the room-template cleaning are theirs; this fork changes the
region to the US cloud and adds the current-room sensor and name-based room
cleaning. MIT licensed — see [`LICENSE`](LICENSE).
