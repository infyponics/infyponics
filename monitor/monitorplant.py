'''
Created on Jun 4, 2016

@author: Debanjan.Mahata
'''
import requests
import json
import sys
import config
import yagmail
import csv
from time import sleep
from config import DEVICE_PLANT_MAPPING 
from config import PLANT_DEVICE_MAPPING
from config import DEVICE_STALE_DATA_MINS
from config import CAM_STALE_DATA_MINS
from config import max_ph, min_ph
from config import max_ec, min_ec
from config import max_tfw, min_tfw
from config import max_tbw, min_tbw
from config import proxy
from config import DEVICE_CONN_NO_TRIES
from config import DEVICE_CONN_WAIT_TIME
from config import GROWTH_URL
from config import proxies
from dateutil import parser
from datetime import datetime
from utility import time_diff
from utility import to_datetime
from utility import variance
from datetime import timedelta
from config import report_emails
from config import admin_email, admin_passwd

class Plant:
    """Class representing individual plants monitored by the system"""
    def __init__(self, plant_id):
        #id allocated to the plant
        self.plant_id = plant_id
        #id of the photon device monitoring the plant
        self.plant_device_id = None
        #name of the photon device monitoring the plant
        self.plant_device_name = None
        #pH value of the solution containing the plant
        self.ph = None
        #Electrical Conductivity value of the solt containing the plant
        self.ec = None
        #Time between watering set for the plant
        self.tbw = None
        #Time for watering set for the plant
        self.tfw = None
        #Current height of the plant as captured by the camera
        self.current_height = None
        #Current growth of the plant as captured by the camera
        self.current_growth = None
        #Growth of the plant as captured on the previous day
        self.last_day_growth = None
        #Height of the plant as captured on the previous day
        self.last_day_height = None
        #Hourly growth difference
        self.hourly_growth_diff = None
        #Hourly height difference
        self.hourly_height_diff = None
        #Daily growth difference
        self.daily_growth_diff = None
        #Daily height difference
        self.daily_height_diff = None
        #Time when the factors of the system were manipulated
        self.last_time_manipulated = None
        #Time when the reading of the measurements were taken
        self.read_time = None
        #Time when the plant was last heard
        self.last_time_heard = None
        #Time when the camera shot was taken for measuring height and growth
        self.cam_shot_time = None
        #Indicates whether the reading currently recorded is stale due to
        #loss in connection
        self.stale_read_flag = False
        #Indicates whether the reading currently recorded is stale due to loss
        #in connection with the camera
        self.stale_cam_flag = False
        #Flag indicating whether the pH value recorded is abnormal 
        self.abnormal_ph_val_flag = False
        #Flag indicating whether the EC value recorded is abnormal
        self.abnormal_ec_val_flag = False
        #Flag indicating whether the time between watering is abnormal
        self.abnormal_tbw_flag = False
        #Flag indicating whether the time for watering is abnormal
        self.abnormal_tfw_flag = False
        
    def get_plant_id(self):
        """Gets the plant id"""
        return self.plant_id
    
    def get_plant_device_id(self):
        """Gets the id of the photon device to which the plant is connected"""
        return self.plant_device.get_device_id()
    
    def get_plant_device_name(self):
        """Gets the name of the device to which the plant is connected"""
        return self.plant_device.get_device_name()
    
    def get_ph(self):
        """Gets the pH value of the solution for the plant"""
        return self.ph
    
    def set_ph(self, ph):
        """Sets the pH value of the solution for the plant"""
        self.ph = ph
        
    def get_ec(self):
        """Gets the EC value of the solution for the plant"""
        return self.ec
    
    def set_ec(self, ec):
        """Sets the EC value of the solution for the plant"""
        self.ec = ec
        
    def get_tbw(self):
        """Gets the time between water value for the plant"""
        return self.tbw
    
    def set_tbw(self, tbw):
        """Sets the time between water value for the plant"""
        self.tbw = tbw
        
    def get_tfw(self):
        """Gets the time for water value for the plant"""
        return self.tfw
    
    def set_tfw(self, tfw):
        """Sets the time for water value for the plant"""
        self.tfw = tfw
    
    def get_current_height(self):
        """Gets the current height for the plant"""
        return self.current_height
    
    def set_current_height(self, curr_height):
        """Sets the current height for the plant"""
        self.current_height = curr_height
        
    def get_current_growth(self):
        """Gets the current growth for the plant"""
        return self.current_growth
    
    def set_current_growth(self, curr_growth):
        """Sets the current growth for the plant"""
        self.current_growth = curr_growth
        
    def get_last_day_growth(self):
        """Gets the Growth of the plant as captured on the previous day """
        return self.last_day_growth
    
    def set_last_day_growth(self, last_day_growth):
        """Sets the Growth of the plant as captured on the previous day """
        self.last_day_growth = last_day_growth
        
    def get_last_day_height(self):
        """Gets the Height of the plant as captured on the previous day"""
        return self.last_day_height
    
    def set_last_day_height(self, last_day_height):
        """Sets the Height of the plant as captured on the previous day"""
        self.last_day_height = last_day_height
        
    def get_daily_growth_diff(self):
        """Gets the Daily growth difference"""
        return self.daily_growth_diff
    
    def set_daily_growth_diff(self, daily_growth_diff):
        """Sets the Daily growth difference"""
        self.daily_growth_diff = daily_growth_diff
    
    def get_daily_height_diff(self):
        """Gets the Daily height difference"""
        return self.daily_height_diff
    
    def set_daily_height_diff(self, daily_height_diff):
        """Sets the Daily height difference"""
        self.daily_height_diff = daily_height_diff
        
    def get_hourly_height_diff(self):
        """Gets the Hourly height difference"""
        return self.hourly_height_diff
    
    def set_hourly_height_diff(self, diff):
        """Sets the Hourly height difference"""
        self.hourly_height_diff = diff
        
    def get_hourly_growth_diff(self):
        """Gets the Hourly growth difference"""
        return self.hourly_growth_diff
    
    def set_hourly_growth_diff(self, diff):
        """Sets the Hourly growth difference"""
        self.hourly_growth_diff = diff

    def get_last_time_manipulated(self):
        """Gets the Time when the factors of the system were manipulated"""
        return self.last_time_manipulated
    
    def set_last_time_manipulated(self, date_time):
        """Sets the Time when the factors of the system were manipulated"""
        self.last_time_manipulated = date_time
        
    def get_read_time(self):
        """Gets the Time when the reading of the measurements were taken"""
        return self.read_time
    
    def set_read_time(self, last_time_read):
        """Sets the Time when the reading of the measurements were taken"""
        self.read_time = last_time_read
        
    def get_cam_shot_time(self):
        """Gets the Time when the camera shot was taken for measuring height 
        and growth"""
        return self.cam_shot_time
    
    def set_cam_shot_time(self, date_time):
        """Sets the Time when the camera shot was taken for measuring height 
        and growth"""
        self.cam_shot_time = date_time
    
    def get_last_time_heard(self):
        """Gets the Time when the plant was last heard"""
        return self.last_time_heard
    
    def set_last_time_heard(self, last_time_heard):
        """Sets the Time when the plant was last heard"""
        self.last_time_heard = last_time_heard
    
    def get_stale_read_flag(self):
        """Gets the flag indicating whether the reading currently recorded is 
        stale due to loss in connection"""
        return self.stale_read_flag
    
    def set_stale_read_flag(self, flag):
        """Sets the flag indicating whether the reading currently recorded is 
        stale due to loss in connection"""
        self.stale_read_flag = flag
        
    def get_stale_cam_flag(self):
        """Gets the flag indicating whether the reading currently recorded 
        is stale due to loss in connectivity with the camera"""
        return self.stale_cam_flag
    
    def set_stale_cam_flag(self, flag):
        """Sets the flag indicating whether the reading currently recorded 
        is stale due to loss in connectivity with the camera"""
        self.stale_cam_flag = flag
        
    def get_abnormal_ph_val_flag(self):
        """Gets the Flag indicating whether the pH value is abnormal"""
        return self.abnormal_ph_val_flag
    
    def set_abnormal_ph_val_flag(self, flag):
        """Sets the Flag indicating whether the pH value is abnormal"""
        self.abnormal_ph_val_flag = flag
        
    def get_abnormal_ec_val_flag(self):
        """Gets the Flag indicating whether the EC value is abnormal"""
        return self.abnormal_ec_val_flag
    
    def set_abnormal_ec_val_flag(self, flag):
        """Sets the Flag indicating whether the EC value is abnormal"""
        self.abnormal_ec_val_flag = flag
    
    def get_abnormal_tbw_flag(self):
        """Gets the Flag indicating whether the time between watering is abnormal"""
        return self.abnormal_tbw_flag
    
    def set_abnormal_tbw_flag(self, flag):
        """Sets the Flag indicating whether the time between watering is abnormal"""
        self.abnormal_tbw_flag = flag
        
    def set_abnormal_tfw_flag(self, flag):
        """Sets the Flag indicating whether the time for watering is abnormal"""
        self.abnormal_tfw_flag = flag
        
    def get_abnormal_tfw_flag(self):
        """Gets the Flag indicating whether the time for watering is abnormal"""
        return self.abnormal_tfw_flag
        
        
