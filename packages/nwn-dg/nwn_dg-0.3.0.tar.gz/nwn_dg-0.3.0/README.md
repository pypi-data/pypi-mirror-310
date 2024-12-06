[![license](https://img.shields.io/badge/license-MIT-brightgreen)](https://spdx.org/licenses/MIT.html)
[![pipelines](https://gitlab.com/cappysan/nwn-dg/badges/master/pipeline.svg?ignore_skipped=true)](https://gitlab.com/cappysan/nwn-dg/pipelines)
[![coverage](https://gitlab.com/cappysan/nwn-dg/badges/master/coverage.svg)](/coverage/index.html)

# nwn-dg

Work in progress: in alpha stage.

Neverwinter Nights (nwn) dungeon generator


## Installation

You can install the latest version from PyPI package repository.

~~~bash
pipx install nwn-dg
~~~


## Roadmap

- Transitions (stairs up, stairs down, transitions)
  - Not all tilesets support these features. Valid for at least crypt, sewers, dungeons and steamworks.
  - map-stairs-up (U), map-stairs-down (D), map-transitions (T)
    - Can replace deadend
    - Can be placed on the border of a corridor, entering into the corridor
    - Can be placed on the border of a room, entering into the room
    - Allow param "count", but also preferred direction (N,E,S,W), and preferred type (deadend, corridor, room)?
  - map-exits 0 (E)
    - On a room border, in the middle of 3 cells
    - Requires group tile support

- Extra map layouts (cross, dagger, round, ...)

- Doors
  - Does not occupy a cell, but is rather between two cells
  - Can not be placed anywhere, especially two in the same corner of a room. Either two corridors, or two doors.
  - Close off all rooms?

- For are and are.json generation, accept an json input file to set basic information (tag, name, etc...)

- An HTTP REST API frontend to be called via nwnxee requests.

- Allow new room size (3x5, 5x5, etc.)

- Extend room reshaping to create L, U shape rooms, cutting corners, pillars, etc..

- Use tileset "set" file for dungeon generation?

- Accept a configuration file as input.

- Decide on how to handle minimum rooms: 1 or 2, retry idefinitly if we can?

## Known bugs & limitations

- Crypt tileset only.
- Currently limited to maps from 5 to 31 cells in height and width.
- Some deadends are not marked as such.
- Entrance point is always stairs up tile, and is always added on a deadend.
- Random seed might generate different dungeons depending on nwn-dg version upgrades.
- Binary file is not accepted as a random seed


## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.


## Locations

  * Website: [https://gitlab.com/cappysan/nwn-dg](https://gitlab.com/cappysan/nwn-dg)
  * PyPi: [https://pypi.org/project/nwn_dg](https://pypi.org/project/nwn_dg)
