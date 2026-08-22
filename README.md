# Collisions

You can <a href="https://github.com/j-a-ryan/Collisions/releases">download the application, launch it, and try it</a>. Once it's running, you can click on Help to get a quick start about how to use it. The software is introduced below, after some salient notes and a note on current status.

## Some Salient Notes

Many thanks to physicists Ted Rogers and Kazuki Makino for working with me on this.

<b>Python devs</b> keen on particle physics and on the possibility of contributing, please reach out. There are more notes for you below, too.

<b>Physicists</b> desiring an app for visualizing particle accelerator experiments, please download <a href="https://github.com/j-a-ryan/Collisions/releases">the latest version</a> and play with it. Click on the Help button to read the manaul. After getting the hang of what it does, if you would like a similar application be built, please tell me about your ideas at j dot a dot ryan at protonmail. I am a former software developer headed to the physics graduate program at ODU in the fall of 2026. I have just been given an at odu.edu address: jryan017. Use either.

## Current status, August 20, 2026:
Apha release 0.4.1 is available. I'm cleaning up the code (refactoring for closer MVC adherence, making more Pythonic, etc.) Beta 1.0.0 will be released in a few weeks.

Collisions v0.4.1-alpha has logging of unhandled exceptions to a local file. Also, the user can now see the components of the vectors in the graphs by right-clicking on the particles (vector tips).
- TODOs for later, such as
  - Fix little issues raised by the linter
  - Refactor style strings for maintainability
  - Experiment objects needs to have Transformation objects. Currently transformations are shattered and need a class.

## Introduction
An application in Python (PyQt-PySide6, Matplotlib) for particle accelerator physicists and theoretical physicists working in particle physics, QCD, or nuclear physics. The purpose of the application is to allow physicists to see, rather than having to imagine, the vectors of particle just after particle collisions both in (a.) the laboratory (collider) reference frame and in (b.) a frame obtained by transformation of the vector set with a transformation matrix stipulated by the physicist. The application allows the physicist to enter a set of four-vectors, see them graphed, and vary the vectors on the fly by using sliders, so as to show the results of "what-if" scenarios of interest.

The application is currently available. It is called Collisions-QCD/TMD, and it is in <a href="https://github.com/j-a-ryan/Collisions/releases/tag/v0.4.1-alpha">pre-release version v0.4.1-alpha</a> for Windows and MacOS. More updates will be coming in June. I plan to release a beta version in early summer.

#### More Notes for Software Developers:
The application design is regular, old-fashioned MVC but not PyQt/PySide's native form of MVC (which is MV). So, the application has controller classes, as in regular MVC. (I looked at PyQt's innate MV pattern but I couldn't see its superiority for a complicated application like Collisions. For small applications I suppose it might be nice.)

I am trying to make an application for the specific use-case of a QCD team while keeping reusable components available to be used as a platform for any particle collider physicist who wants to analyze collision vectors of particles in a collider. I am probably failing at this, such that a sizeable refactoring task (for platform creation) will remain after this application is deployed in a stable beta version. As usual, platformability falls by the wayside when there aren't enough man hours to do it. This summer is for refactoring. By September 2026, the code will, I hope, be in fairly good shape, OOP-wise. Then, a platform may begin to be abstracted.

I am an old Java hand (2006 - 2018) with experience in Java for robotics, Java Web development, and many other areas (JDBC, RXTX, JAXP, Vaadin, etc). I more recently became a Python developer, but I'm no Python master. I realize that some of my code is not Pythonic and am working to change that over the course of 2026. If this application takes off while I am busy in graduate school, I will want a collaborator. A Python guru familiar with linear algebra, vaguely acquainted with special relativity, and having an interest in particle physics would fit the bill. Give me a holler. By "take off" I mean that it will need to be refactored into a platform and similar but different applications from Collisions-QCD/TMD built for physicists who have requested them. Alternatively, if the requested new functionality might be fit into Collisions-QCD/TMD that might be the way to go. The "QCD/TMD name could be removed, leaving "Collisions". But we do not want a Frankenapp to evolve. In the ideal case, any physicist who studies the vectors of particles just after particle accelerator collisions would find the application useful. There may be a handful of similar applications based on the same platform and proving useful to these physicists.

## GUI
Below you see a set of vectors in the laboratory (particle collider) reference frame representing the paths of particles emerging from a collision at the origin (left) and their transformation into a different frame (right). One of the six possible 2D representations of these graphs is seen as a popup. Sliders at the left under "CONTROLS" allow the user to vary the vectors and observe the effects on both the 3D graph on the left and the transformation on the right simultaneously. Other controls will eventually be implemented. The application represents the tips of the vectors with circles containing the names of the particles, rather than arrowheads. This may change.

<img width="1915" height="1020" alt="image" src="https://github.com/user-attachments/assets/f25fc4d8-c467-4905-8881-294e07084171" />
<p><i><sub>Figure 1. The GUI. At the far left are sliders for vector components, m<sup>2</sup>, and a boost parameter. The graph on the left is the original vector set, presumably based in the lab (collider) frame. The graph on the right is the transformed set. A popup shows one of the six possible 2D projections (three each for the two 3D graphs.) The light blue circles around two of the particles indicate that those are the two selected by the user for the purpose of configuring the transformation matrix in this instance.</sub></i></p>

Various 4x4 transformation matrices can be used on the four-vectors entered by the user. The vector entry form is shown below:

<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/202a78b2-1214-42f3-9718-02d07bb7a98b" />
<p><i><sub>Figure 2. Vector set entry form.</sub></i></p>

The user selects and configures a transformation as seen below.
<p align="center"><img width="500" alt="image" src="https://github.com/user-attachments/assets/ae62d7f2-200c-4053-9627-f694985c4a69" /></p>

<p><i><sub>Figure 3. The transformation configuration form has popped up. The three checkboxes indicated three types of transformation.The user has selected a two-step transformation.</sub></i></p>

## Transformation Matrices
The application currently applies a transformation matrix described by T.C. Rogers' 2025, "A system for analyzing hadron kinematics" (work-in-progress) as shown below. 

<img width="921" height="765" alt="image" src="https://github.com/user-attachments/assets/8147aeae-9730-4813-b34b-848ead15f22b" />
</br>
<p><i><sub>Figure 4. Image excerpt from T.C. Rogers' 2025, "A system for analyzing hadron kinematics" (work-in-progress) showing the transformation matrix used by Collisions-QCD/TMD.</sub></i></p>

However, Collisions could apply any matrix of interest to physicists. The application could offer a list of matrices for the user to choose from or allow the user to submit a custom matrix. Etc.

## Dependencies
I gratefully use these third-party libraries. I hope I am adhering to their licensing requirements properly. If I am not, kindly let me know.

Uses <a href="https://github.com/niklashenning/pyqt-advanced-slider">PyQt Advanced Slider</a>

Uses <a href="https://github.com/5yutan5/PyQtDarkTheme">PyQtDarkTheme</a>

## Current Status: alpha
August, 2026: Finishing up the last few alpha releases. The first beta version will be released in September.

## License
This software is licensed under the MIT license.
