import math

from gridding import GIS, GPS, PostalAddress, Tile, WGS84

KILOMETER = "km"
METER = "m"


class Resolution:
    """
    Defines the resolution of a tile / "carreau", eg. `200m`
    """

    @staticmethod
    def FromString(value: str):
        if "km" in value:
            unit = KILOMETER
        else:
            unit = METER
        size = int(value.replace(unit, ""))
        return Resolution(size, unit)

    def __init__(self, size: int, unit: str):
        self.size = size
        if unit == KILOMETER or unit == METER:
            self.unit = unit
        else:
            raise Exception("Unknown unit")

    def to_string(self) -> str:
        """
        Returns the code to use in a tile's ID, eg. `RES200m`
        """
        return "RES%d%s" % (self.size, self.unit)


class Grid:
    """
    A Grid is defined by:
    - a resolution: the size and unit to use for one tile / "carreau";
    - its pivot: the bottom-left corner of the bounding box covered (defaults to metropolitan France's);
    - the geodesic system to use (defaults to `WGS84`).
    """

    def __init__(
        self,
        resolution: Resolution,
        pivot: GPS = GPS(-5.151110, 41.316666),
        system: GIS = WGS84(),
    ):
        self.resolution = resolution
        self.pivot = pivot
        self.system = system

    def from_address(self, address: str, repository: PostalAddress) -> tuple[str, Tile]:
        """
        Returns the tile informations (code, coordinate) from the passed full address,
        eg. code: `WGS84|RES200m|N2471400|E0486123`, coordinate: `1234.4567`
        """
        point = repository.address2gps(address)
        return self.from_gps(point)

    def from_gps(self, point: GPS) -> tuple[str, Tile]:
        """
        Returns the tile informations (code, coordinate) from the passed GPS coordinates,
        eg. code: `WGS84|RES200m|N2471400|E0486123`, coordinate: `1234.4567`
        """
        side = self._get_side_in_meters()

        # First, search along latitude
        current_y = self.pivot.y()
        previous_y = current_y
        y = 0
        if current_y <= point.y():
            up = self.system.delta_latitude(side, current_y)
            current_y += up
            while point.y() >= self._rounded_coord(current_y):
                previous_y = current_y
                current_y += up
                up = self.system.delta_latitude(side, current_y)
                y += 1
        else:
            down = self.system.delta_latitude(side, current_y)
            current_y -= down
            y -= 1
            while point.y() <= self._rounded_coord(current_y):
                current_y -= down
                down = self.system.delta_latitude(side, current_y)
                y -= 1
            previous_y = current_y

        # Then, search along longitude
        current_x = self.pivot.x()
        previous_x = current_x
        x = 0
        if current_x <= point.x():
            right = self.system.delta_longitude(side, current_x, current_y)
            current_x += right
            while point.x() >= self._rounded_coord(current_x):
                previous_x = current_x
                current_x += right
                x += 1
        else:
            left = self.system.delta_longitude(side, current_x, current_y)
            current_x -= left
            x -= 1
            while point.x() <= self._rounded_coord(current_x):
                current_x -= left
                x -= 1
            previous_x = current_x

        # Finally, build code and coordinate
        return self._get_code(GPS(previous_x, previous_y)), Tile(x, y)

    def get_tile(self, from_carreau: str) -> Tile:
        """
        Returns the tile from the passed carreau ID in the current grid
        """
        if not from_carreau.startswith(self.system.name()):
            raise Exception("Invalid GIS")
        parts = from_carreau.split("|")
        latitude = float(parts[2][1:]) / (
            -100000.0 if parts[2].startswith("S") else 100000.0
        )
        longitude = float(parts[3][1:]) / (
            -100000.0 if parts[3].startswith("W") else 100000.0
        )
        point = GPS(longitude, latitude)
        carreau, tile = self.from_gps(point)
        if carreau == from_carreau:
            return tile
        else:
            raise Exception("Impossible case")

    # Private methods

    def _get_code(self, bottom_left: GPS) -> str:
        """
        Returns the actual code using the passed bottom-left GPS coordinates of the tile

        NB: only 5 digits are kept in the decimal degree used
        """
        ns = "N" if bottom_left.y() >= 0 else "S"
        y = str("%08.5f" % abs(self._rounded_coord(bottom_left.y()))).replace(".", "")
        we = "E" if bottom_left.x() >= 0 else "W"
        x = str("%08.5f" % abs(self._rounded_coord(bottom_left.x()))).replace(".", "")
        return "|".join(
            [self.system.name(), self.resolution.to_string(), f"{ns}{y}", f"{we}{x}"]
        )

    def _rounded_coord(self, x_or_y: float) -> float:
        """
        Return the computed 5-digit coordinate
        """
        coord = abs(x_or_y * 100000)
        sign = -1 if x_or_y < 0 else 1
        return (
            float(
                "%07d"
                % (sign * (math.ceil(coord) if x_or_y < 0 else math.floor(coord)))
            )
            / 100000
        )

    def _get_side_in_meters(self) -> float:
        """
        Returns the grid side size in meters
        """
        if self.resolution.unit == KILOMETER:
            return self.resolution.size * 1000.0
        else:
            return self.resolution.size
