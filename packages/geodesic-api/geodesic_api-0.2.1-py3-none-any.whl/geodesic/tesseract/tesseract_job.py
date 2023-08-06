from typing import List, Union
from shapely.geometry import box, shape
from geodesic.bases import reset_attr
from geodesic.tesseract.job import Job
from geodesic.tesseract.global_properties import GlobalProperties
from geodesic.tesseract.asset_spec import AssetSpec


class TesseractJob(Job):
    """TesseractJob represents a tesseract process that produces a tesseract.

    Args:
        desc(dict): A dictionary representing the job request.

    """
    def __init__(self, job_id: str = None, **spec):
        self._bbox = None
        self._bbox_epsg = None
        self._geometry = None
        self._raster_format = None
        self._output_epsg = None
        self._global_properties = None
        self._asset_specs = None
        self._api_name = 'tesseract'
        self._api_version = 1
        self._dry_run = False

        self.global_properties = GlobalProperties()
        self.bbox_epsg = 4326
        self.output_epsg = 3857

        if job_id is None:
            super().__init__(**spec)
            for k, v in spec.items():
                setattr(self, k, v)
        else:
            super().__init__(job_id=job_id)

    @property
    def bbox(self):
        if self._bbox is not None:
            return self._bbox
        bb = self.get("bbox", [])
        if len(bb) >= 4:
            self._bbox = box(bb[0], bb[1], bb[2], bb[3])
        return self._bbox

    @bbox.setter
    def bbox(self, b: Union[list, tuple]):
        if isinstance(b, (list, tuple)):
            self._set_item('bbox', b)
            return
        try:
            self._set_item('bbox', b.__geo_interface__)
            try:
                self._set_item('bbox', b.bounds)
            except AttributeError:
                try:
                    self._set_item('bbox', b.extent)
                except Exception:
                    pass
            return
        except AttributeError:
            raise ValueError("unknown bbox or geometry type")

    @property
    def geometry(self):
        if self._geometry is not None:
            return self._geometry

        try:
            self._geometry = shape(self["geometry"])
        except KeyError:
            return None
        return self._geometry

    @geometry.setter
    @reset_attr
    def geometry(self, g):
        if isinstance(g, dict):
            # make sure g is a geometry
            try:
                _ = shape(g)
            except Exception as e:
                raise ValueError("this does not appear to be a valid geometry") from e
            self._set_item("geometry", g)
            return
        try:
            self._set_item("geometry", g.__geo_interface__)
            return
        except AttributeError:
            raise ValueError("unknown geometry object")

    @property
    def raster_format(self) -> str:
        if self._raster_format is not None:
            return self._raster_format
        self._raster_format = self.get("raster_format", None)
        return self._raster_format

    @raster_format.setter
    def raster_format(self, f: str):
        assert isinstance(f, str)
        self._set_item("raster_format", f)

    @property
    def dry_run(self) -> str:
        if self._dry_run is not None:
            return self._dry_run
        self._dry_run = self.get("dry_run", None)
        return self._dry_run

    @dry_run.setter
    @reset_attr
    def dry_run(self, x: bool):
        assert isinstance(x, bool)
        self._set_item("dry_run", x)

    @property
    def bbox_epsg(self):
        if self._bbox_epsg is not None:
            return self._bbox_epsg

        self._bbox_epsg = self.get("bbox_epsg", None)
        return self._bbox_epsg

    @bbox_epsg.setter
    def bbox_epsg(self, epsg: int):
        assert isinstance(epsg, int)
        self._set_item("bbox_epsg", epsg)

    @property
    def output_epsg(self):
        if self._output_epsg is not None:
            return self._output_epsg

        self._output_epsg = self.get("output_epsg", None)
        return self._output_epsg

    @output_epsg.setter
    def output_epsg(self, epsg: int):
        assert isinstance(epsg, int)
        self._set_item("output_epsg", epsg)

    @property
    def global_properties(self):
        if self._global_properties is not None:
            return self._global_properties
        p = self.get("global_properties", {})
        self._global_properties = GlobalProperties(**p)
        return self._global_properties

    @global_properties.setter
    def global_properties(self, v: dict):
        self._set_item('global_properties', dict(GlobalProperties(**v)))

    @property
    def asset_specs(self):
        if self._asset_specs is not None:
            return self._asset_specs
        a = self.get("asset_specs", [])
        self._asset_specs = [AssetSpec(**_) for _ in a]
        return self._asset_specs

    @asset_specs.setter
    def asset_specs(self, specs: List[dict]):
        self._set_item('asset_specs', [dict(AssetSpec(**_)) for _ in specs])
