# Copyright CNRS/Inria/UCA
# Contributor(s): Eric Debreuve (since 2022)
#
# eric.debreuve@cnrs.fr
#
# This software is governed by the CeCILL  license under French law and
# abiding by the rules of distribution of free software.  You can  use,
# modify and/ or redistribute the software under the terms of the CeCILL
# license as circulated by CEA, CNRS and INRIA at the following URL
# "http://www.cecill.info".
#
# As a counterpart to the access to the source code and  rights to copy,
# modify and redistribute granted by the license, users are provided only
# with a limited warranty  and the software's author,  the holder of the
# economic rights,  and the successive licensors  have only  limited
# liability.
#
# In this respect, the user's attention is drawn to the risks associated
# with loading,  using,  modifying and/or developing or reproducing the
# software by the user in light of its specific status of free software,
# that may mean  that it is complicated to manipulate,  and  that  also
# therefore means  that it is reserved for developers  and  experienced
# professionals having in-depth computer knowledge. Users are therefore
# encouraged to load and test the software's suitability as regards their
# requirements in conditions enabling the security of their systems and/or
# data to be ensured and,  more generally, to use and operate it in the
# same conditions as regards security.
#
# The fact that you are presently reading this means that you have had
# knowledge of the CeCILL license and that you accept its terms.

from __future__ import annotations

from typing import Any, Callable, List, Optional, Tuple, Union

import matplotlib as mlpl  # noqa
import matplotlib.pyplot as pypl  # noqa
import numpy as nmpy
import skimage.measure as msre
from matplotlib.artist import Artist as backend_plot_t  # noqa
from matplotlib.gridspec import GridSpec as grid_spec_t  # noqa
from matplotlib.markers import MarkerStyle as marker_style_t  # noqa
from matplotlib.patches import Polygon as polygon_t  # noqa
from matplotlib.pyplot import Axes as backend_frame_2d_t  # noqa
from matplotlib.pyplot import Figure as backend_figure_t  # noqa
from matplotlib.pyplot import figure as NewBackendFigure  # noqa
from mpl_toolkits.mplot3d import Axes3D as backend_frame_3d_t

from babelplot.backend.specification.implemented import backend_e
from babelplot.backend.specification.plot import UNAVAILABLE_for_this_DIM, plot_e
from babelplot.brick.log import LOGGER
from babelplot.type.base import backend_element_h, backend_plot_h
from babelplot.type.dimension import dim_e
from babelplot.type.figure import figure_t as base_figure_t
from babelplot.type.frame import frame_t as base_frame_t
from babelplot.type.plot import plot_t as base_plot_t


NAME = backend_e.MATPLOTLIB.value


array_t = nmpy.ndarray
backend_frame_h = Union[backend_frame_2d_t, backend_frame_3d_t]


def _NewFrame(
    figure: backend_figure_t,
    _: int,
    __: int,
    *args,
    title: str = None,
    dim: dim_e = dim_e.XY,
    **kwargs,
) -> backend_frame_h:
    """"""
    if dim is dim_e.XY:
        output = figure.subplots(*args, **kwargs)
    elif dim is dim_e.XYZ:
        # See note below
        output = backend_frame_3d_t(figure, *args, auto_add_to_figure=False, **kwargs)
        figure.add_axes(output)
    else:
        raise NotImplementedError(f"{dim}: Dimension management not implemented yet")
    if title is not None:
        output.set_title(title)

    return output


def _NewPlot(
    frame: frame_t,
    type_: Union[str, plot_e, type(backend_plot_h)],
    plot_function: Optional[Callable],
    *args,
    title: str = None,  # /!\ If _, then it is swallowed by kwargs!
    **kwargs,
) -> tuple[Any, Callable]:
    """"""
    if plot_function is None:
        # Next, priority is given to 2-D plots... which might be a problem if a 2-D and 3-D frame have plot types with the
        # same name. For example, scatter in 2-D and 3-D.
        if hasattr(backend_frame_2d_t, type_):
            plot_function = getattr(backend_frame_2d_t, type_)
        elif hasattr(backend_frame_3d_t, type_):
            plot_function = getattr(backend_frame_3d_t, type_)
        else:
            LOGGER.error(f"{type_}: Unknown {NAME} graph object.")

    output = plot_function(frame.backend, *args, **kwargs)

    return output, plot_function


