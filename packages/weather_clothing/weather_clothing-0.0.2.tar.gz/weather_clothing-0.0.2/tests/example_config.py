import yaml

jacket_cfg_str = """
"Winter Jacket":
- temperature < 5
"Rain Jacket":
- precipitation_probability > 20
- temperature >= 5
"Jacket":
- temperature < 15
"Long Sleeves":
- temperature < 20
- temperature >= 15
"Short Sleeves":
- temperature > 20
"""
example_jacket_config = yaml.load(jacket_cfg_str, Loader=yaml.Loader)

boots_cfg_str = """
"Winter Boots":
- temperature < 5
"Rain Boots":
- precipitation_probability > 20
"Shoes":
- temperature >= 5
"""
example_boots_config = yaml.load(boots_cfg_str, Loader=yaml.Loader)

pants_cfg_str = """
"Snow Pants":
- temperature < -2
"Rain Pants":
- precipitation_probability > 40
"Pants":
- temperature >= -2
- temperature < 17
"Shorts":
- temperature >= 17
"""
example_pants_config = yaml.load(pants_cfg_str, Loader=yaml.Loader)
