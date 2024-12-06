# %% [markdown]
# ### Example script for reading and calibrating DGS raw (aka serial) data from an R/V Ride transit, with comparison to laptop (lightly processed) files output from the meter.
#
# Data files are downloaded by the script using pooch
#
# Read DGS (serial and laptop) and navigation files
#
# Calibrate the raw counts
#
# Correct for meter bias with info from shipgrav
#
# Use timestamps to sync more accurate nav with the gravity data.
#
# Plot laptop and raw data to compare
#
# Calculate FAA (free air anomaly) for laptop data
#
# Plot laptop FAA along with satellite
#
# satellite data was tracked from v32.1 Global Gravity grid, which
# includes data from SIO, NOAA, and NGA.
#
# Reference: Sandwell et al. (2014) New global marine gravity model
# from CryoSat-2 and Jason-1 reveals buried tectonic struture.
# Science 346(6205), DOI: 10.1126/science.1258213

# %%
import os
from glob import glob

import matplotlib.pyplot as plt
import numpy as np
import pooch
import tomli as tm
from scipy.interpolate import interp1d
from scipy.signal import filtfilt, firwin
from tqdm import tqdm

import shipgrav.grav as sgg
import shipgrav.io as sgi
import shipgrav.utils as sgu

# %%
# set some general metadata
ship = 'Ride'
cruise = 'SR2312'       # this is used for filepaths
sampling = 1            # 1 Hz - data should be at this rate already

# read a few constants etc from our toml database file
with open('../shipgrav/database.toml', 'rb') as f:
    info = tm.load(f)
nav_tag = info['nav-talkers'][ship]
biases = info['bias-values'][ship]
cal_factor = info['dgs-stuff']['calibration_factor']

# %%
# get the data: raw DGS from zenodo, laptop and nav from R2R
dgs_files_raw = pooch.retrieve(url="https://zenodo.org/records/12733929/files/data.zip", 
        known_hash="md5:83b0411926c0fef9d7ccb2515bb27cc0", progressbar=True, 
        processor=pooch.Unzip(
            members=['data/Ride/SR2312/gravimeter/DGS/serial/SR2312_grav_dgs-2023-06-16.txt',
                    'data/Ride/SR2312/gravimeter/DGS/serial/SR2312_grav_dgs-2023-06-17.txt',
                    'data/Ride/SR2312/gravimeter/DGS/serial/SR2312_grav_dgs-2023-06-18.txt',
                    'data/Ride/SR2312/gravimeter/DGS/serial/SR2312_grav_dgs-2023-06-19.txt',
                    'data/Ride/SR2312/gravimeter/DGS/serial/SR2312_grav_dgs-2023-06-20.txt']))

dgs_files = pooch.retrieve(url="https://service.rvdata.us/data/cruise/SR2312/fileset/157179", 
        known_hash="53f53c45aa59ce19cd1e75e3d847b5697123ad0a1296aa2be28bf26ff0ad19ac", progressbar=True, 
        processor=pooch.Untar(
            members=['SR2312/157179/data/AT1M-25_20230616_167.dat',
                     'SR2312/157179/data/AT1M-25_20230617_168.dat',
                     'SR2312/157179/data/AT1M-25_20230618_169.dat',
                     'SR2312/157179/data/AT1M-25_20230619_170.dat',
                     'SR2312/157179/data/AT1M-25_20230620_171.dat']))

nav_files = pooch.retrieve(url="https://service.rvdata.us/data/cruise/SR2312/fileset/157188", 
        known_hash="eb5992eadd87b09f66308a4d577c6ba6965d8ed8489959ffaed8bf5556ee712f", progressbar=True, 
        processor=pooch.Untar(
            members=['SR2312/157188/data/SR2312_mru_seapath330_navbho-2023-06-16.txt',
                     'SR2312/157188/data/SR2312_mru_seapath330_navbho-2023-06-17.txt',
                     'SR2312/157188/data/SR2312_mru_seapath330_navbho-2023-06-18.txt',
                     'SR2312/157188/data/SR2312_mru_seapath330_navbho-2023-06-19.txt',
                     'SR2312/157188/data/SR2312_mru_seapath330_navbho-2023-06-20.txt']))

