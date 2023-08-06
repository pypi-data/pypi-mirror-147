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

import itertools as ittl

import numpy as nmpy
import scipy as scpy

from babelplot import NewBabelPlotFigure, ShowAllFigures


nmpy.random.seed(0)

# --- Scatter plots
n_scatter_points = 100
scatter_x = nmpy.random.random(n_scatter_points)
scatter_y = nmpy.random.random(n_scatter_points)
scatter_z = nmpy.random.random(n_scatter_points)
sizes = 100.0 * nmpy.random.random(n_scatter_points)
colors = nmpy.random.random((n_scatter_points, 3))

figure = NewBabelPlotFigure()

frame = figure.AddFrame(title="SCATTER PLOT 2-D")
frame.AddPlot("scatter", scatter_x, scatter_y, size=sizes, color=colors, alpha=0.5)

frame = figure.AddFrame(title="SCATTER PLOT 3-D", dim="xyz", col=1)
frame.AddPlot(
    "scatter", scatter_x, scatter_y, scatter_z, size=sizes, color=colors, alpha=0.5
)

# --- Line plots
n_vertices = 5
polyline_x = scatter_x[:n_vertices]
polyline_y = scatter_y[:n_vertices]
polyline_z = scatter_z[:n_vertices]
polygon_x = scatter_x[:n_vertices]
polygon_y = scatter_y[:n_vertices]

figure = NewBabelPlotFigure()

frame = figure.AddFrame(title="POLYLINE 2-D")
frame.AddPlot("polyline", polyline_x, polyline_y, color="r")

frame = figure.AddFrame(title="POLYLINE 3-D", dim="xyz", col=1)
frame.AddPlot("polyline", polyline_x, polyline_y, polyline_z, color="r")

frame = figure.AddFrame(title="POLYGON", col=2)
frame.AddPlot("polygon", polygon_x, polygon_y, color_face="b", color_edge="r")

# --- Arrow fields
n_arrows = 80
arrows_x = scatter_x[:n_arrows] * nmpy.random.choice((-1.0, 1.0), size=n_arrows)
arrows_y = scatter_y[:n_arrows] * nmpy.random.choice((-1.0, 1.0), size=n_arrows)
arrows_z = scatter_z[:n_arrows] * nmpy.random.choice((-1.0, 1.0), size=n_arrows)
arrow_colors = colors[:n_arrows, :]

figure = NewBabelPlotFigure()

frame = figure.AddFrame(title="ARROW FIELD 2-D")
frame.AddPlot("arrows", 8, 10, arrows_x, arrows_y, color=arrow_colors)

frame = figure.AddFrame(title="ARROW FIELD 3-D", dim="xyz", col=1)
frame.AddPlot("arrows", 4, 4, 5, arrows_x, arrows_y, arrows_z, color=arrow_colors)

# --- Image-based plots
side = 100
volume = nmpy.random.random((side + 40, side + 20, side))
elevation = volume[:, :, 0]
elevation = scpy.ndimage.gaussian_filter(elevation, 3)

figure = NewBabelPlotFigure()

frame = figure.AddFrame(title="IMAGE")
frame.AddPlot("image", elevation, cmap="jet")

frame = figure.AddFrame(title="ELEVATION", dim="xyz", col=1)
frame.AddPlot(
    "elevation", elevation, width_edge=0.5, color_face=(0.0, 1.0, 1.0), color_edge="b"
)

frame = figure.AddFrame(title="ISOCONTOUR", col=2)
frame.AddPlot("isoset", elevation, 0.85 * nmpy.amax(elevation), color="r")

frame = figure.AddFrame(title="ISOSURFACE", dim="xyz", col=3)
frame.AddPlot(
    "isoset",
    volume,
    0.85 * nmpy.amax(volume),
    step_size=5,
    width_edge=0.5,
    color_face="r",
    color_edge="b",
)

# --- Mesh plot
triangles = tuple(ittl.combinations(range(4), 3))
vertices = []
for x in (-1.0, 1.0):
    vertices.append([x, 0.0, -1.0 / nmpy.sqrt(2.0)])
for y in (-1.0, 1.0):
    vertices.append([0.0, y, 1.0 / nmpy.sqrt(2.0)])
vertices = nmpy.array(vertices)

figure = NewBabelPlotFigure()

frame = figure.AddFrame(title="MESH", dim="xyz")
frame.AddPlot(
    "mesh", triangles, vertices, width_edge=0.5, color_face="r", color_edge="b"
)

# --- Count-based plots
n_counts = 12
counts = 10.0 * scatter_x[:n_counts]
bar_colors = colors[:n_counts, :]

figure = NewBabelPlotFigure()

frame = figure.AddFrame(title="BAR H")
frame.AddPlot("barh", counts, color="r")

frame = figure.AddFrame(title="BAR V", col=1)
frame.AddPlot("barv", range(1, counts.size + 1), counts, color="g")

frame = figure.AddFrame(title="PIE", col=2)
frame.AddPlot("pie", counts, color=bar_colors)

frame = figure.AddFrame(title="BAR 3", dim="xyz", col=3)
frame.AddPlot("bar3", 3, 4, counts, color=bar_colors)


ShowAllFigures()
