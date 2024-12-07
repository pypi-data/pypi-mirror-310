# ver 1.0.1

import atexit
import numpy as np
import serial
import time
import struct

class force_torque_sensor:
    class _msg_command:
        get_MaxWrench = 0x2b
        single_read = 0x30
        continue_read_start = 0x32
        continue_read_stop = 0x33

    class idx:
        fx = 0
        fy = 1
        fz = 2
        mx = 3
        my = 4
        mz = 5

    def __init__(self):
        self._read_msg = self._make_msg(self._msg_command.single_read)
        self._get_MaxWrench_msg = self._make_msg(self._msg_command.get_MaxWrench)
        self._continue_read_start_msg = self._make_msg(self._msg_command.continue_read_start)
        self._continue_read_stop_msg = self._make_msg(self._msg_command.continue_read_stop)
        atexit.register(self._exit)

    def init(self, com):
        # baudrate = 460800
        baudrate = 921600
        try:
            self._serial = serial.Serial(com, baudrate=baudrate, parity=serial.PARITY_NONE)
        except serial.serialutil.SerialException:
            return False
        # 定格値の取得：取得できなければ通信エラーと判定
        self.maxWrench = self._read_MaxWrench()
        self._serial.write(bytes(self._continue_read_start_msg))
        self._serial.flush()
        time.sleep(0.1)
        return 1

    def _make_msg(self, request):
        dle = 0x10
        stx = 0x02
        etx = 0x03
        now_message = [dle, stx, dle, etx]
        cmd = [0x04, 0xFF, request, 0x00]
        bcc = self._calc_BCC(cmd)
        now_message[2:2] = cmd
        now_message.append(bcc)
        return now_message

    def _calc_BCC(self, cmd):
        bcc = 0x00
        etx = 0x03
        for i in range(len(cmd)):
            if i == 0:
                bcc = cmd[i]
            else:
                bcc = bcc ^ cmd[i]
        bcc = bcc ^ etx
        return bcc

    def read(self):
        start = b'\x10\x02'  # データの送信開始の記号
        end = b'\x10\x03'    # データの送信終了の記号
        data = b''

        while len(data) == 0:
            raw_data = self._serial.read_all()
            data = raw_data.split(start)
            data = [now_data.split(end)[0] for now_data in data if len(now_data)==23]
        wrench = [struct.unpack('6h', now_data[4:-4]) for now_data in data]
        wrench = np.average(np.array(wrench), axis=0)
        wrench = np.array(wrench) * self.maxWrench / 10000
        return wrench

    def _read_MaxWrench(self):
        start = b'\x10\x02'  # データの送信開始の記号
        end = b'\x10\x03'    # データの送信終了の記号

        while True:
            self._serial.write(bytes(self._get_MaxWrench_msg))
            time.sleep(0.01)
            data = self._serial.read_all()
            data = data.split(start)[1:]
            data = [now_data.split(end)[0] for now_data in data if now_data[2]==self._msg_command.get_MaxWrench]
            if len(data)==0:
                self._serial.write(bytes(self._continue_read_stop_msg))
            else:
                break
        MaxWrench = struct.unpack('6f', data[0][4:])
        return np.array(MaxWrench)

    def _exit(self):
        self._serial.write(bytes(self._continue_read_stop_msg))
        self._serial.close()

