# light_automation

Note: no longer maintained.

This appdaemon app fully automates your lights, with multiple on/off times, regular service data, and constraint options.

Options:
---

Key | Required | Description | Default | Unit
------------ | ------------- | ------------- | ------------- | -------------
entity_id | True | List of lights | None | List
on_time | False if off_time set | List of times in format 'HH:MM:SS' to turn on; also can be 'sunset +- HH:MM:SS'. | None | Time list
off_time | False if on_time set | List of times 'HH:MM:SS' to turn off; also can be 'sunrise +- HH:MM:SS'. | None | Time list
data | False | Dictionary of light attributes to set. Can take any attribute that home-assistant allows in a light service call. | None | Dictionary
off_data | False | Dictionary of light data to use during turn off (e.g. transistion to turn off). Can take any attribute that home-assistant allows in a light service call. | None | Dictionary
constraint | False | List of entities that when active disable the functionality of this code. Takes a comma separated condition (e.g. input_boolean.party_mode,on in this case when input_boolean.party_mode is on the code is disabled). If an on and off time are defined and all constraints are turned off during that period (in other words the on_time is missed because one or more constraints are on) the lights will turn on when the last constraint is lifted. | None | List

AppDaemon constraints can be used as well, see AppDaemon API Docs https://appdaemon.readthedocs.io/en/latest/APPGUIDE.html#callback-constraints

## Example apps.yaml:

```
sunset_lights_away:
  module: light_automation
  class: light_automation
  entity_id:
    - light.main_hallway
    - light.office
    - light.gym
  data:
    brightness: 255
    kelvin: 5000
  on_time: sunset - 00:30:00
  off_time: '21:30:00'
  constraint:
    - binary_sensor.workday_tomorrow,off
    - input_boolean.party_mode,on
    - input_boolean.hold_lights,on
    - group.presence,on

sunset_lights_weekend_away:
  module: light_automation
  class: light_automation
  entity_id:
    - light.main_hallway
    - light.office
    - light.gym
  data:
    brightness: 255
    kelvin: 5000
  on_time: sunset - 00:30:00
  off_time: '22:00:00'
  constraint:
    - binary_sensor.workday_tomorrow,on
    - input_boolean.party_mode,on
    - input_boolean.hold_lights,on
    - group.presence,on

sunset_lights_home:
  module: light_automation
  class: light_automation
  entity_id:
    - light.group_hallway
    - light.office
    - light.gym
    - light.guest_room
    - light.kitchen_spotlight
  data:
    brightness: 255
    kelvin: 5000
  off_data:
    transition: 300
  on_time: sunset - 00:30:00
  off_time: '21:30:00'
  constraint:
    - binary_sensor.workday_tomorrow,off
    - input_boolean.party_mode,on
    - group.presence,off

sunset_lights_weekend_home:
  module: light_automation
  class: light_automation
  entity_id:
    - light.group_hallway
    - light.office
    - light.gym
    - light.guest_room
    - light.kitchen_spotlight
  data:
    brightness: 255
    kelvin: 5000
    transition: 10
  off_data:
    transition: 300
  on_time: sunset - 00:30:00
  off_time: '22:00:00'
  constraint:
    - binary_sensor.workday_tomorrow,on
    - input_boolean.party_mode,on
    - group.presence,off

lights_off_late:
  module: light_automation
  class: light_automation
  entity_id:
    - group.interior_lights
  off_time: 
    - 01:00:00
    - 23:00:00
  constraint:
    - input_boolean.party_mode,on
    - input_boolean.hold_lights,on

lights_off_morning:
  module: light_automation
  class: light_automation
  entity_id: all
  off_time: 
    - sunrise + 00:30:00
    - sunrise + 01:00:00
```
