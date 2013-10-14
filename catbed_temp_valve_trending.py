from kadi import events
from utilities import append_to_array, same_limits

close('all')

bad_all = ['2000:048:00:00:00 2000:052:00:00:00',
           '2000:228:00:00:00 2000:229:00:00:00',
           '2000:302:00:00:00 2000:303:00:00:00',
           '2001:111:00:00:00 2001:114:00:00:00',
           '2004:200:00:00:00 2004:201:00:00:00',
           '2004:208:00:00:00 2004:209:00:00:00',
           '2004:213:00:00:00 2004:214:00:00:00',
           '2008:225:00:00:00 2008:228:00:00:00',
           '2008:292:00:00:00 2008:295:00:00:00',
           '2010:150:00:00:00 2010:152:00:00:00',
           '2011:187:00:00:00 2011:193:00:00:00',
           '2011:297:00:00:00 2011:304:00:00:00',
           '2012:150:00:00:00 2012:153:00:00:00']

for fig, thr, ab, sub in zip([1,1,1,1,2,2,2,2],[1,1,2,2,3,3,4,4],
                             [1,2,1,2,1,2,1,2],[1,3,2,4,1,3,2,4]):
    
    # Get Data
    temp = 'PM' + str(thr) + 'THV' + str(ab) + 'T'
    x = fetch.Msid(temp, '2000:001', stat='daily')
    x.filter_bad_times(table=bad_all)
    
    # Set up axes
    figure(fig)
    ax1 = subplot(2, 2, sub)
    ax1.ticklabel_format(useOffset=False)
    ax_pos = ax1.get_position().get_points()
    ax_width = ax_pos[1,0] - ax_pos[0,0]
    ax_height = ax_pos[1,1] - ax_pos[0,1]
    delaxes(ax1)
    ax2 = axes([ax_pos[0,0], ax_pos[0,1] + .20 * ax_height, 
                ax_width, .75 * ax_height]) 
    ax2.ticklabel_format(useOffset=False)               
    
    # Plot Trending
    plot_cxctime(x.times, x.mins, 'g.', label='mins')
    plot_cxctime(x.times, x.maxes, 'b.', label='maxes')
    plot_cxctime(x.times, x.means, 'k.', label='means')
    title(temp + ' Daily Trending')
    legend(loc='best')   
    if thr == 1 or thr == 2:
        ylim([50,200])
    elif thr == 3 or thr == 4:
        ylim([50,120])
    ylabel('deg F')
    
    # Set up Standard Dev Axes and plot
    ax2.set_xticklabels([])
    ax3 = axes([ax_pos[0,0], ax_pos[0,1] + .05 * ax_height, 
                   ax_width, .15 * ax_height])
    plot_cxctime(x.times, x.stds, color='k', label=(' stdev'))
    ax3.yaxis.set_major_locator(ticker.MaxNLocator(2))
    if thr == 1 or thr == 2:
        ylim([0,50])
    elif thr == 3 or thr == 4:
        ylim([0,15])
    y_ticks = yticks()
    y_lim = ylim()
    ylabel('St Dev')
    
    # Prevent overlap between y-axis and stdev y-axis
    if (y_lim[1] - y_ticks[0][-1]) / y_lim[-1] < .70:
        yticks(y_ticks[0][:-1])        
       

#same_limits((221, 222))
#same_limits((223, 224))