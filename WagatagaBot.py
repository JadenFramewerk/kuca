import multiprocessing
import subprocess

def run_script1():
    subprocess.run(['python', 'bintest.py'])

def run_script2():
    subprocess.run(['python', 'cugotter.py'])

def run_script3():
    subprocess.run(['python', 'kubot.py'])

if __name__ == "__main__":
    process1 = multiprocessing.Process(target=run_script1)
    process2 = multiprocessing.Process(target=run_script2)
    process3 = multiprocessing.Process(target=run_script3)

    process1.start()
    process2.start()
    process3.start()

    process1.join()
    process2.join()
    process3.join()

    print("All scripts have finished.")
