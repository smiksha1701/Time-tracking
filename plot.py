#import matplotlib.pyplot as plt
import plotly.graph_objects as go
import pickle
import numpy as np
import os
from plotly.subplots import make_subplots
import plotly.graph_objects as go
"""def load(filename):
    # If it does, open the file and load the stored data using pickle
    with open(filename, 'rb') as f:
        return pickle.load(f)"""
"""
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
plt.show()"""

def load(filename):
    # If it does, open the file and load the stored data using pickle
    with open(filename, 'rb') as f:
        return pickle.load(f)
file_pattern = ""
data_folder = 'data' 
relb_files = [f'{i}relb.pkl' for i in range(7)]
fish_files = [f'{i}fish.pkl' for i in range(7)]
time_files = [f'{i}time.pkl' for i in range(7)]
bash_files = [f'{i}bash.pkl' for i in range(7)]


def unpack_data(files):
    obs_list = []
    rep_list = []
    wall_list =[]
    for file in files:
        path = os.path.join(os.getcwd(), data_folder, 'with_wall_rpi', file)
        wall, rep, obs = load(path)
        wall_list.append(wall)
        rep_list.append(rep)
        obs_list.append(obs)
    return wall_list, rep_list, obs_list
fish_wall_list, fish_rep_list, fish_obs_list = unpack_data(fish_files)
time_wall_list, time_rep_list, time_obs_list = unpack_data(time_files)
bash_wall_list, bash_rep_list, bash_obs_list = unpack_data(bash_files)
relb_wall_list, relb_rep_list, relb_obs_list = unpack_data(relb_files)
def plot_wall():
    for i, (wall_list, group_name) in enumerate(zip([relb_wall_list, fish_wall_list,  bash_wall_list, time_wall_list],['relb','fish','bash','time'])):
        row = (i // 2) + 1
        col = (i % 2) + 1
        for j, wall in enumerate(wall_list, start=1):
            fig.add_trace(go.Histogram(x=wall, legendgroup=i , legendgrouptitle_text = group_name, name=f'num of proc {j} {np.mean(wall)}', xbins=dict(size = 10)), row=row, col=col)

        fig.update_layout(
            title=f'Run-times distribution (wall)',
            xaxis_title='millis',
            yaxis_title='count',
            barmode='overlay',
            bargap=0.1
        )

        fig.update_traces(opacity=0.75, row=row, col=col)

    fig.show()
def plot_rep():
    for i, (rep_list, group_name) in enumerate(zip([relb_rep_list, fish_rep_list,  bash_rep_list, time_rep_list],['relb','fish','bash','time'])):
        row = (i // 2) + 1
        col = (i % 2) + 1

        for j, rep in enumerate(rep_list):
            fig.add_trace(go.Histogram(x=rep, legendgroup=i , legendgrouptitle_text = group_name, name=f'num of proc {j} {np.mean(rep)}', xbins=dict(size = 10)), row=row, col=col)


        fig.update_layout(
            title=f'Run-times distribution (rep)',
            xaxis_title='millis',
            yaxis_title='count',
            barmode='overlay',
            bargap=0.1
        )

        fig.update_traces(opacity=0.75, row=row, col=col)

    fig.show()

def plot_obs():
    for i, (obs_list, group_name) in enumerate(zip([relb_obs_list, fish_obs_list,  bash_obs_list, time_obs_list],['relb','fish','bash','time'])):
        row = (i // 2) + 1
        col = (i % 2) + 1

        for j, obs in enumerate(obs_list):
            fig.add_trace(go.Histogram(x=obs, legendgroup=i , legendgrouptitle_text = group_name, name=f'num of proc {j} {np.mean(obs)}', xbins=dict(size = 10)), row=row, col=col)

        fig.update_layout(
            title=f'Run-times distribution (obs)',
            xaxis_title='millis',
            yaxis_title='count',
            barmode='overlay',
            bargap=0.1
        )

        fig.update_traces(opacity=0.75, row=row, col=col)

    fig.show()
fig = make_subplots(rows=2, cols=2, subplot_titles=['relb', 'fish', 'bash', 'time'])
plot_obs()

# This code creates a cumulative histogram of the observed run-times for each command
# (fish, bash, /usr/bin/time, and runexec) and displays it.
"""plt.hist([fish_obs, relb_obs], bins=50, cumulative=True)
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
"""