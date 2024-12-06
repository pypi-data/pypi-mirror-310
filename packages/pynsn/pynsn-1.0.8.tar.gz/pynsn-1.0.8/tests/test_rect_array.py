import unittest
from pynsn import NSNFactory
from pynsn import distributions as distr
from pynsn import Dot
from .test_dot_array import DotsSmall


class RectanglesSmall(DotsSmall):
    def settings(self):
        self.factory = NSNFactory(target_area=Dot(diameter=400))
        self.factory.set_appearance_rectangles(
            width=distr.Normal(min_max=(10, 40), mu=20, sigma=10),
            height=distr.Normal(min_max=(10, 40), mu=20, sigma=10))
        self.n_dots = 5

    def setUp(self):
        self.settings()
        self.stimulus = self.factory.random_rectangle_array(
            n_objects=self.n_dots)

    def test_fit_av_size(self):
        first = 0.8
        second = 1.15
        scale_factor = 1.1
        places = 7
        # check scale
        stim = self.stimulus.copy()
        new_value = stim.properties.average_rectangle_size * scale_factor
        stim.properties.fit_average_rectangle_size(new_value)
        self.assertAlmostEqual(stim.properties.average_rectangle_size[0],
                               new_value[0], places=places)
        self.assertAlmostEqual(stim.properties.average_rectangle_size[1],
                               new_value[1], places=places)

        #  changes two time feature (e.g. first decrease and then increase)
        # first
        new_value = stim.properties.average_rectangle_size * first
        stim.properties.fit_average_rectangle_size(new_value)
        self.assertAlmostEqual(stim.properties.average_rectangle_size[0],
                               new_value[0], places=places)
        self.assertAlmostEqual(stim.properties.average_rectangle_size[1],
                               new_value[1], places=places)
        # second
        new_value = stim.properties.average_rectangle_size * second
        stim.properties.fit_average_rectangle_size(new_value)
        self.assertAlmostEqual(stim.properties.average_rectangle_size[0],
                               new_value[0], places=places)
        self.assertAlmostEqual(stim.properties.average_rectangle_size[1],
                               new_value[1], places=places)


class RectanglesMedium(RectanglesSmall):
    def settings(self):
        super().settings()
        self.factory.set_appearance_rectangles(
            width=distr.Normal(min_max=(10, 40), mu=20, sigma=10),
            height=distr.Normal(min_max=(10, 40), mu=20, sigma=10))
        self.n_dots = 25


class RectanglesLarge(RectanglesSmall):
    def settings(self):
        super().settings()
        self.factory.set_appearance_rectangles(
            width=distr.Normal(min_max=(5, 30), mu=10, sigma=5),
            height=distr.Normal(min_max=(5, 30), mu=10, sigma=5))
        self.n_dots = 75


if __name__ == "__main__":
    unittest.main()
