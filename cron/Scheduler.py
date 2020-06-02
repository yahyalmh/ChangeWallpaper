import os
import subprocess
import sys

from lib.pythoncrontab.crontab import CronTab

from Utils import Util


class Scheduler:
    hourly_comment = "changeWall"
    reboot_comment = "changeWall_reboot"

    def __init__(self):
        self.project_dir = Util.get_instance().get_project_root()
        self.log_file_path = self.project_dir + os.sep + "logs.txt"
        if not os.path.exists(self.log_file_path):
            fi = open(self.log_file_path, "a+")
            fi.write("# change wallpaper logs \n")
            fi.close()

        self.project_root_dir = Util.get_instance().get_project_root()
        self.main_class_path = self.project_root_dir + os.sep + "Main.py"

    def schedule(self):
        if sys.platform.__contains__("win"):
            #  schtasks /end /tn "changeWall" // end task
            #  schtasks /run /tn "changeWall" //run task immediately
            cmd = "schtasks /query /fo LIST /tn " + self.hourly_comment
            result = subprocess.run(cmd, stdout=subprocess.PIPE).stdout.decode('utf-8')

            if result != "":
                cmd = "schtasks /f /delete /tn " + self.hourly_comment
                result = subprocess.run(cmd, stdout=subprocess.PIPE).stdout.decode('utf-8')

            python_path = "\" cmd /c python3 " + self.main_class_path + ">" + self.log_file_path + "\""
            # p = "python3 " + self.main_class_path + ">" + self.log_file_path
            # bat_path = self.project_root_dir + os.sep + "test.bat"
            # file = open(bat_path, "+a")
            # file.write(p)
            # file.close()

            # cmd = "schtasks /create /sc minute /tn " + self.hourly_comment + " /tr " + bat_path
            cmd = "schtasks /create /sc hourly /tn " + self.hourly_comment + " /tr " + python_path  # minute
            subprocess.run(cmd, stdout=subprocess.PIPE).stdout.decode('utf-8')

        elif sys.platform.__contains__("linux"):
            cron = CronTab(user=os.getenv('USER'))

            pre_hourly_job = cron.find_comment(comment=self.hourly_comment)
            cron.remove(pre_hourly_job)

            pre_reboot_job = cron.find_comment(comment=self.reboot_comment)
            cron.remove(pre_reboot_job)
            cron.write()

            python_path = subprocess \
                .run(["which", "python3"], stdout=subprocess.PIPE) \
                .stdout.decode('utf-8') \
                .rstrip("\n")

            command = python_path + " " + self.main_class_path + " &>> " + self.log_file_path
            hourly_job = cron.new(command=command, comment=self.hourly_comment)
            hourly_job.every(1).hours()

            reboot_job = cron.new(command=command, comment=self.reboot_comment)
            reboot_job.every_reboot()
            cron.write()

