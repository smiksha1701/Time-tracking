# Time-Tracking API
## Results 
""In order to run correctly first of all you need to find out what exactly you want to measure.""
Here are some configuration I made to collect data:
1 configuration:
Fish: Not Isolated(No sudo)
Bash: Not Isolated
Time: Not Isolated
RunExec: Isolated(core 1)
Parallel processes: 1
2 configuration:
Fish: Not Isolated(No sudo)
Bash: Not Isolated
Time: Not Isolated
RunExec: Isolated(core 1)
Parallel processes: 0
3 configuration:
Fish: Isolated(core 1)(No sudo)
Bash: Isolated(core 1)
Time: Isolated(core 1)
RunExec: Isolated(core 1)
Parallel processes: 1
4 configuration:
Fish: Isolated(core 1)(sudo)
Bash: Isolated(core 1)
Time: Isolated(core 1)
RunExec: Isolated(core 1)
Parallel processes: 1
5 configuration:
Fish: Isolated(core 1)(sudo)
Bash: Isolated(core 1)
Time: Isolated(core 1)
RunExec: Isolated(core 1)
Parallel processes: 2
## Assign core
To assign specific cpu for my time-tracking API I was using `taskset [CPUMASK] command`(in my case `taskset 0x02 python main.py`). RunExec isolates cpu using cgroups so no additional isolation needed for it.
[Source](https://www.xmodulo.com/run-program-process-specific-cpu-cores-linux.html)
## Isolate core
To isolate core I added `isolcpus=` argument in /boot/cmdline.txt and set it's value to desired core. Afterwards you need to reboot machine for changes to take place. 
### Checking current status
To check what cores are currently isolated:
`$cat /sys/devices/system/cpu/isolated`
empty line means no CPU-core isolated.

After setting isolcpus:
`$ cat /sys/devices/system/cpu/kernel_max`
the system should report:
`3`
[Source](https://yosh.ke.mu/raspberry_pi_isolating_cores_in_linux_kernel)
## Data
In order to make analysis I collected results from 5 (to update) different configurations described above:
Names encryption:
`[]_iso` - index of isolated core or `no` in case no cores was isolated 
`[]par` - number of parallel processes
`[]runexec` - core assigned for RunExec
Additional:
`fish_sudo` - fish run with sudo    