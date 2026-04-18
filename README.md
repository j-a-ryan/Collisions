# Collisions

An application in Python (PyQt-PySide6, Matplotlib) for particle accelerator physicists and theoretical physicists working in particle physics, QCD, or nuclear physics. The purpose of the application is to allow physicists to see, rather than having to imagine, the vectors of particle just after particle collisions in both the laboratory (collider) reference frame and in a frame obtained by transformation of the vector set with a transformation matrix stipulated by the physicist. The application allows the physicist to vary the vectors on the fly by using sliders, so as to show the results of "what-if" scenarios of interest.

Now (April 16, 2026) the application is available for the first time. It is called Collisions-QCD/TMD, and it is in <a href="https://github.com/j-a-ryan/Collisions/releases/tag/v0.1.2-alpha">pre-release version v0.1.2-alpha</a> for Windows and MacOS. Two physicists are test-driving it now and versions v0.1.3-alpha, v0.1.4-alpha, etc. will doubtless be appearing in the coming days and weeks. I hope to release a beta version in early summer.

Physicists interested in this software are encouraged to download it and use it. Physicists who would like a similar application be built are invited to tell me about their ideas at j dot a dot ryan at protonmail.

## GUI
Below you see a set of vectors in the laboratory (particle collider) reference frame representing the paths of particles emerging from a collision at the origin (left) and their transformation into a different frame (right). One of the six possible 2D representations of these graphs is seen as a popup. Sliders at the left under "CONTROLS" allow the user to vary the vectors and observe the effects on both the 3D graph on the left and the transformation on the right simultaneously. Other controls will eventually be implemented.

<img width="1918" height="1019" alt="GUI" src="https://github.com/user-attachments/assets/cec77057-9ee9-4301-84e7-84a165d50588" />

Various 4x4 transformation matrices can be used on the four-vectors entered by the user. Currently the matrix being used is one stipulated by a team of QCD researchers at ODU. The vector entry form is shown below:

<img width="1917" height="1019" alt="image" src="https://github.com/user-attachments/assets/e773ad9d-fdf4-4e0a-888f-572c0fd988c0" />

## Dependencies
I gratefully use these third-party libraries:

Uses <a href="https://github.com/niklashenning/pyqt-advanced-slider">PyQt Advanced Slider</a>

Uses <a href="https://github.com/5yutan5/PyQtDarkTheme">PyQtDarkTheme</a>

## Current Status: alpha
Very rough prototype, offering only a use case or two, currently being built for physicist to evaluate. I hope to have a working app that will allow the visualization of three particles emerging from a collision, as stipulated by user data entry, along with slider bars for user to manipulate the data on the fly to see how it effects the visualization. Transformation matrix is currently working, allowing the reference frame of any particle to be used in the graph and displayed next to a graph of the collision in the lab refrence frame.
