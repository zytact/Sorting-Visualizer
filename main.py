import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from insertion_sort import insertion_sort

plt.rcParams["figure.figsize"] = (12, 8)
plt.rcParams["font.size"] = 16
FPS = 30.0
N = 100
arr = np.round(np.linspace(0, 1000, N))
np.random.seed(0)
np.random.shuffle(arr)

class TrackedArray():

    def __init__(self, arr):
        self.arr = np.copy(arr)
        self.reset()

    def reset(self):
        self.indices = []
        self.values = []
        self.access_type = []
        self.full_copies = []

    def track(self, key, access_type):
        self.indices.append(key)
        self.values.append(self.arr[key])
        self.access_type.append(access_type)
        self.full_copies.append(np.copy(self.arr))

    def GetActivity(self, idx=None):
        if isinstance(idx, type(None)):
            return [(i, op) for (i, op) in zip(self.indices, self.access_type)]
        else: 
            return (self.indices[idx], self.access_type[idx])


    def __getitem__(self, key):
        self.track(key, "get")
        return self.arr.__getitem__(key)

    def __setitem__(self, key, value):
        self.arr.__setitem__(key, value)
        self.track(key, "set")

    def __len__(self):
        return self.arr.__len__()

arr = TrackedArray(arr)
sorted_arr = insertion_sort(arr)
fig, ax = plt.subplots()
fig.canvas.toolbar.pack_forget()
container = ax.bar(np.arange(0, len(sorted_arr), 1), sorted_arr, align="edge", width=0.8)
ax.set(xlabel="Index", ylabel="Value", title="Insertion Sort")
txt = ax.text(0, 1000, "")

def update(frame):
    global arr, container
    txt.set_text(f"Accesses = {frame}")
    for(rectangle, height) in zip(container.patches, arr.full_copies[frame]):
        rectangle.set_height(height)
        rectangle.set_color("#1f77b4")
    
    idx, op = arr.GetActivity(frame)
    if op == "get":
        container.patches[idx].set_color("magenta")
    if op == "set":
        container.patches[idx].set_color("red")

    return (*container,txt)

ani = FuncAnimation(fig, update, frames=range(len(arr.full_copies)),
                    blit=True, interval=1000/FPS, repeat=False)
plt.show()

