import json
import numpy as np
from pynsn import rnd
import pynsn
from pynsn.image import pil_image

da = pynsn.Dot(xy=(-20, 120), diameter=5,  attribute=pynsn.Colour("black"))
db = pynsn.Ellipse(xy=(20, 17), size=(120, 50), attribute="#FF0000")
dc = pynsn.Ellipse(xy=(120, 57), size=(60, 120),
                   attribute="#00F000")  # big dot

ra = pynsn.Rectangle(xy=np.array((-70, -175)),
                     size=(40, 40), attribute="#FF0000")
rb = pynsn.Rectangle(xy=(-50, -45), size=(10, 10), attribute="#cc0F00")
r_big = pynsn.Rectangle(xy=(10, -40), size=(150, 60), attribute="#000088")

rnd_ell = rnd.RndRectangle(width=(40.8, 10.4), height=(20, 50),
                           attributes=["green", "black", "orange", "red"])
rnd_dot = rnd.RndDot(diameter=(40.8, 10),
                     attributes=["green", "black", "orange", "red"])

if False:

    nsn = pynsn.NSNStimulus(
        # target_area_shape=pynsn.Dot(diameter=500, attribute="#00FFFF"),
        target_area_shape=pynsn.Rectangle(
            size=(300, 500), attribute="#00FFFF"),
        min_distance_target_area=10,
        min_distance=2)
    # random dot
    nsn.shape_add_random_pos(rnd_ell, n=20)
    print(nsn.properties_txt(short_format=True))
    print(nsn.contains_overlaps())
    print(nsn.properties.numerosity)

if True:

    factory = pynsn.StimulusFactory(
        target_area_shape=pynsn.Rectangle((500, 400), attribute="white"),
        min_distance_target_area=10,
        min_distance=2)
    factory.shape_add(rnd_ell, 10)
    factory.shape_add(rnd_dot, 10)

    nsn = factory.create()
    factory.to_json(filename="demo.json")

stim = pynsn.NSNStimulus(target_area_shape=pynsn.Dot(300))
stim.shape_add_random_pos(pynsn.Dot(diameter=10), n=20)
stim.colours.convex_hull = "green"


print(nsn.properties_txt())

nsn.to_json("demo.json", tabular=True)
x = pynsn.NSNStimulus.from_json("demo.json")

print(x.properties_txt())

a = pil_image.create(nsn)
a.save("shapes_test.png")

a = pil_image.create(x)
a.save("shapes_test2.png")
