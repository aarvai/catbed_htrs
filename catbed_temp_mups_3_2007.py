# Range 1
#t_start = '2006:351:00:00:00.000'
#t_stop = '2006:351:12:00:00.000'

# Range 2
#t_start = '2006:349:00:00:00.000'
#t_stop = '2006:354:00:00:00.000'

# Range 3
t_start = '2000:001'
t_stop = None

t_event = '2006:351:04:38:00.000'

t_event_pad = DateTime(t_event).secs + 60
old_setpoints = [[59.55,96.9],[58.32, 97.77]]

close('all')

x = fetch.Msidset(['PM3THV1T','PM3THV2T'], t_start, t_stop, stat='5min')
#x.interpolate(dt=32.8)
post = x['PM3THV1T'].times > DateTime(t_event).secs
dt = x['PM3THV1T'].vals - x['PM3THV2T'].vals

for ab in range(1,3):
    subplot(3,1,ab)
    temp = 'PM3THV' + str(ab) + 'T'
    x[temp].plot('b', label='Pre-event')
    plot_cxctime(x[temp].times[post], x[temp].vals[post], 'r', label='Post-event')
    title(temp)
    ylabel('deg F')
    ylim([45,115])
    old_on = array([old_setpoints[ab-1][0], old_setpoints[ab-1][0]])
    old_off = array([old_setpoints[ab-1][1], old_setpoints[ab-1][1]])
    plot(xlim(), old_on, 'b:', label='Pre-Event Range')
    plot(xlim(), old_off, 'b:')
    legend()
    
subplot(3,1,3)
plot_cxctime(x['PM3THV1T'].times, dt, 'b', label='Pre-event')
plot_cxctime(x['PM3THV1T'].times[post], dt[post], 'r', label='Post-event')
title('PM3THV1T minus PM3THV2T')
ylabel('deg F')
ylim([-5,5])
plot(xlim(), array([2.45,2.45]), 'b:', label='Pre-Event Range')
plot(xlim(), array([-.86,-.86]), 'b:')
legend(loc='best')
