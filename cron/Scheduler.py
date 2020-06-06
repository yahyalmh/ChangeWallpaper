import os
import subprocess
import sys

from lib.pythoncrontab.crontab import CronTab

from Utils import Util


class Scheduler:
    hourly_comment = "changeWall_hourly"
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
        self.find_delete_job(self.hourly_comment)
        self.find_delete_job(self.reboot_comment)

        self.add_new_job()

    def add_new_job(self):
        if sys.platform.__contains__("win"):
            #  schtasks /end /tn "changeWall_hourly" // end task
            #  schtasks /run /tn "changeWall" //run task immediately

            python_path = "\" cmd /c python3 " + self.main_class_path + ">" + self.log_file_path + "\""
            hourly_cmd = "schtasks /create /sc hourly /tn " + self.hourly_comment + " /tr " + python_path  # minute
            subprocess.run(hourly_cmd, stdout=subprocess.PIPE).stdout.decode('utf-8')

            reboot_cmd = "schtasks /create /sc ONSTART /tn " + self.reboot_comment + " /tr " + python_path  # minute
            subprocess.run(reboot_cmd, stdout=subprocess.PIPE).stdout.decode('utf-8')

        elif sys.platform.__contains__("linux"):
            cron = CronTab(user=os.getenv('USER'))

            python_path = subprocess \
                .run(["which", "python3"], stdout=subprocess.PIPE) \
                .stdout.decode('utf-8') \
                .rstrip("\n")

            hourly_command = python_path + " " + self.main_class_path + " &>> " + self.log_file_path
            hourly_job = cron.new(command=hourly_command, comment=self.hourly_comment)
            hourly_job.every(1).hours()

            sleep = "sleep 30 &&  "
            reboot_command = sleep + python_path + " " + self.main_class_path + " &>> " + self.log_file_path
            reboot_job = cron.new(command=reboot_command, comment=self.reboot_comment)
            reboot_job.every_reboot()
            cron.write()

    def find_delete_job(self, job_comment):
        if sys.platform.__contains__("win"):
            list_job = "schtasks /query /fo LIST /tn " + job_comment
            result = subprocess.run(list_job, stdout=subprocess.PIPE).stdout.decode('utf-8')
            if result != "":
                delete_job = "schtasks /f /delete /tn " + job_comment
                subprocess.run(delete_job, stdout=subprocess.PIPE).stdout.decode('utf-8')

        elif sys.platform.__contains__("linux"):
            cron = CronTab(user=os.getenv('USER'))
            list_job = cron.find_comment(comment=job_comment)
            cron.remove(list_job)
            cron.write()
