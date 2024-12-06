import numpy as np
from PIL import Image as _Image
from PIL import ImageDraw as _ImageDraw

from pynsn import Colour, Dot, Rectangle, AbstractShape
from pynsn.image._base import cartesian2image_coordinates as _c2i_coord


class Line(object):
    """to draw lines in the test pictures"""

    def __init__(self, xy_a, xy_b, colour):
        self.xy_a = xy_a
        self.xy_b = xy_b
        self.colour = Colour(colour)


def _draw_shape(img, shape: AbstractShape, scaling_factor=1):
    if isinstance(shape, Line):
        xy_a = _c2i_coord(np.asarray(shape.xy_a), img.size).tolist()
        xy_b = _c2i_coord(np.asarray(shape.xy_b), img.size).tolist()
        xy_a.extend(xy_b)
        _ImageDraw.Draw(img).line(xy_a, fill=shape.colour.value, width=2)
        return
    shape = shape.copy()
    shape.xy = _c2i_coord(np.array(shape.xy) * scaling_factor, img.size)
    if isinstance(shape, Dot):
        r = (shape.diameter * scaling_factor) / 2
        x, y = shape.xy
        _ImageDraw.Draw(img).ellipse(
            (x - r, y - r, x + r, y + r), fill=shape.colour.value
        )
    elif isinstance(shape, Rectangle):
        shape.size = (shape.size[0] * scaling_factor,
                      shape.size[1] * scaling_factor)

        # rectangle shape
        _ImageDraw.Draw(img).rectangle(
            (shape.left, shape.bottom, shape.right,
             shape.top), fill=shape.colour.value
        )  # TODO decentral _shapes seems to be bit larger than with pyplot
    # elif isinstance(shape, _shapes.Picture):
    #     tmp = _np.asarray(shape.size) * scaling_factor
    #     shape.size = tmp.tolist()
    #     # picture
    #     target_box = _np.round(shape.get_ltrb(), decimals=0)
    #     # type: ignore # reversed y axes
    #     target_box[:, 1] = _np.flip(target_box[:, 1])
    #     pict = _Image.open(shape.filename, "r")
    #     if pict.size[0] != shape.size[0] or pict.size[1] != shape.size[1]:
    #         pict = pict.resize(shape.size, resample=_Image.ANTIALIAS)

    #     tr_layer = _Image.new("RGBA", img.size, (0, 0, 0, 0))
    #     tr_layer.paste(pict, target_box)
    #     res = _Image.alpha_composite(img, tr_layer)
    #     img.paste(res)
    #     pass

    else:
        raise NotImplementedError(
            "Shape {} NOT YET IMPLEMENTED".format(type(shape)))


def shapes_test_picture(
    shapes,
    size=(500, 500),
    filename="shapes_test.png",
    background_colour="#888888",
    reverse_order=False,
):
    """makes the shape test picture"""

    img = _Image.new("RGBA", size, color=background_colour)
    if reverse_order:
        shapes = reversed(shapes)
    for s in shapes:
        _draw_shape(img, s)
    img.save(filename)
    print(f"saved {filename}")
