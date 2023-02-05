
import json
from pathlib import Path
import random
import uuid

import matplotlib.pyplot as plt
from descartes import PolygonPatch


class OhioMap:

    def __init__(self):


        self.config = self.load_config()

        self.odot_county_geojson = None
        self.load_odot_county_geojson()

        self.county_names = None
        self.load_county_names()


    def load_config(self):
        self.FONT_SIZE = 4
        self.DOTS_PER_INCH = 1000
        self.FORMAT = "png"
        self.BBOX_INCHES = "tight"


    def random_color(self):
        """

        salmon       #ea7e7e
        lightblue    #5588ff
        yellow       #f7dd78
        burgundy     #913945
        fuschia      #be29ec
        """

        colors = [
            "#ea7e7e",
            "#5588ff",
            "#f7dd78",
            "#913945",
            "#be29ec"
        ]

        return random.choice(colors)


    def load_json_file(self, file_path):
        f = Path(Path(__file__).parent, file_path)
        with open(f, "r") as handle:
            obj =json.loads(handle.read())
        return obj


    def load_odot_county_geojson(self):
        f = Path(Path(__file__).parent, "ODOT_County_Boundaries.geojson")
        self.odot_county_geojson = self.load_json_file(f)


    def load_county_names(self):
        f = Path(Path(__file__).parent, "ohio_counties_fips_code.json")
        county_name_arr = self.load_json_file(f)

        county_name_obj = {}

        for obj in county_name_arr:
            code = obj["fips_code"]
            county_name = obj["county"]
            county_name_obj[code] = county_name

        self.county_names = county_name_obj


    def draw_plot(self):

        plt.rcParams.update({'font.size': self.FONT_SIZE})

        fig = plt.figure()
        ax = fig.gca()

        for feature in self.odot_county_geojson["features"]:

            color = self.random_color()

            county_fips = feature["properties"]["FIPS_COUNT"]

            county_name = self.county_names[county_fips]
            county_name = "\n".join(county_name.split())

            lat_north = feature["properties"]["LAT_NORTH_"]
            lat_south = feature["properties"]["LAT_SOUTH_"]
            long_east = feature["properties"]["LONG_EAST_"]
            long_west = feature["properties"]["LONG_WEST_"]

            county_vertical_center = (abs(lat_north - lat_south) / 2) + lat_south
            county_horizontal_center = (abs(long_east - long_west) / 2) + long_west

            geo = feature["geometry"]

            ax.add_patch(PolygonPatch(geo,
                                    fc=color,
                                    ec=color,
                                    alpha=0.5,
                                    zorder=2))

            ax.axis('scaled')

            plt.text(county_horizontal_center,
                    county_vertical_center,
                    county_name,
                    horizontalalignment='center',
                    verticalalignment='center')

        output_path = f"{uuid.uuid4()}.png"
        print(f"Writing output to: {output_path}")
        plt.savefig(output_path,
                    dpi=self.DOTS_PER_INCH,
                    format=self.FORMAT,
                    bbox_inches=self.BBOX_INCHES)
