#!/usr/bin/env python3
                
import pantone




p.add_light_sensor(


def main(argv=None):

    if argv is None:
        argv = sys.argv[1:]

    # Parse command line
    try:
        control_file = argv[0]
    except IndexError:
        err = "Incorrect arguments. Usage:\n\n{}\n\n".format(__usage__)
        raise ValueError(err)

    # load in json file
    data = json.loads(open(control_file,'r').read())

    # Parse configuration file.  Keys should be keyword arguments to 
    # PantoneClock.__init__.  The key "ambient" is a special key that should
    # point to a dictionary of keywords to be passed to 
    # AmbientLightSensor.__init__.
    ambient_kwargs = {}
    pantone_kwargs = {}
    for k in data.keys():
        if k == "ambient":
            ambient_kwargs = copy.deepcopy(data[k])
        else:
            pantone_kwargs[k] = copy.deepcopy(data[k])

    # Create clock 
    clock = PantoneClock(**pantone_kwargs) 
    
    # Potentially create an ambient light sensor
    if len(ambient_kwargs) > 0:
        light_sensor = AmbientLightSensor(**ambient_kwargs)
        clock.add_ambient_light_sensor(light_sensor)
   
    # Start the clock 
    clock.start() 
  

if __name__ == "__main__":
    main()

