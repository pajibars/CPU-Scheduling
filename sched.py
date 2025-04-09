class Process:
    def __init__(self, pid, arrival_time, burst_time):
        self.pid = pid
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.remaining_time = burst_time
        self.completion_time = 0
        self.waiting_time = 0
        self.turnaround_time = 0

def fcfs(processes):
    print("\n--- First Come First Serve (FCFS) ---")
    processes.sort(key=lambda x: x.arrival_time)
    time = 0
    for p in processes:
        if time < p.arrival_time:
            time = p.arrival_time
        p.waiting_time = time - p.arrival_time
        time += p.burst_time
        p.completion_time = time
        p.turnaround_time = p.completion_time - p.arrival_time

    print_results(processes)

def sjf(processes):
    print("\n--- Shortest Job First (Non-Preemptive) ---")
    time = 0
    completed = []
    while len(completed) < len(processes):
        ready = [p for p in processes if p.arrival_time <= time and p not in completed]
        if ready:
            current = min(ready, key=lambda x: x.burst_time)
            current.waiting_time = time - current.arrival_time
            time += current.burst_time
            current.completion_time = time
            current.turnaround_time = current.completion_time - current.arrival_time
            completed.append(current)
        else:
            time += 1
    print_results(completed)

def round_robin(processes, quantum):
    print("\n--- Round Robin ---")
    queue = []
    time = 0
    completed = 0
    processes.sort(key=lambda x: x.arrival_time)
    queue.append(processes[0])
    visited = set()
    visited.add(processes[0])
    
    while queue:
        current = queue.pop(0)
        if current.arrival_time > time:
            time = current.arrival_time
        exec_time = min(current.remaining_time, quantum)
        time += exec_time
        current.remaining_time -= exec_time

        for p in processes:
            if p not in visited and p.arrival_time <= time:
                queue.append(p)
                visited.add(p)
        if current.remaining_time == 0:
            current.completion_time = time
            current.turnaround_time = current.completion_time - current.arrival_time
            current.waiting_time = current.turnaround_time - current.burst_time
            completed += 1
        else:
            queue.append(current)

    print_results(processes)

def print_results(processes):
    print(f"{'PID':<5}{'Arrival':<8}{'Burst':<6}{'Waiting':<8}{'Turnaround':<11}{'Completion':<11}")
    for p in processes:
        print(f"{p.pid:<5}{p.arrival_time:<8}{p.burst_time:<6}{p.waiting_time:<8}{p.turnaround_time:<11}{p.completion_time:<11}")
    avg_wait = sum(p.waiting_time for p in processes) / len(processes)
    avg_turnaround = sum(p.turnaround_time for p in processes) / len(processes)
    print(f"\nAverage Waiting Time: {avg_wait:.2f}")
    print(f"Average Turnaround Time: {avg_turnaround:.2f}")

# Sample data
processes = [
    Process("P1", 0, 5),
    Process("P2", 1, 3),
    Process("P3", 2, 8),
    Process("P4", 3, 6),
]

fcfs([Process(p.pid, p.arrival_time, p.burst_time) for p in processes])
sjf([Process(p.pid, p.arrival_time, p.burst_time) for p in processes])
round_robin([Process(p.pid, p.arrival_time, p.burst_time) for p in processes], quantum=3)
