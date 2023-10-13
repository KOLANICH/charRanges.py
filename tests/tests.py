#!/usr/bin/env python3
import sys
from pathlib import Path
import unittest
import itertools, re
import colorama

sys.path.insert(0, str(Path(__file__).parent.parent))

from collections import OrderedDict

dict = OrderedDict

from charRanges import *
#from escapelib import *

class Tests(unittest.TestCase):

	def test_ranges2CharClassRangedString(self):
		testVectors = {
			((range(43, 44), range(45, 46)), None): "+-",
			((range(43, 44),), None): "+"
		}
		for (rs, escaperCtor), resp in testVectors.items():
			with self.subTest(rs=rs, escaperCtor=escaperCtor, resp=resp):
				if escaperCtor is not None:
					escaper = escaperCtor()
				else:
					escaper = escaperCtor

				actual = ranges2CharClassRangedString(rs, escaper=escaper)
				self.assertEqual(resp, actual)


if __name__ == "__main__":
	unittest.main()
