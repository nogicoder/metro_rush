1. The name of the team: The Bohemian
2. The working hours/days each member commits to: at least 20 hours per week
      + We gather at least two times a week to discuss all of the problems and merge code
      + The fixed time: 5pm in the afternoon
      + The working hour of each member:
            + mbach: 5h/day
            + nlequan: 3h/day
            + vnam: 5h/day

3. How often you will check-in with each others' progress: Once a day
4. The strengths and weaknesses of each member, and how to leverage/mitigate them for the project:
      + mbach:
              - strengths: Focus, long working hour, deep research on related topics
              - weaknesses: Lack of experience in coding
      + nlequan:
              - strengths: Highly experienced with OOP and graph-plan
              - weaknesses: Short working hour due to office work
      + vnam:
              - strengths: Research skill on problems
              - weaknesses: Lack of coding skill
5. The allocation of the workload: *The status: research => implement => test => done* 
        + Date: Fri Jan 04/2019 - 1st => *MEMBERS*: MBACH, VNAM JOINED THE MEETING
                _CONTENT_ : Research on the aspects of project
                _DISCUSSION_ :
                    + WORK ALLOCATION FOR THE PROJECT:
                        (-) mbach: Research on path-finding algorithm to apply
                        (-) vnam: Research on graph theory and how to represent the metro system
                _DEADLINE: Sun Jan 06/2019 
        + Date: Sun Jan 06/2019 - 2nd => *MEMBERS*: MBACH, VNAM, NLEQUAN JOINED THE MEETING
                _CONTENT_ : Building the Skeleton and elements of the project
                _DISCUSSION_ :
                    + WORK ALLOCATION FOR THE PROJECT:
                        (-) mbach: Applying Dijkstra to find the shortest path
                        (-) vnam: Figure out way to visualize the metro system through Pyglet
                        (-) nlequan: Structure the skeleton of the script (including these classes: Train, Line, Station, Action classes)
                _DEADLINE: Tue 08/2019 
        + Date: Wed Jan 09/2019 - 3rd => *MEMBERS*: MBACH, VNAM, NLEQUAN JOINED THE ONLINE MEETING
                _CONTENT_ : Building the Skeleton and elements of the project
                _DISCUSSION_ :
                    + WORK ALLOCATION FOR THE PROJECT:
                        (-) mbach: Finished shortest path -> adapt to the script structure
                        (-) vnam: Finished the representation for metro system through Pyglet -> visualizing Train
                        (-) nlequan: Finished the skeleton -> Employing the movement of the train and printing out result
                _DEADLINE: Thu Jan 10/2019
        + Date: Thu Jan 10/2019 - 3rd => *MEMBERS*: MBACH, VNAM, NLEQUAN JOINED THE MEETING
                _CONTENT_ : Applying Algorithm to direct the trains & Pyglet description of train movement
                _DISCUSSION_ :
                    + WORK ALLOCATION FOR THE PROJECT:
                        (-) mbach: Finished adaptation -> Pyglet and adding test cases
                        (-) vnam: Visualizing Train
                        (-) nlequan: Finished train movement -> Employing algorithm
                _DEADLINE: Sat Jan 12/2019
        + Sun Jan 13/2019: Finalizing and refactoring codes

6. The features you want to implement and how they interface together:
        + The core algorithm: Train moving along 1 path with subsequence train lining up
        + The bonus algorithm: Solving the case when there are multiple stations before the ending stations -> no bottleneck
        + Pyglet representation of the train moving and metro system, based on the objects and actions defined in the previous features
        Note: 
                + Handle cases of data file that might lead to error
                + Test cases for each code blocks (doctest)
                + Handle argument passing