class MonitorPlantData:
    """Class representing and performing the regular monitoring of the plants
    in the system"""
    def __init__(self, devices, plants):
        #list of photon device objects connected to the system
        self.devices = devices
        #List of plant objects in the system
        self.plants = plants
        #device plant mapping from the configuration file
        self.DEVICE_PLANT_MAPPING = DEVICE_PLANT_MAPPING
        #plant device mapping from the configuration file
        self.PLANT_DEVICE_MAPPING = PLANT_DEVICE_MAPPING
        #list of photon devices connected to the cloud
        self.connected_devices = []
        #list of photon device disconnected from the cloud
        self.disconnected_devices = []
        #list of plants connected to the cloud
        self.connected_plants = []
        #list of plants disconnected to the cloud
        self.disconnected_plants = []
        
    def plant_connectivity_check(self):
        """Performs the connectivity check of the photon devices and the plants
        connected to them at a given instance. Groups the connected and 
        disconnected plants and devices into separate lists"""
        for device in self.DEVICE_PLANT_MAPPING:
            if self.check_device_connection(device):
                self.connected_devices.append(device)
                for plant in self.DEVICE_PLANT_MAPPING[device]:
                    self.connected_plants.append(plant)
            else:
                self.disconnected_devices.append(device)
                for plant in self.DEVICE_PLANT_MAPPING[device]:
                    self.disconnected_plants.append(plant)

    def hourly_monitor(self):   
        """Performs the hourly monitoring and readings of the plants"""
        
        #performs connectivity check
        self.plant_connectivity_check()
        
        #monitors and reads the plant data connected at that instant
        for plant in self.connected_plants:        
            self.read_plant_data(plant)
        
        #Returns back to the disconnected plants in order to check for the
        #current connectivity. Tries for a set number of attempts and then
        #breaks, notifying the failure to connect and asking for checking the
        #connectivity.
        for plant in self.disconnected_plants:
            status = self.check_device_connection(self.PLANT_DEVICE_MAPPING[plant]["device_name"])
            
            no_tries = 0
            while status == False:
                sleep(DEVICE_CONN_WAIT_TIME)
                status = self.check_device_connection(self.PLANT_DEVICE_MAPPING[plant]["device_name"])
                no_tries += 1
                if no_tries > DEVICE_CONN_NO_TRIES:
                    print "The readings for "+plant+" could not be recorded. Please check the connectivity"
                    break
                
            if status == True:
                self.disconnected_plants.remove(plant)
                self.read_plant_data(plant)
                    
    def status_check(self):
        """A utility method for checking and printing the status of the 
        photon devices and plants in the system connected to the cloud.
        Used for report generation"""
        
        print("Report Generated at: ", datetime.now())
        print("\n")
        print("Connected Devices:", self.connected_devices)
        print("Disconnected Devices:", self.disconnected_devices)
        print("\n")
        print("Connected Plants:", self.connected_plants)
        print("Disconnected Plants:", self.disconnected_plants)
        print("\n\n")
        print("Latest values for connected plants:")
        print("\n")
        connected_plants = self.get_connected_plants()
        for plant in connected_plants:
            print("Plant Id: ", plant.get_plant_id())
            print("pH value: ", plant.get_ph())
            print("EC value: ", plant.get_ec())
            print("Time for watering: ", plant.get_tfw())
            print("Time between watering: ", plant.get_tbw())
            print("Growth: ", plant.get_current_growth())
            print("Height: ", plant.get_current_height())
            print("Latest Cam Shot Time (EST): ", plant.get_cam_shot_time())
            print("Last time the plant was heard: ", plant.get_last_time_heard())
            print("Is the latest data recorded from device stale? ", plant.get_stale_read_flag())
            print("Is the latest cam shot data recorded stale? ", plant.get_stale_cam_flag())
            print("Is the latest ph Value recorded abnormal? ", plant.get_abnormal_ph_val_flag())
            print("Is the latest EC value recorded abnormal? ", plant.get_abnormal_ec_val_flag())
            print("Is the latest time between watering recorded abnormal? ", plant.get_abnormal_tbw_flag())
            print("Is the latest time for watering recorded abnormal? ", plant.get_abnormal_tfw_flag())
            print("\n------------------------\n")
            
        print("Latest values for disconnected plants:")
        disconnected_plants = self.get_disconnected_plants()
        for plant in disconnected_plants:
            print("Plant Id: ", plant.get_plant_id())
            print("pH value: ", plant.get_ph())
            print("EC value: ", plant.get_ec())
            print("Time for watering: ", plant.get_tfw())
            print("Time between watering: ", plant.get_tbw())
            print("Growth: ", plant.get_current_growth())
            print("Height: ", plant.get_current_height())
            print("Latest Cam Shot Time (EST): ", plant.get_cam_shot_time())
            print("Last time the plant was heard: ", plant.get_last_time_heard())
            print("Is the latest data recorded from device stale? ", plant.get_stale_read_flag())
            print("Is the latest cam shot data recorded stale? ", plant.get_stale_cam_flag())
            print("Is the latest ph Value recorded abnormal? ", plant.get_abnormal_ph_val_flag())
            print("Is the latest EC value recorded abnormal? ", plant.get_abnormal_ec_val_flag())
            print("Is the latest time between watering recorded abnormal? ", plant.get_abnormal_tbw_flag())
            print("Is the latest time for watering recorded abnormal? ", plant.get_abnormal_tfw_flag())
            print("\n------------------------\n")
        print("\n%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%\n")    
        
        
    def create_summary_report(self, coll):
        """Method for generating a summarized report of the plants from the 
        mongodb collections used for storing the plant data."""
        print("\nSummary of pH, EC and Growth values for the past 24 hours.\n")
        plant_keys = PLANT_DEVICE_MAPPING.keys()
        plant_dict = {}
        times = []
        
        for plant_id in plant_keys:
            print("Plant Id:", plant_id)
            
            current_time = datetime.now()
            past24hr = current_time - timedelta(hours=24)
            last_observations = coll.find({"plant_id" : plant_id, 
                                           "read_time" : {"$gte" : past24hr ,
                                                          "$lt" : current_time}})
            
            ph_values = []
            ec_values = []
            growth_values = []
            height_values = []
            for entries in last_observations:
                #print("Ph Value of the plant", entries["phVal"])
                times.append(entries["read_time"])
                try:
                    ph_values.append((float(str(entries["phVal"])), entries["read_time"]))
                    growth_values.append((float(str(entries["growth"])), entries["read_time"]))
                    height_values.append((float(str(entries["height"])), entries["read_time"]))
                    ec_val = float(str(entries["nutrient_conductivity"]))
                    ec_values.append((ec_val, entries["read_time"]))
                    
                except ValueError:
                    pass
                
            plant_dict[plant_id] = {"phVals": ph_values, "ecVals": ec_values, 
                                    "growthVals" : growth_values, 
                                    "heightVals": height_values}
            
            #print(plant_dict)
            
            self.get_plant_summary(plant_dict, plant_id, times, coll)

    
    def get_plant_summary(self, plant_dict, plant_id, times, data_collection):
        """Method for getting the plant summary information from the plant
        data stored in the mongodb collections"""
        
        ph_vals = [entries[0] for entries in plant_dict[plant_id]["phVals"]]
        if ph_vals == []:
            print("No pH values were recorded in the given time period")
        else:
            min_time = min(times)
            max_time = max(times)
            print("Summary of recorded readings for ph between "+str(min_time)+" and "+str(max_time))
            ph_variance = variance(ph_vals)
            min_ph = min(ph_vals)
            max_ph = max(ph_vals)
            
            erratic_ph_vals = [entries[0] for entries in plant_dict[plant_id]["phVals"]
                               if entries[0] > config.max_ph or entries[0] < config.min_ph]
            
            print("The minimum ph value recorded: "+ str(min_ph))
            print("The maximum ph value recorded: "+ str(max_ph))
            print("Variance in ph values recorded: "+ str(ph_variance))
            print("Unique ph values: "+ str(list(set(ph_vals))))
            print("Erratic ph values: "+ str(erratic_ph_vals))
            print("\nph values and their respective timings:\n")
            for entries in plant_dict[plant_id]["phVals"]:
                print(str(entries[1])+" : "+str(entries[0]))
            print("\n----------------------\n")
                
        ec_vals = [entries[0] for entries in plant_dict[plant_id]["ecVals"]]
        if ec_vals == []:
            print("No EC values were recorded in the given period of time")
        else:
            ec_variance = variance(ec_vals)
            min_time = min(times)
            max_time = max(times)
            print("Summary of recorded readings for ec between "+str(min_time)+" and "+str(max_time))
            
            min_ec = min(ec_vals)
            max_ec = max(ec_vals)
            
            erratic_ec_vals = [entries[0] for entries in plant_dict[plant_id]["ecVals"]
                               if entries[0] > config.max_ec or entries[0] < config.min_ec]
            
            print("The minimum ec value recorded: "+ str(min_ec))
            print("The maximum ec value recorded: "+ str(max_ec))
            print("Variance in ec values recorded: "+ str(ec_variance))
            print("Unique ec values: "+ str(list(set(ec_vals))))
            print("Erratic ec values: "+ str(erratic_ec_vals))
            print("\nec values and their respective timings:\n")
            for entries in plant_dict[plant_id]["ecVals"]:
                print(str(entries[1])+" : "+str(entries[0]))  
            print("\n----------------------\n")
              
        growth_vals = [entries[0] for entries in plant_dict[plant_id]["growthVals"]]
        if growth_vals == []:
            print("No growth values were recorded in the given period of time")
        else:
            growth_variance = variance(growth_vals)
            min_time = min(times)
            max_time = max(times)
            print("Summary of recorded readings for growth between "+str(min_time)+" and "+str(max_time))        
            min_growth = min(growth_vals)
            max_growth = max(growth_vals)
            
            print("The minimum growth value recorded: "+ str(min_growth))
            print("The maximum growth value recorded: "+ str(max_growth))
            print("Variance in growth values recorded: "+ str(growth_variance))
            print("Unique growth values: "+ str(list(set(growth_vals))))
            print("\ngrowth values and their respective timings:\n")
            for entries in plant_dict[plant_id]["growthVals"]:
                print(str(entries[1])+" : "+str(entries[0]))
                
            print("\n----------------------\n")
                    
        height_vals = [entries[0] for entries in plant_dict[plant_id]["heightVals"]]
        if height_vals == []:
            print("No height values were recorded in the given period of time")
        else:
            height_variance = variance(height_vals)
            min_time = min(times)
            max_time = max(times)
            print("Summary of recorded readings for height between "+str(min_time)+" and "+str(max_time))
            min_height = min(height_vals)
            max_height = max(height_vals)
            
            print("The minimum height value recorded: "+ str(min_height))
            print("The maximum height value recorded: "+ str(max_height))
            print("Variance in height values recorded: "+ str(height_variance))
            print("Unique height values: "+ str(list(set(height_vals))))
            print("\nheight values and their respective timings:\n")
            for entries in plant_dict[plant_id]["heightVals"]:
                print(str(entries[1])+" : "+str(entries[0]))        
            print("\n----------------------\n")
                    
        print("\n%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%\n")

        
    def read_plant_data(self, plant):
        """Method used for reading all the data points related to a plant
        connected to the system"""

        plant_obj = self.plants[plant]
        plant_device_name = self.PLANT_DEVICE_MAPPING[plant]["device_name"]
        plant_device = self.devices[plant_device_name]
        
        #get the time when the plant was last heard
        plant_last_heard = to_datetime(self.devices[plant_device_name].last_heard)
        plant_obj.set_last_time_heard(plant_last_heard)
        
        #get the current read time
        curr_read_time = datetime.now()
        plant_obj.set_read_time(curr_read_time)
        
        #get the stale device flag
        STALE_PLANT_DATA_FLAG = self.is_data_read_stale(curr_read_time, 
                                                         plant_last_heard)
        plant_obj.set_stale_read_flag(STALE_PLANT_DATA_FLAG)
        
        #get camera data for the plant
        camera_data_obj = PlantGrowth(plant)
        if proxy == False:
            pass
        else:
            camera_data_obj.set_proxy()
        
        plant_growth_tuple = camera_data_obj.get_growth_data()
        #set the camera data for the plant instance
        if plant_growth_tuple == None:
            growth = None
            STALE_CAM_DATA = True
            shot_time = None
            height = None
            
            last_plant_height = plant_obj.get_current_height()
            plant_obj.set_current_height(last_plant_height)
            plant_obj.set_hourly_height_diff(0.0)
            
            last_plant_growth = plant_obj.get_current_growth()
            plant_obj.set_current_growth(last_plant_growth)
            plant_obj.set_hourly_growth_diff(0.0)
            
            plant_obj.set_stale_cam_flag(STALE_CAM_DATA)
            plant_obj.set_cam_shot_time(plant_obj.get_cam_shot_time())
            
        else:
            
            growth = plant_growth_tuple[0]
            STALE_CAM_DATA = plant_growth_tuple[1]
            shot_time = plant_growth_tuple[2]
            height = plant_growth_tuple[3]
            
            last_plant_height = plant_obj.get_current_height()
            hourly_height_diff = height - last_plant_height
            plant_obj.set_current_height(height)
            plant_obj.set_hourly_height_diff(hourly_height_diff)
            
            last_plant_growth = plant_obj.get_current_growth()
            hourly_growth_diff = growth - last_plant_growth
            plant_obj.set_current_growth(growth)
            plant_obj.set_hourly_growth_diff(hourly_growth_diff)
            
            plant_obj.set_stale_cam_flag(STALE_CAM_DATA)
            plant_obj.set_cam_shot_time(shot_time)
        
        #get the ph readings of the plant
        plant_ph_obj = PlantPh(plant, plant_device)
        ph_reading = plant_ph_obj.get_ph_reading()
        
        #set the current ph readings of the plant
        if ph_reading == None:
            plant_obj.set_ph(plant_obj.get_ph())
            plant_obj.set_abnormal_ph_val_flag(True)
        else:
            plant_obj.set_ph(ph_reading[0])
            plant_obj.set_abnormal_ph_val_flag(ph_reading[1])
        

        #get the ec readings of the plant
        plant_ec_obj = PlantEc(plant, plant_device)
        ec_reading = plant_ec_obj.get_ec_reading()
        
        #set the current ph readings of the plant
        if ec_reading == None:
            plant_obj.set_ec(plant_obj.get_ec())
            plant_obj.set_abnormal_ec_val_flag(True)
        else:
            plant_obj.set_ec(ec_reading[0])
            plant_obj.set_abnormal_ec_val_flag(ec_reading[1])
            
        #get the watering readings of the plant
        plant_watering_obj = PlantWatering(plant, plant_device)
        watering_reading = plant_watering_obj.get_watering_reading()
        
        #set the current ph readings of the plant
        if watering_reading == None:
            plant_obj.set_tbw(plant_obj.get_tbw())
            plant_obj.set_tfw(plant_obj.get_tfw())
            plant_obj.set_abnormal_tbw_flag(True)
            plant_obj.set_abnormal_tfw_flag(True)
        else:
            plant_obj.set_tbw(watering_reading[0])
            plant_obj.set_tfw(watering_reading[2])
            plant_obj.set_abnormal_tbw_flag(watering_reading[1])
            plant_obj.set_abnormal_tfw_flag(watering_reading[3])
                    
    def check_device_connection(self, device_name):
        """Checks the current connectivity of the given photon device identified
        by its name"""
        return self.devices[device_name].connected
    
    def get_plants(self):
        """Gets the list of plant objects"""
        return self.plants.values()
    
    def get_connected_devices(self):
        """Gets the list of connected photon devices"""
        return self.connected_devices
    
    def get_disconnected_devices(self):
        """Gets the list of disconnected photon devices"""
        return self.disconnected_devices
    
    def get_connected_plants(self):
        """Gets the list of connected plants"""
        return [self.plants[entries] for entries in self.connected_plants]
            
    def get_disconnected_plants(self):
        """Gets the list of disconnected plants"""
        return [self.plants[entries] for entries in self.disconnected_plants]
        
    def is_data_read_stale(self, curr_time, last_heard):
        """Method for calculating if the time at which the plant data is read
        is too old. This may be due to previously stored values in the photon
        device which got disconnected from the cloud and did not update the
        recent data"""
        time_diff = curr_time - last_heard
        time_diff_mins = float(time_diff.seconds) / 60.0
        
        STALE_DATA = False
        if time_diff_mins >= DEVICE_STALE_DATA_MINS:
            STALE_DATA = True
        
        return STALE_DATA
    
    
