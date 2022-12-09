import numpy as np
import os
import psutil
import threading
import csv
import argparse
import signal
from datetime import datetime

cpu64_percent_list = []
cpu256_percent_list = []
cpu1024_percent_list = []
isCalculating = True
max_rss64 = 0
max_rss256 = 0
max_rss1024 = 0

start_time = datetime.now()
timeout = 10 #timeout in minutes

def calCpuPercent(id):
    global isCalculating, cpu64_percent_list, max_rss64, cpu256_percent_list, max_rss256, cpu1024_percent_list, max_rss1024, start_time

    process = psutil.Process(os.getpid())
    print("Process ID: ", os.getpid())

    while True:
        if isCalculating:
            cpu_pr = process.cpu_percent()
            mem_pr = process.memory_info().rss

            if id == 64:
                if(cpu_pr > 0):
                    cpu64_percent_list.append(cpu_pr)
                if(mem_pr > max_rss64):
                    max_rss64 = mem_pr
            
            elif id == 256:
                if(cpu_pr > 0):
                    cpu256_percent_list.append(cpu_pr)
                if(mem_pr > max_rss256):
                    max_rss256 = mem_pr

            elif id == 1024:
                if(cpu_pr > 0):
                    cpu1024_percent_list.append(cpu_pr)
                if(mem_pr > max_rss1024):
                    max_rss1024 = mem_pr
            
            if((datetime.now() - start_time).total_seconds() > (timeout * 60)):
                print("Timeout of 10 mins exceeded, killing the process")
                if id == 64:
                    print(max_rss64)
                    with open('cpu_64_64_numpy_timeout', 'w') as f:
                        # using csv.writer method from CSV package
                        write = csv.writer(f)
                        write.writerows([cpu64_percent_list])
                        f.close()
                        os.kill(os.getpid(), signal.SIGKILL) #Trying to kill current process
                        return
            
                elif id == 256:
                    print(max_rss256)
                    with open('cpu_256_256_numpy_timeout', 'w') as f:
                        # using csv.writer method from CSV package
                        write = csv.writer(f)
                        write.writerows([cpu256_percent_list])
                        f.close()
                        os.kill(os.getpid(), signal.SIGKILL) #Trying to kill current process
                        return

                elif id == 1024:
                    print(max_rss1024)
                    with open('cpu_1024_1024_numpy_timeout', 'w') as f:
                        # using csv.writer method from CSV package
                        write = csv.writer(f)
                        write.writerows([cpu1024_percent_list])
                        f.close()
                        os.kill(os.getpid(), signal.SIGKILL) #Trying to kill current process
                        return

        else:
            return


if __name__ == "__main__":

    ap = argparse.ArgumentParser()
    ap.add_argument("-s", "--size", type=str, required=True,
    help="size of matrix")
    args = vars(ap.parse_args())
    print(args["size"])
    process = psutil.Process(os.getpid())

    if (args["size"] == "64"):
        M1_64 = np.ones((64,64), dtype=np.int64)
        M2_64 = np.ones((64,64), dtype=np.int64)
        
        # Executing 64x64 matrix
        start = datetime.now()
        start_time = datetime.now()
        t1 = threading.Thread(target=calCpuPercent, args = (64,))
        t1.daemon = True
        t1.start()

        M3_64 =  np.matmul(M1_64, M2_64)
        isCalculating = False
        
        end = datetime.now()
        td = (end - start).total_seconds() * 10**3
        print(f"The time of execution of 64x64 is : {td:.03f}ms")    
        
        print("M3_256: \n", M3_64)
        print("\n\n")
        process1 = psutil.Process(os.getpid())
        print("Max Bytes used in RAM for 64x64:", max_rss64)

        with open('cpu_64_64_numpy', 'w') as f:
            # using csv.writer method from CSV package
            write = csv.writer(f)
            write.writerows([cpu64_percent_list])
            f.close()
    
    elif (args["size"] == "256"):
        M1_256 = np.ones((256,256), dtype=np.int64)
        M2_256 = np.ones((256,256), dtype=np.int64)
        
        # Executing 256x256 matrix
        start = datetime.now()
        start_time = datetime.now()
        t2 = threading.Thread(target=calCpuPercent, args = (256,))
        t2.daemon = True
        t2.start()

        M3_256 =  np.matmul(M1_256, M2_256)
        isCalculating = False
        
        end = datetime.now()
        td = (end - start).total_seconds() * 10**3
        print(f"The time of execution of 256x256 is : {td:.03f}ms")    
        
        print("M3_256: \n", M3_256)
        print("\n\n")
        process1 = psutil.Process(os.getpid())
        print("Max Bytes used in RAM for 256x256:", max_rss256)
        
        with open('cpu_256_256_numpy', 'w') as f:
            # using csv.writer method from CSV package
            write = csv.writer(f)
            write.writerows([cpu256_percent_list])
            f.close()

    elif (args["size"] == "1024"):
        M1_1024 = np.ones((1024,1024), dtype=np.int64)
        M2_1024 = np.ones((1024,1024), dtype=np.int64)
        # Executing 1024x1024 matrix
        start = datetime.now()
        start_time = datetime.now()
        t3 = threading.Thread(target=calCpuPercent, args = (1024,))
        t3.daemon = True
        t3.start()

        M3_1024 =  np.matmul(M1_1024, M2_1024)
        isCalculating = False
        
        end = datetime.now()
        td = (end - start).total_seconds() * 10**3
        print(f"The time of execution of 1024x1024 is : {td:.03f}ms")    
        
        print("M3_1024: \n", M3_1024)
        print("\n\n")
        process1 = psutil.Process(os.getpid())
        print("Max Bytes used in RAM for 1024x1024:", max_rss1024)
        
        with open('cpu_1024_1024_numpy', 'w') as f:
            # using csv.writer method from CSV package
            write = csv.writer(f)
            write.writerows([cpu1024_percent_list])
            f.close()
