import matplotlib.pyplot as plt
import subprocess
import re
import os
import pickle
import numpy as np
from tqdm import tqdm

CMD = ['./main', '43434343']

def normalize(magnitude, unit):
    factors = {'micros': 0.001, 'millis': 1, 'secs': 1000}  # Define conversion factors for different units
    return magnitude * factors[unit]  # Return the normalized value of the magnitude in the specified unit

def fish(cmd=CMD):
    # Run the specified command and capture the output
    proc = subprocess.run(['fish', '-c', f'time {" ".join(cmd)}'], capture_output=True)
    rep = float(proc.stdout.decode())

    # Extract the user time and normalize it
    REGEX = 'usr time\s*([\d\.]*)\s(\w*)'
    m = re.search(REGEX, proc.stderr.decode())
    usr_time, unit = float(m.group(1)), m.group(2)
    usr_time = normalize(usr_time, unit)
    
    # Extract the system time and normalize it
    REGEX = 'sys time\s*([\d\.]*)\s(\w*)'
    m = re.search(REGEX, proc.stderr.decode())
    sys_time, unit = float(m.group(1)), m.group(2)
    sys_time = normalize(sys_time, unit)

    # Return the combined time (user + system) and the reported time
    return rep, usr_time + sys_time

def bash(cmd=CMD):
    # Run the specified command and capture the output
    proc = subprocess.run(['bash', '-c', f'time {" ".join(cmd)}'], capture_output=True)
    rep = float(proc.stdout.decode())

    # Extract the user time and normalize it
    REGEX = 'user\s*([\d\.]*)m([\d\.]*)s'
    m = re.search(REGEX, proc.stderr.decode())
    minutes, seconds = float(m.group(1)), float(m.group(2))
    usr_time = normalize(seconds + 60 * minutes, 'secs')
    
    # Extract the system time and normalize it
    REGEX = 'sys\s*([\d\.]*)m([\d\.]*)s'
    m = re.search(REGEX, proc.stderr.decode())
    minutes, seconds = float(m.group(1)), float(m.group(2))
    sys_time = normalize(seconds + 60 * minutes, 'secs')

    # Return the combined time (user + system) and the reported time
    return rep, usr_time + sys_time

def time(cmd=CMD):
    # Run the specified command and capture the output
    proc = subprocess.run(['/usr/bin/time'] + cmd, capture_output=True)
    rep = float(proc.stdout.decode())

    # Extract the user time and normalize it
    REGEX = '([\d\.]*)user\s([\d\.]*)system'
    m = re.search(REGEX, proc.stderr.decode())
    usr_time = normalize(float(m.group(1)), 'secs')
    
    # Extract the system time and normalize it
    sys_time = normalize(float(m.group(2)), 'secs')

    # Return the combined time (user + system) and the reported time
    return rep, usr_time + sys_time

def relb(cmd=CMD):
    # Run the specified command with restricted resources
    cmd_arr = ['systemd-run', '--user', '--scope', '--slice=benchexec', '-p', 'Delegate=yes', './benchexec/bin/runexec', '--no-container', '--read-only-dir', '/'] + cmd
    proc = subprocess.run(cmd_arr, capture_output=True)
    stdout = proc.stdout.decode()

    # Extract the CPU time and normalize it
    REGEX = 'cputime=(\d+\.\d+)'
    m = re.search(REGEX, stdout)
    cpu_time = normalize(float(m.group(1)), 'secs')

    # Read the output file and parse the last line as a float
    with open('output.log', 'r') as f:
        # Read the file contents and split by lines
        file_contents = f.read()
        lines = file_contents.splitlines()

        # Check if the file has any lines
        if len(lines) == 0:
            print('The file is empty')
        else:
            # Parse the last line as a float
            last_line = lines[-1]
            try:
                rep = float(last_line)
            except ValueError:
                print('The last line in the file is not a float')

    # Return the reported time and the CPU time
    return rep, cpu_time

def run(method, n=1000):
    reported, observed = [], []
    # Loop n times and run the specified method
    for _ in tqdm(range(n)):
        # Call the specified method and store the reported and observed times
        rep, obs = method()
        reported.append(rep)
        observed.append(obs)
    # Return the lists of reported and observed times
    return reported, observed

