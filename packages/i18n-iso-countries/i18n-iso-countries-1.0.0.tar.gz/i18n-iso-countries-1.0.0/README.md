# py-i18n-countries
i18n for ISO 3166-1 country codes. We support Alpha-2, Alpha-3 and Numeric codes from: [Wiki](https://en.wikipedia.org/wiki/ISO_3166-1#Officially_assigned_code_elements)

## Install
```
pip install i18n-iso-countries
```

## Code to Country
###  Get the name of a country by its ISO 3166-1 Alpha-2, Alpha-3 or Numeric code
```python
from i18n_iso_countries import get_country_name

get_country_name(code="US", language='en') # United States of America
get_country_name(code="US", language='de') # Vereinigte Staaten von Amerika
get_country_name(code="USA", language='en') # United States of America
get_country_name(code="840", language='en') # United States of America
```
#### Get aliases/short name using select
```python
from i18n_iso_countries import get_country_name

# Some countries have alias/short names defined. `select` is used to control which
# name will be returned.
get_country_name(code="GB", language='en', select="official") # United Kingdom
get_country_name(code="GB", language='en', select="alias") # UK
get_country_name(code="GB", language='en', select="all") # ["United Kingdom", "UK", "Great Britain"]

# Countries without an alias will always return the offical name
get_country_name(code="LT", language='en', select="official") # Lithuania
get_country_name(code="LT", language='de', select="alias") # Lithuania
get_country_name(code="LT", language='en', select="all") # ["Lithuania"]

```

###  Get all names by their ISO 3166-1 Alpha-2 code
```python
from i18n_iso_countries import get_country_name

get_country_name(language='en', select="official") # { 'AF': 'Afghanistan', 'AL': 'Albania', [...], 'ZM': 'Zambia', 'ZW': 'Zimbabwe' }

```

### Get all supported languages (ISO 639-1)

```python
from i18n_iso_countries import get_supported_languages
get_supported_languages() # ["cy", "dv", "sw", "eu", "af", "am", ...]
```

### Supported languages (ISO 639-1)

> In case you want to add new language, please refer [ISO 639-1 table][iso:639-1].

- `af`: Afrikaans
- `am`: Amharic
- `ar`: Arabic
- `az`: Azerbaijani
- `be`: Belorussian
- `bg`: Bulgarian
- `bn`: Bengali
- `bs`: Bosnian
- `ca`: Catalan
- `cs`: Czech
- `cy`: Cymraeg
- `da`: Danish
- `de`: German
- `dv`: Dhivehi
- `en`: English
- `es`: Spanish
- `et`: Estonian
- `eu`: Basque
- `fa`: Persian
- `fi`: Finnish
- `fr`: French
- `gl`: Galician
- `el`: Greek
- `ha`: Hausa
- `he`: Hebrew
- `hi`: Hindi
- `hr`: Croatian
- `hu`: Hungarian
- `hy`: Armenian
- `is`: Icelandic
- `it`: Italian
- `id`: Indonesian
- `ja`: Japanese
- `ka`: Georgian
- `kk`: Kazakh
- `km`: Khmer
- `ko`: Korean
- `ku`: Kurdish
- `ky`: Kyrgyz
- `lt`: Lithuanian
- `lv`: Latvian
- `mk`: Macedonian
- `ml`: Malayalam
- `mn`: Mongolian
- `ms`: Malay
- `nb`: Norwegian Bokmål
- `nl`: Dutch
- `nn`: Norwegian Nynorsk
- `no`: Norwegian
- `pl`: Polish
- `ps`: Pashto
- `pt`: Portuguese
- `ro`: Romanian
- `ru`: Russian
- `sd`: Sindhi
- `sk`: Slovak
- `sl`: Slovene
- `so`: Somali
- `sq`: Albanian
- `sr`: Serbian
- `sv`: Swedish
- `sw`: Swahili
- `ta`: Tamil
- `tg`: Tajik
- `th`: Thai
- `tr`: Turkish
- `tt`: Tatar
- `ug`: Uyghur
- `uk`: Ukrainian
- `ur`: Urdu
- `uz`: Uzbek
- `zh`: Chinese
- `vi`: Vietnamese

[List of ISO 639-1 codes](https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes)

## Codes

### Convert Alpha-3 to Alpha-2 code

```python
from i18n_iso_countries import alpha3_to_alpha2

alpha3_to_alpha2('USA') #US
```

### Convert Numeric to Alpha-2 code

```python
from i18n_iso_countries import numeric_to_alpha2

numeric_to_alpha2('840') # US
```

### Convert Alpha-2 to Alpha-3 code

```python
from i18n_iso_countries import alpha2_to_alpha3

alpha2_to_alpha3('DE') # DEU
```

### Convert Numeric to Alpha-3 code

```python
from i18n_iso_countries import numeric_to_alpha3

numeric_to_alpha3('840') # USA
```

### Convert Alpha-3 to Numeric code

```python
from i18n_iso_countries import alpha3_to_numeric

alpha3_to_numeric('SWE') #752
```

### Convert Alpha-2 to Numeric code

```python
from i18n_iso_countries import alpha2_to_numeric

alpha2_to_numeric("SE") # 752
```

### Get all Alpha-2 codes

```python
from i18n_iso_countries import get_alpha2_codes

get_alpha2_codes() # { 'AF': 'AFG', 'AX': 'ALA', [...], 'ZM': 'ZMB', 'ZW': 'ZWE' }
```

### Get all Alpha-3 codes

```python
from i18n_iso_countries import get_alpha3_codes

get_alpha3_codes() # { 'AFG': 'AF', 'ALA': 'AX', [...], 'ZMB': 'ZM', 'ZWE': 'ZW' }
```

### Get all Numeric codes

```python
from i18n_iso_countries import get_numeric_codes

get_numeric_codes() # { '004': 'AF', '008': 'AL', [...], '887': 'YE', '894': 'ZM' }
```

### Validate country code

```python
from i18n_iso_countries import is_valid_country_code

is_valid_country_code("US") # True
is_valid_country_code("USA") # True
is_valid_country_code("XX") # False
```