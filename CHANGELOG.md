# Changelog

## 0.14.0

- New dock buttons: **Empty dustbin** (`supply/dust_gathering`), **Dry dust
  bin** (`supply/dry_dust_bag`) and **Dry dock dust bag**
  (`supply/dry_station_bag`), using the station commands from the local
  integration. Sent without waiting for an acknowledgement; use **Finish mop
  washing/drying** (`task/force_end`) to stop a running station task.

## 0.13.0

- New sensors from the robot's `status/working_status` broadcast: **Cleaned
  area** (m²), **Cleaning time**, **Cleaning progress** (%), **Remaining
  cleaning time**, and **Cleaning room** (the room the robot reports it is
  cleaning, as opposed to Current room, which is where it physically is).
- Values are for the current or most recent session and update whenever the
  broadcast is seen during a status poll.

## 0.12.2

- `clean_rooms` suction now uses the Freo Z Ultra app's five tiers: `ai`,
  `quiet`, `standard`, `strong`, `super_powerful` (FanLevel 0-4).

## 0.12.1

- `narwal_cloud.clean_rooms` accepts optional per-job `mode` (vacuum, mop,
  vacuum_and_mop, vacuum_then_mop), `suction` (quiet, standard, strong) and
  `passes` (1-3), overriding the device selects for that job only.

## 0.12.0

- Room cleaning no longer depends on Narwal's per-room templates. The robot
  never answers the cloud template request on the Freo Z Ultra, so `auto` now
  sends a direct `clean/start_clean` room task (the layout the local
  integration verified on the CX7) unless a Freo Mind template is cached.
- `narwal_cloud.clean_rooms` gains an optional `method`
  (`auto` / `start_clean` / `easy_clean`).
- Room cleans fail fast with a clear message instead of waiting minutes for a
  template fetch; a "not docked" reply (code 4) is reported as such.

## 0.11.1

- Map retrieval now tries four request variants in order (app body, empty
  body, then each again after the app-style wake burst) and keeps the first
  map that parses. The empty body is the one the local integration uses on the
  Freo Z Ultra (CX7).
- Logs each failed map attempt at debug level, and one warning summarising all
  attempts (error type and topics seen, no payloads) when every variant fails.

## 0.11.0 (US edition)

- Forked from madsah211/ha-narwal-cloud-eu 0.10.1 and switched the API host,
  country code and broker discovery to the US cloud.
- Added a **Current room** sensor and `current_room` vacuum attribute, derived
  from the live robot pose on the saved map grid.
- Added the `narwal_cloud.clean_rooms` action, which takes room names
  (case-insensitive) or ids and refuses unknown names instead of starting a
  whole-home clean.

## 0.10.1

- Completes Danish translations for dock buttons, cleaning selectors, selector
  options, and the five known consumable sensors.
- Stops waiting for MQTT acknowledgements that the verified YJCC012 firmware
  does not send for cleaning-start and return-to-dock commands. This removes a
  false `connection lost` error after an otherwise successful room task.
- Clarifies first-time setup: keep the official app open on its map for about
  two minutes so both the saved map and room templates can arrive.

## 0.10.0

- Replaced the inherited Korean project documentation and translation with an
  English-first README and an initial Danish Home Assistant translation.
- Rewrote compatibility, setup, privacy, provenance, and feature documentation
  to match the behavior actually verified on the EU YJCC012 integration.
- Documented that fan speed affects the next task, dock presence can be reported
  incorrectly by Narwal, and compatibility outside the tested Danish setup is
  not yet guaranteed.
- Kept the original MIT copyright and upstream attribution while identifying
  this repository as the maintained home of the EU edition.
- Adopted normal semantic versioning; `EU` remains part of the project name
  instead of being repeated in every future version number.

## 0.9.3-eu.10

- Stores official per-room cleaning templates together with the saved map so
  safe segment cleaning survives Home Assistant restarts.
- Invalidates cached templates whenever the map revision or room definition
  changes, then refreshes and stores a coherent map-and-plan snapshot.
- Refuses Freo Mind room cleaning when an official template is unavailable,
  instead of falling back to a command that may clean the whole map.

## 0.9.3-eu.9

- Stores the last valid saved map in Home Assistant's private local storage so
  rooms and the rendered base map survive restarts while older Freo firmware is
  asleep.
- Captures `map/display_map` alongside the existing MQTT base-status request
  while cleaning, without logging or exposing the raw payload.
- Merges live robot pose, frame timestamp, and Narwal's native trajectory into
  the cached saved map and renders the route on the normal map camera.

## 0.9.3-eu.8

- Sends the official app-style named broadcast-topic subscription for ten
  minutes instead of the incomplete numeric activation payload.
- Preserves the saved map's verified origin offsets and uses the validated
  `pixel = position - origin` coordinate transform.
- Restores the robot marker when the saved response contains an in-bounds pose.

## 0.9.3-eu.7

- Publishes a decoded saved map before requesting optional cleaning-plan data.
- A cleaning-plan timeout no longer discards map, room, renderer, or pose data.
- Uses the verified app-open wake sequence before sleeping-robot queries.

## 0.9.3-eu.6

- Reads the active map ID from saved-map field 1.
- Locates complete maps through validated nested protobuf envelopes.
- Rejects empty parser results instead of reporting a false successful map.

## 0.9.3-eu.5

- Treats `map/display_map` as live position, trajectory, and cleaning-overlay
  data rather than a complete saved map.
- Keeps map requests open until the actual saved-map response arrives.
- Retains privacy-safe topic and payload-length diagnostics without raw data.

## 0.9.3-eu.4

- Adds strict parsing for unframed complete-map protobuf messages published on
  `map/display_map`.
- Keeps only privacy-safe protobuf shape diagnostics.

## 0.9.3-eu.3

- Adds privacy-safe map diagnostics without exposing raw maps, account IDs,
  broker addresses, tokens, or device identifiers.

## 0.9.3-eu.2

- Accepts the YJCC012 live `map/display_map` publication as a fallback response
  when some EU firmware does not answer on `map/get_map/response`.

## 0.9.2

- Added explicit dark-theme icons and logos for Home Assistant 2026.8.

## 0.9.1

- Added local Narwal app icon and wordmark assets for Home Assistant 2026.3+.

## 0.9.0

- Reduced default state polling from 30 seconds to 1 second.
- Added a configurable 1–300 second polling interval.
- Isolated the slower map refresh from primary state polling.
- Documented that some idle YJCC012 sessions do not answer fresh map requests.

## 0.8.0

- Added Narwal account login and automatic token recovery.
- Changed segment cleaning to use the app's official per-room templates.
- Fixed timezone arithmetic that could make all entities unavailable.