# %%
# read and sort the nav data
gps_nav = sgi.read_nav(ship, nav_files, talker='GPGGA')
gps_nav.sort_values('time_sec', inplace=True)
gps_nav.reset_index(inplace=True, drop=True)

# %%
# read and sort the DGS laptop data
dgs_data = sgi.read_dgs_laptop(dgs_files, ship)
dgs_data.sort_values('date_time', inplace=True)
dgs_data.reset_index(inplace=True, drop=True)
dgs_data['tsec'] = [e.timestamp()
                    for e in dgs_data['date_time']]  # get posix timestamps
dgs_data['grav'] = dgs_data['rgrav'] + biases['dgs']

# %%
# sync data geographic coordinates to nav by interpolating with timestamps
# (interpolators use posix timestamps, not datetimes)
gps_lon_int = interp1d(gps_nav['time_sec'].values, gps_nav['lon'].values,
                       kind='linear', fill_value='extrapolate')
gps_lat_int = interp1d(gps_nav['time_sec'].values, gps_nav['lat'].values,
                       kind='linear', fill_value='extrapolate')
dgs_data['lon_new'] = gps_lon_int(dgs_data['tsec'].values)
dgs_data['lat_new'] = gps_lat_int(dgs_data['tsec'].values)

# %%
# calculate corrections for FAA
ellipsoid_ht = np.zeros(len(dgs_data))  # we are working at sea level
lat_corr = sgg.wgs_grav(dgs_data['lat_new']) + \
    sgg.free_air_second_order(dgs_data['lat_new'], ellipsoid_ht)
eotvos_corr = sgg.eotvos_full(dgs_data['lon_new'].values, dgs_data['lat_new'].values,
                              ellipsoid_ht, sampling)
tide_corr = sgg.longman_tide_prediction(
    dgs_data['lon_new'], dgs_data['lat_new'], dgs_data['date_time'])

dgs_data['faa'] = dgs_data['grav'] - lat_corr + eotvos_corr + tide_corr
dgs_data['full_field'] = dgs_data['grav'] + eotvos_corr + tide_corr

# %%
# the serial files for this cruise have some issues, so clean them up first
dgs_raw_clean = []
for path in tqdm(dgs_files_raw,desc='cleaning serial files'):  # clean up weird Ride serial files
    splitpath = path.split('/')
    newname = 'clean_' + splitpath[-1]
    splitpath[-1] = newname
    opath = '/'.join(splitpath)
    dgs_raw_clean.append(opath)
    if os.path.isfile(opath):
        continue
    with open(path, 'r') as f:
        A = f.readlines()
    long = []
    for line in A:
        if 'AT1M' in line and len(line.split(',')) == 19:
            long.append(line)
    with open(opath, 'w') as f:
        for line in long:
            f.write(line)
dgs_files_raw = np.sort(dgs_raw_clean)

# %%
# read the raw (serial) DGS data
raw_dgs = sgi.read_dgs_raw(dgs_files_raw, ship)

# %%
# read some meter info for the raw data calibration
# find the meter config file
ini_file = pooch.retrieve(url="https://zenodo.org/records/12733929/files/data.zip", 
        known_hash="md5:83b0411926c0fef9d7ccb2515bb27cc0", progressbar=True, 
        processor=pooch.Unzip(
            members=['data/Ride/SR2312/Meter.ini']))
opath = sgu.clean_ini_to_toml(ini_file[0])  # make it a little easier to read
meter_conf = tm.load(open(opath, 'rb'))

# %%
# calibrate stuff (though we won't use all of these things here)
# 24-bit channels
raw_dgs['grav_cal'] = (raw_dgs['Gravity']*meter_conf['Sensor']['GravCal']/cal_factor) + \
    meter_conf['Sensor']['g0']
raw_dgs['long_cal'] = (raw_dgs['Long']*meter_conf['Sensor']['LongCal']/cal_factor) + \
    meter_conf['Sensor']['LongOffset']
raw_dgs['cross_cal'] = (raw_dgs['Cross']*meter_conf['Sensor']['CrossCal']/cal_factor) + \
    meter_conf['Sensor']['CrossOffset']
raw_dgs['beam_cal'] = (raw_dgs['Beam']*meter_conf['Sensor']['beamgain']/cal_factor) + \
    meter_conf['Sensor']['beamzero']
