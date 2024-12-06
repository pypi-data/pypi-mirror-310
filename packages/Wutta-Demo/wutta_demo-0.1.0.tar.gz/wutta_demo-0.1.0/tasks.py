# -*- coding: utf-8; -*-
"""
Tasks for Wutta Demo
"""

import os
import shutil

from invoke import task


@task
def release(c):
    """
    Release a new version of Wutta Demo
    """
    if os.path.exists('dist'):
        shutil.rmtree('dist')

    c.run('python -m build --sdist')
    c.run('twine upload dist/*')
