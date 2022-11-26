import subprocess
import os
# import re for findall
import time


def main():

    REFRESH_TIME = 10

    if not os.path.exists(r"C:\Users\Public\internet_status"):
        os.mkdir(r"C:\Users\Public\internet_status")

    log_file = open(r"C:\Users\Public\internet_status\logfile.txt", "a")

    prev_status = my_ping()

    line = line_generator(prev_status)
    log_file.write(line)  # Writing the first internet status.
    log_file.close()

    time.sleep(REFRESH_TIME)

    while True:
        current_status = my_ping()

        if current_status != prev_status:
            log_file = open(r"C:\Users\Public\internet_status\logfile.txt", "a")
            line = line_generator(current_status)
            log_file.write(line)
            prev_status = current_status
            log_file.close()

        time.sleep(REFRESH_TIME)


def line_generator(internet_status):

    """
    This function create the line which be written to the file
    :param: internet_status
    :return:the line
    """
    date = "{0}/{1}/{2}".format(time.localtime().tm_mday, time.localtime().tm_mon, time.localtime().tm_year)
    current_time = "{0}:{1}:{2}".format(time.localtime().tm_hour, time.localtime().tm_min, time.localtime().tm_sec)
    current_line = "{0}\t{1}\t{2}\n".format(date, current_time, internet_status)
    return current_line


def my_ping():

    """
    This function send a ping request to google and return the response.
    :param: none
    :return: internet status
    """

    command = r"ping -n 1 www.google.com > C:\Users\Public\internet_status\ping.txt"
    #os.system(command)  # Send the ping command
    subprocess.call(command, shell=True)
    # Read the response file
    f = open(r"C:\Users\Public\internet_status\ping.txt", "r")
    f = f.readlines()

    if len(f) == 1:
        return "Disconnected"
    if f[2].startswith("Request timed out."):
        return "Timed-Out"
    if f[2].startswith("Reply"):
        return "Connected"


if __name__ == "__main__":
    main()