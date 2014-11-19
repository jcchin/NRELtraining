================
Getting Started
================

This plugin contains the documentation and component definitions for the
OpenMDAO instructional class that was given at the  National Renewable Energy
Laboratory (NREL) Wind Energy Systems Engineering workshop.
The class was given by Tristan Hearn and Jeff Chin of the NASA Glenn
Research Center. Tristan and Jeff are members of the OpenMDAO development team
and built the content of this class to demonstrate the basic usage of OpenMDAO
on some simple wind turbine design problems. The class covers:

- Understanding the use cases of OpenMDAO
- Basic usage for creating components
- Building optimizations around models, working with design of experiments
- Recording data from your runs
- Building more complex/robust models

The plugin and this tutorial have been updated for compatibility with
OpenMDAO Version 0.10.3.2

What is OpenMDAO?
========================

OpenMDAO is a Multidisciplinary Design Analysis and Optimization
(MDAO) framework, written in Python.

5 Core Principles of OpenMDAO:

- Open-Source and Professionally Maintained
- Powerful Algorithms
- Modular Development
- Interoperable 
- Development Tools


Who Uses OpenMDAO?
========================

NASA

Academia

- Stanford
- U Michigan
- Purdue
- Technical University of Denmark
- Texas A & M


Industry

- NREL
- Sandia
- Boeing
- AeroVelo
- M4 Engineering

What has OpenMDAO been used for?
========================

Satellite Design

Design Optimization: Quiet Aircraft Wing Slats

Hyperloop

Heartbeat Sensor

Aero-Structural Optimization of Wind Turbine Blades

Installation and Activating your environment
=========================================

Installation is covered in the docs `here <http://openmdao.org/docs/index.html>`_.

Everytime OpenMDAO code is run, an activated environment is required.
Activation adds your virtual environment’s ``bin`` directory to your system path.
This enables a customized Python interpreter, giving you access to everything in OpenMDAO.
Read more `here <http://openmdao.org/docs/getting-started/index.html>`_.

First, open a terminal window and navigate to the folder created by your install script. 
It will have a name of the form ``openmdao-X.X.X``.

The next step is platform specific. (make sure to include the "." in the Linux/OS X command)

Linux:
::

    bash
    . bin/activate

OS X:
::   

    . bin/activate

Windows:
:: 

    Scripts\activate