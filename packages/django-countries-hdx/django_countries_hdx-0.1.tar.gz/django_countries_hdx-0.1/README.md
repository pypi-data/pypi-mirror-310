# django-countries-hdx

Adds extra M49 data to django-countries.

## Installation

Install this library using `pip`:
```bash
pip install django-countries-hdx
```
## Usage

Extends [django-countries](https://pypi.org/project/django-countries/) to add region and sub-region, and SIDS, LLDC and LDC grouping data  (as defined by the [UN M49 Standard](https://en.wikipedia.org/wiki/UN_M49)).

It also contains helper methods to retrieve the countries in a region or sub-region.

```python
In[1]:
from django_countries.fields import Country

In[2]:
from django_countries_hdx import regions

In[3]: Country('NZ').region
Out[3]: '009'

In[4]: Country("NZ").region_name
Out[4]: 'Oceania'

In[5]: Country('NZ').subregion
Out[5]: '053'

In[6]: Country("NZ").subregion_name
Out[6]: 'Australia and New Zealand'

In[7]: regions.region_name('009')
Out[7]: 'Oceania'

In[8]: regions.subregion_name('053')
Out[8]: 'Australia and New Zealand'

In[9]: regions.countries_by_region('009')
Out[9]:
['AS',
 'AU',
 'CK',
 # …
 ]

In[10]: regions.countries_by_subregion('053')
Out[10]: ['AU', 'NZ', 'NF']
```

## Development

To contribute to this library, first checkout the code. Then create a new virtual environment:
```bash
cd django-countries-hdx
python -m venv .venv
source .venv/bin/activate
```
Now install the test dependencies:
```bash
pip install -e '.[test]'
```
To run the tests:
```bash
pytest
```
