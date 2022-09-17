### Use of Artificial Neural Network for anomaly detection over a timeseries database

---

Data Acquisition: using PX4 Firmware integrated to Gazebo + QGroundControl GUI:

![image](https://user-images.githubusercontent.com/60454486/190869658-0f86a52b-d46d-407b-a1c0-7789630531a1.png)

---

# Dependencies:

1. Ros Installation

## Install Ubuntu

- `sudo sh -c 'echo "deb http://packages.ros.org/ros/ubuntu $(lsb_release -sc) main" > /etc/apt/sources.list.d/ros-latest.list'`
- `sudo apt-key adv --keyserver 'hkp://keyserver.ubuntu.com:80' --recv-key C1CF6E31E6BADE8868B172B4F42ED6FBAB17C654`
- `sudo apt update`
- `sudo apt install ros-noetic-desktop-full`
- `echo "source /opt/ros/noetic/setup.bash" >> ~/.bashrc`
- `source ~/.bashrc`
- `sudo apt install python3-rosdep python3-rosinstall python3-rosinstall-generator python3-wstool build-essential`
- `sudo rosdep init`
- `rosdep update`
