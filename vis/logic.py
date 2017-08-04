import logging
import string

# http://www.cs.cornell.edu/courses/cs312/2002fa/lectures/lec26.htm

class BoyerMoore:

    def __init__(self, needle, haystack):
        self.needle = needle
        self.haystack = haystack

    def search(self):
        T = self.haystack
        P = self.needle

        n = len(T)
        m = len(P)

        # NOTE: Using 0 for not found in pattern doesn't allow us to shift by the
        #       entire patten lenght. Change it and see.

        last = {c: P.rindex(c) if c in P else -1 for c in T}
        yield locals()

        # pattern offset in relation to text
        offset = 0
        success = None
        mismatch = None

        # the amount to move offset
        shift = None

        while offset <= n - m:
            j = m - 1
            yield locals()

            while P[j] == T[offset+j] and j >= 0:
                j -= 1
                yield locals()

            if j < 0:
                success = True
                yield locals()
                return offset

            mismatch = T[offset+j]
            shift = j - last[mismatch]
            offset = offset + max(1, shift)
            yield locals()

        success = False
        yield locals()
