import tkinter as tk
from tkinter import messagebox


class Process:
    def __init__(self, pid, arrival_time, burst_time, priority):
        self.pid = pid
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.priority = priority
        self.remaining_time = burst_time
        self.start_time = 0
        self.end_time = 0
        self.waiting_time = 0
        self.turnaround_time = 0
        self.response_time = 0 

class PriorityScheduler:
    def __init__(self, processes):
        self.processes = processes
        self.current_time = 0
        self.ready_queue = []

    def run_scheduler(self):
        completed_processes = []
        timeline = []
        
        while self.processes or self.ready_queue:
            while self.processes and self.processes[0].arrival_time <= self.current_time:
                self.ready_queue.append(self.processes.pop(0))
            
            if self.ready_queue:
                current_process = min(self.ready_queue, key=lambda x: x.priority)
                
                if current_process.response_time == 0:
                    current_process.response_time = self.current_time - current_process.arrival_time
                    current_process.start_time = self.current_time


                current_process.remaining_time -= 1
                timeline.append(current_process.pid)

                if current_process.remaining_time == 0:
                    current_process.end_time = self.current_time + 1
                    completed_processes.append(current_process)
                    self.ready_queue.remove(current_process)
            else:
                timeline.append(-1)

            self.current_time += 1

        return completed_processes, timeline

    def calculate_metrics(self, completed_processes):
        total_waiting_time = 0
        total_turnaround_time = 0
        total_response_time = 0

        for process in completed_processes:
            process.turnaround_time = process.end_time - process.arrival_time
            process.waiting_time = process.turnaround_time - process.burst_time
            total_waiting_time += process.waiting_time
            total_turnaround_time += process.turnaround_time
            total_response_time += process.response_time

        num_processes = len(completed_processes)
        avg_waiting_time = total_waiting_time / num_processes
        avg_turnaround_time = total_turnaround_time / num_processes
        avg_response_time = total_response_time / num_processes

        return avg_waiting_time, avg_turnaround_time, avg_response_time

class PrioritySimulationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Priority (Preemptive) Simulation")

        self.process_widgets = []
        self.processes = []

        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.root, text="Number of processes:").pack()
        self.num_processes_entry = tk.Entry(self.root)
        self.num_processes_entry.pack()
        tk.Button(self.root, text="Enter", command=self.get_num_processes).pack()

    def get_num_processes(self):
        try:
            num_processes = int(self.num_processes_entry.get())
            self.create_process_input_fields(num_processes)
        except ValueError:
            tk.messagebox.showerror("Error", "Please enter a valid number")

    def create_process_input_fields(self, num_processes):
        for i in range(num_processes):
            process_frame = tk.Frame(self.root)
            process_frame.pack(pady=10)

            tk.Label(process_frame, text=f"Process {i+1}").grid(row=i+2, column=0)
            tk.Label(process_frame, text="Arrival Time:").grid(row=i+2, column=1)
            tk.Label(process_frame, text="Burst Time:").grid(row=i+2, column=3)
            tk.Label(process_frame, text="Priority:").grid(row=i+2, column=5)

            arrival_entry = tk.Entry(process_frame)
            arrival_entry.grid(row=i+2, column=2)
            burst_entry = tk.Entry(process_frame)
            burst_entry.grid(row=i+2, column=4)
            priority_entry = tk.Entry(process_frame)
            priority_entry.grid(row=i+2, column=6)

            self.process_widgets.append((arrival_entry, burst_entry, priority_entry))

        tk.Button(self.root, text="Simulate", command=self.simulate).pack()




     
    def simulate(self):
        try:
            self.processes = []
            for arrival_entry, burst_entry, priority_entry in self.process_widgets:
                arrival_time = int(arrival_entry.get())
                burst_time = int(burst_entry.get())
                priority = int(priority_entry.get())
                if arrival_time < 0 or burst_time <= 0 or priority < 0:
                    tk.messagebox.showerror("Error", "Input values are invalid")
                    return
                self.processes.append(Process(len(self.processes) + 1, arrival_time, burst_time, priority))

            scheduler = PriorityScheduler(self.processes)
            completed_processes, timeline = scheduler.run_scheduler()
            avg_waiting_time, avg_turnaround_time, avg_response_time = scheduler.calculate_metrics(completed_processes)


            # Display Gantt Chart
            gantt_chart_window = tk.Toplevel(self.root)
            gantt_chart_window.title("Gantt Chart")
            canvas = tk.Canvas(gantt_chart_window, width=900, height=100)
            canvas.pack()
            time_unit = 50
            for i, pid in enumerate(timeline):
                x0 = i * time_unit
                x1 = (i + 1) * time_unit
                y0 = 20
                y1 = 80

                if pid != -1:
                    process = next(p for p in completed_processes if p.pid == pid)
                    canvas.create_rectangle(x0, y0, x1, y1, fill="sky blue")
                    canvas.create_text((x0 + x1) / 2, y0 + 10, text=f"P{process.pid}")
                    canvas.create_text((x0 + x1) / 2, y1 - 10, text=str(i))
                else:
                    canvas.create_rectangle(x0, y0, x1, y1, fill="lightgray")
                    canvas.create_text((x0 + x1) / 2, y0 + 10, text="IDLE")
                    canvas.create_text((x0 + x1) / 2, y1 - 10, text=str(i))

                    

            # Display results
            results_window = tk.Toplevel(self.root)
            results_window.title("Simulation Results")

            tk.Label(results_window, text=f"Average Waiting Time: {avg_waiting_time:.2f}").pack()
            tk.Label(results_window, text=f"Average Turnaround Time: {avg_turnaround_time:.2f}").pack()
            tk.Label(results_window, text=f"Average Response Time: {avg_response_time:.2f}").pack()

        except ValueError:
            tk.messagebox.showerror("Error", "Invalid input values")




            

if __name__ == "__main__":
    root = tk.Tk()
    app = PrioritySimulationApp(root)
    root.mainloop()
