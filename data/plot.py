import matplotlib.pyplot as plt
import pickle
import numpy as np
def load(filename):
    # If it does, open the file and load the stored data using pickle
    with open(filename, 'rb') as f:
        return pickle.load(f)
fish_file = input("fish file")
bash_file = input("bash file")
time_file = input("time file")
relb_file = input("relb file")
fish_rep, fish_obs = load(fish_file)
bash_rep, bash_obs = load(bash_file)
time_rep, time_obs = load(time_file)
relb_rep, relb_obs = load(relb_file)
plt.hist([fish_obs,  relb_obs], bins=50)
plt.legend(['fish built-in' , 'runexec'])
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
