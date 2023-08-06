# TMotorCANControl
A Python API for controlling the AK-series Tmotor Actuators from CubeMars over the CAN bus.
The project is geared towards the control of the AK80-9 actuator using a raspberry pi CAN hat, but
could eaisly be adapted for use with a different CAN interface. The API files are in the src/TMotorCANControl
folder in this repository. The main interface is in the file TMotorManager.py, and sample scripts
can be found in the test folder. The CAN_Manager file contains a low-level CAN interface for 
interacting with the motor, which is used by the TMotorManager class to control the motor 
in a more user-friendly way.

## Calibrating and Configuring the Motor
Before you can use the motor, you may need to run an encoder callibration routine and you may
desire to change the motor's CAN ID from 1 (the default) to a number of your choosing. This can be
done by connecting to the UART port on the motor and sending a few commands. CubeMars sells a custom
device called [R-Link](https://store.tmotor.com/goods.php?id=1185) that can be used with their GUI 
(downloadable from the same page) to connect to the motor over serial, or you can connect using an 
FTDI usb to serial chip, or something similar. If you use your own serial connection, the baud rate is 921600.
The advantage of the R-Link device is that it can be used to send test CAN messages to verify that 
the motor is working, but the same thing can be achieved with the TControl library if it is eaiser 
to connect to the UART port via another method.

Whichever method you choose to connect to the serial port, you can use the TMotor company's software
to connect to the motor. It can be downloaded from the [R-Link page](https://store.tmotor.com/goods.php?id=1185)
To use the software, you will need to switch the language to English in the bottom left. You can 
then find your serial port in the list on the middle-top right of the screen, and press the connect button 
next to that list. Then enter DEBUG mode to bring up the serial interface by pressing the DEBUG button near the
middle-bottom right. Then, turn the motor on with around 24V, and you should see that the motor 
has sent messages offering a menu of configuration choices. It's okay if a list of possible error 
codes prints out one time, but if they keep printing turn the motor off and try to identify the problem. 
From the menu of options, send the code to calibrate the encoders, which will start a short routine 
in which the motor turns slowly and records encoder positions. When this routine finishes, you can 
change things such as the CAN ID in the settings menu by sending the codes that it prompts you. 
For a more detailed guide on the setup and configuration of the motor, see the 
[AK-series motor manual](https://store.cubemars.com/images/file/20211201/1638329381542610.pdf)
from the TMotor site.

## Setting up the PiCAN 2 Hat and TMotor
We used the [PiCAN 2 CAN Bus Hat](https://copperhilltech.com/pican-2-can-bus-interface-for-raspberry-pi/) 
from CopperHill technologies to interface between the raspberry pi and the motor's CAN network.
Before using the hat, you will need to activate the termination resistor by soldering a 2 pin 
header to JP3 on the hat and connecting the leads. Of course, you will also need to connect
the hat's CAN high and CAN low screw terminals to the motor's CAN port. You also need to connect
the hat's ground screw terminal to a common ground with the motor--connecting to the ground pin
on the UART port on the motor will work for this purpose.

With the elctronics set up, you can follow the [instructions](https://copperhilltech.com/blog/pican2-pican3-and-picanm-driver-installation-for-raspberry-pi/)
given on the CopperHill website to set up the software on the pi to drive the PiCAN 2 Hat. 
Once this is done, you can verify that the PiCAN hat is functioning properly by
starting up the network in loopback mode as recommended in the
[troubleshooting guide](https://copperhilltech.com/blog/pican2-can-bus-board-for-raspberry-pi-functionality-test/)
on the CopperHill website. 

If the loopback mode test worked successfully, then the PiCAN hat is working properly, and you
can begin to test the motor. To verify that the CAN connection to the motor is working properly,
run the "test_motor_connection.py" script in the test folder, with the "ID" and "type" variables
set to the proper CAN ID and motor type (default 1 and AK80-9) for your setup. If all is working
correctly, you should see a message saying the motor is successfully connected. If 
you see an error related to the CAN bus, then check the connection and verify the CAN hat is working.
If you see an error that seems to be related to the TControl API implementation, then let us know
so we can help you troubleshoot.

With the motor configured and connected, you can now start programming!

## API usage
For some code examples, see the src/TMotorCANControl/test folder in this repository.
These examples make use of the soft_real_timeloop class from the [NeuroLocoMiddleware library]() 
for the control loops, in order to ensure safe exiting of the loop when the program is terminated.

The intended use case would be to declare a TMotorManager object in a with block, and then
write your controller within that block, in order to ensure the motor is powered on when in use
and powered off afterwards. The TMotorManager class is in the TMotorManager module in the TMotorCANControl package.
As such, it can be imported like this:

```python
from TMotorCANControl.TMotorManager import TMotorManager
```

To instantiate a motor object, you need to specify the motor's type as a string (eg, "AK80-9"), as well
as it's CAN ID and an optional log file and set of logging parameters. Note, with multiple motors 
each log file must have a different name.  The logger will always log a time stamp for each line 
in the log, starting from the instantiation of the TMotorManager object. By default, it will also log the 
output position, output velocity, output acceleration, current, and output torque. To specify
a different log format, you can pass in a list of parameters. The full list is shown below:

```python
logvars = [
    "output_angle", 
    "output_velocity", 
    "output_acceleration",
    "current",
    "output_torque",
    "motor_angle", 
    "motor_velocity", 
    "motor_acceleration", 
    "motor_torque"
]
```

And motor control could be entered as such for an AK80-9 motor with CAN ID 3:
```python
with TMotorManager(motor_type='AK80-9', motor_ID=3, CSV_file="log.csv", log_vars=logvars) as dev:
```

The motor can be controlled in current/torque or impedance mode. Additionally, both a
current/torque and a position could be specified, in what we call "Full State Feedback" mode.
Before using any of these control modes, the mode must be entered by calling the appropriate 
function, as follows:

- set_impedance_gains_real_unit(K=stiffness,B=damping): Used to enter impedance control only mode.
- set_current_gains(): Used to enter current control only mode, for current or torque control.
- set_impedance_gains_real_unit_full_state_feedback(K=stiffness,B=damping): Used to enter full state feedback mode.

Once entered, the motor can be controlled in any of these modes by setting the TMotorManager's
internal command, and then calling the update() method to send the command. The values of the
internal command can be set with the following methods:

- set_output_angle_radians(pos): Sets the position command to "pos" radians
- set_motor_current_qaxis_amps(current): Sets the current command to "current" amps
- set_output_torque_newton_meters(torque): Sets the current command based on the torque supplied
- set_motor_torque_newton_meters(torque): Sets torque command based on the torque specified, adjusted for the gear ratio to control motor-side torque.
- set_motor_angle_radians(pos): Sets position command based on the position specified, adjusted for the gear ratio to control motor-side position.

Furthermore, the motor state can be accessed with the following methods. The state is updated
every time the update() method is called, which are pretty self explanitory.
- get_current_qaxis_amps()
- get_output_angle_radians()
- get_output_velocity_radians_per_second()
- get_output_acceleration_radians_per_second_squared()
- get_output_torque_newton_meters()
- get_motor_angle_radians()
- get_motor_velocity_radians_per_second()
- get_motor_acceleration_radians_per_second_squared()
- get_motor_torque_newton_meters()

A second interface is also provided, which will use these methods to streamline your Python
code and make it look more like math. In this interface, properties are set to call the
above getters and setters as follows:

- i: current
- θ: output angle
- θd: output velocity
- θdd: output acceleration
- τ: output torque
- ϕ: motor-side angle
- ϕd: motor-side velocity
- ϕdd: motor-side acceleration
- τm: motor-side torque

Another notable function is the zero_position() function, which sends a command to the motor to 
zero it's current angle. This function will shut off control of the motor for about a second
while the motor zeros (sort of like zeroing a scale, it seems to record a few points to get 
a good measurement). As such, after calling the method you should delay for at least a second
if timely communication is important.

The following example would instantiate a TMotorManager for an AK80-9 motor with a CAN ID of 3,
logging into a CSV file named "log.csv", with the full set of log variables specified above. Then
it will zero the motor position and wait long enough for the motor to be done zeroing. Finally,
it will enter impedance control mode with gains of 10Nm/rad and 0.5Nm/(rad/s). It then will set 
the motor position to 3.14 radians until the program is exited.

```python
with TMotorManager(motor_type='AK80-9', motor_ID=3, CSV_file="log.csv", log_vars=logvars) as dev:
    dev.zero_position()
    time.sleep(1.5)
    dev.set_impedance_gains_real_unit(K=10,B=0.5)
    loop = SoftRealtimeLoop(dt = 0.01, report=True, fade=0)

    for t in loop:
        dev.update()
        dev.θ = 3.14
```

For more examples, see the src/TMotorCANControl/test folder. Have fun controlling some TMotors!

## Other Resources
1. [AK-series motor manual](https://store.cubemars.com/images/file/20211201/1638329381542610.pdf)
The documentation for the AK-series TMotors, which includes the CAN protocol and how to use R-Link

2. [PiCAN 2 CAN Bus Hat](https://copperhilltech.com/pican-2-can-bus-interface-for-raspberry-pi/) 
The documentation for the CopperHill Raspberry Pi CAN hat.

3. [RLink Youtube videos](https://www.youtube.com/channel/UCs-rBZ4uKBpOT9vokLZPhog/featured)
Yoyo's youtube channel has some tutorials on how to use the RLink software.

4. [Mini-Cheetah-TMotor-Python-Can](https://github.com/dfki-ric-underactuated-lab/mini-cheetah-tmotor-python-can)
This is another, more low-level library for controlling these motors that functions simillarly to
our CAN_Manager class.

This work is performed under the [Neurobionics Laboratory](https://neurobionics.robotics.umich.edu/) 
under Drs. Elliott Rouse and Gray Thomas.
