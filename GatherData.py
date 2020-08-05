import os
import glob
import time
from gpiozero import LED

#USER DEFINED SETTINGS:
#==================================================
#allows the user to switch between fahrenheit and celsius readings
#it tells the code which value to use when returning read_temp
    #0 for celsius and 1 for fahrenheit
degree = 0 

 #switches to danger if temp is greater than or equal to:
hTemp_dang = 30
 #switches to danger if temp is less than or equal to:
lTemp_dang = 20

#controls how many data points are taken 
#before the data is saved to a text file
size = 4

#sets how long the until the next sample is taken
tDelay = 4
#==================================================




#CODE FROM https://www.circuitbasics.com/raspberry-pi-ds18b20-temperature-sensor-tutorial/
#slightly modified
#==================================================

#Goes to the the directory in which w1_slave exits
#w1_slave contains raw data from the sensor
base_dir = '/sys/bus/w1/devices/'

#If multiple sensors are used the '28*' will have to be changed to accomidate that
#The following functions read_temp_raw and read_temp could be added to a loop and each iteration
 #of the loop could be a different sensor
device_folder = glob.glob(base_dir + '28*')[0]

#Gets the data from w1_slave
device_file = device_folder + '/w1_slave'

#Reads all the data from w1_slave
def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines

#Returns just the temperature data from w1_slave
def read_temp():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c= float(temp_string) / 1000.0
        temp_f = temp_c *9.0 /5.0 + 32.0
        return temp_c, temp_f
#==================================================



#VARIABLES USED IN MAIN PART OF CODE: 
#==================================================
#initialize two arrays of size 'size' 
    #samp is the raw sample data of the sensor
samp = [0] * size
    #indicator is an array comprised of three states
        #H indicates the temperater is High
        #N indicates the temperater is Normal
        #L indicates the temerpater is Low
indicator = ['']* size

#i is the variable that iterates through an array till it equals 'size-1'
i = 0

#initializes the GPIO pins used for the LEDs and sets the name to be used
#latter in the code
Hled = LED(14)
Nled = LED(15)
Lled = LED(18)
#==================================================




while True:
    #GETTING AND SAVING A SAMPLE:
    #==================================================
    #gets a reading from the sensor
    temp = read_temp()

    #saves reading into the samp array
    samp[i] = temp[degree]

    #used for testing purposes to make sure data is being added to the array
    ##print(str(samp))
    #==================================================

    #EXAMINE THE SAMPLE: 
    #================================================== 
    #Check to see if the reading is to high
    if (temp[degree] >= hTemp_dang):
        #Used to test if there are no LEDs present
        print('Danger temperture is HIGH')
        
        #Adds the appropriate temperature indicator to the 'indicator' array
        indicator[i] = 'H'

        #Turns off the Normal LED without this it will remain on
        Nled.off()
        #Turns on the High LED
        Hled.on()
    #Check to see if the reading is to low
    elif ( temp[degree] <= lTemp_dang):
        #Used to test the code if there are no LEDs present
        print('Danger temperture is LOW!')
        
        #Adds the appropriate temperature indicator to the 'indicator' array
        indicator[i] = 'L'

        #Turns off the Normal LED and turns on the Low LED
        Nled.off()
        Lled.on()

    #If the sensor is above the High temp or below the Low temp then it is in the user normal range
    else:

        #Adds the appropriate temperature indicator to the 'indicator' array
        indicator[i] = 'N'
        
        #Sets the LEDs to the Normal LED being the only one on
        Nled.on() 
        Hled.off()
        Lled.off()
    #================================================== 
   
    #CREATES A TEXT FILE AND RESETS BOTH ARRAYS:
    #================================================== 
    #Checks to see if the max size of the array has been reached
    if (i == size-1):

        #Opens the file with name 'temperatureData'/ Creates a file of the same name if one does not exist
        #This operation earses the previous file if this is not desired and appending the new data 
        # is more desired change 'w' to 'a'
        f = open('temperatureData', 'w')
        
        #Creates a string for f.write comprised of two lines the first being the raw sample data
         #and the second being the indicator array
        string = str(samp) + '\n' + str(indicator)
        #Adds two lines to the file the first being the raw data the second line adds the indicator array
        f.write(string)

        #Closes the file
        f.close()
        #Used for testing purposes to make sure the file was written to
        ##f = open('temperatureData', 'r')
        ##print('Reading the file') 
        ##print(f.read())

        #Resets i for the next iteration through the code
        #-1 one is used as aftter this statement i will be increasing by one back to 0 
         #which is the start of the arry
        i = -1

        #Resets both arrays back to a 0 state
        samp = [0] * size
        indicator = [''] * size
    #================================================== 

    #Interates through the array
    i = i+1

    #Delays taking the next sample by tDelay seconds
    time.sleep(tDelay)

    #END OF CODE
