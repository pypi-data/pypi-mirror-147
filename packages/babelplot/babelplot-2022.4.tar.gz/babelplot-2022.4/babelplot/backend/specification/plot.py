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

from enum import Enum as enum_t, unique
from operator import itemgetter as ItemAt
from typing import Any, Callable, Dict, Optional, Sequence, Tuple, Union

from babelplot.brick.enum import EnumMembers, EnumValues
from babelplot.brick.log import LOGGER


UNAVAILABLE_for_this_DIM = None


positional_to_keyword_h = Tuple[Callable, int]
keyword_to_positional_h = Tuple[Callable, str]
arguments_translations_h = dict[
    keyword_to_positional_h | positional_to_keyword_h | str, str | int
]


@unique
class plot_e(enum_t):
    """
    Available plot types.

    The value of each enum member is the plot name that can be used in place of the enum member in some
    function/method calls.
    """

    SCATTER = "scatter"
    POLYLINE = "polyline"
    POLYLINES = "polylines"
    POLYGON = "polygon"
    POLYGONS = "polygons"
    ARROWS = "arrows"
    ELEVATION = "elevation"
    ISOSET = "isoset"
    MESH = "mesh"
    PMESH = "pmesh"
    BARH = "barh"
    BARV = "barv"
    BAR3 = "bar3"
    PIE = "pie"
    IMAGE = "image"

    @classmethod
    def PlotsIssues(cls, plots: dict, /) -> Optional[Sequence[str]]:
        """"""
        issues = []

        for key, value in plots.items():
            if isinstance(key, cls):
                if isinstance(value, tuple):
                    how_defined = PLOT_DESCRIPTION[key]
                    if (n_dimensions := value.__len__()) == (
                        n_required := how_defined[2].__len__()
                    ):
                        for d_idx, for_dim in enumerate(value):
                            if isinstance(
                                for_dim, (type(UNAVAILABLE_for_this_DIM), Callable)
                            ):
                                pass
                            else:
                                issues.append(
                                    f"{key}/{for_dim}: Invalid plot function for dim {how_defined[2][d_idx]}. "
                                    f"Expected=UNAVAILABLE_for_this_DIM or Callable."
                                )
                    else:
                        issues.append(
                            f"{key}/{n_dimensions}: Invalid number of possible dimensions. Expected={n_required}."
                        )
                else:
                    issues.append(
                        f"{key}/{type(value).__name__}: Invalid plot record type. Expected=tuple."
                    )
            else:
                issues.append(
                    f"{key}/{type(key).__name__}: Invalid plot type. Expected={cls.__name__}."
                )

        missing = set(cls.__members__.values()).difference(plots.keys())
        if missing.__len__() > 0:
            missing = str(sorted(_elm.name for _elm in missing))[1:-1].replace("'", "")
            issues.append(f"Missing plot type(s): {missing}")

        if issues.__len__() > 0:
            return issues

        return None

    @classmethod
    def FormattedPlots(cls, /, *, with_descriptions: bool = True) -> str:
        """"""
        members = EnumMembers(cls)
        as_members = str(members)[1:-1].replace("'", "")
        as_names = str(KNOWN_PLOT_TYPES)[1:-1].replace("'", "")

        if with_descriptions:
            descriptions = []
            for member in members:
                description = PLOT_DESCRIPTION[
                    cls[member[(cls.__name__.__len__() + 1) :]]
                ]
                dimensions = ", ".join(str(_dim) for _dim in description[2])
                descriptions.append(
                    f"{member}: {description[0]}\n{description[1]}\nDim(s): {dimensions}"
                )
            descriptions = "\n\n--- Descriptions:\n" + "\n\n".join(descriptions)
        else:
            descriptions = ""

        output = (
            f"As {cls.__name__} members: {as_members}\n"
            f"As names: {as_names}{descriptions}"
        )

        return output

    @staticmethod
    def IsValid(name: str, /) -> bool:
        """"""
        return name in KNOWN_PLOT_TYPES

    @classmethod
    def NewFromName(cls, name: str, /) -> plot_e:
        """"""
        if name in KNOWN_PLOT_TYPES:
            return cls(name)

        LOGGER.error(f"{name}: Invalid plot type. Expected={KNOWN_PLOT_TYPES}.")


