.. cartograph documentation master file, created by
   sphinx-quickstart on Fri Sep 13 14:09:24 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Introduction
=====================================

Cartograph is a Python package for drawing OpenStreetMap compatible map tiles. The tiles it produces can be viewed as a `slippy map <https://wiki.openstreetmap.org/wiki/Slippy_Map>`_ or by various apps.

Installation
============

Cartograph can be installed using pip

::

  pip install cartograph

Reference
=========

.. toctree::
  map
  feature
  style
  projection

Basic Usage
===========

The following script is a minimal demonstration of how to create a map, add some features to it and draw the map as a single image.

::

  from cartograph import Map
  from cartograph.style import AreaStyle, NameStyle

  map = Map()
  map.bound_by_box(0.0, 1.0, 0.0, 1.0) # degrees of latitude / longitude
  map.set_background_color('blue')

  square = np.array([[0.3, 0.7, 0.7, 0.3], [0.3, 0.3, 0.7, 0.7]]) # degrees of latitude / longitude
  square_style = AreaStyle(color='green')
  map.add_area(square, square_style)

  name = 'A. Square'
  location = np.array([0.5, 0.5]) # degrees of latitude / longitude
  name_style = NameStyle(fontsize=5)
  map.add_name(name, location, name_style)

  map.draw_image('map.png')

This should create an image called "map.png" like the one below

.. image:: map.png
  :width: 50%
  :align: center

Tutorial
========

Coming soon.

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
