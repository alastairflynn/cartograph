import numpy as np
from scipy.interpolate import griddata
import matplotlib as mpl

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

class Elevation(Feature):
    def __init__(self, data, style):
        super().__init__(style)
        self.data = data
        self.grid_x = None
        self.grid_y = None
        self.ele = None
        self.im_extent = None

    def generate_elevation_grid(self, bounds, resolution=(100, 100), padding=1):
        mask0 = np.logical_and(bounds[0,0]-padding <= self.data[:,0], self.data[:,0] <= bounds[0,1]+padding)
        mask1 = np.logical_and(bounds[1,0]-padding <= self.data[:,1], self.data[:,1] <= bounds[1,1]+padding)
        mask = np.logical_and(mask0, mask1)

        self.grid_x, self.grid_y = np.mgrid[x0:x1:resolution[0]*1j, y0:y1:resolution[1]*1j]
        self.ele = griddata(self.data[mask][:,0:2], self.data[mask][:,2], (self.grid_x, self.grid_y), method='cubic')
        self.im_extent = [self.grid_x[0,0], self.grid_x[-1,0], self.grid_y[0,0], self.grid_y[0,-1]]

    def draw_background_image(self, axes):
        if self.ele is None:
            raise TypeError('Elevation grid is not initialised, call generate_elevation_grid before this method')
        else:
            axes.imshow(self.ele.T, origin='lower', extent=self.im_extent, interpolation='bilinear', cmap=self.style.colormap, vmin=self.style.vmin, vmax=self.style.vmax, alpha=self.style.colormap_alpha)

    def draw_hillshade(self, axes):
        if self.ele is None:
            raise TypeError('Elevation grid is not initialised, call generate_elevation_grid before this method')
        else:
            ls = mpl.colors.LightSource(azdeg=30, altdeg=60)
            shade = ls.hillshade(self.ele, vert_exag=1, fraction=1.0).T
            axes.imshow(shade, origin='lower', extent=self.im_extent, interpolation='bilinear', cmap='gray', alpha=self.style.hillshade_alpha)

    def plot_contours(self, axes):
        if self.ele is None:
            raise TypeError('Elevation grid is not initialised, call generate_elevation_grid before this method')
        else:
            self.contours = axes.contour(self.grid_x, self.grid_y, self.ele, levels=self.style.contour_levels, colors=self.style.contour_color, linewidths=self.style.contour_width)
            self.labels = axes.clabel(contours, self.style.clabel_levels, inline=1, inline_spacing=0.0, fontsize=self.style.clabel_fontsize, fmt='%0.0f', use_clabeltext=False)
            self.artists = self.contours.collections + self.labels

    def remove_contours(self):
        for c in self.contours.collections:
            c.remove()
        for l in self.labels:
            l.remove()
