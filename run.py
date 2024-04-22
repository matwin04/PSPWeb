import subprocess
import os
import time

app_path = os.path.join(os.path.dirname(__file__), 'app.py')
scanner_path = os.path.join(os.path.dirname(__file__), 'scanner.py')
def run():
    app_process = subprocess.Popen(['python', app_path])
    time.sleep(1)
    scanner_process = subprocess.Popen(['python',scanner_path])
    
    app_process.wait()
    scanner_process.wait()
if __name__ == "__main__":
    run()