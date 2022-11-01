from djitellopy import Tello
import constants
import time

class Missions():

    @staticmethod
    def __init__(self):
        super(Missions, self).__init__()
    
    @classmethod
    def simpleMission(params=Tello()):

        start = time.time()

        missionObject = {
                            "flight_statistics":constants.loadStatistics(),
                            "rot_clk":[270,180], #rotates clockwise [dg]
                            "rot_count_clk":[90], #rotates counter-clockwise [dg]
                            "move_fwd":[55] #moves forward [cm]
                        }

        drone = Tello()
        statistics = missionObject["flight_statistics"]

        #-----------------------#
        # CONNECTION AND TAKEOFF:
        print("\n","-"*50)
        print(f">> Connecting drone on port {Tello.TELLO_IP}")
        drone.connect()
        drone.query_battery()
        print("connected\n")
        
        print("\n>> Starting takeoff...")
        drone.takeoff()
        drone.move_up(70)

        #-----------------------#
        # ROTATION:
        print("\n","-"*50)
        print(f">> Rotating {missionObject['rot_clk'][0]}dg")
        
        drone.query_battery()

        yaw_0,t0 = drone.get_yaw(),time.time()
        drone.rotate_clockwise(missionObject['rot_clk'][0])
        yaw_f,tf = drone.get_yaw(),time.time()
        yawRate = abs((yaw_f-yaw_0)/(tf-t0))
        print("\nReading current values...")
        print(f"* Yaw Rate: {round(yawRate,5)}")
        print(f"* Mean: {list(statistics.loc[statistics['flight_variables']=='yawRate']['avg'].values)[0]}")
        print(f"* Std: {list(statistics.loc[statistics['flight_variables']=='yawRate']['std'].values)[0]}")
        
        #-----------------------#
        # MOVING FORWARD:
        print("\n","-"*50)
        print(f">> Moving {missionObject['move_fwd'][0]}cm forward")
        
        drone.query_battery()
        
        drone.move_forward(missionObject['move_fwd'][0])
        print("\nReading current values...")
        print(f"* Speed-x:{drone.get_speed_x()} ; Speed-y:{drone.get_speed_y()} ; Speed-z:{drone.get_speed_z()}")
        print(f"* Acceleration-x:{drone.get_acceleration_x()} ; Acceleration-y:{drone.get_acceleration_y()} ; Acceleration-z:{drone.get_acceleration_z()}")
        
        #-----------------------#
        # ROTATION:
        print("\n","-"*50)
        print(f">> Rotating {missionObject['rot_clk'][1]}dg")
        
        drone.query_battery()

        yaw_0,t0 = drone.get_yaw(),time.time()
        drone.rotate_clockwise(missionObject['rot_clk'][1])
        yaw_f,tf = drone.get_yaw(),time.time()
        yawRate = abs((yaw_f-yaw_0)/(tf-t0))
        print("\nReading current values...")
        print(f"* Yaw Rate: {round(yawRate,5)}")
        print(f"* Mean: {list(statistics.loc[statistics['flight_variables']=='yawRate']['avg'].values)[0]}")
        print(f"* Std: {list(statistics.loc[statistics['flight_variables']=='yawRate']['std'].values)[0]}")

        #-----------------------#
        # MOVING FORWARD:
        print("\n","-"*50)
        print(f">> Moving {missionObject['move_fwd'][0]}cm forward")
        
        drone.query_battery()
        
        drone.move_forward(missionObject['move_fwd'][0])
        print("\nReading current values...")
        print(f"* Speed-x:{drone.get_speed_x()} ; Speed-y:{drone.get_speed_y()} ; Speed-z:{drone.get_speed_z()}")
        print(f"* Acceleration-x:{drone.get_acceleration_x()} ; Acceleration-y:{drone.get_acceleration_y()} ; Acceleration-z:{drone.get_acceleration_z()}")
    
        #-----------------------#
        # ROTATION:
        print("\n","-"*50)
        print(f">> Rotating {missionObject['rot_count_clk'][0]}dg")
        
        drone.query_battery()

        yaw_0,t0 = drone.get_yaw(),time.time()
        drone.rotate_counter_clockwise(missionObject['rot_count_clk'][0])
        yaw_f,tf = drone.get_yaw(),time.time()
        yawRate = abs((yaw_f-yaw_0)/(tf-t0))
        print("\nReading current values...")
        print(f"* Yaw Rate: {round(yawRate,5)}")
        print(f"* Mean: {list(statistics.loc[statistics['flight_variables']=='yawRate']['avg'].values)[0]}")
        print(f"* Std: {list(statistics.loc[statistics['flight_variables']=='yawRate']['std'].values)[0]}")
        
        #-----------------------#
        # LANDING:
        print("\n","-"*50)
        print(">> Landing...")
        
        drone.query_battery()
        drone.move_down(70)
        drone.land()

        #-----------------------#
        # END MISSION:
        end = time.time()
        print("\n","-"*50)
        print(f'>> Time elapsed is {round((end-start),3)} seconds.','\n\tEnd of execution.\n')


# tello = Tello()

# tello.connect()

# tello.takeoff()
# print(tello.get_temperature(),' °C')
# print(tello.get_barometer(),' cm')
# tello.rotate_clockwise(270)
# tello.move_forward(50)
# print(tello.query_distance_tof(),' cm')
# tello.land()