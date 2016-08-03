from pygame import midi


def main():
    print 'Number of devices: %d' % midi.get_count()
    print 'Default input id: %d' % midi.get_default_input_id()
    print 'Default output id: %d' % midi.get_default_output_id()
    for index in xrange(midi.get_count()):
        device = midi.get_device_info(index)
        if 1 == device[2]:
            input_dev = 'in'
        else:
            input_dev = '-'
        if 1 == device[3]:
            output_dev = 'out'
        else:
            output_dev = '-'
            
        print 'Device id: %d - %s (%r,%r)' % (index, device[1], input_dev, output_dev)
if __name__ == '__main__':
    midi.init()
    main()
    midi.quit()