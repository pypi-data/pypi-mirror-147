================
render_me_harder
================


.. image:: https://img.shields.io/pypi/v/render_me_harder.svg
        :target: https://pypi.python.org/pypi/render_me_harder

.. image:: https://img.shields.io/travis/minexew/render_me_harder.svg
        :target: https://travis-ci.com/minexew/render_me_harder

.. image:: https://readthedocs.org/projects/render-me-harder/badge/?version=latest
        :target: https://render-me-harder.readthedocs.io/en/latest/?version=latest
        :alt: Documentation Status




Stupidly simple API for rendering 3D models to images


* Free software: MIT license
* Documentation: ~~https://render-me-harder.readthedocs.io.~~

It exports exactly one function: ::

    def render_frames(mesh: trimesh.Trimesh,
                      w: int,
                      h: int,
                      num_frames: int) -> Sequence[Image.Image]


Features
--------

* easy to use

Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
