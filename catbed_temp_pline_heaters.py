from kadi import events
from utilities import append_to_array, same_limits

close('all')

proxies = ['PLINE02T','PLINE03T','PLINE08T','PLINE09T']
htr_ranges = [60, 70, 60, 80]
abs = ['A','A','B','A']

for thr in range(1,5):
    temp = proxies[thr-1]
    ab = abs[thr-1]
    x = fetch.Msid(temp, '2000:001', stat='5min')
    dt = diff(x.midvals)
    local_min = (append_to_array(dt <= 0, pos=0, val=bool(0)) & 
                 append_to_array(dt > 0, pos=-1, val=bool(0)))
    htr_range = x.vals < htr_ranges[thr-1]
    htr_cycle = local_min & htr_range
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
    plot_cxctime(dates, htr_freq, 'r.', label=temp)
    title(temp + '(MUPS-' + str(thr) + str(ab) + ' Proxy) Heater Cycling Frequency')

same_limits((221, 222))
same_limits((223, 224))
