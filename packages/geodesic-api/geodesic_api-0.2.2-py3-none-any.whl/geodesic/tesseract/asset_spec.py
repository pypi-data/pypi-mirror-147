from typing import List, Tuple, Sequence, Union

import numpy as np
import datetime
from dateutil.parser import isoparse
from geodesic.account.projects import Project, get_project
from geodesic.bases import APIObject
from geodesic.entanglement.dataset import Dataset

from geodesic.utils import datetime_to_utc
from geodesic.stac import Item
from geodesic.tesseract.aggregation import FeatureAggregation
from geodesic.tesseract.temporal_binning import TemporalBinning
__all__ = ["AssetSpec"]

###################################################################################
# AssetSpec Class
###################################################################################

resample_options = [
    'nearest',
    'bilinear',
    'cubic',
    'cubicspline',
    'lanczos',
    'average',
    'mode',
    'max',
    'min',
    'median',
    'q1',
    'q3',
    'sum'
]


class AssetSpec(APIObject):
    """AssetSpec is a class to represent the requested output assets in a tesseract job.

    Args:
        spec(dict): A dictionary that can be used to initialize the object. Optional.

    """
    def __init__(self, **spec):
        self._name = None
        self._dataset = None
        self._assets = None
        self._resample = None
        self._processors = None
        self._project = None
        self._shape = None
        self._pixel_size = None
        self._pixel_dtype = None
        self._compression = None
        self._input_no_data = None
        self._output_no_data = None
        self._ids = None
        self._datetime = None
        self._query = None
        self._feature_aggregation = None
        self._items = None
        self._aggregation_rules = None
        self._fill_value = None
        self._temporal_binning = None

        # Set defaults
        self.resample = 'nearest'
        self.fill_value = 0
        self.pixel_dtype = np.float32
        self.compression = 'blosc'

        for k, v in spec.items():
            if k == 'items':
                k = 'items_'
            setattr(self, k, v)

    @property
    def name(self):
        if self._name is not None:
            return self._name
        self._name = self.get('name', None)
        return self._name

    @name.setter
    def name(self, name: str):
        if not isinstance(name, str):
            raise ValueError('asset name must be a string')
        self._set_item('name', name)

    @property
    def dataset(self):
        if self._dataset is not None:
            return self._dataset
        self._dataset = self.get('dataset', None)
        return self._dataset

    @dataset.setter
    def dataset(self, v):
        if not isinstance(v, (str, Dataset)):
            raise ValueError("dataset must be a string or Dataset")

        if isinstance(v, Dataset):
            p = v.project
            v = v.name
            self.project = p
        self._set_item('dataset', v)

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
        self._set_item('chip_size', v)

    @property
    def assets(self):
        if self._assets is not None:
            return self._assets
        self._assets = self.get('assets', None)
        return self._assets

    @assets.setter
    def assets(self, assets: Union[List[str], Tuple[str]]):
        if not isinstance(assets, (list, tuple)):
            raise ValueError("assets must be an tuple or list")
        self._set_item('assets', [_ for _ in assets])

    @property
    def resample(self):
        if self._resample is not None:
            return self._resample
        self._resample = self.get('resample', 'nearest')
        return self._resample

    @resample.setter
    def resample(self, r: str):
        assert isinstance(r, str)
        if not (r in resample_options):
            raise ValueError(f"invalid resample type, must be in {', '.join(resample_options)}")
        self._set_item('resample', r)

    @property
    def processors(self):
        if self._processors is not None:
            return self._processors
        self._processors = self.get('processors', None)
        return self._processors

    @processors.setter
    def processors(self, p: Union[List[str], Tuple[str]]):
        if p is None:
            return
        if not isinstance(p, (list, tuple)):
            raise ValueError("processors must be a Sequence of str or None")
        # Could put some stuff in here to check that the processors are valid
        self._set_item('processors', [_ for _ in p])

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
        self._set_item('shape', s)

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
        self._set_item('pixel_size', s)

    @property
    def pixel_dtype(self):
        if self._pixel_dtype is not None:
            return self._pixel_dtype
        self._pixel_dtype = np.dtype(self.get('pixel_dtype', 'float32'))
        return self._pixel_dtype

    @pixel_dtype.setter
    def pixel_dtype(self, d: Union[str, np.dtype]):
        dt = np.dtype(d)

        self._set_item('pixel_dtype', dt.descr[0][1])

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
        self._set_item('compression', c)

    @property
    def input_no_data(self):
        if self._input_no_data is not None:
            return self._input_no_data
        self._input_no_data = self.get("input_no_data", None)
        return self._input_no_data

    @input_no_data.setter
    def input_no_data(self, v: Union[List[float], Union[float, int]]):
        assert (isinstance(v, List) or isinstance(v, (float, int)))
        self._set_item('input_no_data', v)

    @property
    def output_no_data(self):
        if self._output_no_data is not None:
            return self._output_no_data
        self._output_no_data = self.get("output_no_data", None)
        return self._output_no_data

    @output_no_data.setter
    def output_no_data(self, v: Union[List[float], Union[float, int]]):
        assert (isinstance(v, List) or isinstance(v, (float, int)))
        self._set_item('output_no_data', v)

    @property
    def ids(self):
        if self._ids is not None:
            return self._ids
        self._ids = self.get('ids', None)
        return self._ids

    @ids.setter
    def ids(self, v: List[str]):
        if not isinstance(v, (tuple, list)):
            raise ValueError("ids must be a list of strings")
        self._set_item('ids', v)

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
        self._set_item('datetime', f'{dts0}/{dts1}')

    @property
    def query(self):
        if self._query is not None:
            return self._query
        self._query = self.get("query", None)
        return self._query

    @query.setter
    def query(self, q: dict):
        self._set_item('query', dict(q))

    @property
    def feature_aggregation(self):
        if self._feature_aggregation is not None:
            return self._feature_aggregation
        self._feature_aggregation = FeatureAggregation(**self.get('feature_aggregation', {}))
        return self._feature_aggregation

    @feature_aggregation.setter
    def feature_aggregation(self, f: Union[FeatureAggregation, dict]):
        self._set_item('feature_aggregation', dict(f))

    @property
    def items_(self):
        if self._items is not None:
            return self._items
        self._items = [Item(**i) for i in self.get('items', [])]
        return self._items

    @items_.setter
    def items_(self, v: List[dict]):
        self._set_item('items', v)

    @property
    def aggregation_rules(self):
        if self._aggregation_rules is not None:
            return self._aggregation_rules
        self._aggregation_rules = self.get('aggregation_rules', None)
        return self._aggregation_rules

    @aggregation_rules.setter
    def aggregation_rules(self, r: Sequence[str]):
        self._set_item('aggregation_rules', [_ for _ in r])

    @property
    def fill_value(self):
        if self._fill_value is not None:
            return self._fill_value
        self._fill_value = self.get('fill_value', None)
        return self._fill_value

    @fill_value.setter
    def fill_value(self, v: Union[float, int]):
        if not isinstance(v, (int, float)):
            raise ValueError("fill value must be an int or float")
        self._set_item('fill_value', v)

    @property
    def temporal_binning(self):
        if self._temporal_binning is not None:
            return self._temporal_binning
        p = self.get("temporal_binning", {})
        self._temporal_binning = TemporalBinning(**p)
        return self._temporal_binning

    @temporal_binning.setter
    def temporal_binning(self, v: Union[dict, TemporalBinning]):
        self._set_item('temporal_binning', dict(v))
