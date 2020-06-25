import numpy as np
from scipy import optimize
from coordinate_system_converter import CoordinateSystemConverter
from data_manager import DataManager
from datetime import datetime
import time

class Calculator():
    #analyzes data.csv

    def __init__(self):
        #intializes objects and recieves data
        data = DataManager()
        self.__cord = CoordinateSystemConverter()
        self.__sense_time, self.__magnet_x, self.__magnet_y, self.__magnet_z, self.__brightness = data.read()


    def time_to_next_index(self, time, start_index = 0):
        #returns first index in range of time
        #if time is out of the experiment time, substract orbit duration
        while time > self.__sense_time[-1]:
            time = time - self.__T
        #checking elements from start_index (optional) to length of self.__sense_time
        for i in range(start_index, len(self.__sense_time)):

            #if time is larger than self.__sense_time[i] return index
            if self.__sense_time[i] >= time:
                return i

        raise Exception("There is no time_to_next index for: " + str(time))


    def mag_to_first_index(self, mag, start_index = 0, accuracy = 3):
        #find first index, which has given self.__magnet_z
        while accuracy < 200:

            #checking elements from start_index (optional) to length of self.__magnet_z
            for i in range(start_index, len(self.__magnet_z)):

            #if  self.__magnet_z between self.__magnet_z +- accuracy set start index
                if (self.__magnet_z[i] - accuracy) <= mag and (self.__magnet_z[i] + accuracy) >= mag:
                    return i

            #if no index is found, decrease accuracy
            accuracy += 1
        raise Exception("There is no mag_to_next index for: " + str(mag))


    def get_max_min_index(self):
        #returning index of highest and lowest  self.__magnet_z
        max = 0
        max_index = 0
        min = 100
        min_index = 0

        #check all elements in  self.__magnet_z
        for i in range(len(self.__magnet_z)):

            #if  self.__magnet_z[i] is higher than max set new max
            if max <= self.__magnet_z[i]:
                max = self.__magnet_z[i]
                max_index = i

            #if  self.__magnet_z[i] is lower than min set new min
            if min >= self.__magnet_z[i]:
                min = self.__magnet_z[i]
                min_index = i

        #return indexes
        return max_index, min_index


    def calculate_orbit(self, high_noon):
        #calculates the orbit
        t = np.array(self.__sense_time)
        y = np.array(self.__magnet_z)

        # We want to fit a cosinus function to the data of the z magnatic field component.
        # There for we need a starting function.
        # We are using the fast fourier transform algorithm to get this starting function.
        # This is based on a best practice from the documentation

        # getting the start values with fft
        f = np.fft.fftfreq(len(t), ((t[5]-t[1])/4.0))
        fy = abs(np.fft.fft(y))
        start_freq = abs(f[np.argmax(fy[1:])+1])
        start_amp = np.std(y) * 2.**0.5
        start_offset = np.mean(y)
        start = np.array([start_amp, 2.*np.pi*start_freq, 0., start_offset])

        def cosfunc(t, A, w, p, c):   return A * np.cos(w*t + p) + c


        #fitting the curve
        try:
            popt, pcov = optimize.curve_fit(cosfunc, t, y, p0 = start)
        except Exception as err:
            raise Exception("Fitting impossible: is allowed during testing with no real data")
        A, w, p, c = popt
        #defines orbit duration
        T = (2*np.pi)/w
        self.__T = T

        #transforms cosine to positve amplitude
        if (A < 0):
            A = - A
            p = p + np.pi
        #transfoms p to interval 0 - 2pi
        p = (p + (2*np.pi)) % (2*np.pi)


        #analyzing the curve
        wp1 = int((2.5*np.pi - p)/w)
        wp1_index = self.time_to_next_index(wp1+self.__sense_time[0])

        wp2 = int((3.5*np.pi - p)/w)
        wp2_index = self.time_to_next_index(wp2+self.__sense_time[0])

        maximum_index, minimum_index = self.get_max_min_index()
        maximum = self.__sense_time[maximum_index]
        minimum = self.__sense_time[minimum_index]

        #defining north_offset using maximum and minimum
        north_offset = 0
        if (self.__magnet_x[maximum_index] + self.__magnet_x[minimum_index]) == 0:
            north_offset = np.arctan((self.__magnet_y[maximum_index] + self.__magnet_y[minimum_index])/( 0.0001))
        else:
            north_offset = np.arctan((self.__magnet_y[maximum_index] + self.__magnet_y[minimum_index])/(self.__magnet_x[maximum_index] + self.__magnet_x[minimum_index]))

        #calibrates magnet data
        cal_magnet_x = [self.__magnet_x[i] * np.cos(north_offset) - self.__magnet_y[i] * np.sin(north_offset) for i in range(len(self.__magnet_x))]
        cal_magnet_y = [self.__magnet_x[i] * np.sin(north_offset) + self.__magnet_y[i] * np.cos(north_offset) for i in range(len(self.__magnet_y))]


        #inclination
        if ( cal_magnet_y[wp1_index - 1] + cal_magnet_y[wp1_index] +cal_magnet_y[wp1_index +1]) == 0:
            inclination_1 = np.arctan( (cal_magnet_x[wp1_index - 1] + cal_magnet_x[wp1_index] + cal_magnet_x[wp1_index + 1]) / (0.0001))
        else:
            inclination_1 = np.arctan( (cal_magnet_x[wp1_index - 1] + cal_magnet_x[wp1_index] + cal_magnet_x[wp1_index + 1]) / ( cal_magnet_y[wp1_index - 1] + cal_magnet_y[wp1_index] +cal_magnet_y[wp1_index +1]))

        if ( cal_magnet_x[wp2_index - 1] + cal_magnet_x[wp2_index] +cal_magnet_x[wp2_index +1]) == 0:
            inclination_2 = np.arctan((cal_magnet_y[wp2_index - 1] + cal_magnet_y[wp2_index] + cal_magnet_y[wp2_index + 1])/0.0001)
        else:
            inclination_2 = np.arctan((cal_magnet_y[wp2_index - 1] + cal_magnet_y[wp2_index] + cal_magnet_y[wp2_index + 1])/( cal_magnet_x[wp2_index - 1] + cal_magnet_x[wp2_index] +cal_magnet_x[wp2_index +1]))


        inclination = (abs(inclination_1) + abs(inclination_2))/2

        #longitude
        #calculates real high noon time (time at minimum + fraction of T (because we know the angle of r_h_n))
        r_h_n_time = self.__sense_time[minimum_index]+(T*(self.__cord.get_day_night_phi(high_noon)/(2*np.pi)))

        #if minimum is out of measurement time, subtract orbit duration until it fits
        if minimum > self.__sense_time[0] + T:
            minimum = minimum - T
            minimum_index = self.time_to_next_index(minimum)

        #if r_h_n_time is out of measurement, subtract orbit duration until it fits
        while r_h_n_time >= self.__sense_time[-1]:
            r_h_n_time = r_h_n_time - T


        #calculates time, when longitude is 0
        phi_0_time = minimum + (r_h_n_time - high_noon)


        #if phi_0_time is out of measurement, subtract orbit duration until it fits
        while phi_0_time >= self.__sense_time[-1]:
            phi_0_time = phi_0_time - T


        #calculates time delta between minimum and phi_0
        delta_t = phi_0_time - (minimum)

        #calculates correction angle
        a = w * delta_t

        #gets cartesian vector of orbit
        vector_m = self.__cord.polar_to_cartesian(a, inclination)

        return vector_m, T


    def night(self,i):
        #returns, if it is night
        if ( i <= ( len(self.__brightness) - 3 ) ):
            if (  ( int(self.__brightness[i]) + int(self.__brightness[i+1]) + int(self.__brightness[i+2]) ) <= 180 ):
                return True
        return False


    def get_high_noon(self):
        #analyzes the brightness data to get sunrise
        is_first_night = False
        is_first_day = False

        for i in range(len(self.__brightness) - 3 ):

            #waiting for day night transition
            if (self.night(i) or is_first_night):
                is_first_night = True
                #waiting for first sunrise
                if (not self.night(i) or is_first_day):
                    if (not is_first_day):
                        t1_index = i+3
                        t1 = self.__sense_time[t1_index]
                    is_first_day = True
                    #waiting for sunset
                    if (self.night(i)):
                        t2_index = i+3
                        t2 = self.__sense_time[t2_index]

                        #the middle of sunrise (t1) and sunset (t2) is high_noon
                        return (t1+t2)/2
        raise Exception('There are no day night transitions!')


    def get_orbit_height(self,duration):
        #returns orbit_height
        orbit_height = (((6.6743e-11*(duration**2)*5.9722e24)/(4*(np.pi**2)))**(1/3))-6371000

        return orbit_height


    def analyze(self):
        #returns results
        high_noon = self.get_high_noon()
        vector_orbit, T = self.calculate_orbit(high_noon)
        orbit_height = self.get_orbit_height(T)
        vector_day = self.__cord.get_day_night(high_noon)
        vector_sunrise = np.cross(vector_day, vector_orbit)
        vector_sunrise = vector_sunrise/np.linalg.norm(vector_sunrise)

        return vector_orbit, vector_day, T, orbit_height, vector_sunrise
