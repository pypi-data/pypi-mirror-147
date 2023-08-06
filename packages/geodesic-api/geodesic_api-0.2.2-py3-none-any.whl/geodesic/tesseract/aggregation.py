from typing import Iterable, Union, List


class FeatureAggregation(dict):
    def __init__(self, **spec):
        self._value = None
        self._aggregation_rules = None
        self._groups = None

        for k, v in spec.items():
            setattr(self, k, v)

    @property
    def value(self):
        if self._value is not None:
            return self._value
        self._value = self.get('value', None)
        return self._value

    @value.setter
    def value(self, v: Union[str, float, int]):
        assert isinstance(v, (str, float, int))
        self['value'] = v

    @property
    def aggregation_rules(self):
        if self._aggregation_rules is not None:
            return self._aggregation_rules
        self._aggregation_rules = self.get('aggregation_rules', None)
        return self._aggregation_rules

    @aggregation_rules.setter
    def aggregation_rules(self, v: Iterable[str]):
        if not isinstance(v, Iterable):
            raise ValueError("aggregation rules must be a sequence")
        self['aggregation_rules'] = [_ for _ in v]

    @property
    def groups(self):
        if self._groups is not None:
            return self._groups
        self._groups = self.get('groups', None)
        return self._groups

    @groups.setter
    def groups(self, v: List[dict]):
        for i in v:
            if not ('field' in i and 'values' in i):
                raise ValueError("each group must have keys ['field', 'values']")
        self['groups'] = v
