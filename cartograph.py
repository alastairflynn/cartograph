from os import mkdir
from os.path import join
import numpy as np
import matplotlib as mpl
# mpl.use('agg')
from projection import *

class Map():
    def __init__(self):
        self.areas = []
        self.ways = []
        self.names = []
        self.nodes = []

        self.bounds = np.zeros((2,2))
        self.bounds[:,0] = self.projection(-85.0511, -180.0)
        self.bounds[:,1] = self.projection(85.0511, 180.0)
        self.latlon_bounds = np.array([[85.0511, -85.0511], [-180.0, 180.0]])

        self.elevation = None
        self.elevation_style = None

        self.background_color = 'white'

        self.figure = None
        self.axes = None

    def bound_by_box(self, bottom, top, left, right):
        self.bounds[:,0] = self.projection(bottom, left)
        self.bounds[:,1] = self.projection(top, right)
        self.latlon_bounds = np.array([[top, bottom], [left, right]])

    def bound_by_osm_tiles(self, zoom, *args):
        min_lat = 85.0511
        max_lat = -85.0511
        min_lon = 180.0
        max_lon = 180.0
        for lon, lat in args:
            min_lat = min(min_lat, lat)
            max_lat = max(max_lat, lat)
            min_lon = min(min_lon, lon)
            max_lon = max(max_lon, lon)
        min_x, min_y = deg2num(max_lat, min_lon, zoom)
        max_x, max_y = deg2num(min_lat, max_lon, zoom)
        top, left = num2deg(min_x, min_y, zoom)
        bottom, right = num2deg(max_x+1, max_y+1, zoom)
        self.bound_by_box(self, bottom, top, left, right)

    def projection(self, lat, lon):
        return mercator(lat, lon)

    def add_area(self, boundary, style):
        area = Area(np.array(mercator(boundary[0], boundary[1])), style)
        if area.is_inbounds(self.bounds):
            self.areas.append(area)

    def add_way(self, vertices, style):
        way = Way(np.array(mercator(vertices[0], vertices[1])), style)
        if way.is_inbounds(self.bounds):
            self.ways.append(way)

    def add_name(self, label, location, style):
        name = Name(label, np.array(mercator(location[0], location[1])), style)
        if name.is_inbounds(self.bounds):
            self.names.append(name)

    def add_node(self, location, style):
        node = Node(np.array(mercator(location[0], location[1])), style)
        if node.is_inbounds(self.bounds):
            self.nodes.append(node)

    def add_elevation(self, elevation_data, elevation_style):
        self.elevation = elevation_data
        self.elevation_style = elevation_style

    def set_background_color(self, background_color):
        self.background_color = background_color

    def plot(self):
        if self.elevation is not None:
            ls = mpl.colors.LightSource(azdeg=30, altdeg=60)
            shade = ls.hillshade(elevation[2], vert_exag=1, fraction=1.0).T

            im_extent = [self.elevation[0][0,0], self.elevation[0][-1,0], self.elevation[1][0,0], self.elevation[1][0,-1]]
            self.axes.imshow(elevation[2].T, origin='lower', extent=im_extent, interpolation='bilinear', cmap=self.elevation_style.colormap, vmin=self.elevation_style.vmin, vmax=self.elevation_style.vmax, alpha=self.elevation_style.colormap_alpha)
            self.axes.imshow(shade, origin='lower', extent=im_extent, interpolation='bilinear', cmap='gray', alpha=self.elevation_style.hillshade_alpha)

        for area in self.areas:
            area.plot(self.axes)
            area.set_visible(False)

        for way in self.ways:
            way.plot(self.axes)
            way.set_visible(False)

        for node in self.nodes:
            node.plot(self.axes)
            node.set_visible(False)

        for name in self.names:
            name.plot(self.axes)
            name.set_visible(False)

    def draw_zoom_levels(self, min, max=None):
        if max is None:
            max = min + 1

        self.figure = mpl.figure.Figure(figsize=(1, 1), frameon=False)
        self.axes = self.figure.add_axes([0.0, 0.0, 1.0, 1.0], frameon=False, facecolor=self.background_color)
        self.plot()

        for zoom in range(min, max):
            if self.elevation is not None and zoom >= self.elevation_style.contour_appears_at:
                contours = self.axes.contour(elevation[0], elevation[1], elevation[2], levels=self.elevation_style.contour_levels, colors=self.elevation_style.contour_color, linewidths=self.elevation_style.contour_width)
                labels = self.axes.clabel(contours, self.elevation_style.clabel_levels, inline=1, inline_spacing=0.0, fontsize=self.elevation_style.clabel_fontsize, fmt='%0.0f', use_clabeltext=False)

            for area in self.areas:
                if zoom >= area.style.appears_at:
                    area.set_visible(True)

            for way in self.ways:
                if zoom >= way.style.appears_at:
                    way.set_visible(True)

            for node in self.nodes:
                if zoom >= node.style.appears_at:
                    node.set_visible(True)

            for name in self.names:
                if zoom >= name.style.appears_at:
                    name.set_visible(True)

            x_start, y_start = deg2num(self.latlon_bounds[0,0], self.latlon_bounds[1,0], zoom)
            x_stop, y_stop = deg2num(self.latlon_bounds[0,1], self.latlon_bounds[1,1], zoom)
            for x in range(x_start, x_stop):
                for y in range(y_start, y_stop):
                    self.draw_tile(x, y, zoom)

            if self.elevation is not None and zoom >= self.elevation_style.contour_appears_at:
                for c in contours.collections:
                    c.remove()
                for l in labels:
                    l.remove()

    def draw_tile(self, x, y, zoom, directory='tiles'):
        lat0, lon0 = num2deg(x, y, zoom)
        lat1, lon1 = num2deg(x+1, y+1, zoom)
        x0, y0 = self.projection(lat1, lon0)
        x1, y1 = self.projection(lat0, lon1)

        self.axes.xlim(x0, x1)
        self.axes.ylim(y0, y1)

        path = join(directory, '%d' % zoom)
        try:
            mkdir(path)
        except FileExistsError:
            pass

        path = join(path, '%d' % x)
        try:
            mkdir(path)
        except FileExistsError:
            pass

        path = join(path, '%d.png.tile' % y)
        bbox = mpl.transforms.Bbox(np.array([[0,0], [1,1]]))
        self.figure.savefig(path, format='png', dpi=256, bbox_inches=bbox)

    def draw_image(self, path='map.png', dpi=1024):
        width = (self.bounds[0,1] - self.bounds[0,0]) / (self.bounds[1,1] - self.bounds[1,0])
        self.figure = mpl.figure.Figure(figsize=(width, 1), frameon=False)
        self.axes = self.figure.add_axes([0.0, 0.0, 1.0, 1.0], frameon=False, facecolor=self.background_color)
        self.plot()

        contours = self.axes.contour(elevation[0], elevation[1], elevation[2], levels=self.elevation_style.contour_levels, colors=self.elevation_style.contour_color, linewidths=self.elevation_style.contour_width)
        labels = self.axes.clabel(contours, self.elevation_style.clabel_levels, inline=1, inline_spacing=0.0, fontsize=self.elevation_style.clabel_fontsize, fmt='%0.0f', use_clabeltext=False)

        for area in self.areas:
            area.set_visible(True)

        for way in self.ways:
            way.set_visible(True)

        for node in self.nodes:
            node.set_visible(True)

        for name in self.names:
            name.set_visible(True)

        self.axes.xlim(self.bounds[0,0], self.bounds[0,1])
        self.axes.ylim(self.bounds[1,0], self.bounds[1,1])

        bbox = mpl.transforms.Bbox(np.array([[0,0], [1,1]]))
        self.figure.savefig(path, dpi=dpi, bbox_inches=bbox)

