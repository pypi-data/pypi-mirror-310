# ecoaliface
Pure Python interface to [eCoal](https://esterownik.pl/nasze-produkty/ecoal) water boiler controller from [eSterownik.pl](http://esterownik.pl).
Implements small subset of operations/readings available in controller.

Based on code from https://github.com/uzi18/sterownik .

## Versions

### 0.7.0
Add fuel left calculation logic

### 0.6.0
Add max fuel feeder time parameter to enable calculation of fuel level
Added async examples

### 0.5.1
Fixed an incorrect parameter name to match the homeassistant ecoal boiler plugin

### 0.5.0
Added all methods available in https://github.com/uzi18/sterownik code.

### 0.4.0
Initial public release for Homeassistant component.
