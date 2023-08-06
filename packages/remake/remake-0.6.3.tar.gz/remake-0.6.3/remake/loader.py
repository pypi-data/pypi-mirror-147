from pathlib import Path

from remake.util import load_module
from remake.remake_exceptions import RemakeLoadError


def load_remake(filename):
    # Avoids circular import.
    from remake import Remake
    filename = Path(filename)
    if not filename.suffix:
        filename = filename.with_suffix('.py')
    remake_module = load_module(filename)
    # remakes = [o for o in [getattr(remake_module, m) for m in dir(remake_module)]
    #            if o.__class__.__name__ == 'Remake']
    remakes = [o for o in [getattr(remake_module, m) for m in dir(remake_module)]
               if isinstance(o, Remake)]
    if len(remakes) > 1:
        raise RemakeLoadError(f'More than one remake defined in {filename}')
    elif not remakes:
        raise RemakeLoadError(f'No remake defined in {filename}')
    return remakes[0]