class PlantGrowth:
    """Class representing the growth data captured by the camera"""
    def __init__(self, plant_id):
        #plant id for which the growth data needs to be captured
        self.plant_id = plant_id
        #URL for the camera server
        self.GROWTH_URL = GROWTH_URL
        #set the proxy flag
        self.proxy = False
        
    def set_proxy(self):
        """Sets the proxy flag"""
        self.proxy = True
        
    def get_growth_data(self):
        """gets the current growth value of the given plant id"""
        
        payload = {}
        payload["plant"] = self.plant_id
        
        base_url = self.GROWTH_URL
        
        if self.proxy:
            response = requests.get(base_url, params=payload, proxies=proxies)
        else:
            response = requests.get(base_url, params=payload)
        
        try:
            json_resp = json.loads(response.text)
            
            STALE_CAM_DATA = False
    
            growth = json_resp[0]["camera_output"]
            height = json_resp[0]["height"]
            shot_time = parser.parse(json_resp[0]["shot_time"]).replace(tzinfo=None)
                 
            time_diff = time_diff(shot_time, datetime.now())
                
            time_diff_mins = time_diff[0]
            
            if time_diff_mins >= CAM_STALE_DATA_MINS:
                STALE_CAM_DATA = True
                return (growth, STALE_CAM_DATA, shot_time, height)
            else:
                return (growth, STALE_CAM_DATA, shot_time, height)
        except:
            return None
    
        
