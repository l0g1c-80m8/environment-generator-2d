# Dynamic 2D Environment Generator

This is a 2D environment generator useful for random generation of random layouts in 2D.
The implementation has been inspired by the environment description as specified in 
[Appendix G of RoCUS](https://arxiv.org/pdf/2012.13615.pdf).


### Environment Description

The environment is the area defined in the domain of (xmin, xmax) × (ymin, ymax) along with
starting point (xstart, ystart) and ending point (xgoal, ygoal). The environment representation is a
summation of radial basis function (RBF) kernels centered "obstacle points" that are randomly generated 
based on a seed value. Specifically, given n obstacle points $p_{1}, p{2}, ..., p{n} ∈ R^2$,
the environment is defined at each point in the domain R^2 (within limits) as:

$$e(P) = \sum_{i=1}^{n} \exp(-\gamma || P - P_{i} ||_{2}^2)$$

A point P in the limits of the environment (xmin, xmax) × (ymin, ymax) is an obstacle if $e(P) > \eta$.
