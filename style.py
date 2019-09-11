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
