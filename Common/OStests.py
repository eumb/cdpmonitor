import subprocess
import os
import csv
import time
import datetime
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import settings
from modules.termcolor.termcolor import colored
ts = time.time()


timestamp = datetime.datetime.fromtimestamp(int(ts)).strftime('%Y-%m-%d %H:%M:%S')


filename = "results/result.csv"

if "check_output" not in dir( subprocess ): # duck punch it in!
    def f(*popenargs, **kwargs):
        if 'stdout' in kwargs:
            raise ValueError('stdout argument not allowed, it will be overridden.')
        process = subprocess.Popen(stdout=subprocess.PIPE, *popenargs, **kwargs)
        output, unused_err = process.communicate()
        retcode = process.poll()
        if retcode:
            cmd = kwargs.get("args")
            if cmd is None:
                cmd = popenargs[0]
            raise subprocess.CalledProcessError(retcode, cmd)
        return output
    subprocess.check_output = f

def checkProcess():
 testname= "checkProcess"
 output = subprocess.check_output(['ps', '-A'])
 processes  = ["httpd","openhab2","sshd"]
 for i in processes:
  if i in output:
    print(i + " is up an running!")
    logTestResult(testname,i,"is up an running!")
  else:
    print(i+ " is not running!")
    logTestResult(testname,i,"is not running!")

def pingAllHosts():
  testname="ping"
  with open('servers.txt', 'r') as f:
      lines = f.readlines()
      lines = [line.rstrip('\n') for line in open('servers.txt')]   
      for ip in lines:
            result=subprocess.Popen(["ping", "-c", "1", "-n", "-W", "2",    ip],stdout=f, stderr=f).wait()
            if result:
                print(ip, "inactive")
		logTestResult(testname,ip,"inactive")
            else:
                print(ip, "active")
		logTestResult(testname,ip,"iactive")

def usedSpace():
    used_space=os.popen("df -h / | grep -v Filesystem | awk '{print $5}'").readline().strip()
    testname ="usedSpace"
    diskSpace_critic = settings.config['DiskSpaceThreshold']['CRITICAL']+"%"
    diskSpace_major = settings.config['DiskSpaceThreshold']['MAJOR']+"%"
    diskSpace_warning = settings.config['DiskSpaceThreshold']['WARNING']+"%"
    if (used_space < diskSpace_warning):
        print("OK - %s of disk space used." % used_space)
        logTestResult(testname,used_space,"OK")
    elif (used_space > diskSpace_warning and used_space < diskSpace_major):
       	print("WARNING - %s of disk space used." % used_space)
	logTestResult(testname,used_space,"WARNING")
    elif (used_space > diskSpace_critic):
       	print("CRITICAL - %s of disk space used." % used_space)
	logTestResult(testname,used_space,"CRITICAL")
    else:
       	print("UKNOWN - %s of disk space used." % used_space)
	logTestResult(testname,used_space,"UKNOWN")

