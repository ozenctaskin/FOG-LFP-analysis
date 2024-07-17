import json, mne
import numpy as np

def read_data(json_file, pre, left_stim, right_stim, post):
    
    # Load json file 
    with open(json_file, 'r') as file:
        data = file.read() 
    raw_data = json.loads(data)
    streaming = raw_data['IndefiniteStreaming']
        
    # Create empty list to append the data and channel names 
    data_matrix = []
    channels = [] 
    
    # Loop through the data list and append to the array
    for i in streaming:
        data_matrix.append(i['TimeDomainData'])
        channels.append(i['Channel'])
 
    # Get the sample rate from the first measurements 
    sample_rate = streaming[0]['SampleRateInHz']        
 
    # Make dataset MNE style 
    mne_dataset = []
    for i in range(len(data_matrix)):
        info = mne.create_info([channels[i]], sample_rate)
        mne_data = mne.io.RawArray(np.reshape(np.array(data_matrix[i]), [1, len(data_matrix[i])]), info)  
        mne_dataset.append(mne_data)
        
    # Combine pre, post, left, right conditions together 
    data = {}
    data['pre'] = []
    if pre != 'NA':
        for i in pre:
            data['pre'].append(mne_dataset[i])
    data['post'] = []
    if post != 'NA':
        for i in post:
            data['post'].append(mne_dataset[i])
    data['left'] = []
    if left_stim != 'NA':
        for i in left_stim:
            data['left'].append(mne_dataset[i])
    data['right'] = []
    if right_stim != 'NA':
        for i in right_stim:
            data['right'].append(mne_dataset[i])
     
    # Create concatanated channels 
    concatanated_data = {}
    num_unique_channels = len(set(channels)) 
    for i in data.keys():
        concatanated_data[i] = []
        for t in range(len(data[i])):
            if t < num_unique_channels:
                concatanated_data[i].append(data[i][t])
            if t >= num_unique_channels: 
                to_concat = t % num_unique_channels
                concatanated_data[i][to_concat] = mne.concatenate_raws([concatanated_data[i][to_concat], data[i][t]].copy())

    return data, concatanated_data