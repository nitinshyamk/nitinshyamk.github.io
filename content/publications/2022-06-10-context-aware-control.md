---
title: "Towards context-aware learning for control: Balancing stability and model-learning error"
authors: Nitin Shyamkumar, Serkan Gugercin, Benjamin Peherstorfer
venue: IEEE American Control Conference
date: 2022-06-10
url: https://cims.nyu.edu/~pehersto/preprints/contextc_preprint.pdf
---

Classical data-driven control typically follows the learn-then-stabilize scheme where first a model of the system of interest is identified from data and then a controller is constructed based on the learned model. However, learning a model from data is challenging since it can incur high training costs and the model quality critically depends on the available data. In this work, we address how well one needs to learn a model to derive a controller by formalizing the trade off between learning error and controller performance in the specific setting of robust H-infinity control. We propose a bound on the stability radius of a robust controller with respect to the error of the learned model. The proposed analysis suggests that tolerating an increased learning error leads to a small decrease in the performance objective of the controller. Numerical experiments with systems from aerospace engineering demonstrate that judiciously balancing learning error and control performance can indeed reduce the number of data points by one order of magnitude with less than 5% decrease in control performance as measured with the H-infinity stability radius.