KNOWN_PLOT_TYPES = EnumValues(plot_e)


backend_plots_per_type_h = Tuple[Union[type(UNAVAILABLE_for_this_DIM), Callable], ...]
backend_plots_h = Dict[plot_e, backend_plots_per_type_h]


_NUMPY_ARRAY_PAGE = (
    "https://numpy.org/doc/stable/reference/generated/numpy.ndarray.html"
)


# The second element of the description is a tuple of the dimensions the plot type is available in
PLOT_DESCRIPTION = {
    # Brief description
    # Description
    # Valid frame dimension(s)
    plot_e.SCATTER: (
        "Set of Points",
        "A set of points X, (X, Y), or (X, Y, Z) depending on the dimension. They are plotted using a so-called "
        "marker.\n"
        "Required arguments: X coordinates, Y coordinates, Z coordinates (depending on the dimension).",
        (1, 2, 3),
    ),
    plot_e.POLYLINE: (
        "Polygonal Chain",
        "A polygonal chain is a connected series of line segments specified by a sequence of points enumerated "
        "consecutively called vertices [https://en.wikipedia.org/wiki/Polygonal_chain]. "
        "It typically describes an open path. It can have markers like a scatter plot.\n"
        "A polygonal chain may also be called a polygonal curve, polygonal path, polyline, piecewise linear curve, "
        "or broken line.\n"
        "Required arguments: X coordinates, Y coordinates, Z coordinates (depending on the dimension).",
        (2, 3),
    ),
    plot_e.POLYLINES: (
        "Set of Polygonal Chains",
        'See "Polygonal Chain". Use case: some plotting libraries may deal with sets more efficiently than looping '
        "over the chains in Python.\n"
        "Required arguments: List of X coordinates, list of Y coordinates, list of Z coordinates (depending on the "
        "dimension).",
        (2, 3),
    ),
    plot_e.POLYGON: (
        "Polygon",
        "A polygon is a closed polygonal chain represented as a sequence of vertices without repetition of the first "
        'one at the end of the sequence. See "Polygonal Chain".\n'
        "Required arguments: X coordinates and Y coordinates.",
        (2,),
    ),
    plot_e.POLYGONS: (
        "Set of Polygons",
        'See "Polygon". Use case: some plotting libraries may deal with sets more efficiently than looping over the '
        "polygons in Python.\n"
        "Required arguments: List of X coordinates and list of Y coordinates.",
        (2,),
    ),
    plot_e.ARROWS: (
        "Set of Arrows",
        "A set, or field, of arrows.\n"
        "Required arguments: U arrow components, V arrow components, W arrow components (depending on the dimension).\n"
        "Optional arguments: X coordinates, Y coordinates, Z coordinates passed as first, second and third positional "
        "arguments (depending on the dimension).",
        (2, 3),
    ),
    plot_e.ELEVATION: (
        "Elevation Surface",
        'An elevation surface is defined as the set of points (X,Y,Z) where Z is the (unique) "elevation" computed by '
        "a function f for each planar coordinates (X,Y): Z = f(X,Y).\n"
        "Required argument: An elevation map Z.\n"
        'Optional arguments: X and Y passed as keyword arguments "x" and "y" to specify a non-regular grid.',
        (3,),
    ),
    plot_e.ISOSET: (
        "Isoset",
        f"An isoset, or level set, is the set of points at which a function f takes a given value (or level) V: "
        f"{{point | f(point)=V}} where point=X,Y in 2 dimensions or X,Y,Z in 3 dimensions. In 2 dimensions, an isoset "
        f"is also called an isocontour. In 3 dimensions, it is also called an isosurface.\n"
        f"Required arguments: A 2- or 3-dimensional Numpy array [{_NUMPY_ARRAY_PAGE}] with the values f(point) for "
        f"each point in a domain, and V.\n"
        f'Optional arguments: X, Y, and Z (depending on the dimension) passed as keyword arguments "x", "y", and '
        f'"z" to specify a non-regular grid.',
        (2, 3),
    ),
    plot_e.MESH: (
        "Triangular Mesh",
        f"A triangular mesh is a 2-dimensional surface in the 3-dimensional space. It is composed of triangles T "
        f"defined by vertices V.\n"
        f"Required arguments: Some triangles as an Nx3-Numpy array [{_NUMPY_ARRAY_PAGE}] of vertex indices (between "
        f"zero and M-1), and the vertices coordinates as an Mx3-Numpy array.",
        (3,),
    ),
    plot_e.PMESH: (
        "Polygonal Mesh",
        'A mesh with polygonal faces instead of triangular ones. See "Triangular Mesh". Use case: probably rare.',
        (3,),
    ),
    plot_e.BARH: (
        "Horizontal Bar Plot",
        'See "Vertical Bar Plot".\n'
        "Required argument: bar widths W\n"
        "Optional arguments: Y coordinates of the bars passed as first positional argument and width offsets passed as "
        '"offset".',
        (2,),
    ),
    plot_e.BARV: (
        "Vertical Bar Plot",
        "A vertical bar plot is equivalent to a 2-dimensional histogram.\n"
        "Required argument: bar heights H\n"
        "Optional arguments: X coordinates of the bars passed as first positional argument and height offsets passed "
        'as "offset".',
        (2,),
    ),
    plot_e.BAR3: (
        "Three-dimensional Bar Plot",
        "A three-dimensional bar plot is equivalent to a 3-dimensional histogram.\n"
        "Required argument: bar heights H.\n"
        "Optional arguments: X coordinates and Y coordinates of the bars passed as first and second positional "
        'arguments, width(s) and depth(s) of bars passed as "width" and "depth", and height offsets passed as '
        '"offset".',
        (3,),
    ),
    plot_e.PIE: (
        "Pie Plot",
        "A pie plot, or pie chart or circle chart, is a circular statistical graphic which is divided into slices to "
        "illustrate proportions. The angle of each slice is proportional to the quantity it represents "
        "[https://en.wikipedia.org/wiki/Pie_chart].\n"
        "Required argument: Proportions or quantities.",
        (2,),
    ),
    plot_e.IMAGE: (
        "Two-dimensional Image",
        "A grayscale or color two-dimensional image, with or without alpha channel. When plotting a 2-dimensional "
        "image in a 3-dimensional frame, a plotting plane specification is required.\n"
        "Required argument: An image.\n"
        'Optional argument: An axis-aligned plane position passed as a keyword argument "x", "y", or "z".',
        (2, 3),
    ),
}


def TranslatedArguments(
    plot_function: Optional[Callable],
    args: Sequence[Any],
    kwargs: Dict[str, Any],
    translations: Optional[
        Dict[
            Union[keyword_to_positional_h, positional_to_keyword_h, str],
            Union[str, int],
        ]
    ],
    /,
) -> Tuple[Sequence[Any], Dict[str, Any]]:
    """"""
    if (translations is None) or (translations.__len__() == 0):
        return args, kwargs

    output_1 = []
    output_2 = {}

    for idx, value in enumerate(args):
        if (key := translations.get((plot_function, idx))) is None:
            output_1.append(value)
        else:
            output_2[key] = value

    from_kwargs_to_args = []
    for key, value in kwargs.items():
        # It is important to search for specific translation first (i.e. (plot_function, key), as opposed to key alone)
        if (translation := translations.get((plot_function, key))) is None:
            output_2[translations.get(key, key)] = value
        elif isinstance(translation, int):
            from_kwargs_to_args.append((value, translation))
        else:
            output_2[translation] = value
    for value, idx in sorted(from_kwargs_to_args, key=ItemAt(1)):
        output_1.insert(idx, value)

    return output_1, output_2
