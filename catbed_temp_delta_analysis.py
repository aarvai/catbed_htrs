from kadi import events
from utilities import heat_map

dumps = events.dumps
dumps.interval_pad = (10, 7200)

close('all')

for thr in range(1, 5):
    t1 = 'PM' + str(thr) + 'THV1T'
    t2 = 'PM' + str(thr) + 'THV2T'
    
    x = fetch.Msidset([t1, t2],'2000:001',stat='5min')
    
    # Hack to avoid bug where midvals aren't removed with remove_intervals
    x[t1].vals = x[t1].midvals
    x[t2].vals = x[t2].midvals
    
    x[t1].remove_intervals(dumps)
    x[t2].remove_intervals(dumps)
    
    if all(x[t1].times == x[t2].times):
        dt = x[t1].vals - x[t2].vals
        
        figure(1)
        subplot(2,2,thr)
        plot_cxctime(x[t1].times, dt, 'b.', alpha=.01)
        ylabel('deg F')
	title(t1 + ' - ' + t2 + ' (Excluding Dumps)')
        ylim([-15,15])

        figure(2)
        subplot(2,2,thr)
        heat_map(x[t1].times, dt, bins=(25,25), y_lim=[-15,15])
        ylabel('deg F')
	title(t1 + ' - ' + t2 + ' (Excluding Dumps)')
        
    
