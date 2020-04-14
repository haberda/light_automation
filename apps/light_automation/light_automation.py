import hassapi as hass
import datetime
from datetime import timedelta
import math

class light_automation(hass.Hass):
    def initialize(self):
        self.lights = self.args.get('entity_id', None)
        self.on_time = self.args.get('on_time', None)
        self.off_time = self.args.get('off_time', None)
        self.constraint = self.args.get('constraint', [])
        self.service_data = self.args.get('data', {"entity_id": None})
        self.service_data['entity_id'] = self.lights
        self.off_service_data = self.args.get('off_data', {"entity_id": None})
        self.off_service_data['entity_id'] = self.lights

        if isinstance(self.on_time, str):
            self.on_time = self.on_time.split(',')
        if isinstance(self.off_time, str):
            self.off_time = self.off_time.split(',')

        if self.service_data['entity_id'] is None or (self.on_time is None and self.off_time is None):
            self.log('No lights or times defined, exiting')
            return
        if self.constraint is not None:
            for entity in self.constraint:
                if len(entity.split(',')) > 1:
                    entity = entity.split(',')[0]
                self.listen_state(self.state_change, entity)
        if self.on_time is not None:
            for time in self.on_time:
                if isinstance(time, str):
                    on = self.parse_time(time)
                if isinstance(time, int):
                    on = timedelta(seconds=time)
                    on = self.parse_time(str(on))
                self.run_daily(self.lights_on, on)
        if self.off_time is not None:
            for time in self.off_time:
                if isinstance(time, str):
                    off = self.parse_time(time)
                if isinstance(time, int):
                    off = timedelta(seconds=time)
                    off = self.parse_time(str(off))
                self.run_daily(self.lights_off, off)

    def lights_on(self, kwargs):
        check = self.constraint_check()
        if not check:
            self.log('Lights on')
            self.call_service("light/turn_on", **self.service_data)

    def lights_off(self, kwargs):
        check = self.constraint_check()
        if not check:
            self.log('Lights off')
            # off_service_data = {}
            # off_service_data['entity_id'] = self.service_data['entity_id']
            self.call_service("light/turn_off", **self.off_service_data)

    def state_change(self, entity, attribute, old, new, kwargs):
        check = self.constraint_check()
        if not check:
            if self.on_time is not None and self.off_time is not None:
                for on_time in self.on_time:
                    for off_time in self.off_time:
                        if self.now_is_between(on_time,off_time):
                            self.lights_on(kwargs)
                            return
                self.lights_off(kwargs)

    def constraint_check (self):
        value = False
        if self.constraint is not None:
            condition_states = ['on', 'Home', 'home', 'True', 'true']
            for entity in self.constraint:
                if len(entity.split(',')) > 1:
                    if  entity.split(',')[1] == self.get_state(entity.split(',')[0]):
                        value = True
                elif self.get_state(entity) in condition_states:
                    value = True
        return value
