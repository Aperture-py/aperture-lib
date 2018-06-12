import unittest
import PIL as pillow


class ApertureLibTest(unittest.TestCase):
    """An extension of the unittest TestCase base class to provide
    helper methods or test fixtures (i.e. Pillow) to be used in aperturelib
    tests.
    """

    def setUp(self):
        """Setup test fixtures before each ApertureLibTest."""

        # Give each test a copy of pillow
        self.pillow = pillow