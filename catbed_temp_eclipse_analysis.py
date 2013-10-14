
from kadi import events

from utilities import find_closest, find_last_before, find_first_after, same_limits

close('all')

eclipses_t1 = array(events.eclipses.table['tstart'])
eclipses_t2 = array(events.eclipses.table['tstop'])
durs = eclipses_t2 - eclipses_t1

marker_i = 0

for thr in range(1,5):

    for ab, c in zip(range(1,3), ('b','r')):

        temp = 'PM' + str(thr) + 'THV' + str(ab) + 'T'
        x = fetch.Msid(temp, '2000:001')

        x.select_intervals(events.eclipses)

        eclipses_i1 = find_first_after(eclipses_t1, x.times)
        eclipses_i2 = find_last_before(eclipses_t2, x.times)
        eclipses_time0 = x.times[eclipses_i1]
        eclipses_temp0 = x.vals[eclipses_i1]

        cooling_rates = (x.vals[eclipses_i2] - x.vals[eclipses_i1]) * 3600 / durs
        
        figure(1)
        subplot(2,2,thr)
        x.plot(c + '.', label=temp)
        title('MUPS-' + str(thr) + ' Valve Temps During Eclipses')
        ylabel('deg F')
        legend(loc='best')

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
        plot_cxctime(eclipses_t1, cooling_rates, c + '*', label=temp, mew=0)
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
            plot_cxctime(eclipses_t1, cooling_rates, marker[marker_i], label=temp, mew=0)
            title('MUPS-1 and MUPS-2 Cooling Rates During Eclipses')
            ylabel('Cooling Rate [deg F/hr]')
            ylim([-100, 20])
            legend(loc='lower left')

            figure(6)
            plot(cooling_rates, marker[marker_i], label=temp, mew=0)
            xlabel('Eclipse Number Since 2000:001')
            title('MUPS-1 and MUPS-2 Cooling Rates During Eclipses')
            ylabel('Cooling Rate [deg F/hr]')
            ylim([-100, 20])
            legend(loc='lower left')

            marker_i = marker_i + 1

for fig in range(1, 5):
    figure(fig)
    subplot(221)
    axis1 = axis()
    subplot(222)
    axis(axis1)
    same_limits((223, 224))
    if fig < 4:
        tight_layout()      

    
    