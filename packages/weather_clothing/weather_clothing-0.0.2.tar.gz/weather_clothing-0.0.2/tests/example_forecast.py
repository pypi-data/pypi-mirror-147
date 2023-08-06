import yaml

fc_str = """
  - datetime: '2022-04-18T13:00:00+00:00'
    temperature: -3
    condition: sunny
    precipitation_probability: 0
  - datetime: '2022-04-18T14:00:00+00:00'
    temperature: -2
    condition: sunny
    precipitation_probability: 0
  - datetime: '2022-04-18T15:00:00+00:00'
    temperature: 0
    condition: sunny
    precipitation_probability: 0
  - datetime: '2022-04-18T16:00:00+00:00'
    temperature: 3
    condition: sunny
    precipitation_probability: 0
  - datetime: '2022-04-18T17:00:00+00:00'
    temperature: 5
    condition: sunny
    precipitation_probability: 0
  - datetime: '2022-04-18T18:00:00+00:00'
    temperature: 8
    condition: sunny
    precipitation_probability: 0
  - datetime: '2022-04-18T19:00:00+00:00'
    temperature: 8
    condition: sunny
    precipitation_probability: 0
  - datetime: '2022-04-18T20:00:00+00:00'
    temperature: 8
    condition: sunny
    precipitation_probability: 0
  - datetime: '2022-04-18T21:00:00+00:00'
    temperature: 8
    condition: partlycloudy
    precipitation_probability: 0
  - datetime: '2022-04-18T22:00:00+00:00'
    temperature: 8
    condition: partlycloudy
    precipitation_probability: 20
  - datetime: '2022-04-18T23:00:00+00:00'
    temperature: 7
    condition: partlycloudy
    precipitation_probability: 20
  - datetime: '2022-04-19T00:00:00+00:00'
    temperature: 7
    condition: cloudy
    precipitation_probability: 20
  - datetime: '2022-04-19T01:00:00+00:00'
    temperature: 6
    condition: cloudy
    precipitation_probability: 20
  - datetime: '2022-04-19T02:00:00+00:00'
    temperature: 5
    condition: cloudy
    precipitation_probability: 20
  - datetime: '2022-04-19T03:00:00+00:00'
    temperature: 4
    condition: rainy
    precipitation_probability: 100
  - datetime: '2022-04-19T04:00:00+00:00'
    temperature: 3
    condition: rainy
    precipitation_probability: 100
  - datetime: '2022-04-19T05:00:00+00:00'
    temperature: 3
    condition: rainy
    precipitation_probability: 100
  - datetime: '2022-04-19T06:00:00+00:00'
    temperature: 2
    condition: rainy
    precipitation_probability: 100
  - datetime: '2022-04-19T07:00:00+00:00'
    temperature: 2
    condition: rainy
    precipitation_probability: 100
  - datetime: '2022-04-19T08:00:00+00:00'
    temperature: 1
    condition: snowy-rainy
    precipitation_probability: 100
  - datetime: '2022-04-19T09:00:00+00:00'
    temperature: 1
    condition: snowy-rainy
    precipitation_probability: 100
  - datetime: '2022-04-19T10:00:00+00:00'
    temperature: 1
    condition: snowy
    precipitation_probability: 100
  - datetime: '2022-04-19T11:00:00+00:00'
    temperature: 1
    condition: snowy
    precipitation_probability: 100
  - datetime: '2022-04-19T12:00:00+00:00'
    temperature: 1
    condition: snowy
    precipitation_probability: 100
"""

example_forecast = yaml.load(fc_str, Loader=yaml.Loader)
