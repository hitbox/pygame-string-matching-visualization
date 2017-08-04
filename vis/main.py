import argparse

from .engine import engine
from .state import VisState

def main():
    """
    Visualization of Boyer-Moore using pygame.
    """
    parser = argparse.ArgumentParser(description=main.__doc__)
    parser.add_argument('pattern', help='Needle')
    parser.add_argument('text', help='Haystack')
    args = parser.parse_args()

    engine.init(VisState(args.pattern, args.text))
    engine.run()