class PlantPh:
    """Class representing the pH readings for a plant"""
    def __init__(self, plant_id, device):
        #Id of the plant for which the pH reading is being recorded
        self.plant_id = plant_id
        #Device from which the reading is recorded
        self.device = device
        #Flag indicating whether the pH reading is abnormal
        self.abnormal_ph_flag = False
        
    def get_ph_reading(self):
        """Method for reading the pH value of the solution for a particular
        plant"""
        
        if self.plant_id[1] == "0":
            try:
                ph_plant0 = float(self.device.P0_phVal)
                if ph_plant0 > max_ph or ph_plant0 < min_ph:
                    self.abnormal_ph_flag = True
                return (ph_plant0, self.abnormal_ph_flag)
            except TypeError:
                print "Not registered variable"
                return None
            except AttributeError:
                print "Not registered variable"
                return None
            except IOError:
                print "Photon not connected"
                return None
            except:
                print "Error from Spark Cloud"
                return None

        if self.plant_id[1] == "1":
            try:
                ph_plant1 = float(self.device.P1_phVal)
                if ph_plant1 > max_ph or ph_plant1 < min_ph:
                    self.abnormal_ph_flag = True
                return (ph_plant1, self.abnormal_ph_flag)
            except TypeError:
                print "Not registered variable"
                return None
            except AttributeError:
                print "Not registered variable"
                return None
            except IOError:
                print "Photon not connected"
                return None
            except:
                print "Error from Spark Cloud"
                return None
            
            
