'''
Created on Jun 5, 2016

@author: Debanjan.Mahata
'''

"""Particle.io ACCESS_TOKEN"""
PARTICLE_IO_ACCESS_TOKEN = ""

"""Base Url for retrieving the latest growth data"""
GROWTH_URL = ""

"""Base URL for particle.io REST api"""
PARTICLE_IO = "https://api.particle.io/v1/"

"""Base URL for particle.io devices"""
PARTICLE_IO_DEVICE = "https://api.particle.io/v1/devices"


"""Plant to Device Mappings"""
PLANT_DEVICE_MAPPING = {"00" : {"device_name":"photon0", 
                                "device_id":"1d002f000347343339373536"},
                        "01" : {"device_name":"photon0", 
                                "device_id":"1d002f000347343339373536"},
                        "10" : {"device_name":"photon1", 
                                "device_id":"25002b001347343432313031"},
                        "11" : {"device_name":"photon1", 
                                "device_id":"25002b001347343432313031"},
                        "20" : {"device_name":"photon2", 
                                "device_id":"1c0030001947343339383036"},
                        "21" : {"device_name":"photon2", 
                                "device_id":"1c0030001947343339383036"},
                        "30" : {"device_name":"photon3", 
                                "device_id":"2c0040001047353138383138"},
                        "31" : {"device_name":"photon3", 
                                "device_id":"2c0040001047353138383138"},
                        "40" : {"device_name":"photon4", 
                                "device_id":"2d0029000247353138383138"},
                        "41" : {"device_name":"photon4", 
                                "device_id":"2d0029000247353138383138"},
                        "50" : {"device_name":"photon5", 
                                "device_id":"2f002e000347353138383138"},
                        "51" : {"device_name":"photon5", 
                                "device_id":"2f002e000347353138383138"},
                        "60" : {"device_name":"photon6", 
                                "device_id":"290020001147353138383138"},
                        "61" : {"device_name":"photon6", 
                                "device_id":"290020001147353138383138"},
                        "70" : {"device_name":"photon7", 
                                "device_id":"37002b000647343232363230"},
                        "71" : {"device_name":"photon7", 
                                "device_id":"37002b000647343232363230"},
                        "80" : {"device_name":"photon8", 
                                "device_id":"2b002a000a47353138383138"},
                        "81" : {"device_name":"photon8", 
                                "device_id":"2b002a000a47353138383138"},
                        "90" : {"device_name":"photon9", 
                                "device_id":"2b0038000147353138383138"},
                        "91" : {"device_name":"photon9", 
                                "device_id":"2b0038000147353138383138"}
                        }

"""Device to Plant Mapping"""
DEVICE_PLANT_MAPPING = {"photon0" : ["00", "01"],
                        "photon1" : ["10", "11"],
                        "photon2" : ["20", "21"],
                        "photon3" : ["30", "31"],
                        "photon4" : ["40", "41"],
                        "photon5" : ["50", "51"],
                        "photon6" : ["60", "61"],
                        "photon7" : ["70", "71"],
                        "photon8" : ["80", "81"],
                        "photon9" : ["90", "91"]
                         }

"""Plant ids of the different groups segmented according to different factors.
This setting is used for initiating the automated data collection and manipulation
process"""

"""pH groups"""
group_ph_high = ["90", "81", "20", "11", "40", "51"]
group_ph_med = ["91", "30", "21", "00", "41", "60"]
group_ph_low = ["80", "31", "10", "01", "50", "61"]

"""Soil nutrient groups"""
group_nutrient_high = ["90", "91", "80", "11", "00", "01"]
group_nutrient_low = ["20", "21", "10", "51", "60", "61"]
group_nutrient_med = ["81", "30", "31", "40", "41", "50"]

"""Watering frequency groups"""
"""Soil nutrient groups"""
group_waterfreq_high = ["40", "41", "50", "51", "60", "61"]
group_waterfreq_med = ["20", "21", "10", "11", "00", "01"]
group_waterfreq_low = ["90", "91", "80", "81", "30", "31"]

"""Maximum ph allowed"""
max_ph = 6.5
"""Minimum ph allowed"""
min_ph = 5.5

"""Maximum ec allowed"""
max_ec = 4.0
"""Minimum ec allowed"""
min_ec = 1.0

"""Maximum Watering Frequency"""
max_water_freq = 10
"""Minimum watering frequency"""
min_water_freq = 2
"""Maximum time for watering"""
max_tfw = 30
"""Minimum time for watering"""
min_tfw = 1
"""Maximum time between watering"""
max_tbw = 1440/min_water_freq
"""Minimum time betweeb watering"""
min_tbw = 1440/max_water_freq 

"""Increment value in pH level"""
ph_inc = 0.2
"""Decrement value in pH level"""
ph_dec = 0.2

"""Increment value in ec level"""
ec_inc = 0.2
"""Decrement value in ec level"""
ec_dec = 0.2

"""Increment value in watering frequency"""
water_freq_inc = 1
"""Decrement in watering frequency"""
water_freq_dec = 1

"""Initial values"""
initial_val_dict = {"ph": {"low": 5.5, "med": 6.0, "high": 6.5},
                    "ec": {"low": 1.0, "med": 2.0, "high": 3.0},
                    "water_freq": {"low": 2, "med": 4, "high": 6}}

"""Fixed time for watering in minutes"""
time_for_watering = 15

"""proxy settings"""
proxies = {}

"""Set the time in minutes for which the recorded device data would be considered
stale"""
DEVICE_STALE_DATA_MINS = 90

"""Set the time in minutes for which the recorded camera data would be considered
stale"""
CAM_STALE_DATA_MINS = 270

"""Proxy"""
proxy = False 

"""Device connecting re-checking wait time in seconds"""
DEVICE_CONN_WAIT_TIME = 30

"""Number of tries for rechecking Device connectivity"""
DEVICE_CONN_NO_TRIES = 2


"""List of emails to which daily reports needs to be sent"""
report_emails = []


