import sys
sys.path.append("../../")
from ros_atlas.pidTracker.SingletonDrone import _Drone

if __name__ == "__main__":
    a = _Drone()
    print(a)
    print(id(a))
    print(id(a.uav))
    while True:
        pass