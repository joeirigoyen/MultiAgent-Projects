# MultiAgentes

This repository contains a series of activities and documents elaborated during the Multi-Agent System Modelling course. There are two main programs within this repository:

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

If you want to know in more detail about the agent communication protocol, the agents' structure or the whole objective of the project, check the documents within the same folder as the simulation.

## Final Project

![Demo](https://media1.giphy.com/media/0SI4m4E7LFcxT3INFM/giphy.gif?cid=790b76116c71c3023888ba3b7c4dec16373a271d898ca1a6&rid=giphy.gif&ct=g "Demo")

This project is still under it's development phase. This project simulates traffic in a particular area, where each of the cars present during the simulation will have a point to travel to, avoiding collisions with any other car, a building or any other obstacle, as well as taking care of the state of the lights' states to decide whether to stop or keep going. This also utilizes the ***mesa*** package since it makes use of the multi-agent paradigm. Also, the cars re-trace their trajectories on each step using the A* algorithm to avoid collisions. This project can be visualized in 2D using a browser, but Unity can be used to visualize it in 3D with more realistic models.