def _DefaultProperties(type_: Callable, /) -> dict[str, Any]:
    """"""
    name = type_.__name__
    properties = mlpl.rcParams.find_all(f"^{name}\\.")

    return {_key.replace(f"{name}.", ""): _vle for _key, _vle in properties.items()}


def _SetProperty(element: backend_element_h, name: str, value: Any, /) -> None:
    """"""
    if name == "marker":
        new_marker = marker_style_t(value)
        element.set_paths((new_marker.get_path(),))
    else:
        property_ = {name: value}
        try:
            pypl.setp(element, **property_)
        except AttributeError:
            LOGGER.warning(
                f'Property "{name}": Invalid property for element of type "{type(element).__name__}"'
            )


def _Property(element: backend_element_h, name: str, /) -> Any:
    """"""
    try:
        output = pypl.getp(element, property=name)
    except AttributeError:
        output = None
        LOGGER.warning(
            f'Property "{name}": Invalid property for element of type "{type(element).__name__}"'
        )

    return output


def _ShowPreparation(
    figure: backend_figure_t,
    shape: List[int],
    frames: List[frame_t],
    locations: List[Tuple[int, int]],
    /,
) -> None:
    """"""
    if frames.__len__() < 2:
        return

    grid_spec = grid_spec_t(*shape, figure=figure)
    bottoms, tops, lefts, rights = grid_spec.get_grid_positions(figure)

    for frame, (row, col) in zip(frames, locations):
        left, bottom, width, height = (
            lefts[col],
            bottoms[row],
            rights[col] - lefts[col],
            tops[row] - bottoms[row],
        )
        frame.backend.set_position((left, bottom, width, height))


def _Show(
    figure: backend_figure_t,
    /,
) -> None:
    """"""
    figure.show()

    event_manager = figure.canvas
    event_manager.mpl_connect("close_event", lambda _: event_manager.stop_event_loop())
    event_manager.start_event_loop()


# noinspection PyTypeChecker
plot_t: base_plot_t = type(
    "plot_t",
    (base_plot_t,),
    {
        "BackendDefaultProperties": staticmethod(_DefaultProperties),
        "BackendSetProperty": staticmethod(_SetProperty),
        "BackendProperty": staticmethod(_Property),
    },
)
# noinspection PyTypeChecker
frame_t: base_frame_t = type(
    "frame_t",
    (base_frame_t,),
    {
        "plot_class": plot_t,
        "NewBackendPlot": _NewPlot,
        "BackendSetProperty": staticmethod(_SetProperty),
        "BackendProperty": staticmethod(_Property),
    },
)
# noinspection PyTypeChecker
figure_t: base_figure_t = type(
    "figure_t",
    (base_figure_t,),
    {
        "frame_class": frame_t,
        "NewBackendFigure": staticmethod(NewBackendFigure),
        "NewBackendFrame": staticmethod(_NewFrame),
        "BackendShowPreparation": staticmethod(_ShowPreparation),
        "BackendShow": staticmethod(_Show),
        "BackendSetProperty": staticmethod(_SetProperty),
        "BackendProperty": staticmethod(_Property),
    },
)


def _Polygon(
    frame: backend_frame_2d_t, xs: array_t, ys: array_t, *_, **kwargs
) -> polygon_t:
    """"""
    output = polygon_t(nmpy.vstack((xs, ys)).T, **kwargs)
    frame.add_patch(output)

    return output


def _Arrows2(frame: backend_frame_2d_t, *args, **kwargs) -> backend_plot_t:
    """"""
    if args.__len__() == 2:
        u, v = args
        u = nmpy.asarray(u)
        v = nmpy.asarray(v)
        if u.ndim != 2:
            LOGGER.error(
                f"{u.ndim}/{v.ndim}: Invalid dimension(s) of arrow component(s). Expected=2 for all."
            )
        x, y = u.shape
    else:
        x, y, u, v = args
        u = nmpy.asarray(u)
        v = nmpy.asarray(v)
        if u.ndim != 1:
            LOGGER.error(
                f"{u.ndim}/{v.ndim}: Invalid dimension(s) of arrow component(s). Expected=1 for all."
            )
    if isinstance(x, int):
        x = range(x)
        y = range(y)
        x, y = nmpy.meshgrid(x, y, indexing="ij")
    if u.ndim == 1:
        x = x.ravel()
        y = y.ravel()

    return frame.quiver(x, y, u, v, **kwargs)


