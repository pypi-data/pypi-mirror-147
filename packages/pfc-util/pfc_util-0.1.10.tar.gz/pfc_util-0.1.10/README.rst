PFC simulation in python
==============================

created by michael in 2022/04

pfc_util is a python package for PFC (phase field crystal) simulations.

Required Packages
======================
* numpy
* scipy
* matplotlib
* pyfftw
* tqdm
* torusgrid
* michael960lib


Modules
========

:code:`pfc_util.core.base` - Definitions of PFC free energy functional and state functions

:code:`pfc_util.core.evolution` - PFC minimizers, including constant chemical potential & nonlocal conserved minimization and stress relaxer

:code:`pfc_util.toolkit` - Tools for Editting/Analyzing PFC Fields

:code:`pfc_util.profile_prompt` - Interactive PFC Prompt (WIP)


