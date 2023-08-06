from typing import List, Sequence, Union

import numpy as np
import datetime
from dateutil.parser import isoparse
from geodesic.account.projects import Project, get_project

from geodesic.utils import datetime_to_utc
from geodesic.tesseract.temporal_binning import TemporalBinning
__all__ = ["GlobalProperties"]


class GlobalProperties(dict):
    def __init__(self, **spec):
        self._shape = None
        self._pixel_size = None
        self._pixel_dtype = None
        self._compression = None
        self._project = None
        self._datetime = None
        self._output_no_data = None
        self._temporal_binning = None

        for k, v in spec.items():
            setattr(self, k, v)

    @property
    def project(self):
        """
        Get the object's project
        """
        return self['project']

    @project.setter
    def project(self, v: Union[str, Project]):
        """
        Set the object's project.
        """
        if not isinstance(v, (str, Project)):
            raise ValueError("project must be a string or a Project")
        if isinstance(v, str):
            if self._project is not None:
                if self._project.name != v:
                    v = get_project(v)
                else:
                    v = self._project
            else:
                v = get_project(v)
        self._project = v
        self._set_item("project", v.name)

    @property
    def chip_size(self):
        return self['chip_size']

    @chip_size.setter
    def chip_size(self, v: int):
        self['chip_size'] = v

    @property
    def shape(self):
        if self._shape is not None:
            return self._shape
        self._shape = self.get('shape', None)
        return self._shape

    @shape.setter
    def shape(self, s: Sequence[int]):
        if len(s) != 2:
            raise ValueError("shape must be 2 values: (rows, columns)")
        self['shape'] = s

    @property
    def pixel_size(self):
        if self._pixel_size is not None:
            return self._pixel_size
        self._pixel_size = self.get('pixel_size', None)
        return self._pixel_size

    @pixel_size.setter
    def pixel_size(self, s: Union[Sequence[float], float]):
        if isinstance(s, float):
            self['pixel_size'] = (s, s)
            return
        if len(s) != 2:
            raise ValueError("pixel_size must be 2 values: (x, y)")
        self['pixel_size'] = s

    @property
    def pixel_dtype(self):
        if self._pixel_dtype is not None:
            return self._pixel_dtype
        self._pixel_dtype = np.dtype(self.get('pixel_dtype', 'float32'))
        return self._pixel_dtype

    @pixel_dtype.setter
    def pixel_dtype(self, d: np.dtype):
        self['pixel_dtype'] = str(d)

    @property
    def compression(self):
        if self._compression is not None:
            return self._compression
        self._compression = self.get('compression', 'blosc')
        return self._compression

    @compression.setter
    def compression(self, c: str):
        assert isinstance(c, str)
        if not (c in ["zlib", "blosc", "none"]):
            raise ValueError("invalid compression type, must be in ['zlib', 'blosc', 'none']")
        self['compression'] = c

    @property
    def output_no_data(self):
        if self._output_no_data is not None:
            return self._output_no_data
        self._output_no_data = self.get("output_no_data", None)
        return self._output_no_data

    @output_no_data.setter
    def output_no_data(self, v: Union[List[float], Union[float, int]]):
        assert (isinstance(v, List) or isinstance(v, (float, int)))
        self['output_no_data'] = v

    @property
    def datetime(self):
        if self._datetime is not None:
            return self._datetime
        d = self.get('datetime', None)
        if d is None:
            return None
        dates = d.split('/')
        try:
            self._datetime = [None if d == ".." else isoparse(d) for d in dates]
            return self._datetime
        except Exception as e:
            raise e

    @datetime.setter
    def datetime(self, v: Sequence):
        if v is None:
            return None

        if isinstance(v, str):
            try:
                dt0, dt1 = v.split('/')
            except Exception:
                ValueError('datetime as a string must be of the form <start>/<end>')

        elif len(v) != 2:
            raise ValueError("Must provide a start and end datetime. Provide None or '..' string if one end is open")
        else:
            dt0 = v[0]
            dt1 = v[1]

        if isinstance(dt0, str):
            if dt0 == "":
                raise ValueError("string must be either '..' or a valid RFC3339 datetime")
            dts0 = dt0
        elif isinstance(dt0, datetime.datetime):
            dts0 = datetime_to_utc(dt0).isoformat()
        elif dt0 is None:
            dts0 = '..'
        else:
            raise ValueError("not a recognized datetime format. must be either python datetime or string")

        if isinstance(dt1, str):
            if dt1 == "":
                raise ValueError("string must be either '..' or a valid RFC3339 datetime")
            dts1 = dt1
        elif isinstance(dt1, datetime.datetime):
            dts1 = datetime_to_utc(dt1).isoformat()
        elif dt1 is None:
            dts1 = '..'
        else:
            raise ValueError("not a recognized datetime format. must be either python datetime or string")

        if dts0 != "..":
            dts0 = datetime_to_utc(isoparse(dts0)).isoformat()
        if dts1 != "..":
            dts1 = datetime_to_utc(isoparse(dts1)).isoformat()
        self['datetime'] = f'{dts0}/{dts1}'

    @property
    def temporal_binning(self):
        if self._temporal_binning is not None:
            return self._temporal_binning
        p = self.get("temporal_binning", {})
        self._temporal_binning = TemporalBinning(**p)
        return self._temporal_binning

    @temporal_binning.setter
    def temporal_binning(self, v: Union[dict, TemporalBinning]):
        self['temporal_binning'] = dict(v)