class PlantWatering:
    """Class representing the watering frequency readings for a plant"""
    def __init__(self, plant_id, device):
        #Id of the plant for which the watering frequency reading is being recorded
        self.plant_id = plant_id
        #Device from which the reading is recorded
        self.device = device
        #Flag indicating whether the time for watering reading is abnormal
        self.abnormal_tfw_flag = False
        #Flag indicating whether the time between watering reading is abnormal
        self.abnormal_tbw_flag = False
        
    def get_watering_reading(self):
        """Method for reading the watering frequency values for a particular plant"""
        if self.plant_id[1] == "0":
            try:
                tbw_plant0 = int(self.device.P0_TBW)
                tfw_plant0 = int(self.device.P0_TFW)
                if tbw_plant0 > max_tbw or tbw_plant0 < min_tbw:
                    self.abnormal_tbw_flag = True
                if tfw_plant0 > max_tfw or tfw_plant0 < min_tfw:
                    self.abnormal_tfw_flag = True
                return (tbw_plant0, self.abnormal_tbw_flag, tfw_plant0, self.abnormal_tfw_flag)
            except TypeError:
                print "Not registered variable"
                return None
            except AttributeError:
                print "Not registered variable"
                return None
            except IOError:
                print "Photon not connected"
                return None
            except:
                print "Error from Spark Cloud"
                return None

        if self.plant_id[1] == "1":
            try:
                tbw_plant1 = int(self.device.P1_TBW)
                tfw_plant1 = int(self.device.P1_TFW)
                if tbw_plant1 > max_tbw or tbw_plant1 < min_tbw:
                    self.abnormal_tbw_flag = True
                if tfw_plant1 > max_tfw or tfw_plant1 < min_tfw:
                    self.abnormal_tfw_flag = True
                return (tbw_plant1, self.abnormal_tbw_flag, tfw_plant1, self.abnormal_tfw_flag)
            except TypeError:
                print "Not registered variable"
                return None
            except AttributeError:
                print "Not registered variable"
                return None
            except IOError:
                print "Photon not connected"
                return None
            except:
                print "Error from Spark Cloud"
                return None
            
