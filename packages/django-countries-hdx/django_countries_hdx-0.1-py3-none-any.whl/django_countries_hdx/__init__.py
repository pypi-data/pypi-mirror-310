from pathlib import Path

from hdx.location.country import Country

# custom_file_url = Path(__file__).parent.resolve() / "hdx_plus_m49.csv"
# This next will need to change once our PR in the hdx lib has been merged
# Country.set_ocha_url(str(custom_file_url))
Country.set_use_live_default(False)


def get_country_data(country_code: str) -> dict[str, str] | None:
    """Retrieves annotated country information. Will accept either ISO2 or ISO3 country code.

    :param country_code: ISO2 or ISO3 country code.
    :return: Dictionary of country information with HXL hashtags as keys.
    """
    if country_code is None:
        return None

    if len(country_code) == 2:
        return Country.get_country_info_from_iso2(country_code)

    return Country.get_country_info_from_iso3(country_code)


def get_region_name(region_code: int) -> str | None:
    """Retrieves region or sub-region name for a region code.

    :param region_code: UN M49 region code.
    :return: String. Region name
    """
    if not region_code:
        return None

    try:
        countriesdata = Country.countriesdata()
        return countriesdata["regioncodes2names"].get(region_code) # noqa
    except KeyError:
        return None


class Regions:
    """
    An object that can query a UN M49 list of geographical regions and subregions and return a list of countries in
    that region.
    """

    def country_region(self, country_code: str) -> int | None:
        """Return a UN M49 region code for a country.

        Extends django-countries by adding a .region() method to the Country field.

        :param country_code: Two-letter ISO country code.
        :return: Integer. UN M49 region code.
        """
        country_data = get_country_data(country_code)
        if country_data:
            return int(country_data["#region+code+main"])
        else:
            return None

    def country_region_name(self, country_code: str) -> str | None:
        """Retrieves region name for a country.

        Extends django-countries by adding a .region_name() method to the Country field.

        :param country_code: Two-letter ISO country code.
        :return: String. Region name
        """
        country_data = get_country_data(country_code)

        if country_data:
            return country_data["#region+main+name+preferred"]

        return None

    def country_subregion(self, country_code: str) -> int | None:
        """Return a UN M49 sub-region code for a country.

        Extends django-countries by adding a .subregion() method to the Country field.

        :param country_code: Two-letter ISO country code.
        :return: Integer. UN M49 sub-region code.
        """
        country_data = get_country_data(country_code)

        if country_data:
            # Return the intermediate region if populated.
            intermediate_region = country_data.get("#region+code+intermediate", None)

            if intermediate_region:
                return int(intermediate_region)
            else:
                return int(country_data["#region+code+sub"])

        return None

    def country_subregion_name(self, country_code: str) -> str | None:
        """Return the sub-region name for a country

        :param country_code: Two-letter ISO country code.
        :return: String
        """
        country_data = get_country_data(country_code)

        if country_data:
            # Return the intermediate region if populated.
            intermediate_region = country_data.get("#region+intermediate+name+preferred", None)
            return intermediate_region or country_data["#region+name+preferred+sub"]

        return None

    def is_sids(self, country_code: str) -> bool | None:
        """Returns whether a country is classed as a SIDS

        :param country_code: Two-letter ISO country code.
        :return: Boolean
        """
        country_data = get_country_data(country_code)

        if country_data:
            return bool(country_data["#meta+bool+sids"])

        return None

    def is_ldc(self, country_code: str) -> bool | None:
        """Returns whether a country is classed as a LDC

        :param country_code: Two-letter ISO country code.
        :return: Boolean
        """
        country_data = get_country_data(country_code)

        if country_data:
            return bool(country_data["#meta+bool+ldc"])

        return None

    def is_lldc(self, country_code: str) -> bool | None:
        """Returns whether a country is classed as a LLDC

        :param country_code: Two-letter ISO country code.
        :return: Boolean
        """
        country_data = get_country_data(country_code)

        if country_data:
            return bool(country_data["#meta+bool+lldc"])

        return None

    def get_countries_by_region(self) -> dict[int, dict[str, list[tuple[str, str]]]]:
        """Retrieves lists of countries keyed by region, with region name and country tuples.

        :param regions: Boolean to determine whether to use regions or subregions.
        :return: Dict. Keyed by region code, the value is a dictionary containing the
        region name and a list of country_code, country_name tuples.
        """
        region_codes = (2, 9, 19, 142, 150,)

        return {
            region_code: {
                "name": get_region_name(region_code),
                "countries": sorted(
                    [
                        (
                            Country.get_iso2_from_iso3(code),
                            Country.get_country_name_from_iso3(code)
                        )
                        for code in Country.get_countries_in_region(region_code)
                    ],
                    key=lambda x: x[1]  # Sort by country name
                )
            }
            for region_code in sorted(region_codes, key=lambda x: get_region_name(x))
        }

    def get_countries_by_subregion(self) -> dict[int, dict[str, list[tuple[str, str]]]]:
        """Retrieves lists of countries keyed by region, with region name and country tuples.

        :param regions: Boolean to determine whether to use regions or subregions.
        :return: Dict. Keyed by region code, the value is a dictionary containing the
        region name and a list of country_code, country_name tuples.
        """
        subregion_codes = (
            5, 11, 13, 14, 15, 17, 18, 21, 29, 30, 34, 35, 39, 53, 54, 57, 61, 143, 145, 151, 154, 155,
        )

        return {
            region_code: {
                "name": get_region_name(region_code),
                "countries": sorted(
                    [
                        (
                            Country.get_iso2_from_iso3(code),
                            Country.get_country_name_from_iso3(code)
                        )
                        for code in Country.get_countries_in_region(region_code)
                    ],
                    key=lambda x: x[1]  # Sort by country name
                )
            }
            for region_code in sorted(subregion_codes, key=lambda x: get_region_name(x))
        }

    def get_countries_in_region(self, region_code: int) -> list[tuple[str, str]] | None:
        """Retrieves lists of countries in a region/sub-region.

        :return: List. ISO2 country_code, country_name tuples.
        """
        if not region_code:
            return None

        countries_iso3 = Country.get_countries_in_region(region_code)

        countries_list = [(
            Country.get_iso2_from_iso3(code),
            Country.get_country_name_from_iso3(code)
        ) for code in countries_iso3
        ]

        return countries_list


regions = Regions()
