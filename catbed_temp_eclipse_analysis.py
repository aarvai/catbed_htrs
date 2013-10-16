from kadi import events
from Ska.engarchive import fetch_eng as fetch
from Ska.Matplotlib import plot_cxctime

from utilities import (find_closest, find_last_before, find_first_after, 
                       same_limits, remove_therm_dropouts) 

rcParams_orig = rcParams.copy()
rcParams['lines.markersize'] = 3
rcParams['axes.grid'] = True

tstart = '2000:001'

close('all')

eclipses_t1 = array(events.eclipses.table['tstart'])
eclipses_t2 = array(events.eclipses.table['tstop'])
durs = eclipses_t2 - eclipses_t1
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

marker_i = 0

for thr in range(1,5):

    for ab, c in zip(range(1,3), ('b','r')):

        temp = 'PM' + str(thr) + 'THV' + str(ab) + 'T'
        
        x = tlm[temp]

        eclipses_i1 = find_first_after(eclipses_t1, x.times)
        eclipses_i2 = find_last_before(eclipses_t2, x.times)
        
        # Check for eclipses with zero valid data due to dropouts
        ok = eclipses_i2 > eclipses_i1
        eclipses_i1 = eclipses_i1[ok]
        eclipses_i2 = eclipses_i2[ok] 
        
        eclipses_time0 = x.times[eclipses_i1]
        eclipses_temp0 = x.vals[eclipses_i1]

        cooling_rates = (x.vals[eclipses_i2] - x.vals[eclipses_i1]) * (3600 / 
                        durs[ok])
        
        #figure(1)
        #subplot(2,2,thr)
        #zipvals = zip(eclipses_i1, eclipses_i2)
        #for i1, i2 in zipvals:
        #    plot_cxctime(x.times[i1:i2], x.vals[i1:i2], c + '.')       
        #title('MUPS-' + str(thr) + ' Valve Temps During Eclipses')
        #ylabel('deg F')
        #legend(loc='best')

        figure(2)
        subplot(2,2,thr)
        zipvals = zip(eclipses_time0, eclipses_temp0, eclipses_i1, eclipses_i2)
        for time0, temp0, i1, i2 in zipvals:
            plot(x.times[i1:i2] - time0, x.vals[i1:i2] - temp0, c)
        title('Change in MUPS-' + str(thr) + 'Temps During Eclipses')
        xlabel('Time into Eclipse [sec]')
        ylabel('deg F')

        figure(3)
        subplot(2,2,thr)
        plot_cxctime(eclipses_t1[ok], cooling_rates, c + '*', label=temp, mew=0)
        title('MUPS-' + str(thr) + ' Cooling Rates During Eclipses')
        ylabel('Cooling Rate [deg F/hr]')
        ylim([-100, 20])
        legend(loc='best')

        figure(4)
        subplot(2,2,thr)
        plot(x.vals[eclipses_i1], cooling_rates, c + '*', label=temp, mew=0)
        title('MUPS-' + str(thr) + ' Cooling Rates During Eclipses vs Starting Temp')
        ylabel('Cooling Rate [deg F/hr]')
        xlabel('Eclipse Starting Temp [deg F]')
        ylim([-100, 20])
        legend(loc='best')
        
        if thr == 1 or thr == 2:
            marker = ['co','cs', 'mo', 'ms']

            figure(5)

            # Correct cooling rates to a common starting temperature of
            # 130 F.  The correction is based on a rough eyeball fitting of
            # Figure 4.  Exact value could be improved and might depend on thr.
            starting_temps = x.vals[eclipses_i1]
            cooling_rates_corr = cooling_rates - (130 - starting_temps) * 10. / 30.

            plot_cxctime(eclipses_t1[ok], cooling_rates_corr, marker[marker_i], label=temp, mew=0)
            title('MUPS-1 and MUPS-2 Cooling Rates During Eclipses')
            ylabel('Cooling Rate [deg F/hr] \n (Corrected for Eclipse Starting Temp)')
            ylim([-100, 20])
            grid()
            legend(loc='lower left')

            figure(6)
            plot(cooling_rates_corr, marker[marker_i], label=temp, mew=0)
            xlabel('Eclipse Number Since 2000:001')
            title('MUPS-1 and MUPS-2 Cooling Rates During Eclipses')
            ylabel('Cooling Rate [deg F/hr] \n (Corrected for Eclipse Starting Temp)')
            ylim([-100, 20])
            legend(loc='lower left')

            marker_i = marker_i + 1

for fig in range(2, 5):
    figure(fig)
    subplot(221)
    axis1 = axis()
    subplot(222)
    axis(axis1)
    same_limits((223, 224))
    if fig < 4:
        tight_layout()      

show()

rcParams.update(rcParams_orig)
