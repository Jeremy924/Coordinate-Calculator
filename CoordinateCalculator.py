import cv2
from math import *
import keyboard


class VexUMap:
    def __init__(self):
        # new coordinate system defined by user
        self.start_pos = None  # the origin on the map entered by the user
        self.start_angle = None  # the angle of the new coordinate system entered by the user

        self.last_pos = None  # the previous location entered by the user

        self.step_count = 0  # the number of steps entered by the user

        self.generate_code = True

        print("\033[1;92mClick on starting position\033[0m")

    def _to_output(self, translated_x_in, translated_y_in, angle_deg):
        if angle_deg is not None:
            if self.generate_code:
                print(f'path.\033[96madd_turn\033[0m(\033[93mMyTurn\033[0m(\033[95m{angle_deg:.0f}_deg\033[0m));')
            else:
                print(f"\t({angle_deg:.2f} degrees relative to last step)")

        if self.generate_code:
            print("path.\033[96madd_straight\033[0m(\033[93mStraight\033[0m({" + f'\033[95m{translated_x_in:4.0f}_in\033[0m,' + f'\033[95m{translated_y_in:4.0f}_in\033[0m, \033[95m0_deg\033[0m' +
                  '}, \033[95m0_s\033[0m, \033[93mMOTOR_SPEED\033[0m::\033[95mMID\033[0m));')
        else:
            position_string = f"{translated_x_in:6.2f}, {translated_y_in:6.2f}"
            print(f"{self.step_count + 1:3}: {position_string:20}", end='')

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

        # increment the number of steps
        self.step_count += 1

        relative_angle = None
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
        self._to_output(final_pos[0], final_pos[1], relative_angle)
        self.last_pos = final_pos

    def click_event(self, event, x, y, flags, params):
        if event == cv2.EVENT_LBUTTONDOWN:
            # field is 12 ft x 12 ft
            pos_in_inches = x / width * 144, -y / height * 144

            if self.start_pos is None:  # if no origin has been specified, then set the first point as the origin
                self.start_pos = pos_in_inches
                print("Starting position set\n")

                # get the angle of the coordinate system
                # angle is negative because angles are flipped for reckless driver
                self.start_angle = -float(input("\033[1;92mEnter starting angle in degrees (clockwise is positive):\033[0m"))
                print("Starting angle set\n\nClick on first location on map:")
                if self.generate_code:
                    print("\n\033[4mCode Output:\033[0m\n\033[93mPath\033[0m path;")
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