class Feature():
    def __init__(self, style):
        self.style = style
        self.artists = []

    def set_visible(self, visible):
        for artist in self.artists:
            artist.set_visible(visible)

class Area(Feature):
    def __init__(self, boundary, style):
        super().__init__(style)
        self.boundary = boundary

    def is_inbounds(self, bounds):
        has_intersection = np.any(np.logical_and(np.less_equal(bounds[0,0], self.boundary[0]), np.less_equal(self.boundary[0], bounds[0,1]), np.less_equal(bounds[1,0], self.boundary[1]), np.less_equal(self.boundary[1], bounds[1,1])))
        return has_intersection

    def plot(self, axes):
        self.artists = axes.fill(boundary[0], boundary[1], clip_on=True, lw=0, color=self.style.color, fill=self.style.fill, hatch=self.style.hatch)

class Way(Feature):
    def __init__(self, vertices, style):
        super().__init__(style)
        self.vertices = vertices

    def is_inbounds(self, bounds):
        has_intersection = np.any(np.logical_and(np.less_equal(bounds[0,0], self.vertices[0]), np.less_equal(self.vertices[0], bounds[0,1]), np.less_equal(bounds[1,0], self.vertices[1]), np.less_equal(self.vertices[1], bounds[1,1])))
        return has_intersection

    def plot(self, axes):
        self.artists = axes.plot(vertices[0], vertices[1], clip_on=True, color=self.style.color, linestyle=self.style.linestyle, linewidth=self.style.linewidth, marker=self.style.markerstyle, markersize=self.style.markersize)

