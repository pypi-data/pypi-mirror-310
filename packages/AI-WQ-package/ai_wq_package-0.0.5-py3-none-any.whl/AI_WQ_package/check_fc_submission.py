# script to check netCDF file for forecast submission
import xarray as xr
import numpy as np
import ftplib
from datetime import datetime, timedelta

def check_variable_in_list(variable_name, expected_values):
    if variable_name not in expected_values:
        raise ValueError(f"Expected one of {expected_values}, but got {variable_name}.")

def check_Monday_forecast_data(fc_start_date):
    # use datetime to convert string into date_obj
    date_obj = datetime.strptime(fc_start_date,'%Y%m%d')

    # check that it is within allotted time window
    # previous Wednesday to end of succeeding Tuesday
    now = datetime.utcnow()
    # calculate number of days to subtract to get to Wednesday
    days_to_subtract = (date_obj.weekday() - 2)%7
    previous_wednesday = date_obj - timedelta(days=days_to_subtract)
    # set time to 00 UTC
    previous_wed_0z = previous_wednesday.replace(hour=0,minute=0,second=0,microsecond=0)
    pre_wed_str = previous_wed_0z.strftime('%Y%m%d')

    # get succeeding Tuesday
    days_to_add = (8- date_obj.weekday())%7 # use weekday and work out number of days to the following Tuesday
    next_tuesday = date_obj+timedelta(days=days_to_add)
    # set time to 23:59:59
    end_of_next_tues = next_tuesday.replace(hour=23,minute=59,second=59,microsecond=59)
    end_of_next_tues_str = end_of_next_tues.strftime('%Y%m%d')

    # check chosen data is within the Wednesday to Tuesday alloted timewindow
    if previous_wed_0z <= now <= end_of_next_tues:
        print ('forecast submitted within competition time window')
    else:
        raise ValueError(f"Forecast start date of {fc_start_date}, is not within allotted time window. Allowed time window for this forecast start date is {pre_wed_str} to {end_of_next_tues_str}")

def convert_wk_lead_time_to_string(value):
    # convert the wk_lead_time variable to a string for saving
    if isinstance(value,(int,float)):
        return str(int(value)) # save a string of the integer value
    elif isinstance(value,(str)):
        return value # if it already is a string, just return the string value
    else:
        raise ValueError(f"The value '{value}' is not a number nor str.")

def check_and_flip_latitudes(ds, lat_name='latitude'):
    """
    Check if latitudes range from 90 to -90, and flip if necessary.

    Parameters:
        ds (xarray.Dataset): The dataset to check.
        lat_name (str): Name of the latitude variable in the dataset.

    Returns:
        xarray.Dataset: The modified dataset with corrected latitude ordering. Latitude ordering should always be 90 to -90.
    """
    # Check if the latitude variable exists
    if lat_name not in ds.coords:
        raise ValueError(f"Latitude coordinate '{lat_name}' not found in the dataset.")

    # Extract latitude values
    latitudes = ds[lat_name].values

    # Check if latitudes need to be flipped
    if latitudes[0] < latitudes[-1]:  # If increasing order
        print("Latitudes are in ascending order; flipping them to descend from 90 to -90.")
        ds = ds.sortby(lat_name, ascending=False)
    return ds

def check_and_convert_longitudes(ds, lon_name='longitude'):
    """
    Check if longitudes range from 0 to 360 and convert if necessary.

    Parameters:
        ds (xarray.Dataset): The dataset to check.
        lon_name (str): Name of the longitude variable in the dataset.

    Returns:
        xarray.Dataset: The modified dataset with longitudes converted to 0 to 360 range.
    """
    # Check if the longitude variable exists
    if lon_name not in ds.coords:
        raise ValueError(f"Longitude coordinate '{lon_name}' not found in the dataset.")

    # Extract longitude values
    longitudes = ds[lon_name].values

    # Check if longitudes are in the -180 to 180 range
    if np.any(longitudes < 0):
        print("Longitudes are in the -180 to 180 range; converting to 0 to 360.")
        longitudes = (longitudes + 360) % 360  # Convert to 0 to 360 range
        ds = ds.assign_coords({lon_name: longitudes})  # Update the dataset's longitude coordinates
    return ds

def all_checks(data,variable,fc_start_date,wk_lead_time,teamname,modelname):
        ''' This function performs all checks on submitted fields.
    Parameters:
        data (xarray.Dataset): xarray dataset with forecasted probabilites in format (quintile, lat, long).
        variable (str): Saved variable. Options include 'tas', 'mslp' and 'pr'.
        fc_start_date (str): The forecast start date as a string in format '%Y%m%d', i.e. 20241118.
        wk_lead_time (str or number): Three- or four-week forecast, i.e. '3' or 3.
        teamname (str): The teamname that was submitted during registration.
        modelname (str): Modelname for particular forecast. Teams are only allowed to submit three models each.

    '''
    # (1) first check submitted variables apart from data, i.e. components of the filename.
    # (1.a) check submitted variable name. - only allowed to submit 'tas', 'mslp' and 'pr'.
    check_variable_in_list(variable,['tas','mslp','pr'])
    # need to check fc_start_date. (1) is it a Monday. (2) is it within correct time window. 
    # (1.b) is forecast date a Monday and is it within the correct time-window?
    check_Monday_forecast_data(fc_start_date)        

    # (1.c) convert week lead-time to string and check it is 3 or 4.
    wk_lead_time_str = convert_wk_lead_time_to_string(wk_lead_time)
    check_variable_in_list(wk_lead_time_str,['3','4'])

    # (1.d) need to check TEAMNAME and MODELNAME.
    final_filename = variable+'_'+fc_start_date+'_wk'+wk_lead_time_str+'_'+teamname+'_'+modelname+'.nc'

    # (2) Check the submitted xarray dataset.

    # (2.a) check the format of the submitted xarray - should be netcdf.

    # (2.b) check spatial components.
    # (2.bi) lat range [should be 90, -90 , 'degrees_north']
    data = check_and_flip_latitudes(data)
    # (2.bii) long range [should be 0 to 359.0,'degrees_east']
    data = check_and_convert_longitudes(data)

    # (2.c) check the quantile range 

    # (2.d) check for a full global set of values between 0.0 and 1.0

    return data, filename





