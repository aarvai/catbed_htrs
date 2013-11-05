from kadi import events
from utilities import append_to_array, find_first_after, same_limits, heat_map

close('all')

temp = 'PM3THV2T'
on_range = 60
off_range = 89 
t_start = '2000:001'
t_stop = None
#t_stop = '2013:268'

t_event = array([DateTime('2006:351:04:38:00.000').secs, 
                 DateTime('2006:351:04:38:00.000').secs])

x = fetch.Msid(temp, t_start, t_stop)
dt = diff(x.vals)

local_min = (append_to_array(dt <= 0., pos=0, val=bool(0)) & 
             append_to_array(dt > 0., pos=-1, val=bool(0)))
local_max = (append_to_array(dt >= 0., pos=0, val=bool(0)) & 
             append_to_array(dt < 0., pos=-1, val=bool(0)))

htr_on_range = x.vals < on_range
htr_off_range = x.vals > off_range

htr_on = local_min & htr_on_range
htr_off = local_max & htr_off_range

#remove any incomplete heater cycles at end of timeframe
last_off = nonzero(htr_off)[0][-1]
htr_on[last_off:] = 0

t_on = x.times[htr_on]
t_off = x.times[htr_off]

match_i = find_first_after(t_on, t_off)

dur = t_off[match_i] - t_on

#compute duty cycles by month
on_dates = DateTime(t_on).iso
on_yrs = [date[0:4] for date in on_dates]
on_mos = [date[5:7] for date in on_dates]
on_freq = zeros(168)
on_time = zeros(168)
avg_on_time = zeros(168)
dates = zeros(168)
i = 0
for yr in range(2000, 2014):
    for mo in range(1,13):
        yr_match = array([on_yr == str(yr) for on_yr in on_yrs])
        mo_match = array([on_mo == str(mo).zfill(2) 
                          for on_mo in on_mos])
        on_freq[i] = sum(yr_match & mo_match)
        on_time[i] = sum(dur[yr_match & mo_match])
        avg_on_time[i] = mean(dur[yr_match & mo_match])
        dates[i] = DateTime(str(yr) + '-' + str(mo).zfill(2) 
                            + '-01 00:00:00.000').secs
        i = i + 1
dates_range = append(dates, DateTime('2014:001').secs)
dc = on_time / (dates_range[1:] - dates_range[:-1])

figure(1)
plot_cxctime(t_on, dur, 'b.', alpha=.05, mew=0)
plot_cxctime(t_event, ylim(),'r:')
ylabel('On-Time Durations [sec]')
title('MUPS-3 Valve Heater On-Time Durations')

figure(2)
plot_cxctime(x.times, x.vals, mew=0)
plot_cxctime(x.times, x.vals, 'b*',mew=0)
plot_cxctime(x.times[htr_on], x.vals[htr_on], 'c*',mew=0, label='Heater On')
plot_cxctime(x.times[htr_off], x.vals[htr_off], 'r*',mew=0, label='Heater Off')
plot_cxctime(t_event, ylim(),'r:')
legend()

figure(3)
hist(dur, bins=100, normed=True)
xlabel('On-Time Durations [sec]')
title('MUPS-3 Valve Heater On-Time Durations')

figure(4)
plot_cxctime(dates, dc*100, '*', mew=0)
plot_cxctime(t_event, ylim(),'r:')
title('MUPS-3 Valve Heater Duty Cycle')
ylabel('Heater Duty Cycle by Month [%] \n (Total On-time / Total Time)')

figure(5)
plot_cxctime(dates, on_freq, '*', mew=0)
plot_cxctime(t_event, ylim(),'r:')
title('MUPS-3 Valve Heater Cycling Frequency')
ylabel('Heater Cycles per Month')

figure(6)
plot_cxctime(dates, on_time/3600, '*', mew=0)
plot_cxctime(t_event, ylim(),'r:')
title('MUPS-3 Valve Heater On-Time')
ylabel('Heater On-Time by Month [hrs]')

figure(7)
plot_cxctime(dates, avg_on_time/3600, '*', mew=0)
plot_cxctime(t_event, ylim(),'r:')
title('MUPS-3 Valve Heater Average On-Time')
ylabel('Mean Heater On-Time by Month [hrs]')