
from kadi import events

from utilities import find_closest, find_last_before, find_first_after, same_limits

close('all')

tstart = '2013:001'
pitch_bin_min = 156
pitch_bin_max = 166

all_dwells_t1 = array(events.dwells.table['tstart'])
all_dwells_t2 = array(events.dwells.table['tstop'])
all_durs = array(events.dwells.table['dur'])
all_dwells_tmid = all_dwells_t1 + .5 * all_durs

x = fetch.Msid('PITCH', tstart, stat='5min')
all_pitch_tmid_i = find_closest(all_dwells_tmid, x.times)
all_pitch_tmid = x.vals[all_pitch_tmid_i]

in_bin = (all_pitch_tmid > pitch_bin_min) & (all_pitch_tmid < pitch_bin_max)
t1 = all_dwells_t1[in_bin]
t2 = all_dwells_t2[in_bin]
pitch = all_pitch_tmid[in_bin]
durs = all_durs[in_bin]

#marker_i = 0

for thr in range(1,3):

    for ab, c in zip(range(1,3), ('b','r')):

        temp = 'PM' + str(thr) + 'THV' + str(ab) + 'T'
        x = fetch.Msid(temp, '2000:001')

        i1 = find_first_after(t1, x.times)
        i2 = find_last_before(t2, x.times)
        
        cooling_rates = (x.vals[i2] - x.vals[i1]) * 3600 / durs
                
        figure(1)
        subplot(1,2,thr)
        zipvals = zip(i1, i2)
        for i1i, i2i in zipvals:
            plot_cxctime(x.times[i1i:i2i], x.vals[i1i:i2i], c+'.', label=temp)
        title('MUPS-' + str(thr) + ' Valve Temps during Dwells at 156 - 166 Pitch')
        ylabel('deg F')

        figure(2)
        subplot(1,2,thr)
        zipvals = zip(i1, i2)
        for i1i, i2i in zipvals:
            plot(x.times[i1i:i2i] - x.times[i1i], x.vals[i1i:i2i] - x.vals[i1i], c, label=temp)
        title('Change in MUPS-' + str(thr) + 'Temps During Dwells at 156 - 166 Pitch')
        xlabel('Time into Dwell [sec]')
        ylabel('deg F')
          
        figure(3)
        subplot(1,2,thr)
        plot_cxctime(t1 + .5*durs, cooling_rates, c + '*', label=temp, mew=0)
        title('MUPS-' + str(thr) + ' Cooling Rates During Dwells at 156 - 166 Pitch')
        ylabel('Cooling Rate [deg F/hr]')
        #ylim([-100, 20])
        legend(loc='best')

        #figure(4)
        #subplot(1,2,thr)
        #plot(x.vals[eclipses_i1], cooling_rates, c + '*', label=temp, mew=0)
        #title('MUPS-' + str(thr) + ' Cooling Rates During Eclipses vs Starting Temp')
        #ylabel('Cooling Rate [deg F/hr]')
        #xlabel('Eclipse Starting Temp [deg F]')
        #ylim([-100, 20])
        #legend(loc='best')
        
        #if thr == 1 or thr == 2:
        #    marker = ['co','cs', 'mo', 'ms']
        #
        #    figure(5)
        #    plot_cxctime(eclipses_t1, cooling_rates, marker[marker_i], label=temp, mew=0)
        #    title('MUPS-1 and MUPS-2 Cooling Rates During Eclipses')
        #    ylabel('Cooling Rate [deg F/hr]')
        #    ylim([-100, 20])
        #    legend(loc='lower left')
        
        #    figure(6)
        #    plot(cooling_rates, marker[marker_i], label=temp, mew=0)
        #    xlabel('Eclipse Number Since 2000:001')
        #    title('MUPS-1 and MUPS-2 Cooling Rates During Eclipses')
        #    ylabel('Cooling Rate [deg F/hr]')
        #    ylim([-100, 20])
        #    legend(loc='lower left')

        #    marker_i = marker_i + 1

for fig in range(1, 4):
    figure(fig)
    subplot(121)
    axis1 = axis()
    subplot(122)
    axis(axis1)
    if fig < 4:
        tight_layout()      

    
    