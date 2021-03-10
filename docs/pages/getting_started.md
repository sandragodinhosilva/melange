---
layout: default
title: Getting started
nav_order: 1
---

.. _conda: http://anaconda.org/
.. _mamba: https://github.com/TheSnakePit/mamba

Getting Started
***************

Setup
=====

Conda package manager
---------------------

MeLanGE has **one dependency**: conda_. All databases and other dependencies are installed **on the fly**.
MeLanGE is based on snakemake which allows to run steps of the workflow in parallel on a cluster.

To try MeLanGE, you can use `example data`_ for testing.


Memory & system requirements:



You need to install `anaconda <http://anaconda.org/>`_ or miniconda. If you haven't done it already you need to configure conda with the bioconda-channel and the conda-forge channel. This are sources for packages beyond the default one.::

    conda config --add channels defaults
    conda config --add channels bioconda
    conda config --add channels conda-forge

The order is important by the way.

Install mamba
-------------

Conda can be a bit slow because there are so many packages. A good way around this is to use mamba_ (another snake).::

    conda install mamba


From now on you can replace ``conda install`` with ``mamba install`` and see how much faster this snake is.

Install MeLanGE
------------------------
