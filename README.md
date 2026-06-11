# Collisions
#### Current status, May 30, 2026:
- Have just added slider for calculated vector value: the square of the mass (m^2 = t^2 -x^2 - y^2 - z^2) so that user can think in terms of that value, rather than time (t), when adjusting the vectors in a collision. These variable names I also changed to E, px, py, pz in GUI, instead of t, x, y, z.
- Next: refine the calculation  performed in the second step of the two-step transformation option that the user is offered. Currently that step is a kludge that only gets the gist of the calculation.
- Lots of TODOs for later, such as
  - Fix little issues raised by the linter
  - Refactor style strings for maintainability
  - Assorted OOP/MVC refactoring is needed
## Introduction
An application in Python (PyQt-PySide6, Matplotlib) for particle accelerator physicists and theoretical physicists working in particle physics, QCD, or nuclear physics. The purpose of the application is to allow physicists to see, rather than having to imagine, the vectors of particle just after particle collisions both in (a.) the laboratory (collider) reference frame and in (b.) a frame obtained by transformation of the vector set with a transformation matrix stipulated by the physicist. The application allows the physicist to enter a set of four-vectors, see them graphed, and vary the vectors on the fly by using sliders, so as to show the results of "what-if" scenarios of interest.

Now (May 30, 2026) the application is available. It is called Collisions-QCD/TMD, and it is in <a href="https://github.com/j-a-ryan/Collisions/releases/tag/v0.2.3-alpha">pre-release version v0.2.4-alpha</a> for Windows and MacOS. More updates will be coming in June. I plan to release a beta version in early summer.

Physicists interested in this software are encouraged to download it and use it. Physicists who would like a similar application be built are invited to tell me about their ideas at j dot a dot ryan at protonmail. I am a former software developer headed to the physics graduate program at ODU in the fall of 2026.
#### Notes for Software Developers:
The application design is regular, old-fashioned MVC but not PyQt/PySide's native form of MVC which is model-view and has the controller coupled to (embodied in/blurred with) the view. So, the application has controller classes, as in regular MVC. (I looked at PyQt's innate MV pattern but I couldn't see its superiority for a complicated application like Collisions. For small applications I suppose it might be nice. I am no design pattern master, however.)

I am trying to make an application for the specific use-case of a QCD team while keeping reusable components available to be used as a platform for any particle collider physicist who wants to analyze collision vectors of particles in a collider. I am probably failing at this, such that a sizeable refactoring task (for platform creation) will remain after this application is deployed in a stable beta version. As usual, platformability falls by the wayside when there aren't enough man hours to do it.

## GUI
Below you see a set of vectors in the laboratory (particle collider) reference frame representing the paths of particles emerging from a collision at the origin (left) and their transformation into a different frame (right). One of the six possible 2D representations of these graphs is seen as a popup. Sliders at the left under "CONTROLS" allow the user to vary the vectors and observe the effects on both the 3D graph on the left and the transformation on the right simultaneously. Other controls will eventually be implemented. The application represents the tips of the vectors with circles containing the names of the particles, rather than arrowheads. This may change.

<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/693bbe61-667f-4b56-ae0f-ed02dd244357" />

Various 4x4 transformation matrices can be used on the four-vectors entered by the user. The vector entry form is shown below:

<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/202a78b2-1214-42f3-9718-02d07bb7a98b" />

## Transformation Matrices
The application currently applies a transformation matrix described by T.C. Rogers' 2025 work-in-progress, "A system for analyzing hadron kinematics," as shown below. 

<img width="921" height="765" alt="image" src="https://github.com/user-attachments/assets/8147aeae-9730-4813-b34b-848ead15f22b" />
</br>
However, Collisions could apply any matrix of interest to physicists. The application could offer a list of matrices for the user to choose from or allow the user to submit a custom matrix. Etc.

## Dependencies
I gratefully use these third-party libraries:

Uses <a href="https://github.com/niklashenning/pyqt-advanced-slider">PyQt Advanced Slider</a>

Uses <a href="https://github.com/5yutan5/PyQtDarkTheme">PyQtDarkTheme</a>

## Current Status: alpha
Very rough prototype, offering only a use case or two, currently being built for physicist to evaluate. I hope to have a working app that will allow the visualization of three particles emerging from a collision, as stipulated by user data entry, along with slider bars for user to manipulate the data on the fly to see how it effects the visualization. Transformation matrix is currently working, allowing the reference frame of any particle to be used in the graph and displayed next to a graph of the collision in the lab refrence frame.
