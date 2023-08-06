from typing import Union, List
import datetime
import re
from dateutil.parser import isoparse

from geodesic.utils import datetime_to_utc
#########################################################################################
#  Temporal Binning Classes
#########################################################################################

bin_size_re = re.compile(r'^\d+(ms|us|ns|[WDhms]){1}')


class Equal(dict):
    def __init__(self, **spec):
        self._bin_size = None
        self._bin_count = None

        for k, v in spec.items():
            setattr(self, k, v)

    @property
    def bin_size(self):
        if self._bin_size is not None:
            return self._bin_size
        d = self.get('bin_size', None)
        if d is None:
            return None
        r = bin_size_re.match(d)
        self._bin_size = r
        if r:
            return d
        else:
            raise ValueError(r"bin_size must have pattern: 'r^\d+(ms|us|ns|[WDhms]){1}' example: '15h'")

    @bin_size.setter
    def bin_size(self, v: Union[str, datetime.timedelta]):
        if isinstance(v, str):
            r = bin_size_re.match(v)
            if r:
                self['bin_size'] = v
            else:
                raise ValueError(r"bin_size must have pattern: 'r^\d+(ms|us|ns|[WDhms]){1}' example: '15h'")
        elif isinstance(v, datetime.timedelta):
            r = v.total_seconds()
            r = int(r * (1000000))
            r = f'{r}us'
            self['bin_size'] = r
        else:
            raise ValueError("bin_size must be of type str or datetime.timedelta")

    @property
    def bin_count(self):
        if self._bin_count is not None:
            return self._bin_count
        self._bin_count = self.get('bin_count', None)
        return self._bin_count

    @bin_count.setter
    def bin_count(self, v: int):
        assert isinstance(v, int)
        self['bin_count'] = v


class User(dict):
    def __init__(self, **spec):
        self._bins = None
        self._omit_empty = None

        self.omit_empty = False

        for k, v in spec.items():
            setattr(self, k, v)

    @property
    def bins(self):

        if self._bins is not None:
            return self._bins
        b = self.get('bins', None)
        if not isinstance(b, list):
            raise ValueError("bins must be a list of list of datetimes")
        out = []
        for d in b:
            if d is None:
                raise ValueError("bin cannot be None")
            dates = d
            try:
                out.append([d for d in map(isoparse, dates)])
            except Exception as e:
                raise e
        self._bins = out
        return out

    @bins.setter
    def bins(self, v: List[List[Union[datetime.datetime, str]]]):
        b = []
        for d in v:
            if len(d) != 2:
                raise ValueError("bins must be a list of pairs of start/end datetime bin edges")

            if isinstance(d[0], str):
                for dt in d:
                    try:
                        isoparse(dt)
                    except Exception as e:
                        raise ValueError("bin edges must be datetimes or parsable rfc3339 strings") from e
                b.append(list(d))

            elif isinstance(d[0], datetime.datetime):
                b.append([datetime_to_utc(dt).isoformat() for dt in d])
        self['bins'] = b

    @property
    def omit_empty(self):
        if self._omit_empty is not None:
            return self._omit_empty
        self._omit_empty = self.get('omit_empty')
        return self._omit_empty

    @omit_empty.setter
    def omit_empty(self, v: bool):
        if not isinstance(v, bool):
            raise ValueError('omit_empty must be a bool')
        self['omit_empty'] = v


class Cluster(dict):
    """Cluster spec for temporal binning"""
    def __init__(self, **spec):
        self._threshold = None
        self._max_cluster_width = None
        self._direction = None

        for k, v in spec.items():
            setattr(self, k, v)

    @property
    def threshold(self):
        if self._threshold is not None:
            return self._threshold
        self._threshold = self.get('threshold', None)
        return self._threshold

    @threshold.setter
    def threshold(self, v: Union[str, datetime.timedelta]):
        if isinstance(v, str):
            r = bin_size_re.match(v)
            if r:
                self['threshold'] = v
            else:
                raise ValueError(r"threshold must have pattern: 'r^\d+(ms|us|ns|[WDhms]){1}' example: '15h'")
        elif isinstance(v, datetime.timedelta):
            r = v.total_seconds()
            r = int(r * (1000000))
            r = f'{r}us'
            self['threshold'] = r
        else:
            raise ValueError("threshold must be of type str or datetime.timedelta")

    @property
    def max_cluster_width(self):
        if self._max_cluster_width is not None:
            return self._max_cluster_width
        self._max_cluster_width = self.get('max_cluster_width', None)
        return self._max_cluster_width

    @max_cluster_width.setter
    def max_cluster_width(self, v: str):
        if isinstance(v, str):
            r = bin_size_re.match(v)
            if r:
                self['max_cluster_width'] = v
            else:
                raise ValueError(r"max_cluster_width must have pattern: 'r^\d+(ms|us|ns|[WDhms]){1}' example: '15h'")
        elif isinstance(v, datetime.timedelta):
            r = v.total_seconds()
            r = int(r * (1000000))
            r = f'{r}us'
            self['max_cluster_width'] = r
        else:
            raise ValueError("max_cluster_width must be of type str or datetime.timedelta")

    @property
    def direction(self):
        if self._direction is not None:
            return self._direction
        self._direction = self.get('direction', None)
        return self._direction

    @direction.setter
    def direction(self, v: str):
        if not isinstance(v, str):
            raise ValueError("direction must be type str")
        if v not in ['forward', 'backward']:
            raise ValueError("direction must be one of ['forward', 'backward']")
        self['direction'] = v


class TemporalBinning(dict):
    """Temporal binning is a class to represent the temporal binning in a series request.

    Args:
        spec(dict): The dict to initialize the class with.
    """
    def __init__(self, **spec):
        self._equal = None
        self._user = None
        self._cluster = None
        self._reference = None
        self._aggregation_rules = None

        for k, v in spec.items():
            setattr(self, k, v)

    @property
    def equal(self):
        if self._equal is not None:
            return self._equal
        self._equal = self.get('equal', {})
        return self._equal

    @equal.setter
    def equal(self, v: Union[Equal, dict]):
        self['equal'] = dict(Equal(**v))

    @property
    def user(self):
        if self._user is not None:
            return self._user
        self._user = User(**self.get('user', {}))
        return self._user

    @user.setter
    def user(self, v: Union[User, dict]):
        self['user'] = dict(User(**v))

    @property
    def cluster(self):
        if self._cluster is not None:
            return self._cluster
        self._cluster = Cluster(**self.get('user', {}))
        return self._cluster

    @cluster.setter
    def cluster(self, v: Union[Cluster, dict]):
        self['cluster'] = dict(Cluster(**v))

    @property
    def reference(self):
        if self._reference is not None:
            return self._reference
        self._reference = self.get('reference', None)
        return self._reference

    @reference.setter
    def reference(self, v: str):
        if not isinstance(v, str):
            raise ValueError("reference must be a string")
        self['reference'] = v
