from kadi import events

close('all')

msids = ['PLINE02T', 'PLINE03T', 'PLINE08T', 'PLINE09T']

x = fetch.Msidset(msids, '2000:001', stat='5min')

figure(1)
zipvals = zip([1,2,3,4], msids, ['A','A','B','A'])
for thr, msid, ab in zipvals:
    x[msid].remove_intervals(events.safe_suns)
    subplot(2,2,thr)
    plot_cxctime(x[msid].times, x[msid].vals)
    title(msid + ' - near MUPS-' + str(thr) + '-' + ab)
    ylabel('deg F')
same_limits((221, 222, 223, 224))

figure(2)
subplot(2,1,1)
if all(x['PLINE02T'].times == x['PLINE03T'].times):
    plot_cxctime(x['PLINE02T'].times, x['PLINE02T'].vals - x['PLINE03T'].vals)
    title('PLINE02T minus PLINE03T\n(MUPS-1A proxy minus MUPS-2A proxy)')
    ylabel('deg F')
subplot(2,1,2)
if all(x['PLINE08T'].times == x['PLINE09T'].times):
    plot_cxctime(x['PLINE08T'].times, x['PLINE08T'].vals - x['PLINE09T'].vals)
    title('PLINE08T minus PLINE09T\n(MUPS-3B proxy minus MUPS-4A proxy)')
    ylabel('deg F')    
    