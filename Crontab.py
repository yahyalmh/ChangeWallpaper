import os
import subprocess
import sys

from crontab import CronTab

from Utils import Util


class Crontab:
    command_name = "changeWall"

    def __init__(self):
        self.project_dir = Util.get_instance().get_project_dir()
        self.log_file_path = self.project_dir + os.sep + "logs.txt"
        if not os.path.exists(self.log_file_path):
            fi = open(self.log_file_path, "a+")
            fi.write("# change wallpaper logs \n")
            fi.close()

        self.project_root_dir = Util.get_instance().get_project_root()
        self.main_class_path = self.project_root_dir + os.sep + "Main.py"

    def run(self):
        if sys.platform.__contains__("win"):

            #  schtasks /end /tn "changeWall" // end task
            #  schtasks /run /tn "changeWall" //run task immediately
            cmd = "schtasks /query /fo LIST /tn " + self.command_name
            result = subprocess.run(cmd, stdout=subprocess.PIPE).stdout.decode('utf-8')

            if result != "":
                cmd = "schtasks /f /delete /tn " + self.command_name
                result = subprocess.run(cmd, stdout=subprocess.PIPE).stdout.decode('utf-8')

            python_path = "\" cmd /c python3 " + self.main_class_path + ">" + self.log_file_path + "\""
            # p = "python3 " + self.main_class_path + ">" + self.log_file_path
            # bat_path = self.project_root_dir + os.sep + "test.bat"
            # file = open(bat_path, "+a")
            # file.write(p)
            # file.close()

            # cmd = "schtasks /create /sc minute /tn " + self.command_name + " /tr " + bat_path
            cmd = "schtasks /create /sc hourly /tn " + self.command_name + " /tr " + python_path  # minute
            result = subprocess.run(cmd, stdout=subprocess.PIPE).stdout.decode('utf-8')


        elif sys.platform.__contains__("linux"):
            cron = CronTab(user=os.getenv('USER'))
            pre_job = cron.find_comment(comment=self.command_name)
            cron.remove(pre_job)
            cron.write()

            # env_python_path = project_root_dir + os.sep + "venv/bin/python"
            env_python_path = "python3"

            command = env_python_path + " " + self.main_class_path + " &>> " + self.log_file_path
            job = cron.new(command=command, comment=self.command_name)
            job.hours.every(1)
            cron.write()
