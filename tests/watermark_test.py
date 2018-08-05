import unittest
from aperture.aperturelib import resize
from tests import aperturelib_test_helper


class WatermarkTest(aperturelib_test_helper.ApertureLibTest):

    @unittest.skip('need to implement watermark test')
    def test_watermark(self):
        """Test for the watermark function.
        """
        return None


if __name__ == '__main__':
    unittest.main()