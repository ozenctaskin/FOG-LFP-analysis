from read_data import read_data
from pre_post_psd import pre_post_psd

# Session 2
data, concat = read_data('/run/user/1000/gvfs/smb-share:server=chenshare.srv.uhnresearch.ca,share=chenshare/Amitabh Bhattacharya/FOG/Pilot patients/DBS/Report_Json_Session_Report_20240527T152551_fullData.json', range(0,6), range(6,18), range(6,18), range(18,24))
channels, pre_freqs, pre_aperiodic, pre_periodic, post_freqs, post_aperiodic, post_periodic = pre_post_psd(concat['pre'], concat['post'], 'PPN excitatory')

# Session 3
data, concat = read_data('/run/user/1000/gvfs/smb-share:server=chenshare.srv.uhnresearch.ca,share=chenshare/Amitabh Bhattacharya/FOG/Pilot patients/DBS/Report_Json_Session_Report_20240603T145759_FullData_Visit3.json', range(0,6), range(12,18), range(12,18), range(18,24))
channels, pre_freqs, pre_aperiodic, pre_periodic, post_freqs, post_aperiodic, post_periodic = pre_post_psd(concat['pre'], concat['post'], 'PPN inhibitory')

# Session 4
data, concat = read_data('/run/user/1000/gvfs/smb-share:server=chenshare.srv.uhnresearch.ca,share=chenshare/Amitabh Bhattacharya/FOG/Pilot patients/DBS/Report_Json_Session_Report_20240610T155257_FullData_Visit4.json', range(0,18), range(18,24), range(24, 30), range(30,42))
channels, pre_freqs, pre_aperiodic, pre_periodic, post_freqs, post_aperiodic, post_periodic = pre_post_psd(concat['pre'], concat['post'], 'UF excitatory')

# Session 5
data, concat = read_data('/run/user/1000/gvfs/smb-share:server=chenshare.srv.uhnresearch.ca,share=chenshare/Amitabh Bhattacharya/FOG/Pilot patients/DBS/Report_Json_Session_Report_20240617T100401_FullData_Visit5.json', range(0,12), range(12,18), range(18, 24), range(24,42))
channels, pre_freqs, pre_aperiodic, pre_periodic, post_freqs, post_aperiodic, post_periodic = pre_post_psd(concat['pre'], concat['post'], 'UF inhibitory')