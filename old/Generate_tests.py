import os 
import random
curpath = os.getcwd()
tests_path = os.path.join(curpath,"tests.txt")
with open(tests_path, "w") as f:
    for _ in range(1000):
        a, b = random.randint(-1000,1000), random.randint(-1000,1000)
        f.write("{} {} {}\n".format(a, b, int(a + b)))

