#!/usr/bin/python3
"""
Author: Tyler Woods
Program version 1
--------------------------------------------------------------

This backup program is used to locate and back up files manually
further development of this should be able to be ran automatically.

"""
#imports to help implement the written code
import sys #added for function and to help run the code
import os #
import pathlib #opens up a path library
import shutil #allows the ability to copy and create files
import smtplib #imports the library to allow emails
from datetime import datetime #used to create a time stam p on the back up files
from backupcfg import jobs, dstpath, smtp, logpath #used as reference points and variables and smtp information


def logging(message, dateTimeStamp):
    try:
        file = open(logpath, "a")
        file.write(f"{message} {dateTimeStamp}.\n")
        file.close()
    except FileNotFoundError:
        print("ERROR: File does not exist.")
    except IOError:
        print("ERROR: File is not accessible.")

def sendEmail(errormessage, dateTimeStamp):
    """ 
    Send an email message to the specified recipient. 
    Parameters: 
    message (string): message to send. 
    dateTimeStamp (string): Date and time when program was run. 
    """ 
    # create email message 
    email = 'To: ' + smtp["recipient"] + '\n' + 'From: ' + smtp["sender"] +  '\n' + 'Subject: Backup Error \n\n' + errormessage + dateTimeStamp + '\n' 
    # connect to email server and send email
    try:
        smtp_server = smtplib.SMTP(smtp["server"], smtp["port"])
        smtp_server.ehlo()
        smtp_server.starttls()
        smtp_server.ehlo()
        smtp_server.login(smtp["user"], smtp["password"])
        smtp_server.sendmail(smtp["sender"], smtp["recipient"], email)
        smtp_server.close()
    except Exception as e:
        print("ERROR: Send email failed: " + str(e), file=sys.stderr)

def error(errormessage, dateTimeStamp):
    print(f'FAILURE {errormessage}')
    logging(f'FAILURE {errormessage}', dateTimeStamp)
    sendEmail(errormessage, dateTimeStamp)
   # sendEmail(errormessage, dateTimeStamp) #email FAILURE to email
    
def success(message, dateTimeStamp):
    logging(message, dateTimeStamp)


def main():
    dateTimeStamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    argcount = len(sys.argv)

    if argcount != 2:               #identifies if a job has been given or not
        error(f"ERROR: jobname missing from command line", dateTimeStamp)
    else:
        jobname = sys.argv[1]
        if jobname not in jobs:
            error(f"ERROR: jobname {jobname} not defined", dateTimeStamp)
        else:
            for srcpath in jobs[jobname]:
                if not os.path.exists(srcpath): #searches for tthe source of the file or directory named in backupcfg.py
                    error(f"ERROR: source path {srcpath} does not exist", dateTimeStamp)
            else:
                if not os.path.exists(dstpath):
                    error(f"ERROR: Destination path {dstpath} does not exist", dateTimeStamp)
                else:
                    srcdetails = pathlib.PurePath(srcpath) #runs in the background to pick apart the source file/directory to be able to recreate it.
                    
                    dstLoc = dstpath + "/" + srcdetails.name + "-" + dateTimeStamp #creates a file backup with date and time stamp

                    if pathlib.Path(srcpath).is_dir():          #copies directory and files
                        shutil.copytree(srcpath, dstLoc)
                        success(f'SUCCESS: of back up ', dateTimeStamp)
                    else:
                        shutil.copy2(srcpath, dstLoc)           #copies the file
                        success(f'SUCCESS: of back up ', dateTimeStamp)
                        #write SUCCSESS to log file
                    
if __name__ == "__main__":
    main()