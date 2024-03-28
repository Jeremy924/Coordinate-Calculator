# Coordinate-Calculator
A tool for calculating coordinates with the ReveilLib API. 

### How to Use
After launching the script, an image should appear representing the Vex U Over Under field. 
Click on the image to select the starting position of the robot (0,0).
Next, in the terminal, type in the angle that the robot will start at. 0 degrees is horizontal to the right, and positive is clockwise. This angle will be set as 0 degrees. 

Click on the first point in the robot's path. The program will output the position relative to the robot's starting angle and position, in inches.

After each click on the map, the program will output the position relative to the start position and angle. Additionally, the program will output the angle (relative to the starting angle) that the robot would need to turn to to go straight to that point from the previous point. Note that all angles outputted will be positive. 
