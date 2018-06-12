import unittest
from aperture.aperturelib import resize
from tests.aperturelib import aperturelib_test_helper


class ResizeTest(aperturelib_test_helper.ApertureLibTest):

    @unittest.skip('need to implement resize test')
    def test_resize(self):
        """Test for the resize function.

        Things to test:
            - The resizing actually works
            - Aspect ratios are preserved by default
            - Aspect ratios are not preserved if default is overriden
        """
        return None


if __name__ == '__main__':
    unittest.main()