def _Arrows3(frame: backend_frame_3d_t, *args, **kwargs) -> backend_plot_t:
    """"""
    if args.__len__() == 3:
        u, v, w = args
        u = nmpy.asarray(u)
        v = nmpy.asarray(v)
        w = nmpy.asarray(w)
        if u.ndim != 3:
            LOGGER.error(
                f"{u.ndim}/{v.ndim}/{w.ndim}: Invalid dimension(s) of arrow component(s). Expected=3 for all."
            )
        x, y, z = u.shape
    else:
        x, y, z, u, v, w = args
        u = nmpy.asarray(u)
        v = nmpy.asarray(v)
        w = nmpy.asarray(w)
        if u.ndim != 1:
            LOGGER.error(
                f"{u.ndim}/{v.ndim}/{w.ndim}: Invalid dimension(s) of arrow component(s). Expected=1 for all."
            )
    if isinstance(x, int):
        x = range(x)
        y = range(y)
        z = range(z)
        x, y, z = nmpy.meshgrid(x, y, z, indexing="ij")
    if u.ndim == 1:
        x = x.ravel()
        y = y.ravel()
        z = z.ravel()

    if ((color := kwargs.get("color")) is not None) and isinstance(color, nmpy.ndarray):
        kwargs = kwargs.copy()
        kwargs["color"] = nmpy.vstack((color, nmpy.repeat(color, 2, axis=0)))

    return frame.quiver(x, y, z, u, v, w, **kwargs)


def _ElevationSurface(frame: backend_frame_2d_t, *args, **kwargs) -> backend_plot_t:
    """"""
    if args.__len__() == 1:
        elevation = args[0]
        x, y = nmpy.meshgrid(
            range(elevation.shape[0]), range(elevation.shape[1]), indexing="ij"
        )
    else:
        x, y, elevation = args

    return frame.plot_surface(x, y, elevation, **kwargs)


def _Isocontour(frame: backend_frame_2d_t, *args, **kwargs) -> backend_plot_t:
    """"""
    if args.__len__() == 2:
        values, value = args
        output = frame.contour(values, (value,), **kwargs)
    else:
        x, y, values, value = args
        output = frame.contour(x, y, values, (value,), **kwargs)
    if not frame.yaxis_inverted():
        frame.invert_yaxis()
        frame.xaxis.tick_top()

    return output


def _Isosurface(frame: backend_frame_2d_t, *args, **kwargs) -> backend_plot_t:
    """"""
    if "step_size" in kwargs:
        mc_kwargs = {"step_size": kwargs["step_size"]}
        kwargs = kwargs.copy()
        del kwargs["step_size"]
    else:
        mc_kwargs = {}

    vertices, triangles, *_ = msre.marching_cubes(*args, **mc_kwargs)

    return _Mesh(frame, triangles, vertices, **kwargs)


def _Mesh(
    frame: backend_frame_2d_t, triangles: array_t, vertices: array_t, **kwargs
) -> backend_plot_t:
    """"""
    return frame.plot_trisurf(
        vertices[:, 0], vertices[:, 1], triangles, vertices[:, 2], **kwargs
    )


def _BarH(frame: backend_frame_2d_t, *args, **kwargs) -> backend_plot_t:
    """"""
    if args.__len__() == 1:
        counts = args[0]
        positions = range(counts.__len__())
    else:
        positions, counts = args

    return frame.barh(positions, counts, **kwargs)


def _BarV(frame: backend_frame_2d_t, *args, **kwargs) -> backend_plot_t:
    """"""
    if args.__len__() == 1:
        counts = args[0]
        positions = range(counts.__len__())
    else:
        positions, counts = args

    return frame.bar(positions, counts, **kwargs)


def _Bar3(frame: backend_frame_2d_t, *args, **kwargs) -> backend_plot_t:
    """"""
    if args.__len__() == 1:
        counts = nmpy.asarray(args[0])
        if counts.ndim != 2:
            LOGGER.error(
                f"{counts.ndim}: Invalid dimension of counts. Expected=2."
            )
        x, y = counts.shape
    else:
        x, y, counts = args
        counts = nmpy.asarray(counts)
        if counts.ndim != 1:
            LOGGER.error(
                f"{counts.ndim}: Invalid dimension of counts. Expected=1."
            )
    if isinstance(x, int):
        x = range(x)
        y = range(y)
        x, y = nmpy.meshgrid(x, y, indexing="ij")
    if counts.ndim == 1:
        x = x.ravel()
        y = y.ravel()

    width = kwargs.get("width", 0.8)
    depth = kwargs.get("depth", 0.8)
    offset = kwargs.get("offset", 0.0)
    kwargs = {
        _key: _vle
        for _key, _vle in kwargs.items()
        if _key not in ("width", "depth", "offset")
    }

    return frame.bar3d(x, y, offset, width, depth, counts, **kwargs)


