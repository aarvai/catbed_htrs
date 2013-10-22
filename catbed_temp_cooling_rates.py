from scipy.optimize import curve_fit

from kadi import events
from Ska.engarchive import fetch_eng as fetch
from Ska.Matplotlib import plot_cxctime

from utilities import (find_closest, find_last_before, find_first_after, 
                       same_limits, remove_therm_dropouts)

close('all')

tstart = '2000:001'
pitch_bin_min = 160
pitch_bin_max = 170
min_dur = 120 #minutes

dwells = events.dwells.filter(dur__gt=min_dur*60)

all_t1 = array(dwells.table['tstart'])
all_t2 = array(dwells.table['tstop'])
all_durs = array(dwells.table['dur'])
all_tmid = all_t1 + .5 * all_durs

x = fetch.Msid('PITCH', tstart, stat='5min')
all_pitch_i = find_closest(all_tmid, x.times)
all_pitch = x.vals[all_pitch_i]
# Identify dwells without valid pitch data
ok = ((x.times[all_pitch_i] > all_t1) & 
      (x.times[all_pitch_i] < all_t2))     
if sum(~ok) > 0:
    print('Pitch data missing during ' + str(sum(~ok)) + ' dwells')
    
in_bin = (all_pitch > pitch_bin_min) & (all_pitch < pitch_bin_max)
t1 = all_t1[in_bin & ok]
t2 = all_t2[in_bin & ok]
pitch = all_pitch[in_bin & ok]
durs = all_durs[in_bin & ok]

msids = ['PM1THV1T','PM1THV2T','PM2THV1T','PM2THV2T',
         'PM3THV1T','PM3THV2T','PM4THV1T','PM4THV2T']

if 'msid_cache' not in globals():
    print 'Fetching Telemetry'
    tlm = fetch.Msidset(msids, tstart, stat='5min')
    remove_therm_dropouts(tlm)
    # Cache telemetry values between runs (use "run -i ...")
    msid_cache = tlm 
else:
    print 'Getting telemetry from cache'
    tlm = msid_cache
    
def linfit(x, a, b):
    return a + b*x 

for thr in range(1,3):

    for ab, c in zip(range(1,3), ('b','r')):

        temp = 'PM' + str(thr) + 'THV' + str(ab) + 'T'
        x = tlm[temp]
        
        i1 = find_first_after(t1, x.times)
        i2 = find_last_before(t2, x.times)
        
        # Check for eclipses with zero valid data due to dropouts
        ok2 = i2 > i1
        i1 = i1[ok2]
        i2 = i2[ok2] 
        
        cooling_rates = (x.vals[i2] - x.vals[i1]) * 3600 / durs[ok2]
        
        # Correct cooling rates for starting temperature
        # Linear fit varies by valve and by temp
        p_opt, p_cov = curve_fit(linfit, float64(x.vals[i1]), cooling_rates)
        corr_rates = linfit(float64(x.vals[i1]), p_opt[0], p_opt[1])
                
        figure(1)
        subplot(1,2,thr)
        plot_cxctime(t1[ok2] + .5*durs[ok2], cooling_rates, c + '*', 
                     label=temp, mew=0, alpha=.1)
        plot_cxctime(t1[ok2] + .5*durs[ok2], cooling_rates, c + '*', 
                     label=temp, mew=0, alpha=.1)
        title('MUPS-' + str(thr) + ' Cooling Rates During Dwells at ' + 
              str(pitch_bin_min) + ' - ' + str(pitch_bin_max) + ' Pitch')
        ylabel('Uncorrected Cooling Rate [deg F/hr] \n (Filtered for Dwells > ' 
               + str(min_dur) + ' min)')
        #ylim([-100, 20])
        legend(loc='best')

        figure(2)
        subplot(1,2,thr)
        plot(x.vals[i1], cooling_rates, c + '*', label=temp, mew=0)
        plot(xlim(), linfit(array(xlim()), p_opt[0], p_opt[1]), c + ':', alpha=.1)
        plot(xlim(), linfit(array(xlim()), p_opt[0], p_opt[1]), c + ':', alpha=.1)
        title('MUPS-' + str(thr) + 
              ' Cooling Rates During Eclipses vs Starting Temp')
        ylabel('Uncorrected Cooling Rate [deg F/hr]')
        xlabel('Dwell Starting Temp [deg F] \n (Filtered for Dwells > ' 
               + str(min_dur) + ' min & btwn ' + str(pitch_bin_min) + 
               ' - ' + str(pitch_bin_max) + ' Pitch)')
        #ylim([-100, 20])
        legend(loc='best')
        
        figure(3)
	subplot(1,2,thr)
	plot_cxctime(t1[ok2] + .5*durs[ok2], corr_rates, c + '*', label=temp, 
	             mew=0, alpha=.1)
	plot_cxctime(t1[ok2] + .5*durs[ok2], corr_rates, c + '*', label=temp, 
	             mew=0, alpha=.1)
	title('MUPS-' + str(thr) + ' Cooling Rates During Dwells at ' + 
	      str(pitch_bin_min) + ' - ' + str(pitch_bin_max) + 
	      ' Pitch \n Corrected for Starting Temps')
	ylabel('Cooling Rate (Corrected for Starting Temp) [deg F/hr] \n (Filtered for Dwells > ' 
	       + str(min_dur) + ' min)')
	#ylim([-100, 20])
        legend(loc='best')
        
for fig in range(1, 4):
    figure(fig)
    same_limits((121,122))
#    subplot(121)
#    axis1 = axis()
#    subplot(122)
#    axis(axis1)     

    
    