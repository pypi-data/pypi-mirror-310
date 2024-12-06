# -*- coding: utf-8; -*-
"""
Tasks for rattail-demo
"""

import os
# import re
import shutil

from invoke import task


# here = os.path.abspath(os.path.dirname(__file__))
# __version__ = None
# pattern = re.compile(r'^version = "(\d+\.\d+\.\d+)"$')
# with open(os.path.join(here, 'pyproject.toml'), 'rt') as f:
#     for line in f:
#         line = line.rstrip('\n')
#         match = pattern.match(line)
#         if match:
#             __version__ = match.group(1)
#             break
# if not __version__:
#     raise RuntimeError("could not parse version!")


@task
def release(c):
    """
    Release a new version of 'rattail-corepos'.
    """

    if os.path.exists('dist'):
        shutil.rmtree('dist')
    if os.path.exists('rattail_demo.egg-info'):
        shutil.rmtree('rattail_demo.egg-info')

    c.run('python -m build --sdist')
    c.run('twine upload dist/*')


    # if os.path.exists('rattail_corepos.egg-info'):
    #     shutil.rmtree('rattail_corepos.egg-info')
    # c.run('python -m build --sdist')
    # c.run(f'twine upload dist/rattail_corepos-{__version__}.tar.gz')
