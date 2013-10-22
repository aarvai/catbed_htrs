from kadi import events
from utilities import append_to_array, same_limits

close('all')

for thr in range(1,5):
    for ab, c in zip(range(1,3),('b.', 'r.')):
        temp = 'PM' + str(thr) + 'THV' + str(ab) + 'T'
        x = fetch.Msid(temp, '2000:001', stat='5min')
        dt_check = diff(x.midvals) > 8
        large_dt = append_to_array(dt_check, pos=-1, val=bool(0))
        htr_range = x.midvals < 75
        htr_cycle = large_dt & htr_range
        htr_dates = DateTime(x.times[htr_cycle]).iso
        htr_yrs = [date[0:4] for date in htr_dates]
        htr_mos = [date[5:7] for date in htr_dates]
        htr_freq = zeros(168)
        dates = zeros(168)
        i = 0
        for yr in range(2000, 2014):
            for mo in range(1,13):
                yr_match = array([htr_yr == str(yr) for htr_yr in htr_yrs])
                mo_match = array([htr_mo == str(mo).zfill(2) 
                                  for htr_mo in htr_mos])
                htr_freq[i] = sum(yr_match & mo_match)
                dates[i] = DateTime(str(yr) + '-' + str(mo).zfill(2) 
                                    + '-01 00:00:00.000').secs
                i = i + 1
        subplot(2,2,thr)
        plot_cxctime(dates, htr_freq, c, label=temp)
        title('MUPS-' + str(thr) + ' Heater Cycling Frequency')
        legend(loc='best')
        ylabel('Cycles per Month')

same_limits((221, 222))
same_limits((223, 224))