class PlantEc:
    """Class representing the Electrical Conductivity readings for a plant"""
    def __init__(self, plant_id, device):
        #Id of the plant for which the Electrical Conductivity reading is being recorded
        self.plant_id = plant_id
        #Device from which the reading is recorded
        self.device = device
        #Flag indicating whether the EC reading is abnormal
        self.abnormal_ec_flag = False
        
    def get_ec_reading(self):
        """Method for reading the Electrical Conductivity values for a particular plant"""
        if self.plant_id[1] == "0":
            try:
                ec_plant0 = float(self.device.P0_nutrientC)
                if ec_plant0 > max_ec or ec_plant0 < min_ec:
                    self.abnormal_ec_flag = True
                return (ec_plant0, self.abnormal_ec_flag)
            except TypeError:
                print "Not registered variable"
                return None
            except AttributeError:
                print "Not registered variable"
                return None
            except IOError:
                print "Photon not connected"
                return None
            except:
                print "Error from Spark Cloud"
                return None

        if self.plant_id[1] == "1":
            try:
                ec_plant1 = float(self.device.P1_nutrientC)
                if ec_plant1 > max_ec or ec_plant1 < min_ec:
                    self.abnormal_ec_flag = True
                return (ec_plant1, self.abnormal_ec_flag)
            except TypeError:
                print "Not registered variable"
                return None
            except AttributeError:
                print "Not registered variable"
                return None
            except IOError:
                print "Photon not connected"
                return None
            except:
                print "Error from Spark Cloud"
                return None
            
