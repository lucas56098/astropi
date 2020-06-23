class DataManager():
    #writes the data into csv file


    def start(self):
        #initializes the data.csv
        file = open("data.csv", "w")
        file.write("sense_time,magnet_x,magnet_y,magnet_z,brightness,sublat,sublong,image_path\n")
        file.close()

    def save(self, sense_time, magnet_x, magnet_y, magnet_z, brightness, sublat, sublong, image_path):
        #saves data into csv
        #permitting to save 0 to avoid ZeroDivisionError
        if sense_time == 0:
            sense_time += 0.001
        if magnet_x == 0:
            magnet_x += 0.001
        if magnet_y == 0:
            magnet_y += 0.001
        if magnet_z == 0:
            magnet_z += 0.001
        if brightness == 0:
            brightness += 0.001
        file = open("data.csv", "a")
        file.write(str(sense_time) + "," + str(magnet_x) + "," + str(magnet_y) + "," + str(magnet_z) + "," + str(brightness) + "," + str(sublat) + "," + str(sublong) + "," + str(image_path) + "\n")
        file.close()


    def save_result(self,vector_orbit, vector_day, T, orbit_height, vector_sunrise):
        #saving data into result csv
        resultfile = open("result.txt", "w")
        resultfile.write(str(vector_orbit) + "," + str(vector_day) + "," + str(T) + "," + str(orbit_height) + "," + str(vector_sunrise))
        resultfile.close()


    def read(self):
        #reads data from csv
        file = open("data.csv", "r")

        data_array = []
        sense_time = []
        magnet_x = []
        magnet_y = []
        magnet_z = []
        brightness = []

        for line in file:
            data_array.append(line.split(","))

        data_array.pop(0)

        for i in range(len(data_array)):
            sense_time.append(float(data_array[i][0]))
            magnet_x.append(float(data_array[i][1]))
            magnet_y.append(float(data_array[i][2]))
            magnet_z.append(float(data_array[i][3]))
            brightness.append(float(data_array[i][4]))

        file.close()

        return sense_time, magnet_x, magnet_y, magnet_z, brightness