PLOTS = {
    plot_e.SCATTER: (
        UNAVAILABLE_for_this_DIM,
        backend_frame_2d_t.scatter,
        backend_frame_3d_t.scatter,
    ),
    plot_e.POLYLINE: (
        UNAVAILABLE_for_this_DIM,
        backend_frame_2d_t.plot,
        backend_frame_3d_t.plot,
    ),
    plot_e.POLYGON: (
        UNAVAILABLE_for_this_DIM,
        _Polygon,
        UNAVAILABLE_for_this_DIM,
    ),
    plot_e.ARROWS: (
        UNAVAILABLE_for_this_DIM,
        _Arrows2,
        _Arrows3,
    ),
    plot_e.ELEVATION: (
        UNAVAILABLE_for_this_DIM,
        UNAVAILABLE_for_this_DIM,
        _ElevationSurface,
    ),
    plot_e.ISOSET: (
        UNAVAILABLE_for_this_DIM,
        _Isocontour,
        _Isosurface,
    ),
    plot_e.MESH: (
        UNAVAILABLE_for_this_DIM,
        UNAVAILABLE_for_this_DIM,
        _Mesh,
    ),
    plot_e.BARH: (
        UNAVAILABLE_for_this_DIM,
        _BarH,
        UNAVAILABLE_for_this_DIM,
    ),
    plot_e.BARV: (
        UNAVAILABLE_for_this_DIM,
        _BarV,
        UNAVAILABLE_for_this_DIM,
    ),
    plot_e.BAR3: (
        UNAVAILABLE_for_this_DIM,
        UNAVAILABLE_for_this_DIM,
        _Bar3,
    ),
    plot_e.PIE: (
        UNAVAILABLE_for_this_DIM,
        backend_frame_2d_t.pie,
        UNAVAILABLE_for_this_DIM,
    ),
    plot_e.IMAGE: (
        UNAVAILABLE_for_this_DIM,
        backend_frame_2d_t.matshow,
        UNAVAILABLE_for_this_DIM,
    ),
}


TRANSLATIONS = {
    "color": "c",
    "color_edge": "edgecolors",
    "color_face": "facecolors",
    "color_max": "vmax",
    "color_min": "vmin",
    "color_scaling": "norm",
    "depth_shade": "depthshade",
    "plot_non_finite": "plotnonfinite",
    "size": "s",
    "width_edge": "linewidths",
    (_Arrows2, "color"): "color",
    (_Arrows3, "color"): "color",
    (_Bar3, "color"): "color",
    (_BarH, "color"): "color",
    (_BarH, "offset"): "left",
    (_BarV, "color"): "color",
    (_BarV, "offset"): "bottom",
    (_ElevationSurface, "color_face"): "color",
    (_Isocontour, "color"): "colors",
    (_Isosurface, "color_face"): "color",
    (_Mesh, "color_face"): "color",
    (_Polygon, "color_edge"): "edgecolor",
    (_Polygon, "color_face"): "facecolor",
    (backend_frame_2d_t.pie, "color"): "colors",
    (backend_frame_2d_t.quiver, "color"): "color",
    (backend_frame_3d_t.quiver, "color"): "colors",
    (backend_frame_3d_t.scatter, 2): "zs",
}


# From: https://matplotlib.org/stable/api/prev_api_changes/api_changes_3.4.0.html
# *Axes3D automatically adding itself to Figure is deprecated*
#
# New Axes3D objects previously added themselves to figures when they were created, unlike all other Axes
# classes, which lead to them being added twice if fig.add_subplot(111, projection='3d') was called.
#
# This behavior is now deprecated and will warn. The new keyword argument auto_add_to_figure controls the
# behavior and can be used to suppress the warning. The default value will change to False in Matplotlib 3.5,
# and any non-False value will be an error in Matplotlib 3.6.
#
# In the future, Axes3D will need to be explicitly added to the figure
#
# fig = Figure()
# ax = Axes3d(fig)
# fig.add_axes(ax)
#
# as needs to be done for other axes.Axes sub-classes. Or, a 3D projection can be made via:
#
# fig.add_subplot(projection='3d')