class Report:
    """Class representing the daily reports generated"""
    def __init__(self, plant_monitor_obj, data_collection, emails):
        #Instance of the plant monitor object containing the recent plant data
        self.plant_monitor_obj = plant_monitor_obj
        #mongodb collection storing the daily plant data
        self.data_collection = data_collection
        #list of email ids to which the automated reports needs to be sent
        #the list is obtained from the configuration files
        self.emails = emails
        #file for stroing the report for the day
        self.report_file = open("report.txt", "w")
        #csv file containing the daily readings
        self.csv_file = open("daily_plant_readings.csv", "w")
        
    def generate_report(self):
        """Method for generating the daily report"""
        sys.stdout = self.report_file
        #self.plant_monitor_obj.status_check()
        self.plant_monitor_obj.create_summary_report(self.data_collection)
        
    def generate_csv(self):
        """Method for generating csv files for last 24 hours readings"""
        current_time = datetime.now()
        past24hr = current_time - timedelta(hours=24)
        last_observations = self.data_collection.find({"read_time" : 
                                                       {"$gte" : past24hr ,
                                                      "$lt" : current_time}})
        plant_data_list = []
        for entries in last_observations:
            plant_data_list.append(entries)
            
        keys = plant_data_list[0].keys()
        with self.csv_file as output_file:
            dict_writer = csv.DictWriter(output_file, keys)
            dict_writer.writeheader()
            dict_writer.writerows(plant_data_list)
            
    def send_emails(self):
        yagmail.register(admin_email, admin_passwd)
        yag = yagmail.SMTP(admin_email)

        to = self.emails
        subject = '24 hour report for hydroponic environment'
        body = 'Please find the past 24 hour report generarted from the automated \
                hydroponic environment along with the data readings recorded in a csv file. \
                Report File -> report.txt \
                Data Readings -> daily_plant_readings.csv \
                Please note this is an automatically \
                generated email. For more information about the project and its \
                source code please check the GitHub repository: https://github.com/infyponics/infyponics'
        
        report_doc = 'report.txt'
        csv_readings = 'daily_plant_readings.csv'
        
        yag.send(to = to, subject = subject, contents = [body, report_doc, 
                                                                csv_readings])  