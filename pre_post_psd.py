import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D
from neurodsp.spectral import compute_spectrum, trim_spectrum
from neurodsp.filt import filter_signal
from neurodsp.aperiodic import compute_irasa

def pre_post_psd(pre, post, fig_title):

    # Freqs
    freq_bands = {'theta': (4,8), 'alpha': (8,12), 
                  'beta': (12,30), 'low_gamma': (30,90)}
    
    # Filtering freq
    f_range = (5, 40)
    
    # Compute periodic and oscillatory components with IRASA
    channel_names = []
    pre_freqs, pre_aperiodic, pre_periodic = [[],[],[]]
    post_freqs, post_aperiodic, post_periodic = [[],[],[]]    
    pre_orig = []
    post_orig = [] 
    for i in range(len(pre)):
        pre[i].get_data()[0,:] = filter_signal(pre[i].get_data()[0,:], pre[i].info['sfreq'], 'bandpass', f_range)
        channel_names.append(pre[i].ch_names)
        freqs, psd = compute_spectrum(pre[i].get_data()[0,:], pre[i].info['sfreq'], nperseg=int(4*pre[i].info['sfreq']))
        freqs, psd = trim_spectrum(freqs, psd, f_range)
        pre_orig.append(psd)
        freqs, psd_aperiodic, psd_periodic = compute_irasa(pre[i].get_data()[0,:], int(pre[i].info['sfreq']), f_range=f_range)
        pre_freqs.append(freqs), pre_aperiodic.append(psd_aperiodic), pre_periodic.append(psd_periodic)
        
        post[i].get_data()[0,:] = filter_signal(post[i].get_data()[0,:], post[i].info['sfreq'], 'bandpass', f_range)
        freqs, psd = compute_spectrum(post[i].get_data()[0,:], post[i].info['sfreq'], nperseg=int(4*pre[i].info['sfreq']))
        freqs, psd = trim_spectrum(freqs, psd, f_range)
        post_orig.append(psd)
        freqs, psd_aperiodic, psd_periodic = compute_irasa(post[i].get_data()[0,:], int(pre[i].info['sfreq']), f_range=f_range)
        post_freqs.append(freqs), post_aperiodic.append(psd_aperiodic), post_periodic.append(psd_periodic)        
        
    # Average periodic and aperiodic signals from all channels and plot
    fig, axes = plt.subplots(nrows=1, ncols=3, figsize=(15, 5))
    custom_lines = [Line2D([0], [0], color='blue', lw=2), Line2D([0], [0], color='green', lw=2)]
    for i in [1,3]:
        
        axes[0].plot(pre_freqs[0], np.mean(np.stack(pre_orig, axis=0), axis=0), color='blue')
        axes[0].plot(post_freqs[0], np.mean(np.stack(post_orig, axis=0), axis=0), color='green')     
        axes[1].plot(pre_freqs[0], np.mean(np.stack(pre_periodic, axis=0), axis=0), color='blue')
        axes[1].plot(post_freqs[0], np.mean(np.stack(post_periodic, axis=0), axis=0), color='green')
        axes[2].plot(pre_freqs[0], np.mean(np.stack(pre_aperiodic, axis=0), axis=0), color='blue')
        axes[2].plot(post_freqs[0], np.mean(np.stack(post_aperiodic, axis=0), axis=0), color='green')                 

        axes[0].set_title('Original PSD')
        axes[0].set_xlabel('Frequency (Hz)')
        axes[0].set_ylabel('Power (V^2/Hz)')
        axes[0].legend(custom_lines, ['pre', 'post'])
        axes[0].set_ylim([-2, 15])
        
        axes[1].set_title('Periodic')
        axes[1].set_xlabel('Frequency (Hz)')
        axes[1].set_ylabel('Power (V^2/Hz)')
        axes[1].legend(custom_lines, ['pre', 'post'])
        axes[1].set_ylim([-2, 6])
        
        axes[2].set_title('Aperiodic')
        axes[2].set_xlabel('Frequency (Hz)')
        axes[2].set_ylabel('Power (V^2/Hz)')
        axes[2].legend(custom_lines, ['pre', 'post']) 
        axes[2].set_ylim([-2, 20])
    fig.suptitle(fig_title)
        
    return channel_names, pre_freqs, pre_aperiodic, pre_periodic, post_freqs, post_aperiodic, post_periodic