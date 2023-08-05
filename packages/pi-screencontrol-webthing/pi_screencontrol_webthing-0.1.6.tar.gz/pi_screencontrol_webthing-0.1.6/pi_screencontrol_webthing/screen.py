import os
import logging
from time import sleep
from threading import Thread
from datetime import datetime, timedelta


class Screen:

    XSET_CMD = "XAUTHORITY=~pi/.Xauthority DISPLAY=:0 xset "

    def __init__(self, status_listener):
        self.__status_listener = status_listener
        self.__last_date_show_display = datetime.now()
        self.timeout_sec = 180  # 3 min
        self.is_on = True
        self.update_timeout(self.timeout_sec)
        Thread(target=self.__state_refresher, daemon=True).start()

    def update_timeout(self, timeout_sec: int):
        self.__execute_cmd(self.XSET_CMD + "s " + str(timeout_sec))
        self.__execute_cmd(self.XSET_CMD + "dpms " + str(timeout_sec) + " " + str(timeout_sec) + "  " + str(timeout_sec))
        self.timeout_sec = timeout_sec
        self.__refresh_on_flag()

    def show_display(self, activate: bool):
        if activate:
            now = datetime.now()
            if now > (self.__last_date_show_display + timedelta(seconds=1)):
                # wakeup
                self.__execute_cmd(self.XSET_CMD + "dpms force on")
                self.__last_date_show_display = now
                self.__refresh_on_flag()

    def __state_refresher(self):
        while True:
            try:
                sleep(3)
                self.__refresh_on_flag()
            except Exception as e:
                logging.warning(e)

    def __refresh_on_flag(self):
        new_on = self.__last_date_show_display + timedelta(seconds=self.timeout_sec-3) >= datetime.now()
        if self.is_on != new_on:
            self.is_on = new_on
            logging.info("[" + datetime.now().strftime('%Y-%m-%dT%H:%M:%S') + "] screen is active: " + str(self.is_on))
            self.__status_listener(self.is_on)

    def __execute_cmd(self, cmd: str):
        try:
            os.system(cmd)
            logging.info("[" + datetime.now().strftime('%Y-%m-%dT%H:%M:%S') + "]  " + cmd)
        except Exception as e:
            logging.info("[" + datetime.now().strftime('%Y-%m-%dT%H:%M:%S') + "]  error occured executing " + cmd + " -> " + str(e))
