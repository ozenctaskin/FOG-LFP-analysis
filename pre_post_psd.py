import mne 
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

def pre_post_psd(pre, post, epoch_length, fig_title):

    # Freqs
    freq_bands = {'theta': (4,8), 'alpha': (8,12), 
                  'beta': (12,30), 'low_gamma': (30,90)}
    
    # Combine channels into a single matrix and epoch
    pre_data = pre[0].copy()
    for i in range(1, len(pre)):
        pre_data.add_channels([pre[i]].copy())
    epoched_pre_data = mne.make_fixed_length_epochs(pre_data.copy(), epoch_length)

    post_data = post[0].copy()
    for i in range(1, len(post)):
        post_data.add_channels([post[i]].copy())
    epoched_post_data = mne.make_fixed_length_epochs(post_data.copy(), epoch_length)
    
    # Compute and plot average PSDs
    fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(10, 10))
    custom_lines = [Line2D([0], [0], color='blue', lw=2), Line2D([0], [0], color='red', lw=2)]
    fig.legend(custom_lines, ['pre', 'post'])
    fig.suptitle(fig_title)
    channels = ['ONE_THREE_LEFT', 'ONE_THREE_RIGHT', 'ZERO_TWO_LEFT', 'ZERO_TWO_RIGHT']
    average=True
    for idx, i in enumerate(freq_bands.keys()):
        row = idx // 2
        col = idx % 2
        print(row, col)
        epoched_pre_data.load_data().filter(l_freq=2, h_freq=122, picks=channels).compute_psd(picks=channels, fmin=freq_bands[i][0], fmax=freq_bands[i][1]).plot(picks=channels, axes=axes[row, col], color='blue', spatial_colors=False, average=average, show=False)
        epoched_post_data.load_data().filter(l_freq=2, h_freq=122, picks=channels).compute_psd(picks=channels, fmin=freq_bands[i][0], fmax=freq_bands[i][1]).plot(picks=channels, axes=axes[row, col], color='red', spatial_colors=False, average=average, show=False)
        axes[row, col].set_title(i)
        plt.show()
        
    return epoched_pre_data, epoched_post_data