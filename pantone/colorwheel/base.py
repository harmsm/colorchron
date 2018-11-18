
class ColorWheel:

    def __init__(self,
                 seconds_per_cycle=86400,
                 zero_position=240,
                 counterclockwise=False):
        """
        seconds_per_cycle: number of seconds that it takes to sweep the entire
                           wheel.  86400 s corresponds to 24 hr
        zero_position:     wheel position, in degrees, corresponding to 0
                           seconds.  
        counterclockwise:  go counterclockwise around the wheel (True or False)
        """

        self._seconds_per_cycle = seconds_per_cycle
        self._zero_position = zero_position
        self._counterclockwise = bool(counterclockwise)

        if self._seconds_per_cycle <= 0:
            err = "seconds_per_cycle must be greater than zero.\n"
            raise ValueError(err)

        # Put starting position in terms of a fraction of the total
        # sweep 
        fx_zero = self._zero_position % 360
        self._fx_zero = fx_zero/360.0

        self._single_channel = 0

        # Configure each channel
        self._three_channel = [0.,0.,0.]
        self._three_channel_offsets = []
        for i in range(3):
            v = self._fx_zero + i*self._seconds_per_cycle/3
            self._three_channel_offsets.append(v)

        # Configure intervals for cycling the clock
        self._intervals = [1/6.,3/6.,4/6.]

    def _calc_channel_values(self,time):
        """
        Calculate the channel values corresponding to this time.
        """

        for i in range(3):

            # Figure out how far around the clock we should be
            channel_time = time + self._three_channel_offsets[i]
            fx_time = (channel_time % self._seconds_per_cycle)/self._seconds_per_cycle

            # Run counter clockwise if requested
            if self._counterclockwise:
                fx_time = 1 - fx_time
       
   
            # Record the single channel value 
            if i == 0:
                self._single_channel = fx_time

            # Ramp between 0 and 1 for the 1st sixth of the clock
            if fx_time < self._intervals[0]:
                self._three_channel[i] = fx_time/self._intervals[0]
                continue

            # Hold at 1 for the 2nd and 3rd sixth of the clock
            if fx_time >= self._intervals[0] and fx_time < self._intervals[1]:
                self._three_channel[i] = 1.0
                continue

            # Ramp between 1 and 0 for the 4th sixth of the clock 
            if fx_time >= self._intervals[1] and fx_time < self._intervals[2]:
                m = 1/(self._intervals[1] - self._intervals[2]) 
                b = 1 - self._intervals[1]*m 
                self._three_channel[i] = fx_time*m + b
                continue
       
            # Hold at 0 for the 5th and 6th sixth of the clock
            self._three_channel[i] = 0.0

    def get_single_channel(self,time):

        self._calc_channel_values(time)
        return self._single_channel

    def get_three_channel(self,time):

        self._calc_channel_values(time)
        return self._three_channel
