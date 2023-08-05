# Copyright (C) Rouyuntech 2016
# Please see the accompanying LICENSE file for further information.

"""Main shine module."""

import os
import sys
from distutils.util import get_platform

from os.path import join, isfile

import numpy as np


__all__ = ['SHINE']

class ConvergenceError(Exception):
    pass


class KohnShamConvergenceError(ConvergenceError):
    pass


class PoissonConvergenceError(ConvergenceError):
    pass


class ConvergenceError(Exception):
    pass


# Check for special command line arguments:
debug = False
trace = False
dry_run = 0
memory_estimate_depth = 2
parsize_domain = None
parsize_bands = None
buffer_size = None
augment_grids = False
extra_parameters = {}
profile = False
i = 1
while len(sys.argv) > i:
    arg = sys.argv[i]
    if arg == '--trace':
        trace = True
    elif arg == '--debug':
        debug = True
    elif arg.startswith('--dry-run'):
        dry_run = 1
        if len(arg.split('=')) == 2:
            dry_run = int(arg.split('=')[1])
    elif arg.startswith('--memory-estimate-depth'):
        memory_estimate_depth = -1
        if len(arg.split('=')) == 2:
            memory_estimate_depth = int(arg.split('=')[1])
    elif arg.startswith('--buffer_size='):
        # Buffer size for MatrixOperator in MB
        buffer_size = int(arg.split('=')[1])
    elif arg.startswith('--augment-grids='):
        augment_grids = bool(int(arg.split('=')[1]))
    elif arg.startswith('--shine='):
        extra_parameters = eval('dict(%s)' % arg[8:])
    elif arg == '--shine':
        extra_parameters = eval('dict(%s)' % sys.argv.pop(i + 1))
    elif arg.startswith('--profile='):
        profile = arg.split('=')[1]
    else:
        i += 1
        continue
    # Delete used command line argument:
    del sys.argv[i]

if debug:
    np.seterr(over='raise', divide='raise', invalid='raise', under='ignore')

    oldempty = np.empty

    def empty(*args, **kwargs):
        a = oldempty(*args, **kwargs)
        try:
            a.fill(np.nan)
        except ValueError:
            a.fill(-1000000)
        return a
    np.empty = empty

    
build_path = join(__path__[0], '..', 'build')
arch = '%s-%s' % (get_platform(), sys.version[0:3])

# If we are running the code from the source directory, then we will
# want to use the extension from the distutils build directory:
sys.path.insert(0, join(build_path, 'lib.' + arch))


def get_shine_python_path():
    paths = os.environ['PATH'].split(os.pathsep)
    paths.insert(0, join(build_path, 'bin.' + arch))
    for path in paths:
        if isfile(join(path, 'shine-python')):
            return path
    raise RuntimeError('Could not find shine-python!')

try:
    setup_paths = os.environ['SHINE_SETUP_PATH'].split(os.pathsep)
except KeyError:
    if os.pathsep == ';':
        setup_paths = [r'C:\gpaw-setups']
    else:
        setup_paths = ['/usr/local/share/gpaw-setups',
                       '/usr/share/gpaw-setups']


from shine.dft.aseinterface import GPAW

def restart(filename, Class=GPAW, **kwargs):
    calc = Class(filename, **kwargs)
    atoms = calc.get_atoms()
    return atoms, calc


if trace:
    indent = '    '
    path = __path__[0]
    from shine.mpi import world
    if world.size > 1:
        indent = 'CPU%d    ' % world.rank

    def f(frame, event, arg):
        global indent
        f = frame.f_code.co_filename
        if not f.startswith(path):
            return

        if event == 'call':
            print(('%s%s:%d(%s)' % (indent, f[len(path):], frame.f_lineno,
                                    frame.f_code.co_name)))
            indent += '| '
        elif event == 'return':
            indent = indent[:-2]

    sys.setprofile(f)


if profile:
    from cProfile import Profile
    import atexit
    prof = Profile()

    def f(prof, filename):
        prof.disable()
        from shine.mpi import rank
        if filename == '-':
            prof.print_stats('time')
        else:
            prof.dump_stats(filename + '.%04d' % rank)
    atexit.register(f, prof, profile)
    prof.enable()


command = os.environ.get('SHINESTARTUP')
if command is not None:
    exec(command)


home = os.environ.get('HOME')
if home is not None:
    rc = os.path.join(home, '.shine', 'rc.py')
    if os.path.isfile(rc):
        # Read file in ~/.shine/rc.py
        exec(open(rc).read())
