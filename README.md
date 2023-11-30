# In flight orbit calculation - Milliways Regulars
### This high school project was part of the Astro Pi Mission Space Lab 19/20
Welcome at the Milliways regulars repository. Have fun looking through our Project and have a Pan Galactic Gargle Blaster!

### 1. Introduction
We aimed to investigate the possibility of calculating the orbit and position of the ISS with a Raspberry Pi. This is interesting, because in space it is very important to know the orbit. Without that no one would be able to interact with the space station let alone docking resupply missions. The hardware required for orbit and position determination is cheap and lightweight, and therefore might be useful for CubeSats. We expected to be able to determine the orbit partially during flight, as well as learning about orbit calculation and ways to improve them afterwards.

### 2. Method
During flight the program we developed recorded the unixtime, the raw magnet data, the brightness of the IR-Camera and for reference the latitude and longitude. This data was stored in a csv-file. Aditionally 17 Images were saved to see if the brightness method works. Because the ISS spins once during every rotation we expected the magnet-z data to form a cosine wave with maxima, minima and turning points representing the corresponding orbit positions. The program executed a Fast Fourier Transform and a Scipy method to fit the cosine over the data. Thanks to the north at the maximum and minimum, the program was able to calibrate the data and then calculate the inclination using the turning points and the arctangent. Finally, the program used the time, the day-night transitions and the normalized cross product to determine the longitude of the minimum and the position at sunrise. The results were saved in another file. On earth we only illustrated our results.

![Image](./project%20reports/figures/example_image.jpg)
Figure 1: yellowstone nationalpark (taken during mission)

### 3. Results
<div style="float: right; margin: 10px;">
  <img src="./project reports/figures/Figure_1.png" width="300" />
  <figcaption>Figure 2: measurement intervals</figcaption>
</div>
During flight 461 rows of data were recorded. No exception was raised, the fit worked and the day night transitions were correct. The results were saved in the result-file. As seen in Figure 2 the measurement intervals were quite inconsistent and long, considering that we programmed an Intervall of 10s. The average of 22,8s affected the precision of our calculations. The ISS travels about 200km during that time. We also analyzed if the fit-Method worked well. Figure 3 illustrates the connection between magnet-z (blue) and the inclination (green). One can also see that the cosine (orange) was fitted quite well, even though there where some irregularities in the magnetic field in the southern hemisphere. The calculated inclination was 52,26° and the orbital period was 94,1min which corresponds to an orbit height of 475,7km. 

![Image](./project%20reports/figures/Figure_2.png)
Figure 3: magnet-z and fit-method

In the next step we analyzed the efficiency of the brightness-Method. As seen in Figure 4 the day-night-transitions (orange) were calculated well using the brightness data (blue). The calculated longitude of the minimum was 96,25°, which was in the expected range between 92° and 136°, although we underestimated the rotation of the earth wich caused this vague range. The earth rotates about 45° during flight time.

![Image](./project%20reports/figures/Figure_3.png)
Figure 4: day night transitions

In Figure 5 we illustrated the calculated orbit (red) on a equirectangular projection of the earth and also highlighted the actual position (grey). This proves that the orbit calculation worked surprisingly well. The only mayor inaccuracy is because of the rotation of the earth, which we did not consider in our calculations.

![Image](./project%20reports/figures/fit.png)
Figure 5: calculated orbit versus real orbit

### Conclusion
<div style="float: right; margin: 10px;">
  <table>
    <tr>
      <th>parameter</th>
      <th>true</th>
      <th>calculated</th>
    </tr>
    <tr>
      <td>orbital period</td>
      <td>93min</td>
      <td>94.1min</td>
    </tr>
    <tr>
      <td>height</td>
      <td>320-410km</td>
      <td>475.7km</td>
    </tr>
    <tr>
      <td>inclination</td>
      <td>51.5&deg;</td>
      <td>52.26&deg;</td>
    </tr>
    <tr>
      <td>longitude of the minimum</td>
      <td>92-136&deg;</td>
      <td>96.25&deg;</td>
    </tr>
  </table>
</div>
Our program was executed flawlessly over the 180 minutes. The data were saved in the csv-file, evaluated during the flight and the orbit parameters were stored in the result-file. The fit-Method worked well, and so the orbital period and the height were determined approximately. Furthermore, the assumptions could be confirmed that the inclination is related to magnet-z and that day and night could be easily determined with the camera. The earth's rotation was responsible for the biggest inaccuracy, which should be taken into account in the future. In addition, an improvement would certainly be possible if the magnetic field was not assumed to be a bar magnet, considering the anomaly in the southern hemisphere. To conclude, one can state that the Astro Pi can determine the orbit of the ISS surprisingly well. However, due to the high speed in space, the smallest inaccuracy in space already leads to significant position deviations, which is why the accuracy of the program is not precise enough to use it for rendezvous or other interactions.




<p align="center">
  <img src="./project reports/figures/raspberrypi.png" height="100" />
  <img src="./project reports/figures/astropi.png" height="100" /> 
  <img src="./project reports/figures/esa_logo.png" height="100" />
</p>