import matplotlib.pyplot as plt
import subprocess
import re
import os
import pickle
import numpy as np
from tqdm import tqdm

CMD = './main 43434343'

def normalize(magnitude, unit):
    factors = {'micros': 0.001, 'millis': 1, 'secs': 1000}
    return magnitude * factors[unit]

def fish(cmd=CMD):
    REGEX = 'usr time\s*(\S*)\s(\w*)'

    proc = subprocess.run(['fish', '-c', f'time {cmd}'], capture_output=True)
    m = re.search(REGEX, proc.stderr.decode())
    magnitude, unit = m.group(1), m.group(2)

    observed = normalize(float(magnitude), unit)
    real = float(proc.stdout.decode())
    return real, observed

def run(method, n=1000):
    tr, to = [], []
    for _ in tqdm(range(n)):
        real, obs = method()
        tr.append(real)
        to.append(obs)
    return tr, to

def load_or_run(filename, func, *args):
    if os.path.exists(filename):
        with open(filename, 'rb') as f:
            return pickle.load(f)

    res = func(*args)
    with open(filename, 'wb') as f:
        pickle.dump(res, f)
    return res

tr, to = load_or_run('fish.pkl', run, fish)

print(f'real(mean={np.mean(tr)}, std={np.std(tr, ddof=1)})')
print(f'obs(mean={np.mean(to)}, std={np.std(to, ddof=1)})')
plt.hist([tr, to], bins=100)
plt.title('Run-times distribution')
plt.legend(['std::clock', 'fish\'s time'])
plt.xlabel('millis')
plt.ylabel('count')
plt.show()

plt.hist([tr, to], bins=100, cumulative=True)
plt.title('Run-times distribution (cumulative)')
plt.legend(['std::clock', 'fish\'s time'])
plt.xlabel('millis')
plt.ylabel('count')
plt.show()

plt.scatter(tr, to)
bounds = [np.min(tr + to), np.max(tr + to)]
plt.plot(bounds, bounds)
plt.xlabel('real')
plt.ylabel('obs')
plt.show()
