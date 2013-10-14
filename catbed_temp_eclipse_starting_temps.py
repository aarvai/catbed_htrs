from kadi import events
from utilities import find_first_after

close('all')

eclipses_t1 = array(events.eclipses.table['tstart'])

x = fetch.Msidset(['PM1THV2T','PM2THV2T'],'2000:000')

if all(x['PM1THV2T'].times == x['PM2THV2T'].times):
    eclipses_i1 = find_first_after(eclipses_t1, x['PM1THV2T'].times)
    dt = x['PM1THV2T'].vals[eclipses_i1] - x['PM2THV2T'].vals[eclipses_i1]
    
    figure()
    subplot(2,1,1)
    plot_cxctime(x['PM1THV2T'].times[eclipses_i1], x['PM1THV2T'].vals[eclipses_i1], 'co', label='PM1THV2T')
    plot_cxctime(x['PM2THV2T'].times[eclipses_i1], x['PM2THV2T'].vals[eclipses_i1], 'mo', label='PM2THV2T')
    title('MUPS-1 and MUPS-2 Starting Eclipse Temps')
    ylabel('deg F')
    legend(loc='lower left')
    
    subplot(2,1,2)
    plot_cxctime(x['PM1THV2T'].times[eclipses_i1], dt, 'b.')
    title('MUPS-1 minus MUPS-2 Starting Eclipse Temps')
    ylabel('deg F')
    ylim([-20,20])
    plot(xlim(),[0,0],'g:')
