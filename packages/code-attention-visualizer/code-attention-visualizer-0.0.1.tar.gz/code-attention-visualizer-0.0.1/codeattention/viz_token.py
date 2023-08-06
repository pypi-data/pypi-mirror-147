"""Class to represent the Token objects to highlight."""

from matplotlib import colors


class FlexibleVisualToken(object):

    def __init__(self, index_id, text, x, y, width, height, clicked):
        self.text = text
        if (index_id == ""):
            index_id = -1
        self.index_id = int(index_id)
        self.x = int(x)
        self.y = int(y)
        self.width = int(width)
        self.height = int(height)
        self.attention = 0
        self.clicked = clicked

    def draw_PIL(self, drw, global_attention=0,
                 named_color='lime'):
        """Draw the patch on the plot."""
        alpha = 0.1
        if global_attention != 0:
            alpha = int((float(self.attention) / global_attention) * 255)
        if self.attention == 0:
            alpha = 0
        color_rgb = list(colors.to_rgb(named_color))
        color_rgb = [int(c * 255) for c in color_rgb]
        color_rgba = color_rgb + [alpha]
        color_rgba = tuple(color_rgba)
        border = None
        if self.clicked:
            border = 'red'
        rect = \
            drw.rectangle([
                self.x,
                self.y,
                self.x + self.width,
                self.y + self.height],
                outline=border,
                width=2,
                fill=color_rgba)

    def add_attention(self, attention):
        self.attention = attention

    def __repr__(self):
        return 'x:' + str(self.x).zfill(3) \
                + ' - y:' + str(self.y).zfill(3) \
                + ' - width:' + str(self.width).zfill(4) \
                + ' - height:' + str(self.height).zfill(4) \
                + ' - |' + self.text + '|'
