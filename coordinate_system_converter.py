import numpy as np

class CoordinateSystemConverter:
    #converts polar to cartesian and returns other vectors

    def polar_to_cartesian(self, phi, theta, r=1):
        #transforms polar to cartesian coordinates
        x = r * np.cos(phi) * np.sin(theta)
        y = r * np.sin(phi) * np.sin(theta)
        z =               r * np.cos(theta)

        return np.array([x, y, z])


    def get_day_night(self, unixtime):
        #calculates day_night vector at a specific time
        #vector points from the middle of the earth to the sun
        t = (unixtime + 43200) % 86400
        phi = (2*np.pi)-(t/86400 *  2*np.pi)
        theta = (  ((23.44* np.pi)/180) * np.sin(((2*np.pi*((self.day_of_year(unixtime))-81)/365))))+(np.pi/2)

        return self.polar_to_cartesian(phi,theta)


    def get_day_night_phi(self, unixtime):
        #calculates day_night vector at a specific time
        t = (unixtime + 43200) % 86400
        phi = (2*np.pi)-(t/86400 *  2*np.pi)

        return phi


    def day_of_year(self,unixtime):
        #calculates day of the year
        #tropical year in seconds
        return (unixtime % (31556925.261))/60/60/24
