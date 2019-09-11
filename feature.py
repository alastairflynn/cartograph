import numpy as np

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
