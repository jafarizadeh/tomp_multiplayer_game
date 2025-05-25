import time
from utils.logger import Logger

class SimpleRandom:
    """
    A custom pseudo-random number generator using Linear Congruential Generator (LCG).
    Designed for reproducibility, testability, and full control in game environments.
    """

    def __init__(self, seed=None, logger=None):
        """
        Initialize the random generator with optional seed and logger.
        """
        self.logger = logger or Logger(name="RAND", log_level="WARN")
        self.set_seed(seed if seed is not None else int(time.time() * 1000))

    def set_seed(self, seed):
        """
        Set the internal state (seed) of the generator.
        """
        self.state = seed & 0x7FFFFFFF  # Ensure 31-bit state
        self.logger.debug(f"Seed set to: {self.state}")

    def _next(self):
        """
        Generate the next pseudo-random number using LCG.
        """
        a = 1664525
        c = 1013904223
        m = 2 ** 31
        self.state = (a * self.state + c) % m
        return self.state

    def random(self):
        """
        Return a float number between 0 and 1.
        """
        r = self._next() / 2**31
        self.logger.debug(f"Generated random(): {r}")
        return r

    def randint(self, a, b):
        """
        Return a random integer N such that a <= N <= b.
        """
        if a > b:
            self.logger.error(f"Invalid randint range: ({a}, {b})")
            raise ValueError("Invalid range: a must be <= b")
        value = a + self._next() % (b - a + 1)
        self.logger.debug(f"randint({a}, {b}) → {value}")
        return value

    def uniform(self, a, b):
        """
        Return a random float number between a and b.
        """
        result = a + (b - a) * self.random()
        self.logger.debug(f"uniform({a}, {b}) → {result}")
        return result

    def choice(self, seq):
        """
        Return a random element from a non-empty sequence.
        """
        if not seq:
            self.logger.error("choice() called on empty sequence")
            raise IndexError("Cannot choose from an empty sequence")
        index = self.randint(0, len(seq) - 1)
        result = seq[index]
        self.logger.debug(f"choice() picked index {index}: {result}")
        return result

    def sample(self, seq, k):
        """
        Return k unique random elements from the sequence.
        """
        if k > len(seq):
            self.logger.error(f"sample() requested {k} items from {len(seq)}-length sequence")
            raise ValueError("Sample size exceeds sequence length")
        pool = list(seq)
        result = []
        for _ in range(k):
            try:
                idx = self.randint(0, len(pool) - 1)
                picked = pool.pop(idx)
                result.append(picked)
                self.logger.debug(f"sample(): picked {picked} at index {idx}")
            except Exception as e:
                self.logger.error(f"sample() internal error: {e}")
                break
        return result

    def shuffle(self, seq):
        """
        Shuffle a mutable sequence in-place.
        """
        try:
            for i in reversed(range(1, len(seq))):
                j = self.randint(0, i)
                seq[i], seq[j] = seq[j], seq[i]
                self.logger.debug(f"shuffle(): swapped {i} and {j}")
        except Exception as e:
            self.logger.error(f"shuffle() error: {e}")
