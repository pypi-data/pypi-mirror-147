from math import ceil
import time
import os
import re
import ipyleaflet

import numpy as np
from geodesic.account.projects import ProjectDescr, get_active_project
from geodesic.service import ServiceClient
from geodesic.tesseract.utils import animate_tesseract

from geodesic.utils import MockImport
from geodesic.bases import APIObject
from geodesic.client import get_client, raise_on_error
from geodesic import Dataset
from geodesic.stac import FeatureCollection, Item

try:
    import ipywidgets as widgets
    from ipywidgets import VBox, HBox
    from IPython.display import display
    OUTPUT_TYPE = "widget"
except ImportError:
    print("could not import ipywidgets, text output will be used instead")
    OUTPUT_TYPE = "text"

try:
    from ipyleaflet import Map, basemaps, GeoJSON
    USE_MAP = True
except ImportError:
    print("could not load ipyleaflet")
    USE_MAP = False

try:
    import zarr
except ImportError:
    zarr = MockImport("zarr")


job_id_re = re.compile(r'job with ID (\w*) already exists')


class Job(APIObject):
    """Base class for all job types in tesseract.

    This base class has all of the core functionality needed for tesseract jobs except for the submit() funtion.
    Submit should be implemented individually on the different sub-classes since the underlying sub-classes can
    be a bit different and how they are submitted can vary. The class can be initialized either with a dictionary
    that represents the request for the particular type, or can be given an job ID. If a job ID is provided it
    will query for that job on the tesseract service and then update this class with the specifics of that job.

    Args:
        spec(dict): A dictionary representing the job request.
        job_id(str): The job ID string. If provided the job will be initialized
                    with info by making a request to tesseract.
    """
    project = ProjectDescr(doc="which project the job will be saved to")

    def __init__(self, job_id: str = None, **spec):
        self.project = get_active_project()
        self._submitted = False
        self._dataset = None
        self._item = None
        self._bounds = None
        self._widget = None

        try:
            self._service = ServiceClient(self._api_name, self._api_version)
        except AttributeError:
            raise ValueError("inheriting class should set the _api_name and _api_version attributes")

        # status values
        self._state = None
        self._n_quarks = None
        self._n_completed = None

        # geometries
        self._query_geom = None
        self._quark_geoms = None
        self.job_id = None

        if job_id is None:
            self["f"] = self.get("f", "JSON")  # Always json for now. May add http later
            self["async"] = True

        if job_id is not None:
            self.job_id = job_id
            client = get_client()
            ds = raise_on_error(client.get(f'/tesseract/api/v1/job/{self.job_id}')).json()
            self._dataset = Dataset(**ds)
            si = raise_on_error(client.get(f'/tesseract/api/v1/job/{self.job_id}/items/1')).json()
            self._item = Item(dataset=self._dataset, **si)
            self._queryGeom = getattr(self._item, 'geometry', None)

            st = self.status(return_quark_geoms=True)
            qgeoms = st.get('features', None)
            if qgeoms is None:
                raise Exception("job status returned no geometries")
            self.quark_geoms = FeatureCollection(obj=qgeoms)

    def submit(self, load_if_exists=True, overwrite=False):
        """Submits a job to be processed by tesseract

        This function will take the job defined by this class and submit it to the tesserct api for processing.
        Once submitted the dataset and items fields will be populated containing the SeerAI dataset and STAC items
        respectively. Keep in mind that even though the links to files in the STAC item will be populated, the job
        may not yet be completed and so some of the chunks may not be finished.
        """

        if self._submitted and (overwrite or load_if_exists):
            if overwrite:
                self.delete()
                self._submitted = False
                return self.submit(overwrite=True)
            elif self.job_id is not None:
                ds_res = raise_on_error(self._service.get(f'job/{self.job_id}')).json()
                self._dataset = Dataset(**ds_res)
                item_res = raise_on_error(self._service.get(f'job/{self.job_id}/items/{self.job_id}')).json()
                self._item = Item(**item_res)
                self.status(return_quark_geoms=True)
                return

        elif self._submitted:
            raise Exception("this job has already been submitted. \
                            Create a new TesseractJob if you would like to submit a new job")

        response = self._service.post(self._api_name, **self)

        if overwrite or load_if_exists:
            res = response.json()
            if 'error' in res:
                m = job_id_re.search(res['error']['detail'])
                if m:
                    job_id = m.group(1)
                    self.job_id = job_id
                    if overwrite:
                        self.delete()
                        return self.submit(overwrite=True)
                    else:
                        ds_res = raise_on_error(self._service.get(f'job/{self.job_id}')).json()
                        self._dataset = Dataset(**ds_res)
                        item_res = raise_on_error(self._service.get(f'job/{self.job_id}/items/{self.job_id}')).json()
                        self._item = Item(**item_res)
                        self.status(return_quark_geoms=True)
                        return

                else:
                    raise_on_error(response)
            pass
        else:
            res = raise_on_error(response).json()

        self.job_id = res.get("job_id", None)
        if self.job_id is None:
            raise ValueError("no job_id was returned, something went wrong")

        ds = res.get('dataset', None)
        if ds is not None:
            self._dataset = Dataset(**ds)

        si = res.get('stac_item', None)

        if si is not None:
            self._item = Item(**si)

        self.status(return_quark_geoms=True)
        self._submitted = True
        return f"created job: {self.job_id}"

    @property
    def alias(self):
        try:
            return self['alias']
        except KeyError:
            return self.job_id

    @alias.setter
    def alias(self, v: str):
        if not isinstance(v, str):
            raise ValueError("alias must be a string")
        self._set_item('alias', v)

    @property
    def workers(self):
        return self['workers']

    @workers.setter
    def workers(self, v: int):
        if not isinstance(v, int):
            raise ValueError("workers must be an int")
        self._set_item('workers', v)

    @property
    def description(self):
        return self['description']

    @description.setter
    def description(self, v: str):
        if not isinstance(v, str):
            raise ValueError("description must be a string")
        self._set_item('description', v)

    @property
    def dataset(self):
        return self._dataset

    @property
    def item(self):
        return self._item

    def zarr(self, asset_name: str):
        """
        Returns the Zarr group for the corresponding asset name

        Args:
            asset_name: name of the asset to open and return
        Returns:
            zarr file pointing to the results.
        """
        if self._item is None or self._n_completed != self._n_quarks:
            raise ValueError("computation not completed")

        try:
            assets = self._item.assets
        except AttributeError:
            raise AttributeError("item has no assets")

        try:
            asset = assets[asset_name]
        except KeyError:
            raise KeyError(f"asset {asset_name} does not exist")

        href = asset.href

        return zarr.open(href)

    def ndarray(self, asset_name: str):
        """
        Returns a numpy.ndarray for specified asset name.

        USE WITH CAUTION! RETURNS ALL OF WHAT COULD BE A
        HUGE ARRAY

        Args:
            asset_name: name of the asset to open and return
        Returns:
            numpy array of all the results.
        """
        return self.zarr(asset_name)['tesseract'][:]

    def status(self, return_quark_geoms: bool = False, return_quark_status: bool = False):
        """Status queries the tesseract service for the jobs status.

        Args:
            return_quark_geoms(bool): Should the query to the service ask for all of the quarks geometries.
                                    If True it will populate the geometry in this class.
            return_quark_status(bool): If True will query for the status of each individual quark associated with
                                    the job.

        returns:
            A dictionary with the response from the Tesseract service

        """
        if not self.job_id:
            raise Exception("job_id not set, cannot get status")
        client = get_client()
        q = {
            "return_quark_geoms": return_quark_geoms,
            "return_quark_status": return_quark_status
            }
        res = raise_on_error(client.get(f'/tesseract/api/v1/job/{self.job_id}/status', **q)).json()

        status = res.get('job_status', None)
        if status is None:
            raise Exception("status: could not get job status")

        self._n_quarks = status.get('n_quarks', None)
        self._n_completed = status.get('n_quarks_completed', 0)
        self._state = status.get('state', None)

        if return_quark_geoms:
            qgeoms = status.get('features', None)
            if qgeoms is None:
                raise Exception("job status returned no geometries")
            self.quark_geoms = FeatureCollection(obj=qgeoms)

        return status

    def delete(self, remove_data=False):
        """Delete marks a job for deletion in the Tesseract service.

        When delete is called it marks the job to be deleted. This wont immediately delete the job
        from the service. Instead it will just set its state as 'deleted' and it will stop processing
        quarks. If the job is re-submitted it will completely delete the previous job from the service and
        recreate it. Once the job is in the 'deleted' state it will be fully deleted from the service after
        24 hours at which point it is not recoverable.
        """
        if not self.job_id:
            raise Exception("job_id not set, cannot delete")
        client = get_client()

        res = raise_on_error(
            client.delete(f'/tesseract/api/v1/job/{self.job_id}/delete', remove_data=remove_data)
        ).json()

        js = res.get('job_status', None)
        if js is None:
            raise Exception("could not get confirmation of delete")
        state = js.get('state', None)
        if state is None:
            raise Exception("could not get confirmation of delete")
        self._state = state
        self._submitted = False

    def widget(self, basemap=None):
        if OUTPUT_TYPE != "widget":
            raise ValueError("ipywidgets must be installed to view widget")

        if self._item is None:
            raise ValueError("no job found/job not specified")

        if not self.job_id:
            raise Exception("job_id not set, nothing to watch")

        self.quark_geoms_lookup = {}
        for q in self.quark_geoms.features:
            self.quark_geoms_lookup[q['id']] = q

        quark_status = self.status(return_quark_status=True)
        for k, status in quark_status['quark_status'].items():
            self.quark_geoms_lookup[k].properties['status'] = status

        self._prog = widgets.IntProgress(
            value=self._n_completed,
            min=0,
            max=self._n_quarks,
            step=1,
            description="Running: ",
            bar_style='',
            orientation='horizontal'
        )
        self._title = widgets.HTML(
            value=self._get_title()
        )
        self._ratio = widgets.HTML(
            value=self._get_ratio()
        )

        zoom, center, _ = self._calc_zoom_center()

        if basemap is None:
            basemap = basemaps.CartoDB.DarkMatter

        self.map = Map(
            basemap=basemap,
            center=center,
            zoom=zoom,
        )

        vb = VBox([self._title, self._ratio, self._prog])
        w = HBox([vb, self.map])

        if self._item:
            disp = Item(**self._item)
            disp.geometry = disp.geometry.buffer(np.sqrt(disp.geometry.area) * 0.05).envelope
            fci = {
                'type': 'FeatureCollection',
                'features': [
                    disp
                ]
            }
            query_layer = GeoJSON(
                data=fci,
                style={
                    "opacity": 1, "color": "#e2e6d5", "fillOpacity": 0.0, 'weight': 1, "dashArray": "4 4"
                },
                hover_style={
                    'fillOpacity': 0.75
                }
            )
            query_layer.name = "Requested Extent"
            self.map.add_layer(query_layer)

        if self.quark_geoms:

            def _quark_color(feature):
                style = {
                    "opacity": 0.5,
                    "color": "#888888",
                    "fillColor": "#888888",
                    "fillOpacity": 0.05
                }

                sts = feature['properties'].get('status', 'incomplete')
                if sts == "incomplete":
                    style['fillOpacity'] = 0.0
                    return style
                elif sts == "running":
                    style['fillColor'] = 'yellow'
                    style['color'] = 'yellow'
                    style['opacity'] = 1.0
                elif sts == "failed":
                    style['fillColor'] = 'red'
                    style['color'] = 'red'
                    style['opacity'] = 0.0
                elif sts == "completed":
                    style['fillColor'] = 'green'
                    style['color'] = 'green'
                    style['opacity'] = 0.0

                return style

            fc = {
                'type': 'FeatureCollection',
                'features': self.quark_geoms.features
            }
            self._quark_layer = GeoJSON(
                data=fc,
                style={
                },
                hover_style={
                    'fillOpacity': 0.75,
                },
                style_callback=_quark_color,
            )
            self._quark_layer.name = "Quark Extents"
            self.map.add_layer(self._quark_layer)

        self.map.add_control(ipyleaflet.LayersControl(position='topright'))
        self._widget = w
        return self._widget

    def _save_asset_thumbnail(self, idx: int, asset: str, mask_asset: str = None, nodata=0, threshold=None):
        img = self.zarr(asset)['tesseract'][idx, :, :, :]
        if mask_asset is not None:
            img *= self.ndarray(mask_asset)[0]

        img = np.squeeze(img, 0)
        if img.ndim == 3 and img.shape[0] != 3:
            print("couldn't display result, not compatible with visualization")
            return

        import matplotlib.pyplot as plt
        from matplotlib.cm import magma

        if threshold is not None:
            img[img < threshold] = np.nanmin(img[img >= threshold])

        mu = np.nanmedian(img)
        std = np.nanstd(img)

        cmin = mu - std
        cmax = mu + std

        cmin = max(np.nanmin(img), cmin)
        cmax = min(np.nanmax(img), cmax)

        img = (img - cmin) / (cmax - cmin)

        if img.ndim == 2:
            nodata_idx = img == nodata
            img[nodata_idx] = np.nan
            img = magma(img)

            img *= 255
            img = img.astype(np.uint8)
            img = np.ascontiguousarray(img)

        fname = f'tmp-overlay-{asset}.png'
        plt.imsave(fname, img, cmap='magma', vmin=cmin, vmax=cmax)

        return fname

    def watch(self,
              basemap=basemaps.CartoDB.DarkMatter,
              display_last_result=False,
              asset=None,
              nodata=0,
              threshold=None,
              animate=False,
              mask_asset=None):
        """Monitor the tesseract job with the SeerAI widget.

        Will create a jupyter widget that will watch the progress of this tesseract job.
        """
        if not self.job_id:
            raise Exception("job_id not set, nothing to watch")

        if OUTPUT_TYPE != "widget":
            raise ValueError("ipywidgets must be installed to watch job")

        self.status(return_quark_status=True)

        display(self.widget(basemap))

        keep_watching = True
        while keep_watching:
            self._update_widget()
            time.sleep(1)
            if self._n_completed == self._n_quarks:
                break

        if animate:
            x = self.ndarray(asset)
            if mask_asset is not None:
                y = self.ndarray(mask_asset)
            else:
                y = 1

            x[~np.isfinite(x)] = 0
            x[x < 0] = 0
            _ = animate_tesseract(x*y, scale_type='stddev', filename='tmp-animation.mp4')

            img_layer = ipyleaflet.VideoOverlay(
                url='files/'+os.path.split(os.getcwd())[-1]+'/tmp-animation.mp4',
                bounds=self._bounds
            )
            self.map.add_layer(img_layer)

        elif display_last_result and asset is not None:
            fname = self._save_asset_thumbnail(-1, asset, mask_asset, nodata, threshold=threshold)
            img_layer = ipyleaflet.ImageOverlay(
                url='files/'+os.path.split(os.getcwd())[-1]+f'/{fname}',
                bounds=self._bounds
            )
            self.map.add_layer(img_layer)

    def _update_widget(self):
        quark_status = self.status(return_quark_status=True, return_quark_geoms=True)

        for k, status in quark_status['quark_status'].items():
            self.quark_geoms_lookup[k].properties['status'] = status

        feats = {
            'type': "FeatureCollection",
            'features': [f for _, f in self.quark_geoms_lookup.items()]
        }
        self._quark_layer.data = feats

        # set numerics
        self._prog.value = self._n_completed
        self._title.value = self._get_title()
        self._ratio.value = self._get_ratio()

    def _get_title(self):
        return f"<h2>Job ID: {self.alias} - {self._state}</h2>"

    def _get_ratio(self):
        return f"<h2>{self._n_completed} / {self._n_quarks}</h2>"

    def _calc_zoom_center(self):

        x_min = 0
        y_min = 1
        x_max = 2
        y_max = 3

        c = self._item['bbox']
        if self._bounds is None:
            self._bounds = [[c[y_min], c[x_min]], [c[y_max], c[x_max]]]
        center = ((c[y_max]+c[y_min]) / 2.0, (c[x_max] + c[x_min]) / 2.0)

        scale_x = (c[x_max] - c[x_min]) / 360
        scale_y = (c[y_max] - c[y_min]) / 180
        scale = max(scale_x, scale_y)

        if scale > 0:
            zoom = ceil(-np.log2(scale + 1e-9))
        else:
            zoom = 21

        zoom = max(0, zoom)
        zoom = min(21, zoom)
        return zoom, center, self._bounds

    @property
    def state(self):
        return self._state
