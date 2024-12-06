from unittest import TestCase
from django_countries_hdx import regions
from django_countries.fields import Country
from django.conf import settings

settings.configure()


# Test data
world_regions = ["AQ", "BV", "IO", "CX", "CC", "TF", "HM", "GS", "UM"]
au_nz_subregions = ["AU", "NZ", "NF"]


class TestCountry(TestCase):
    def test_country_region(self):
        query = Country("AF").region
        self.assertEqual(query, "142")

    def test_country_region_name(self):
        query = Country("AF").region_name
        self.assertEqual(query, "Asia")

    def test_country_subregion(self):
        query = Country("AF").subregion
        self.assertEqual(query, "034")

    def test_country_subregion_name(self):
        query = Country("AF").subregion_name
        self.assertEqual(query, "Southern Asia")

    def test_invalid_country_region(self):
        query = Country("ZZ").region
        self.assertIsNone(query)

    def test_invalid_country_region_name(self):
        query = Country("ZZ").region_name
        self.assertIsNone(query)

    def test_invalid_country_subregion(self):
        query = Country("ZZ").subregion
        self.assertIsNone(query)

    def test_invalid_country_subregion_name(self):
        query = Country("ZZ").subregion_name
        self.assertIsNone(query)


class TestRegions(TestCase):
    def test_countries_by_region(self):
        query = regions.countries_by_region("001")
        self.assertCountEqual(query, world_regions)

    def test_countries_by_subregion(self):
        query = regions.countries_by_subregion("053")
        self.assertCountEqual(query, au_nz_subregions)

    def test_region_name(self):
        query = regions.region_name("001")
        self.assertEqual(query, "World")

    def test_subregion_name(self):
        query = regions.subregion_name("053")
        self.assertEqual(query, "Australia and New Zealand")

    def test_invalid_countries_by_region(self):
        query = regions.countries_by_region("900")
        self.assertIsNone(query)

    def test_invalid_countries_by_subregion(self):
        query = regions.countries_by_subregion("999")
        self.assertIsNone(query)

    def test_invalid_region_name(self):
        query = regions.region_name("900")
        self.assertIsNone(query)

    def test_invalid_subregion_name(self):
        query = regions.subregion_name("999")
        self.assertIsNone(query)