def load_or_run(filename, func, *args):
    # Check if the file already exists
    if os.path.exists(filename):
        # If it does, open the file and load the stored data using pickle
        with open(filename, 'rb') as f:
            return pickle.load(f)

    # If the file does not exist, call the specified function with the provided arguments
    res = func(*args)
    # Store the result of the function call in the file using pickle
    with open(filename, 'wb') as f:
        pickle.dump(res, f)
    # Return the result of the function call
    return res

# Load or run the function for each program and store the results in variables
fish_rep, fish_obs = load_or_run('fish.pkl', run, fish)
bash_rep, bash_obs = load_or_run('bash.pkl', run, bash)
time_rep, time_obs = load_or_run('time.pkl', run, time)
relb_rep, relb_obs = load_or_run('relb.pkl', run, relb)
# This code calculates the mean and standard deviation of the reported and observed
# times for each command (fish, bash, /usr/bin/time, and runexec) and prints the results
# in a formatted string.
print(f'fish rep(mean={np.mean(fish_rep)}, std={np.std(fish_rep, ddof=1)})')
print(f'fish obs(mean={np.mean(fish_obs)}, std={np.std(fish_obs, ddof=1)})')
print(f'bash rep(mean={np.mean(bash_rep)}, std={np.std(bash_rep, ddof=1)})')
print(f'bash obs(mean={np.mean(bash_obs)}, std={np.std(bash_obs, ddof=1)})')
print(f'time rep(mean={np.mean(time_rep)}, std={np.std(time_rep, ddof=1)})')
print(f'time obs(mean={np.mean(time_obs)}, std={np.std(time_obs, ddof=1)})')
print(f'relb rep(mean={np.mean(relb_rep)}, std={np.std(relb_rep, ddof=1)})')
print(f'relb obs(mean={np.mean(relb_obs)}, std={np.std(relb_obs, ddof=1)})')
# This code creates a histogram of the observed run-times for each command 
# (fish, bash, /usr/bin/time, and runexec) and displays it.
plt.hist([fish_obs,  relb_obs, time_obs, bash_obs], bins=50)
plt.legend(['fish built-in' , 'runexec', 'time', 'bash built-in'])
plt.title('Run-times distribution')
plt.xlabel('millis')
plt.ylabel('count')
plt.show()
# This code creates a cumulative histogram of the observed run-times for each command
# (fish, bash, /usr/bin/time, and runexec) and displays it.
plt.hist([fish_obs, relb_obs], bins=50, cumulative=True)
plt.legend(['fish built-in',  'runexec'])
plt.title('Run-times distribution (cumulative)')
plt.xlabel('millis')
plt.ylabel('count')
plt.show()
# This code creates a scatter plot of the reported and observed times for each command
# (fish, bash, /usr/bin/time, and runexec) and displays it. The plot also includes a 
# line with a slope of 1 to help visualize the relationship between the reported and 
# observed times.
plt.figure(figsize=(20, 20))
plt.scatter(fish_rep, fish_obs)
plt.scatter(bash_rep, bash_obs)
plt.scatter(time_rep, time_obs)
plt.scatter(relb_rep, relb_obs)
times = fish_rep + fish_obs + bash_rep + bash_obs + time_rep + time_obs + relb_obs + relb_rep
bounds = [np.min(times), np.max(times)]
plt.plot(bounds, bounds)
plt.legend(['fish', 'bash', '/usr/bin/time', 'runexec' , 'y = x'])
plt.title('Scatterplot')
plt.xlabel('rep')
plt.ylabel('obs')
plt.show()

# To Document / TODOs
#
# 1. How are these experiments actually executed, i.e. how is the
#    taskset specified? Maybe give a script to execute everything.
# 2. Run fish also with sudo as another experiment?
# 3. Maybe run /usr/bin/time as a separate configuration, but don't add system time? We also have to note here, that /usr/bin/time's precision is only centiseconds.
# 3. Process Priority, i.e. what priority is given to fish? Maybe put it to `realtime`?
# 4. Maybe look at https://gitlab.sai.jku.at/students/organization/-/issues/4
# 5. Put everything into Gitlab
