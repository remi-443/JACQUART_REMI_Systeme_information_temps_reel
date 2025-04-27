import heapq
import math
from functools import reduce
from collections import defaultdict

def lcm(a, b):
    return abs(a * b) // math.gcd(a, b)

def lcm_list(lst):
    return reduce(lcm, lst)

class Task:
    def __init__(self, name, c, t):
        self.name = name
        self.c = c  # Temps de calcul
        self.t = t  # Période
        self.remaining_c = c  # Temps restant à exécuter
        self.next_release = 0  # Prochaine date de libération

    def __lt__(self, other):
        return self.t < other.t

def edf_scheduling(tasks, hyperperiod):
    time = 0
    schedule = []
    task_queue = []
    IdleTime = 0
    WaitingTime = 0
    starting_times = defaultdict(list)
    response_times = defaultdict(list)

    while time < hyperperiod:
        # Release des nouvelles tâches
        for task in tasks:
            if time >= task.next_release:
                new_task = Task(task.name, task.c, task.t)
                new_task.next_release = task.next_release + task.t
                heapq.heappush(task_queue, (task.next_release + task.t, new_task))
                task.next_release += task.t

        if task_queue:
            # Extraction de la tâche EDF (plus petite deadline)
            _, task = heapq.heappop(task_queue)
            start_time = time
            starting_times[task.name].append(start_time)
            WaitingTime += time - (task.next_release - task.t)
            while task.remaining_c > 0 and time < hyperperiod:
                schedule.append((time, task.name))
                task.remaining_c -= 1
                time += 1
                # Enregistrement du temps de réponse pour cette instance
            release_time = task.next_release - task.t
            response_times[task.name].append(time - release_time)
        else:
            schedule.append((time, "Idle"))
            IdleTime += 1
            time += 1

    return schedule, IdleTime, WaitingTime, starting_times,response_times

# Définition des tâches
tasks = [
    Task('τ1', 2, 10),
    Task('τ2', 3, 10),
    Task('τ3', 2, 20),
    Task('τ4', 2, 20),
    Task('τ5', 2, 40),
    Task('τ6', 2, 40),
    Task('τ7', 3, 80)
]

# Hyperpériode
hyperperiod = lcm_list([t.t for t in tasks])

# Forcer τ5 à échouer pour test de deadline
#tasks[4].t = 100

# Ordonnancement EDF avec analyse de temps de réponse
schedule, idle_time, waiting_time, starting_times, response_times = edf_scheduling(tasks, hyperperiod)

print("Schedule  ", schedule[:hyperperiod], "\n Idle Time \n", idle_time, 
 "\n Waiting Time \n", waiting_time, "\n Tasks starting time: \n",dict(starting_times),
 "\n Response Times \n", dict(response_times))

