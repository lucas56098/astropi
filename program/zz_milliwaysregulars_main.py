#
#                                                          /\  /\
#                                                          ||__||
#     _______________          ____________________________( o   \_
#     ______________  /^\   /^\  o ________________________ #\   |_|
#     |\        /|  o |  | |  |      \_________              |   / |
#     | \      / |    |  | |  |  | \           \_________   /____| |
#     | \     /  |  | |  | |  |  |  \    /\       _____  \_(__°_ ) |
#     |  \    /  |  | |  | |  |  |  \    /\    /  ____| |       \__|
#     |  \    /  |  | \  / \  /  |   \  /  \  /  |    | |    | |\
#     |   \  /   |  |  \/   \/   |   \  /  \  /  |    | |    | | \
#     |   \  /   |  |  /\__ /\__ |    \/    \/   |____|  \_  | |  \
#     |    \/    ______________________________________    \_| \
#     |    \/  _//                                     \\_   |  \
#     |      //                                           \_ |   \
#     |     //                                              \| \  |
#     |    //                                               \\  \ |
#     |  ||                                                   || \|
#       //                                                     \\
#     |||                                                       |||
#     |||                                                       |||
#     |||                                                       |||
#
#   This program saves the time, magnet_data, brightness, real position and some pictures.
#   After 175min of saving, the data is going to be analyzed to get the orbit and
#   position of the International Space Station.

from camera_adapter import CameraAdapter
from sense_adapter import SenseAdapter
from led_controller import LedController
from data_manager import DataManager
from calculator import Calculator
import ephem
from ephem import degree
import time
import datetime

error_text = ""

#tle data
name = "ISS (ZARYA)"
line1 = "1 25544U 98067A   20042.59085376  .00001091  00000-0  27837-4 0  9993"
line2 = "2 25544  51.6437 254.8546 0004827 257.1432 132.9530 15.49156046212398"

iss = ephem.readtle(name, line1, line2)

#sense_hat
sense = SenseAdapter()

#led_matrix
led_matrix = LedController()
led_matrix.dont_panic()

#camera
camera = CameraAdapter()

#data_saver
data = DataManager()
data.start()

#start timers
# Recording data for 175 min and analyzing the data in the remaining 5 min
stop_time = time.time() + 60 * 175
# Recording data in 10 sec intervall
measure_time = time.time() + 10

is_camera_running = False

image_record_counter = 0

# recording data
while time.time() < stop_time:
    sense.dummy_measure()

    if not is_camera_running:
        camera.start()
        is_camera_running = True

    if time.time() > measure_time:

        #recording brightness while saving every 25th picture assuming to get 42 images
        if image_record_counter < 25:
            brightness, image_path = camera.brightness()
            image_record_counter += 1
        else:
            brightness, image_path = camera.brightness(True)
            image_record_counter = 0

        camera.end()
        is_camera_running = False

        #measure data
        sense_time, magnet_x, magnet_y, magnet_z = sense.measure()

        #measure position to compare
        now = datetime.datetime.utcnow()
        iss.compute(now)
        sublat = iss.sublat/degree
        sublong = iss.sublong/degree

        #save data
        try:
            data.save(sense_time, magnet_x, magnet_y, magnet_z, brightness, sublat, sublong, image_path)
        except Exception as err:
            error_text += repr(err)

        # update timer
        measure_time = time.time() + 10

        # smile
        led_matrix.smile_a_little_bit()
camera.end()

#calculator
calc = Calculator()

# analyze data in the remaining 5 min
try:
    vector_orbit, vector_day, T, orbit_height, vector_sunrise = calc.analyze()
except Exception as err:
    error_text += repr(err)
else:
    # save result
    data.save_result(vector_orbit, vector_day, T, orbit_height, vector_sunrise)

if (error_text != ""):
    errorlog_file = open("error.txt", "w")
    errorlog_file.write(error_text)
    errorlog_file.close()

led_matrix.show_message("SO LONG, AND THANKS FOR ALL THE FISH")
