from time import sleep, time

#Beats per Minute
class BPM(object):
    def __init__(self, value):
        self._value = value
        self._bps = float(self._value) / 60
        
    def seconds_per_pulse(self, resolution):
        pps = self._bps * resolution.ppqn
        return 1 / pps

#Pulses Per Quarter Note
class PPQN(object):
    def __init__(self, value):
        self._value = value
    
    @property
    def ppqn(self):
        return self._value
    
#Pulse, treat instances are frozen, do not CHANGE fields, only time keeper should
class Pulse(object):
    def __init__(self, time_keeper, initial = 0):
        self.time_keeper = time_keeper
        self._counter = initial
    
    def increment(self):
        self._counter = self._counter + 1
        
    def counter(self):
        return self._counter
        
    def measure(self):
        ppqn = self.time_keeper.resolution.ppqn
        ppm = ppqn * 4
        return self._counter / ppm
        
    def __str__(self):
        ppqn = self.time_keeper.resolution.ppqn
        ppm = ppqn * 4
        measure = float(self._counter) / ppm
        return "Pulse(%s)" % (measure,)

# PulseTimer - keeps time based on BPM and PPQN, BPM can change
# It allows a generator to be registered to be fired at each pulse
# The pulse sent to the generator is assumed to change, if it is needed
# not to, then make a copy
class PulseTimer(object):
    def __init__(self, tempo=BPM(120), resolution=PPQN(24)):
        self.tempo = tempo
        self._res = resolution
    
    @property
    def resolution(self):
        return self._res
    
    def start(self, consumer):
        self._running = True
        pulse = Pulse(self)

        while self._running:
            start_s = time()
            if not consumer(pulse):
                self._running = False
                break
            end_s = time()
            elapsed_s = end_s - start_s
            wait_s = self.tempo.seconds_per_pulse(self._res)
            if elapsed_s > wait_s:
                #could move this to pulse to warn, leave here until then
                print("WARNING: Falling behind by: %s s" % (elapsed_s - wait_s))
            else:
                self._sleep(wait_s - elapsed_s)
            pulse.increment()
    
    def _spp(self):
        bps = float(self.bpm) / 60
        pps = bps * self._ppqn
        return 1 / pps
    
    def _sleep(self, seconds):
        sleep(seconds)