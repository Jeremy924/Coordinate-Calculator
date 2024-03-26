import cv2
from math import *


class VexUMap:
    def __init__(self):
        # new coordinate system defined by user
        self.start_pos = None  # the origin on the map entered by the user
        self.start_angle = None  # the angle of the new coordinate system entered by the user

        self.last_pos = None  # the previous location entered by the user

        self.step_count = 0  # the number of steps entered by the user

        print("Click on starting position")

    def _compute_location(self, x_in, y_in):
        # calculate location relative to the origin entered by the user
        orig_pos = x_in - self.start_pos[0], y_in - self.start_pos[1]

        # calculate the magnitude of the vector pointing to the position
        magnitude = sqrt(orig_pos[0] ** 2 + orig_pos[1] ** 2)

        if 0.05 > orig_pos[0] > -0.0005:  # if x is small, then is may result in a divide-by-zero error
            old_angle = 90 if orig_pos[1] < 0 else 270
        else:
            old_angle = degrees(atan(orig_pos[1] / orig_pos[0]))

        # if the x-value is less than 0, then shift the angle over by 180 degrees, because arc tan goes from -90 to 90
        if orig_pos[0] < 0:
            old_angle += 180

        new_angle = old_angle - self.start_angle  # new angle relative to the offset entered by user

        # calculate the position on the new coordinate system, using trig
        final_pos = cos(radians(new_angle)) * magnitude, -sin(radians(new_angle)) * magnitude

        # format and output the new position
        position_string = f"({final_pos[0]:6.2f}, {final_pos[1]:6.2f})"
        print(f"{self.step_count + 1:3}: {position_string:20}", end='')

        # increment the number of steps
        self.step_count += 1

        # output the angle relative to the previous step
        if self.last_pos is None:
            print()  # if there was no previous angle, then just end the line
        else:
            # calculate the vector from the last position to the current position
            diff = final_pos[0] - self.last_pos[0], final_pos[1] - self.last_pos[1]

            # if the x-value is too small, it may result in a divide-by-zero error
            if abs(diff[0]) < 0.0005:
                relative_angle = 0 if final_pos[1] > self.last_pos[1] else 180
            else:
                relative_angle = degrees(atan(diff[1] / diff[0]))

            # if the x-value is less than 0, then add 180 because arc-tan goes from -90 to 90
            if diff[0] < 0:
                relative_angle += 180

            # all angles should be positive, to make formatting better
            if relative_angle < 0:
                relative_angle += 360

            print(f"\t({relative_angle:.2f} degrees relative to last step)")

        self.last_pos = final_pos

    def click_event(self, event, x, y, flags, params):
        if event == cv2.EVENT_LBUTTONDOWN:
            # field is 12 ft x 12 ft
            pos_in_inches = x / width * 144, -y / height * 144

            if self.start_pos is None:  # if no origin has been specified, then set the first point as the origin
                self.start_pos = pos_in_inches
                print("Starting position set")

                # get the angle of the coordinate system
                # angle is negative because angles are flipped for reckless driver
                self.start_angle = -float(input("Enter starting angle in degrees (clockwise is positive): "))
                print("Starting angle set\n\nClick on first location on map:")
            else:
                # if the origin has already by set, then compute the next spot
                self._compute_location(pos_in_inches[0], pos_in_inches[1])


if __name__ == "__main__":
    # load the image from the file
    img = cv2.imread("map.png", 1)

    # scale the image so that it fits on the screen
    scale_percent = 50
    width = int(img.shape[1] * scale_percent / 100)
    height = int(img.shape[0] * scale_percent / 100)
    dim = (width, height)

    resized = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)

    map = VexUMap()
    cv2.imshow("Vex U Map", resized)
    cv2.setMouseCallback("Vex U Map", map.click_event)

    cv2.waitKey(0)
    cv2.destroyAllWindows()
