import numpy as np
import pandas as pd
import os

def new_alt_values(x): # this function converts original latitude values into the new altitude values
    lat_deltas = x - min_lat
    y_1 = lat_deltas * np.sin(rot_ang_rad)
    conv_alt = y_1 * alt_conv_factor
    output_alt = conv_alt + des_min_alt
    return output_alt

def new_lat_values(x): # this function converts original latitude values into the new latitude values
    lat_deltas = x - min_lat
    x_1 = lat_deltas * np.cos(rot_ang_rad)
    output_lat = x_1 + min_lat
    return output_lat

file_name = input('Enter name of file: ')
rot_ang_deg = input('Please enter desired rotation angle from 0 - 180 degrees: ')
rot_ang_rad = float(rot_ang_deg) * 0.0174533
csv_df = pd.read_csv(file_name, delimiter = ',')
min_lat = csv_df['latitude'][csv_df['latitude'].idxmin()]

if csv_df.columns[2] == 'altitude(m)' : # this runs if the original .CSV file was generated with metric units
    des_min_alt = input('Please enter desired minimum altitude in meters: ')
    des_min_alt = float(des_min_alt)
    alt_conv_factor = 110947.2
    alt_type = 'm'
    csv_df['altitude(m)'] = csv_df['latitude'].apply(new_alt_values)
    print('Minimum Altitude:', des_min_alt, 'meters')

elif csv_df.columns[2] == 'altitude(ft)' : # this runs if the original .CSV file was generated with imperial units
    des_min_alt = input('Please enter desired minimum altitude in feet: ')
    des_min_alt = float(des_min_alt)
    alt_conv_factor = 364000.0
    alt_type = 'ft'
    csv_df['altitude(ft)'] = csv_df['latitude'].apply(new_alt_values)
    print('Minimum Altitude:', des_min_alt, 'feet')

else :
    print('Error with input file!')

csv_df['latitude'] = csv_df['latitude'].apply(new_lat_values)

output_file_name = file_name[0:-4] + '_' + str(des_min_alt) + '_' + alt_type + '_' + rot_ang_deg + '_degrees.csv' # this sets the name of the output file to the minimum altitude and rotation angle
output_file_path = os.path.dirname(os.path.abspath(__file__)) # this is the same path as this running script
csv_df.to_csv(output_file_path + '/' + output_file_name, index = False)

print('Exported' , output_file_name, 'to', output_file_path)
