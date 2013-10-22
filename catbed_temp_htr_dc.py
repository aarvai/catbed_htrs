from kadi import events
from utilities import append_to_array, find_first_after, same_limits, heat_map

close('all')

temp = 'PM3THV1T'
on_range = 65
off_range = 90 

x = fetch.Msid(temp, '2000:001', '2013:286')
dt = diff(x.vals)

local_min = (append_to_array(dt <= 0., pos=0, val=bool(0)) & 
             append_to_array(dt > 0., pos=-1, val=bool(0)))
local_max = (append_to_array(dt >= 0., pos=0, val=bool(0)) & 
             append_to_array(dt < 0., pos=-1, val=bool(0)))

htr_on_range = x.vals < on_range
htr_off_range = x.vals > off_range

htr_on = local_min & htr_on_range
htr_off = local_max & htr_off_range

t_on = x.times[htr_on]
t_off = x.times[htr_off]

#over = nonzero(append_to_array(t_off[:-1] > t_on[1:], pos=-1, val=bool(0)))
#t_off[over] = t_on[over] + .5*(t_on[over+1] - t_on[over])
#t_off = [t_off[i] = t_on[i] + .5*(t_on[i+1] - t_on[i]) for i in range(len(t_on)) if t_off[i] > t_on[i+1]]

match_i = find_first_after(t_on, t_off)


dur = t_off[match_i] - t_on

figure(1)
plot_cxctime(t_on, dur, 'b.', alpha=.2)
plot_cxctime(t_on, dur, 'b.', alpha=.2)
ylabel('On-Time Durations [sec]')
title('MUPS-3 Valve Heater Cycle Durations')

figure(2)
plot_cxctime(x.times, x.vals)
plot_cxctime(x.times, x.vals, 'b*',mew=0)
plot_cxctime(x.times[htr_on], x.vals[htr_on], 'c*',mew=0)
plot_cxctime(x.times[htr_off], x.vals[htr_off], 'r*',mew=0)

figure(3)
heat_map(t_on, dur, y_lim=[0,2000], bins=400)
ylabel('On-Time Durations [sec]')
title('MUPS-3 Valve Heater Cycle Durations')
xlabel('Time since 2000:001 [sec]')