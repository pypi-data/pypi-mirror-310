# 1.0.0

import struct
import time
from socket import socket, AF_INET, SOCK_STREAM
import numpy as np
from scipy.spatial.transform import Rotation
from threading import Thread

class myUniversalRobot:
    class Pos:
        x = 0
        y = 1
        z = 2
        rx = 3
        ry = 4
        rz = 5

    class DH_param:
        d1 = 0.1625
        d2 = d3 = 0
        d4 = 0.1333
        d5 = 0.0997
        d6 = 0.0996
        a1 = a4 = a5 = a6 = 0
        a2 = -0.425
        a3 = -0.3922
        d = np.array([d1, d2, d3, d4, d5, d6])


    class package_type:
        ROBOT_MODE_DATA = 0
        JOINT_DATA = 1
        TOOL_DATA = 2
        MASTERBOARD_DATA = 3
        CARTESIAN_INFO = 4
        KINEMATICS_INFO = 5
        CONFIGURATION_DATA = 6
        FORCE_MODE_DATA = 7
        ADDITIONAL_INFO = 8
        NEEDED_FOR_CALIB_DATA = 9
        TOOL_COMM_INFO = 11
        TOOL_MODE_INFO = 12

    class message_type:
        ROBOT_STATE = 16
        ROBOT_MESSAGE = 20

    def __init__(self, ip):
        port = 30001
        self.s = socket(AF_INET, SOCK_STREAM)
        self.s.settimeout(2)
        self.connected = False
        try:
            self.s.connect((ip, port))
            self.s.send(self._toByte('ConnectCheck\n'))
            self.connected = True
        except OSError:
            print('接続失敗')
        self.joint_angle = np.array([0.0]*6)
        self.joint_velocity = np.array([0.0]*6)
        self.tcp_pos = np.array([0.0]*6)
        self._move_check = False
        th = Thread(target=self._back_loop, daemon=True)
        th.start()
        while np.linalg.norm(self.tcp_pos) < 1:
            pass

    def wait_stop(self):
        time.sleep(0.3)
        while self.isMoving():
            pass

    def exit(self):
        self.stop()
        self.s.close()

    def _back_loop(self):
        while True:
            data = self.s.recv(4096)
            i = 0
            all_data_length = (struct.unpack('!i', data[0:4]))[0]
            now_msg = data[4]
            if now_msg == self.message_type.ROBOT_STATE:
                # if packet type is Robot State, loop until reached end of packet
                while i + 5 < all_data_length:
                    pkg_len = (struct.unpack('!i', data[5 + i:9 + i]))[0]
                    now_pkg_data = data[5 + i:5 + i + pkg_len]
                    pkg_type = now_pkg_data[4]

                    if pkg_type == self.package_type.JOINT_DATA:
                        for j in range(6):
                            # cycle through joints and extract only current joint angle (double precision)  then print to screen
                            # bytes 10 to 18 contain the j0 angle, each joint's data is 41 bytes long (so we skip j*41 each time)
                            self.joint_angle[j] = np.rad2deg((struct.unpack('!d', now_pkg_data[5 + (j * 41):13 + (j * 41)]))[0])
                            self.joint_velocity[j] = np.rad2deg((struct.unpack('!d', data[26 + i + (j * 41):34 + i + (j * 41)]))[0])
                        if np.linalg.norm(self.joint_velocity) > 0.01:
                            self._move_check = True
                        else:
                            self._move_check = False
                    elif pkg_type == self.package_type.CARTESIAN_INFO:
                        # if message type is cartesian data, extract doubles for 6DOF pos of TCP and print to screen
                        self.tcp_pos[self.Pos.x] = (struct.unpack('!d', data[10 + i:18 + i]))[0]*1000
                        self.tcp_pos[self.Pos.y] = (struct.unpack('!d', data[18 + i:26 + i]))[0]*1000
                        self.tcp_pos[self.Pos.z] = (struct.unpack('!d', data[26 + i:34 + i]))[0]*1000
                        self.tcp_pos[self.Pos.rx] = (struct.unpack('!d', data[34 + i:42 + i]))[0]
                        self.tcp_pos[self.Pos.ry] = (struct.unpack('!d', data[42 + i:50 + i]))[0]
                        self.tcp_pos[self.Pos.rz] = (struct.unpack('!d', data[50 + i:58 + i]))[0]
                    i += pkg_len

    def moveJ(self, _angles, _acc=1.0, _vel=1.0, _time=None, unit_is_DEG=True):
        if not self.connected:
            return
        if unit_is_DEG:
            _angles = np.deg2rad(_angles)
        if _time == None:
            command = 'movej({angles}, a={acc}, v={vel})'.format(angles=_angles.tolist(), acc=_acc, vel=_vel)
            self.s.send(self._toByte(command))
        elif _time > 0:
            command = 'movej({angles}, t={time})'.format(angles=_angles.tolist(), time=_time)
            self.s.send(self._toByte(command))
            time.sleep(_time)

    def moveL(self, _position, _acc=1000, _vel=150, _time=None, unit_is_DEG=False):
        if not self.connected:
            return
        _goal_position = np.zeros(6)
        _goal_position[self.Pos.x:self.Pos.z+1] = _position[self.Pos.x:self.Pos.z+1]/1000
        if unit_is_DEG:
            _goal_position[self.Pos.rx:self.Pos.rz+1] = np.deg2rad(_position[self.Pos.rx:self.Pos.rz+1])
        else:
            _goal_position[self.Pos.rx:self.Pos.rz+1] = _position[self.Pos.rx:self.Pos.rz+1]
        if _time == None:
            command = 'movel(p{position}, a={acc}, v={vel})'.format(position=_goal_position.tolist(), acc=_acc/1000, vel=_vel/1000)
            self.s.send(self._toByte(command))
        elif _time > 0:
            command = 'movel(p{position}, t={time})'.format(position=_goal_position.tolist(), time=_time)
            self.s.send(self._toByte(command))
            time.sleep(_time)

    def speedL(self, _speed, _acc=1000):
        if not self.connected:
            return
        _speed[self.Pos.x:self.Pos.z+1] = _speed[self.Pos.x:self.Pos.z+1]/1000
        command = 'speedl({speed}, a={acc}, t=10.0)'.format(speed=_speed.tolist(), acc=_acc/1000)
        self.s.send(self._toByte(command))

    def isMoving(self):
        return self._move_check

    def stop(self):
        command = 'stopj(2)'
        self.s.send(self._toByte(command))

    def get_rotvec(self, relative_posture):
        """ 相対的な回転ベクトル(R^3)を絶対回転ベクトルに変換
        Args:
            relative_rotation ():
        Returns:

        """
        now_posture = self.tcp_pos.copy()[self.Pos.rx:]
        rot_now = Rotation.from_rotvec(now_posture)
        rot_relative = Rotation.from_rotvec(relative_posture)
        ret = rot_relative * rot_now
        return ret.as_rotvec()


    def _toByte(self, str):
        message = str + '\n'
        return bytes(message.encode())

