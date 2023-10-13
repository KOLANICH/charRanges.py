import typing

from rangeslicetools import sjoin, ssub

__all__ = ("stringToRanges", "ranges2CharClassRangedString", "multiRSub")

dashChar = "-"
dash = ord(dashChar)


def _setToRawRanges(s: str) -> typing.Iterable[range]:

	for c in s:
		n = ord(c)
		yield range(n, n + 1)


def setToRanges(s: str) -> typing.Iterable[range]:
	"""Converts a string containing characters into ranges"""

	return joinRanges(_setToRawRanges(s))


def _stringToRanges(s: str) -> typing.Iterable[range]:
	"""Converts POSITIVE char class specifiers as in PCRE [] into a sequence of integer ranges enclosing allowed characters. Inverts `ranges2CharClassRangedString`."""
	ranges = []
	if s[0] == dashChar:
		s = s[1:]
		ranges.append(range(dash, dash + 1))

	if s:
		if s[-1] == dashChar:
			s = s[:-1]
			ranges.append(range(dash, dash + 1))

	s = s.split(dashChar)
	l = len(s)  # noqa
	unprocessed = []
	if l > 1:
		unprocessed.extend((s[0][: -int(l > 1)], s[-1][int(l > 1) :]))
		ranges.append(range(ord(s[0][-1]), ord(s[1][0]) + 1))
	else:
		unprocessed = s[0]

	for i in range(1, l - 1):
		unpr = s[i][1:-1]
		unprocessed.append(unpr)
		r = range(ord(s[i][-1]), ord(s[i + 1][0]) + 1)
		ranges.append(r)

	for g in unprocessed:
		for c in g:
			o = ord(c)
			r = range(o, o + 1)
			ranges.append(r)

	return ranges


def stringToRanges(s: str) -> typing.Iterable[range]:
	return joinRanges(_stringToRanges(s))


stringToRanges.__doc__ = _stringToRanges.__doc__


def sortRanges(ranges: typing.Iterator[range]) -> typing.List[range]:
	return sorted(ranges, key=lambda r: r.start)


def multiRSub(ranges: typing.Iterable[range], base: range = range(32, 256)) -> typing.Iterator[range]:
	"""Subtracts multiple ranges taken from the SORTED iterable `ranges` from a `base` range."""
	ranges = sortRanges(ranges)
	r1 = base
	for r in ranges:
		r2 = tuple(ssub(r1, r))
		yield from r2[:-1]
		r1 = r2[-1]
	yield r1


def joinRanges(ranges: typing.Iterator[range]) -> typing.List[range]:
	return sjoin(sortRanges(set(ranges)))


def ranges2CharClassRangedString(ranges: typing.Iterator[range], escaper: typing.Optional["escapelib.CharEscaper"] = None) -> str:
	"""Converts a sequence of integer ranges enclosing allowed characters into a POSITIVE char class specifier as in PCRE []. Inverts `stringToRanges`."""

	if escaper is None:
		escaper = lambda x: x

	ranges = joinRanges(ranges)
	res = []
	insertDash = False
	for r in ranges:
		s = r.start
		if s == dash:
			s += 1
			insertDash = True
			continue
		e = r.stop
		rangeLength = e - s
		e -= 1
		if e == dash:
			e -= 1
			insertDash = True
			continue
		if rangeLength == 1:
			s = escaper(chr(s))
		elif rangeLength == 2:
			s = escaper(chr(s)) + escaper(chr(e))
		else:
			middleCharStr = dashChar
			if rangeLength == 3:
				middleCharStrCand = escaper(chr(e - 1))
				if len(middleCharStrCand) > len(middleCharStr):
					middleCharStr = middleCharStrCand

			s = escaper(chr(s)) + middleCharStr + escaper(chr(e))
		res.append(s)
	if insertDash:
		res.append(dashChar)
	return "".join(res)
