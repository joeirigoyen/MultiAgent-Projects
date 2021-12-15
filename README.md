# Multi-agent projects

This repository contains a series of activities and documents elaborated during the Multi-Agent Systems Modelling course. There are two main projects within this repository:

## Actividad Integradora
This is a warehouse-like simulation where a given number of robots attempt to put a series of boxes in an available deposit cell (*meaning the deposit doesn't contain more than 5 boxes*) in a given area. The program utilizes the ***mesa*** package in order to achieve an agent-oriented programming paradigm. The simulation can be visualized in a browser by running the **robot_visualizer.py** file. Also, it might be visualized in Unity if it's installed in your local machine following these steps:

  - **Step 1:** In the Unity Editor, open the main scene and click on the Controller GameObject. You will see a script called AgentController within it's components. 
  - **Step 2:** Edit the script's serialized variables as you wish:
    - ***Robots:*** Specifies the amount of robots that will be looking for boxes and putting them back to their deposits.
    - ***Boxes:*** Specifies the amount of boxes to be stored by the robots. Make sure the number you put in does not exceed the total number of cells within the simulation.
    - ***depot_x:*** It's the number of columns a depositing area will contain. 
    - ***depot_y:*** It's the number of rows a depositing area will contain. Make sure none of these variables exceed the total cell limit.
    - ***Width:*** It's the number of columns the whole simulation area will have.
    - ***Height:*** It's the number of rows the whole simulation area will have.
    - ***max_steps:*** It's the step limit the simulation will have. Once the simulation exceed the specified amount, the robots will stop moving.
    - ***Update Time:*** It's the time between each of the steps taken in the simulation.
    - ***NOTE:*** *Timer and Dt might not be necessary to edit since they change to their default values before the start of the simulation.*
  - **Step 3:** Run the simulation's server by running the **robot_server.py** file in your command line. Do not close it.
  - **Step 4:** Run the program inside the Unity Editor by clicking on the Run button.

If you want to know in more detail about the agents' communication protocol, the agents' structure or the goals of the project, check the documents within the same folder as the simulation.

## Final Project

![Demo](https://media.giphy.com/media/0SI4m4E7LFcxT3INFM/giphy-downsized-large.gif)

Simulates traffic by using a cooperation system between agents that lets them decide when to let other car go first, as well as when to stop by using the traffic lights as a reference. Avoids crashing at all costs. Also, every car has a pre-generated path using an A* implementation. The whole simulation is actually done in **python** by using **mesa** to model the agents' behaviour, but the positions and states are passed from Flask to a **C# script** that is run by **Unity** to make the 3D visualization.

The instructions for installation and execution can be found here: https://drive.google.com/file/d/1dqQ8jMA8D8s7RFy_AzHuNuy-B0zpqAqP/view?usp=sharing
