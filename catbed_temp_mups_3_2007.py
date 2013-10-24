#t_start = '2000:001'
#t_stop = None
t_start = '2006:348'
t_stop = '2006:354'

t_event = '2006:351:04:38:30.000'

old_setpoints = [[59.55,96.9],[58.32, 97.77]]

close('all')

for ab in range(1,3):
    subplot(2,1,ab)
    temp = 'PM3THV' + str(ab) + 'T'
    x = fetch.Msid(temp, t_start,t_event)
    x.plot('b', label='Pre-event')
    x = fetch.Msid(temp, t_event, t_stop)
    x.plot('r', label='Post-event')
    title(temp)
    ylabel('deg F')
    ylim([45,115])
    old_on = array([old_setpoints[ab-1][0], old_setpoints[ab-1][0]])
    old_off = array([old_setpoints[ab-1][1], old_setpoints[ab-1][1]])
    plot(xlim(), old_on, 'b:', label='Old Set Points')
    plot(xlim(), old_off, 'b:')
    legend()
    
subplot(212)
plot(xlim(), array([58.32,58.32]), 'b:')
plot(xlim(), array([97.77, 97.77]), 'b:')