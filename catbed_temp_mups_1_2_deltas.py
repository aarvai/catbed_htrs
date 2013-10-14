from utilities import heat_map

close('all')

bad_all = ['2000:048:00:00:00 2000:052:00:00:00',
           '2000:228:00:00:00 2000:229:00:00:00',
           '2000:302:00:00:00 2000:303:00:00:00',
           '2001:111:00:00:00 2001:114:00:00:00',
           '2004:200:00:00:00 2004:201:00:00:00',
           '2004:208:00:00:00 2004:209:00:00:00',
           '2004:213:00:00:00 2004:214:00:00:00',
           '2008:225:00:00:00 2008:228:00:00:00',
           '2008:292:00:00:00 2008:295:00:00:00',
           '2010:150:00:00:00 2010:152:00:00:00',
           '2011:187:00:00:00 2011:193:00:00:00',
           '2011:297:00:00:00 2011:304:00:00:00',
           '2012:150:00:00:00 2012:153:00:00:00']

x = fetch.Msidset(['PM1THV2T','PM2THV2T'],'2000:000', stat='5min')
x.filter_bad_times(table=bad_all)

if all(x['PM1THV2T'].times == x['PM2THV2T'].times):
    dt = x['PM1THV2T'].vals - x['PM2THV2T'].vals
    times = x['PM1THV2T'].times
        
    figure()
    subplot(3,1,1)
    plot_cxctime(times, x['PM1THV2T'].vals, 'c.', label='PM1THV2T', mew=0)
    plot_cxctime(times, x['PM2THV2T'].vals, 'm.', label='PM2THV2T', mew=0)
    title('MUPS-1 and MUPS-2 Valve Temps')
    ylabel('deg F')
    legend(loc='lower left')

    subplot(3,1,2)
    heat_map(DateTime(times).secs, dt, colorbar=False, y_lim=[-30,30])
    title('MUPS-1 minus MUPS-2 Valve Temps')
    ylabel('deg F')
    
    subplot(3,1,3)
    plot_cxctime(times, dt, 'b.')
    title('MUPS-1 minus MUPS-2 Valve Temps')
    ylabel('deg F')
    ylim([-30,30])
    plot(xlim(),[0,0],'g:')
 
    tight_layout()
