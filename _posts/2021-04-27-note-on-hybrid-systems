---
title: 'Hybrid systems - a brief overview'
date: 2021-04-27
permalink: /posts/2020/hybridsystemsoverview/
tags:
  - Hybrid systems
  - Control theory
---
Hybrid systems
======

TLDR: There's a broad class of systems that involve both continuous and discontinuous dynamics called hybrid systems. Intuitively, these systems may have both a discrete automaton and an associated ODE; the combined interaction of both modes describes the time evolution of the system dynamics. There are a lot of different ways that these hybrid systems can be expressed. But a 2007 paper from researchers at Delft showed that many of these systems are equivalent (with a fairly minimal set of restrictions).
For a wide range of hybrid systems, researchers have worked out how to extend traditional control concepts like Lyapunov stability, controllability, identifiability, etc. Understanding when each system might be helpful for a specific problem as well as the task of combined identification and control seems like an interesting and open problem.

Not to long ago,

Here's the summary of the literature I've been reading regarding hybrid systems, which I think are best summarized as dynamical systems that include continuous and discrete dynamics. From Wikipedia, "a system that can both flow (described by a differential equation) and jump (described by a state machine or automaton)".  If you have very limited time, I think the blog https://yalmip.github.io/example/maxplus/ , [4], and the applications section in [5] give a very effective and efficient overview of hybrid systems.
First, work in the Max-Plus framework seems to be pushed mostly by researchers at Delft University. I've seen other researchers use this as well, but more limited ([1 uses the Max-Plus framework to study network congestion control, so probably not super relevant to our research). However, it seems interesting, and it turns out to have a lot of connections to a much broader classes of problems.
https://yalmip.github.io/example/maxplus/ is a brief blog post summarizing the Max-Plus framework and a basic control task. A dynamical system X_{k+1} = A x_{k} in the Max Plus framework has a natural interpretation of a process on a graph, so a common application with max plus systems is to create a timed event graph (imagine a graph representing a partial ordering for events, i.e. event A must happen before B, which must wait for 5 min, etc).
[2] was really helpful for understanding an application of when this Max Plus framework could be useful; it uses the max-plus framework to coordinate a 6-legged robot locomotion by manipulating firing times of key transitions (lift this leg up, hold this leg, etc.).  [3] is another application paper; it discusses stability of a railway timetable in a way that made me think of some of the rare events work we want to do. Using the generalization of eigenvalues and spectral theory for Max-Plus systems, [3] answers some interesting questions for a real train timetable with thousands of nodes: what happens if a train is delayed by D hours? Do delays propagate indefinitely or even get worse? How fast can the system recover from a delay? The same research group extended the Max Plus system to a Max-Min-Plus-Scaling (MMPS) system, adding the minimum and scalar multiplication operations to model a richer class of systems.
It turns out that the MMPS framework is just one class in a broad array of hybrid systems approaches. [4] is a really clear and concise overview of five different types of hybrid systems and when they are equivalent.  [5] is a long textbook, but also has some really clear applications and techniques that I think could be of interest to us.  Here's an interesting application from the book: how does one control a continuous time process with a discrete automaton? The automaton could even be a low fidelity discretized representation of the continuous process - this reminds me a lot of the general model reduction/control concepts and the digital twin presentation Karen Willcox gave at SIAM CSE. Another relevant hybrid system is a continuous PDE with convex constraints on the state space.
[4] describes a few interesting classes of these hybrid systems, although the exact names don't seem to be consistent across the literature. The Linear Complementarity System, for instance, is a linear ODE with the restriction that the solution satisfies a linear complentarity problem (an LCP is a generalization of the quadratic programming problem). In general, the solution to these types of problems have multiple continuous modes. One example of an LCS is an optimal control problem with state constraints of a certain form.
Another related class of problems is the PieceWise Affine (PWA) System. The PWA is an indexed collection of LTI systems, but each system is only valid for a convex polyhedral region of the state / input space. [6] applies tools for PWAs to neural networks, and [7]  composes a PWA model with a ReLU neural net (which is also a PWA system) and then uses Lyapunov stability analysis tools to make the neural net a verified controller.
I think that there is a strong relationship between the PWA system and what the ML community likes to call Switching Linear Dynamical Systems (SLDS) ([8]). But from what I can tell so far, there's not much discussing parameterized SLDSs, which could be an interesting angle to apply some of the model reduction ideas (i.e. my PWA system or SLDS is parameterized by theta, how do I learn an approximation that is valid for a range of theta).  I think there's interest from some of the papers I've read (I know that such tools would actually be really useful for my course project).
Here are another few papers with some more specific directions: [9] is less theoretical and grounded in autonomous vehicle control, including discussion of system identification for PWAs. I haven't gone through [10], but I'm very intrigued by their discussion of H infinity control for PWAs.
[1]  https://ieeexplore.ieee.org/document/4267662
[2]  https://www.dcsc.tudelft.nl/~bdeschutter/pub/rep/09_045.pdf
[3] https://www.sciencedirect.com/science/article/abs/pii/S0191261506000208
[4] https://www.dcsc.tudelft.nl/~bdeschutter/pub/rep/00_07.pdf
[5] https://www.ecse.rpi.edu/~agung/course/vanderschaft.pdf
[6]  https://arxiv.org/pdf/1910.03879.pdf,
[7] https://arxiv.org/pdf/2008.06546.pdf
[8] https://arxiv.org/pdf/1610.08466.pdf
[9] http://citeseerx.ist.psu.edu/viewdoc/download;jsessionid=F39CA5A3A7105AD55753BA83913C77D3?doi=10.1.1.55.5680&rep=rep1&type=pdf
[10]  https://www.sciencedirect.com/book/9781782421610/control-and-estimation-of-piecewise-affine-systems#book-description
