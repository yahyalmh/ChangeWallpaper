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
        if not self.is_job_scheduled(self.hourly_comment):
            self.add_new_job(self.hourly_comment)

        if not self.is_job_scheduled(self.reboot_comment):
            self.add_new_job(self.reboot_comment)

    def add_new_job(self, job_comment):
        if sys.platform.__contains__("win"):
            # python_path = "\" cmd /c python3 " + self.main_class_path + ">" + self.log_file_path + "\""
            run_path = self.project_root_dir + os.sep + "run.vbs"
            command = ""

            if job_comment == self.hourly_comment:
                command = "schtasks /create /sc hourly /tn " + job_comment + " /tr " + run_path
            elif job_comment == self.reboot_comment:
                command = ""  # need admin
                # command = "schtasks /create /sc onstart /tn " + job_comment + " /tr " + python_path

            if command != "":
                subprocess.run(command, stdout=subprocess.PIPE).stdout.decode('utf-8')

        elif sys.platform.__contains__("linux"):
            cron = CronTab(user=os.getenv('USER'))
            python_path = subprocess \
                .run(["which", "python3"], stdout=subprocess.PIPE) \
                .stdout.decode('utf-8') \
                .rstrip("\n")

            if job_comment == self.hourly_comment:
                hourly_command = python_path + " " + self.main_class_path + " &>> " + self.log_file_path
                hourly_job = cron.new(command=hourly_command, comment=job_comment)
                hourly_job.every(1).hours()
            elif job_comment == self.reboot_comment:
                sleep = "sleep 30 &&  "
                reboot_command = sleep + python_path + " " + self.main_class_path + " &>> " + self.log_file_path
                reboot_job = cron.new(command=reboot_command, comment=job_comment)
                reboot_job.every_reboot()

            cron.write()

    def is_job_scheduled(self, job_comment):
        result = False
        if sys.platform.__contains__("win"):
            list_job = "schtasks /query /fo list /tn " + job_comment
            result = subprocess.run(list_job, stdout=subprocess.PIPE).stdout.decode('utf-8')
            if result != "":
                result = True

        elif sys.platform.__contains__("linux"):
            cron = CronTab(user=os.getenv('USER'))
            list_job = cron.find_comment(comment=job_comment)
            cron_list = []
            for item in list_job:
                cron_list.append(item)
            if len(cron_list) > 0:
                result = True
        return result
