from djitellopy import Tello

tello = Tello()

tello.connect()

tello.takeoff()
print(tello.get_temperature(),' °C')
print(tello.get_barometer(),' cm')
tello.rotate_clockwise(90)
tello.move_forward(50)
print(tello.query_distance_tof(),' cm')
tello.land()