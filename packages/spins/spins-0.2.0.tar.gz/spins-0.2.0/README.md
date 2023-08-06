[![image](https://travis-ci.com/stanfordnqp/spins-b.svg?branch=master)](https://travis-ci.com/stanfordnqp/spins-b)

[![image](https://codecov.io/gh/stanfordnqp/spins-b/branch/master/graph/badge.svg)](https://codecov.io/gh/stanfordnqp/spins-b)

# SPINS-B 0.0.2

SPINS-B is the open source version of
[SPINS](https://stanford.resoluteinnovation.com/technologies/S18-012_spins-inverse-design-software-for),
a framework for gradient-based (adjoint) photonic optimization developed
over the past decade at Jelena Vuckovic\'s [Nanoscale and Quantum
Photonics Lab](http://nqp.stanford.edu) at Stanford University. The full
version can be licensed through the [Stanford Office of Technology and
Licensing](http://techfinder.stanford.edu/technologies/S18-012_inverse-design-software-for)
(see FAQ).

The overall architecture is explained in our paper [Nanophotonic Inverse
Design with SPINS: Software Architecture and Practical
Considerations](https://arxiv.org/abs/1910.04829).

## Documentation

[Documentation](http://spins-b.readthedocs.io) is continually updated
over time.

## Features

- Gradient-based (adjoint) optimization of photonic devices
- 2D and 3D device optimization using finite-difference
  frequency-domain (FDFD)
- Support for custom objective functions, sources, and optimization
  methods
- Automatically save design methodology and all hyperparameters used
  in optimization for reproducibility

## Upcoming Features

We are protoyping the next version of SPINS-B. This version of SPINS-B
will support these new features:

- Co-optimization of multiple device regions simulataneously
- Integration with FDTD and other electromagnetic solvers
- Easier to use and extend

## Overview

Traditional nanophotonic design typically relies on parameter sweeps,
which are expensive both in terms of computation power and time, and
restrictive in their parameter space. Likewise, completely blackbox
optimization algorithms, such as particle swarm and genetic algorithms,
are also highly inefficient. In both these cases, the computational
costs limit the degrees of the freedom of the design to be quite small.
In contrast, by leveraging gradient-based optimization methods, our
nanophotonic inverse design algorithms can efficiently optimize
structures with tens of thousands of degrees of freedom. This enables
the algorithms to explore a much larger space of structures and
therefore design devices with higher efficiencies, smaller footprint,
and novel functionalities.

## Publications

Any publications resulting from the use of this software should
acknowledge SPINS-B and cite the following papers:

For general device optimization:

- Su et al. Nanophotonic Inverse Design with SPINS: Software
  Architecture and Practical Considerations. _arXiv:1910.04829_
  (2019).

For grating coupler optimization:

- Su et al. Fully-automated optimization of grating couplers. _Opt.
  Express_ (2018).
- Sapra et al. Inverse design and demonstration of broadband grating
  couplers. _IEEE J. Sel. Quant. Elec._ (2019).
