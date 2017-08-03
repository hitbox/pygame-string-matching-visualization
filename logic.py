import string
from pprint import pprint as pp

# http://www.cs.cornell.edu/courses/cs312/2002fa/lectures/lec26.htm

class BoyerMoore:

    def __init__(self, needle, haystack):
        self.needle = needle
        self.haystack = haystack
        self.reset()

    def reset(self):
        pass

    def search(self):
        T = self.haystack
        P = self.needle

        n = len(T)
        m = len(P)

        # NOTE: Using 0 for not found in pattern doesn't allow us to shift by the
        #       entire patten lenght. Change it and see.

        last = {c: P.rindex(c) if c in P else -1 for c in T}

        offset = 0

        yield locals()

        while offset <= n - m:
            j = m - 1
            while P[j] == T[offset+j] and j >= 0:
                j -= 1
                yield locals()

            if j < 0:
                success = True
                yield locals()
                return

            mismatch = T[offset+j]
            shift = j - last[mismatch]
            offset = offset + max(1, shift)
            yield locals()

    def step(self):
        pass
