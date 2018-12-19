import numpy as np
import pandas as pd
import xdf
import re

def exportStream(file_path, stream_name, markers_stream_name=None, markers_to_write=None):
    streams = xdf.load_xdf(file_path, verbose=False)
    
    subject_number = None
    digits = re.findall('\\d+', file_path[file_path.rfind('/'):])
    if len(digits) > 0:
        subject_number = digits[0]
    
    # Find the desired stream
    desired_stream = None
    for i in range (len(streams[0])):
        if streams[0][i]['info']['name'][0] == stream_name:
            desired_stream = streams[0][i]
            break
    
    if desired_stream is None:
        return "Stream " + stream_name + " not found"

    if markers_stream_name is not None and markers_stream_name is not '':
        # Put the data in array, row by row, with a place for the markers
        desired_stream_data = []
        for i in range(len(desired_stream['time_series'])):
            desired_stream_data.append([desired_stream['time_series'][i][0], 0, desired_stream['time_stamps'][i]])
        
        # Find the Marker data
        markers = None
        for i in range (len(streams[0])):
            if streams[0][i]['info']['name'][0] == markers_stream_name:
                markers = streams[0][i]
                break
        
        if markers is None:
            return "Markers stream " + markers_stream_name + " not found"

        # Define function for finding the nearest value in an array
        # Used to find the closest desired stream timestamp that matches the timestamp of each marker
        def find_nearest(array,value):
            idx = (np.abs(array-value)).argmin()
            return idx

        # Add the markers to right rows of desired stream data
        for i in range(len(markers['time_series'])):
            if markers_to_write == None or len(markers_to_write) == 0 or int(markers['time_series'][i]) in markers_to_write:
                index = find_nearest(desired_stream['time_stamps'], markers['time_stamps'][i])
                desired_stream_data[index][1] = int(markers['time_series'][i])

        # Create a dataframe with the desired stream data
        desired_stream_dataframe = pd.DataFrame(desired_stream_data, columns=[stream_name, 'Markers', 'Time'])
    else:
        # Put the data in array, row by row
        desired_stream_data = []
        for i in range(len(desired_stream['time_series'])):
            desired_stream_data.append([desired_stream['time_series'][i][0], desired_stream['time_stamps'][i]])
        
        # Create a dataframe with the desired stream data
        desired_stream_dataframe = pd.DataFrame(desired_stream_data, columns=[stream_name, 'Time'])

    # Save the desired stream dataframe to CSV
    output_file_path = file_path[:file_path.rfind('/')] # File path without file name
    output_file_name = stream_name
    if subject_number is not None and subject_number is not '':
        output_file_name = output_file_name + '-' + str(subject_number)
    desired_stream_dataframe.to_csv(output_file_path + '/' + output_file_name + '.csv', sep='\t', index=False)

    print("File " + output_file_name + ".csv created successfully")
    return "File " + output_file_name + ".csv created successfully"