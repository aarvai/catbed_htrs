from kadi import events
from utilities import heat_map

#t_start = '1999:204:00:00:00.000'
#t_stop = '2000:001:00:00:00.000'

t_start = '1999:204:00:00:00.000'
t_stop = '1999:250:00:00:00.000'

dumps = events.dumps
dumps.interval_pad = (10, 7200)

close('all')

t1 = 'PM4THV1T'
t2 = 'PM4THV2T'
x = fetch.Msidset([t1, t2],t_start, t_stop)
x.interpolate(dt=32.8)
x[t1].remove_intervals(dumps)
x[t2].remove_intervals(dumps)
if all(x[t1].times == x[t2].times):
    dt = x[t1].vals - x[t2].vals
    
    figure(1)
    x[t1].plot('b',label=t1)
    x[t2].plot('r',label=t2)
    title(t2 + ' (Excluding Dumps)')
    ylabel('deg F')
    legend()
    ylim([40,120])
    
    figure(2)
    plot_cxctime(x[t2].times, dt, 'b.')
    plot_cxctime(x[t2].times, dt, 'b-', alpha=.1)
    title(t1 + ' minus ' + t2 + ' (Excluding Dumps)')
    ylabel('deg F')
    ylim([-5,15])
