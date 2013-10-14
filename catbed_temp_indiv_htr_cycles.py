
x = fetch.Msidset(['PM3THV1T','PM3THV2T','PM4THV1T','PM4THV2T'], '2013:002:05:00:00.000','2013:002:07:00:00.000')

close('all')

subplot(2,1,1)
x['PM3THV1T'].plot('b', label='PM3THV1T')
x['PM3THV2T'].plot('r', label='PM3THV2T')
title('Sample MUPS-3 Temperatures during Heater Cycles')
legend()

subplot(2,1,2)
x['PM4THV1T'].plot('b', label='PM4THV1T')
x['PM4THV2T'].plot('r', label='PM4THV2T')
title('Sample MUPS-4 Temperatures during Heater Cycles')
legend()