def usedMemory():
	testname="usedMemory"
	tot_m, used_m, free_m = map(int, os.popen('free -t -m').readlines()[-1].split()[1:])
	swap_t, swap_u, swap_f = map(int, os.popen('free -t -m').readlines()[-2].split()[1:])

	mem_critic = settings.config['MemoryThreshold']['CRITICAL']
	mem_major = settings.config['MemoryThreshold']['MAJOR']
	mem_warning = settings.config['MemoryThreshold']['WARNING']

	if (swap_t !=0):
                swap_percent = swap_u*100/swap_t
                if swap_percent < int(mem_warning) :
                        print colored("--- SWAP usage OK --- ",'green')
                        print("SWAP Total:" + str(swap_t) + " Usage:" + str(swap_u) + " Free:" + str(swap_f) + " Used:" + str(swap_percent) + "%")
                        logTestResult(testname,"SWAP Total:" + str(swap_t) + " Usage:" + str(swap_u) + " Free:" + str(swap_f) + " Used:" + str(swap_percent) + "%","")
                elif swap_percent >= int(mem_warning) and swap_percent < int(mem_major):
                        print colored("--- SWAP usage NOK --- in Warning alarm", 'yellow')
                        print("SWAP Total:" + str(swap_t) + " Usage:" + str(swap_u) + " Free:" + str(swap_f) + " Used:" + str(swap_percent) + "%")
                        logTestResult(testname,"SWAP Total:" + str(swap_t) + " Usage:" + str(swap_u) + " Free:" + str(swap_f) + " Used:" + str(swap_percent) + "%","")
                elif swap_percent >= int(mem_major) and swap_percent < int(mem_critic):
                        print colored("--- SWAP usage NOK --- in Major alarm", 'magenta')
                        print("SWAP Total:" + str(swap_t) + " Usage:" + str(swap_u) + " Free:" + str(swap_f) + " Used:" + str(swap_percent) + "%")
                        logTestResult(testname,"SWAP Total:" + str(swap_t) + " Usage:" + str(swap_u) + " Free:" + str(swap_f) + " Used:" + str(swap_percent) + "%","")
                elif swap_percent >= int(mem_critic):
                        print colored("--- SWAP usage NOK --- in Critical alarm", 'red')
                        print("SWAP Total:" + str(swap_t) + " Usage:" + str(swap_u) + " Free:" + str(swap_f) + " Used:" + str(swap_percent) + "%")
                        logTestResult(testname,"SWAP Total:" + str(swap_t) + " Usage:" + str(swap_u) + " Free:" + str(swap_f) + " Used:" + str(swap_percent) + "%","")
        else:
                swap_percent = swap_u
                print colored("--- SWAP Not initialized --- ",'green')
                print("SWAP Total:" + str(swap_t) + " Usage:" + str(swap_u) + " Free:" + str(swap_f) + " Used:" + str(swap_percent) + "%")
                logTestResult(testname,"SWAP Total:" + str(swap_t) + " Usage:" + str(swap_u) + " Free:" + str(swap_f) + " Used:" + str(swap_percent) + "%","")


	mem_percent =  int(used_m*100/tot_m)

	if mem_percent < int(mem_warning):
        	print colored("--- MEMORY usage OK --- ",'green')
        	print("MEMORY Total:" + str(tot_m) + " Usage:" + str(used_m) + " Free:" + str(free_m) + " Used:" + str(mem_percent) + "%")
		logTestResult(testname,"MEMORY Total:" + str(tot_m) + " Usage:" + str(used_m) + " Free:" + str(free_m) + " Used:" + str(mem_percent) + "%","")
	elif mem_percent >= int(mem_warning) and mem_percent < int(mem_major):
        	print colored("--- MEMORY usage NOK --- in Warning alarm", 'yellow')
        	print("MEMORY Total:" + str(tot_m) + " Usage:" + str(used_m) + " Free:" + str(free_m) + " Used:" + str(mem_percent) + "%")
		logTestResult(testname,"MEMORY Total:" + str(tot_m) + " Usage:" + str(used_m) + " Free:" + str(free_m) + " Used:" + str(mem_percent) + "%","")
	elif mem_percent >= int(mem_major) and mem_percent < int(mem_critic):
        	print colored("--- MEMORY usage NOK --- in Major alarm", 'magenta')
        	print("MEMORY Total:" + str(tot_m) + " Usage:" + str(used_m) + " Free:" + str(free_m) + " Used:" + str(mem_percent) + "%")
		logTestResult(testname,"MEMORY Total:" + str(tot_m) + " Usage:" + str(used_m) + " Free:" + str(free_m) + " Used:" + str(mem_percent) + "%","")
	elif mem_percent >= int(mem_critic):
        	print colored("--- MEMORY usage NOK --- in Critical alarm", 'red')
        	print("MEMORY Total:" + str(tot_m) + " Usage:" + str(used_m) + " Free:" + str(free_m) + " Used:" + str(mem_percent) + "%")
		logTestResult(testname,"MEMORY Total:" + str(tot_m) + " Usage:" + str(used_m) + " Free:" + str(free_m) + " Used:" + str(mem_percent) + "%","")

def logTestResult(testname,data,state):
    with open(filename, 'a') as csvfile:
        resultwriter = csv.writer(csvfile, delimiter=',')
        resultwriter.writerow([testname,timestamp,data,state])