# 10-bit channels
raw_dgs['temp_cal'] = (raw_dgs['Temp']*meter_conf['Sensor']['stempgain']) + \
    meter_conf['Sensor']['stempoffset']
raw_dgs['pressure_cal'] = (raw_dgs['Pressure']*meter_conf['Sensor']['pressgain']) + \
    meter_conf['Sensor']['presszero']
raw_dgs['electemp_cal'] = (raw_dgs['ElecTemp']*meter_conf['Sensor']['Etempgain']) + \
    meter_conf['Sensor']['Etempzero']
raw_dgs['grav'] = raw_dgs['grav_cal'] + biases['dgs']

# %%
# plot a comparison between serial and laptop data (raw, not FAA)
# select a small portion of the data bc otherwise it's hard to see anything
d0 = dgs_data.iloc[0]['date_time']
d1 = dgs_data.iloc[500]['date_time']
plt.figure(figsize=(11, 4.8))
sl0 = dgs_data.date_time > d0
sl1 = dgs_data.date_time < d1
plt.plot(dgs_data[(sl0) & (sl1)]['date_time'],
         dgs_data[(sl0) & (sl1)]['rgrav'], color='k', label='laptop')
sl0 = raw_dgs.date_time > d0
sl1 = raw_dgs.date_time < d1
plt.plot(raw_dgs[(sl0) & (sl1)]['date_time'], raw_dgs[(sl0) &
         (sl1)]['grav_cal'], color='r', lw=.5, label='serial')
plt.xlabel('Timestamp')
plt.ylabel('Raw gravity')
plt.legend(fontsize=8)
plt.tight_layout()

# %%
# get position information for raw data points from gps nav (serial files for
# this cruise, at least, have zeros where the coordinates are expected to be)
raw_dgs['tsec'] = [e.timestamp() for e in raw_dgs['date_time']
                   ]  # posix stamps in raw file
# have some dropouts
raw_dgs['lon_new'] = gps_lon_int(raw_dgs['tsec'].values)
raw_dgs['lat_new'] = gps_lat_int(raw_dgs['tsec'].values)

# %%
# NOTE that because of issues with the serial output for this cruise, the raw data
# is not sampled at an even time interval.
plt.figure()
plt.scatter(raw_dgs.date_time[1:], np.diff(raw_dgs.tsec), marker='.')
plt.xlabel('timestamp')
plt.ylabel('sampling interval in seconds')
plt.title('uneven sampling interval for serial data files')

# %% [markdown]
# We can get location info by interpolating from the nav files, but we would need to
# interpolate the data as well to obtain (and filter) the FAA from the serial files.
# Having verified that the laptop and serial files match well where there *is* data,
# I'm not going to bother with that here.

# %%
# apply a lowpass filter to FAA
taps = 2*240
freq = 1./240
# we resampled to the specified sampling rate when reading the data
nyquist = sampling/2
wn = freq/nyquist       # (if that wasn't the rate to begin with)
B = firwin(taps, wn, window='blackman')  # approx equivalent to matlab fir1

ffaa = filtfilt(B, 1, dgs_data['faa'])

# %%
# load satellite data for comparison
sat_path = pooch.retrieve(url="https://zenodo.org/records/12733929/files/data.zip", 
        known_hash="md5:83b0411926c0fef9d7ccb2515bb27cc0", progressbar=True, 
        processor=pooch.Unzip(
            members=['data/Ride/SR2312/sandwell_tracked.llg']))
sat_grav = np.loadtxt(sat_path[0], usecols=(2,))

# %%
# plot laptop FAA and satellite data (trim edge effects from filtering)
plt.figure(figsize=(11, 4.8))
plt.plot(dgs_data.iloc[taps:-taps//2]['date_time'],
         ffaa[taps:-taps//2], label='SR2312')
plt.plot(dgs_data.iloc[taps:-taps//2]['date_time'],
         sat_grav[taps:-taps//2], label='satellite')
plt.xlabel('Timestamp')
plt.ylabel('Free air anomaly [mGal]')
plt.legend(fontsize=8)
plt.tight_layout()

# show all of the figures
plt.show()

# %%
