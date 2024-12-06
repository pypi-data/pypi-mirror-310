import unittest
from pynsn import NSNFactory
from pynsn import distributions as distr
from pynsn import flags, Dot


class DotsSmall(unittest.TestCase):

    def settings(self):
        self.factory = NSNFactory(target_area=Dot(diameter=400))
        self.factory.set_appearance_dots(
            diameter=distr.Beta(min_max=(10, 30), mu=15, sigma=2))
        self.n_dots = 5

    def setUp(self):
        self.settings()
        self.stimulus = self.factory.random_dot_array(n_objects=self.n_dots)

    def test_numerosity(self):
        self.assertEqual(self.stimulus.properties.numerosity, self.n_dots)

    def change_prop(self, prop, first=0.8, second=1.15,
                    scale_factor=1.1, places=7):

        # check scale
        stim = self.stimulus.copy()
        new_value = stim.properties.get(prop) * scale_factor
        stim.properties.scale(prop, scale_factor)
        self.assertAlmostEqual(stim.properties.get(prop),
                               new_value, places=places)

        #  changes two time feature (e.g. first decrease and then increase)
        # first
        new_value = stim.properties.get(prop) * first
        stim.properties.fit(prop, new_value)
        self.assertAlmostEqual(stim.properties.get(prop),
                               new_value, places=places)
        # second
        new_value = stim.properties.get(prop) * second
        stim.properties.fit(prop, new_value)
        self.assertAlmostEqual(stim.properties.get(prop), new_value,
                               places=places)

    def test_fit_av_surface_area(self):
        # decrease
        self.change_prop(prop=flags.AV_SURFACE_AREA)

    def test_fit_av_size(self):
        # decrease
        self.change_prop(prop=flags.AV_DOT_DIAMETER)

    def test_fit_av_perimeter(self):
        # decrease
        self.change_prop(prop=flags.AV_PERIMETER)

    def test_fit_total_surface_area(self):
        # decrease
        self.change_prop(prop=flags.TOTAL_SURFACE_AREA)

    def test_fit_total_perimeter(self):
        # decrease
        self.change_prop(prop=flags.TOTAL_PERIMETER)

    def test_fit_field_area(self):
        # decrease
        self.change_prop(prop=flags.SPARSITY, first=1.2,
                         second=0.85, places=4)

    def test_fit_sparcity(self):
        # decrease
        self.change_prop(prop=flags.SPARSITY, first=1.2,
                         second=0.85, places=4)

    def test_fit_log_size(self):
        # decrease
        self.change_prop(prop=flags.LOG_SIZE)

    def test_fit_log_spacing(self):
        # decrease
        self.change_prop(prop=flags.LOG_SPACING, first=1.2,
                         second=0.85)


class DotsMedium(DotsSmall):
    def settings(self):
        super().settings()
        self.n_dots = 25


class DotsLarge(DotsSmall):
    def settings(self):
        super().settings()
        self.n_dots = 75