class Name(Feature):
    def __init__(self, name, location, style):
        super().__init__(style)
        self.name = name
        self.location = location

    def is_inbounds(self, bounds):
        return True

    def plot(self, axes):
        a = axes.text(self.location[0], self.location[1], self.name, clip_on=True, wrap=False, in_layout=False, color=self.style.color, fontsize=self.style.fontsize, fontweight=self.style.fontweight, ha='center', multialignment='center')
        self.artists = [a]

class Node(Name):
    def __init__(self, location, style):
        super().__init__(style.text, location, style)

class Style():
    def __init__(self, appears_at=0):
        self.appears_at = appears_at

    def update(self, zoom):
        pass

class AreaStyle(Style):
    def __init__(self, appears_at=0, color='black', fill=True, hatch=''):
        super().__init__(appears_at)
        self.color = color
        self.fill = fill
        self.hatch = hatch

class WayStyle(Style):
    def __init__(self, appears_at=0, color='black', linestyle='-', linewidth=1.0, markerstyle='', markersize=0):
        super().__init__(appears_at)
        self.color = color
        self.linestyle = linestyle
        self.linewidth = linewidth
        self.markerstyle = markerstyle
        self.markersize = markersize

class NameStyle(Style):
    def __init__(self, appears_at=0, color='black', fontsize=7, fontweight='normal'):
        super().__init__(appears_at)
        self.color = color
        self.fontsize = fontsize
        self.fontweight = fontweight

class NodeStyle(NameStyle):
    def __init__(self, appears_at=0, color='black', text='P', fontsize=7, fontweight='bold'):
        super().__init__(appears_at, color, fontsize, fontweight)
        self.text = text

class ElevationStyle():
    def __init__(self, colormap='gist_terrain', vmin=-3000, vmax=4700, colormap_alpha=0.4, hillshade_alpha=0.25, contour_appears_at=15, contour_levels=np.linspace(0,5000,100,endpoint=False), contour_color='black', contour_width=0.2, clabel_levelskip=2, clabel_fontsize=5):
        self.colormap = colormap
        self.vmin = vmin
        self.vmax = vmax
        self.colormap_alpha = colormap_alpha
        self.hillshade_alpha = hillshade_alpha
        self.contour_appears_at = contour_appears_at
        self.contour_levels = contour_levels
        self.contour_color = contour_color
        self.contour_width = contour_width
        self.clabel_levels = self.contour_levels[::clabel_levelskip]
        self.clabel_fontsize = clabel_fontsize
