import numpy as np
import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
from typing import List, Tuple, Optional

class MemorySimulator:
    def __init__(self, memory_size: int, block_size: int, sc_time: int, ch_time: int):
        if memory_size % block_size != 0:
            raise ValueError("Memory size must be a multiple of block size")

        self.memory_size = memory_size
        self.block_size = block_size
        self.num_blocks = memory_size // block_size
        self.memory = [None] * self.num_blocks
        self.sc_time = sc_time
        self.ch_time = ch_time
        self.total_time = 0
        self.gantt_data = []

    def compact_memory(self) -> int:
        new_memory = [slot for slot in self.memory if slot is not None]
        new_memory += [None] * (self.num_blocks - len(new_memory))
        compaction_time = self.sc_time if new_memory != self.memory else 0
        self.memory = new_memory
        return compaction_time

    def coalesce_holes(self) -> int:
        coalescing_needed = False
        consecutive_holes = 0

        for i in range(self.num_blocks - 1):
            if self.memory[i] is None and self.memory[i + 1] is None:
                consecutive_holes += 1
                coalescing_needed = True
            elif self.memory[i] is not None:
                consecutive_holes = 0

        return self.ch_time * consecutive_holes if coalescing_needed else 0

    def allocate_memory(self, processes: List[Tuple[int, int, int]]) -> Tuple[int, List]:
        for process_id, process_size, process_time in processes:
            blocks_needed = (process_size + self.block_size - 1) // self.block_size

            if blocks_needed > self.num_blocks:
                return None, None

            allocated = False
            for i in range(self.num_blocks - blocks_needed + 1):
                if all(slot is None for slot in self.memory[i:i + blocks_needed]):
                    self.memory[i:i + blocks_needed] = [process_id] * blocks_needed
                    self.total_time += process_time
                    self.gantt_data.append((process_id, self.total_time))
                    allocated = True
                    break

            if not allocated:
                compaction_time = self.compact_memory()
                self.total_time += compaction_time

                for i in range(self.num_blocks - blocks_needed + 1):
                    if all(slot is None for slot in self.memory[i:i + blocks_needed]):
                        self.memory[i:i + blocks_needed] = [process_id] * blocks_needed
                        self.total_time += process_time
                        self.gantt_data.append((process_id, self.total_time))
                        allocated = True
                        break

            coalescing_time = self.coalesce_holes()
            self.total_time += coalescing_time

            if not allocated:
                return None, None

        return self.total_time, self.gantt_data

def run_simulation():
    try:
        memory_size = int(memory_size_entry.get())
        block_size = int(block_size_entry.get())
        num_processes = int(num_processes_entry.get())
        sc_time = int(sc_time_entry.get())
        ch_time = int(ch_time_entry.get())

        if memory_size <= 0 or block_size <= 0 or num_processes <= 0 or sc_time < 0 or ch_time < 0:
            messagebox.showerror("Input Error", "Please enter positive values for all fields.")
            return

        if memory_size % block_size != 0:
            messagebox.showerror("Input Error", "Memory size must be a multiple of block size.")
            return

        processes = []
        for i in range(num_processes):
            process_size = int(process_size_entries[i].get())
            process_time = int(process_time_entries[i].get())
            if process_size <= 0 or process_time <= 0:
                messagebox.showerror("Input Error", f"Process {i + 1} must have positive size and time.")
                return
            processes.append((i + 1, process_size, process_time))

        simulator = MemorySimulator(memory_size, block_size, sc_time, ch_time)
        final_time, gantt_chart_data = simulator.allocate_memory(processes)

        if final_time is not None:
            result_text = f"Final Time: {final_time} units\n"
            result_text += f"Storage Compaction Time: {sc_time} units\n"
            result_text += f"Coalescing Holes Time: {ch_time} units\n"
            result_text += f"Block Size: {block_size} units"
            result_label.config(text=result_text)
            visualize_memory(simulator.memory, gantt_chart_data)
        else:
            result_label.config(text="Not all processes could be allocated.")

    except ValueError:
        messagebox.showerror("Input Error", "Please ensure all inputs are valid integers.")

def create_process_fields():
    try:
        num_processes = int(num_processes_entry.get())
        if num_processes <= 0:
            messagebox.showerror("Input Error", "Number of processes must be positive.")
            return

        for widget in process_frame.winfo_children():
            widget.destroy()

        global process_size_entries, process_time_entries
        process_size_entries = []
        process_time_entries = []

        tk.Label(process_frame, text="Process Size", font=("Helvetica", 12), fg="black", bg="gold").grid(row=0, column=1)
        tk.Label(process_frame, text="Process Time", font=("Helvetica", 12), fg="black", bg="gold").grid(row=0, column=2)

        for i in range(num_processes):
            tk.Label(process_frame, text=f"Process {i + 1}:", font=("Helvetica", 12), fg="black", bg="gold").grid(row=i + 1, column=0, padx=5, pady=2)

            size_entry = tk.Entry(process_frame, font=("Helvetica", 12), fg="black", bg="gold", width=10)
            size_entry.grid(row=i + 1, column=1, padx=5, pady=2)
            process_size_entries.append(size_entry)

            time_entry = tk.Entry(process_frame, font=("Helvetica", 12), fg="black", bg="gold", width=10)
            time_entry.grid(row=i + 1, column=2, padx=5, pady=2)
            process_time_entries.append(time_entry)

    except ValueError:
        messagebox.showerror("Input Error", "Please enter a valid number of processes.")

def visualize_memory(memory, gantt_chart_data):
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))

    unique_processes = sorted(set(filter(None, memory)))
    colors = plt.cm.Set3(np.linspace(0, 1, len(unique_processes)))
    color_map = {pid: color for pid, color in zip(unique_processes, colors)}
    color_map[None] = 'white'

    memory_colors = [color_map[slot] for slot in memory]
    ax1.bar(range(len(memory)), [1] * len(memory), color=memory_colors)
    ax1.set_title("Memory Map (Blocks)")
    ax1.set_xlabel("Block Number")
    ax1.set_ylabel("Status")

    legend_elements = [plt.Rectangle((0, 0), 1, 1, facecolor=color_map[pid], label=f'Process {pid}') for pid in unique_processes]
    legend_elements.append(plt.Rectangle((0, 0), 1, 1, facecolor='white', label='Free'))
    ax1.legend(handles=legend_elements, loc='upper right')

    if gantt_chart_data:
        processes, end_times = zip(*gantt_chart_data)
        start_times = [0] + list(end_times[:-1])
        durations = [end - start for start, end in zip(start_times, end_times)]

        ax2.barh(range(len(processes)), durations, left=start_times, color=[color_map[pid] for pid in processes])
        ax2.set_title("Gantt Chart")
        ax2.set_xlabel("Time Units")
        ax2.set_ylabel("Process ID")
        ax2.set_yticks(range(len(processes)))
        ax2.set_yticklabels([f'P{pid}' for pid in processes])

    plt.tight_layout()

    # Enable interactive mode to avoid blocking behavior
    plt.ion()
    plt.show()  # This will not block the program
    plt.draw()  # Redraw the plot to make sure it's updated



root = tk.Tk()
root.title("MemoPlusGold (First Fit)")
root.geometry("1000x600")
root.configure(bg="black")

# Main Frame with rounded corners
main_frame = tk.Frame(root, bg="black", bd=5, relief="solid", highlightthickness=2, highlightbackground="gold")
main_frame.pack(expand=True, fill="both", padx=20, pady=20)

# Create the two-column layout (process fields and result/output display)
left_frame = tk.Frame(main_frame, bg="black")
left_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

right_frame = tk.Frame(main_frame, bg="black")
right_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")

# Add input fields to the left frame
input_frame = tk.Frame(left_frame, bg="black")
input_frame.pack(pady=20)

tk.Label(input_frame, text="Memory Size:", font=("Helvetica", 14, "bold"), fg="gold", bg="black").grid(row=0, column=0, padx=10, pady=10, sticky="w")
memory_size_entry = tk.Entry(input_frame, font=("Helvetica", 14), fg="gold", bg="black", bd=2)
memory_size_entry.grid(row=0, column=1, padx=10, pady=10)

tk.Label(input_frame, text="Block Size:", font=("Helvetica", 14, "bold"), fg="gold", bg="black").grid(row=1, column=0, padx=10, pady=10, sticky="w")
block_size_entry = tk.Entry(input_frame, font=("Helvetica", 14), fg="gold", bg="black", bd=2)
block_size_entry.grid(row=1, column=1, padx=10, pady=10)

tk.Label(input_frame, text="Number of Processes:", font=("Helvetica", 14, "bold"), fg="gold", bg="black").grid(row=2, column=0, padx=10, pady=10, sticky="w")
num_processes_entry = tk.Entry(input_frame, font=("Helvetica", 14), fg="gold", bg="black", bd=2)
num_processes_entry.grid(row=2, column=1, padx=10, pady=10)

tk.Label(input_frame, text="Storage Compaction Time:", font=("Helvetica", 14, "bold"), fg="gold", bg="black").grid(row=3, column=0, padx=10, pady=10, sticky="w")
sc_time_entry = tk.Entry(input_frame, font=("Helvetica", 14), fg="gold", bg="black", bd=2)
sc_time_entry.grid(row=3, column=1, padx=10, pady=10)

tk.Label(input_frame, text="Coalescing Holes Time:", font=("Helvetica", 14, "bold"), fg="gold", bg="black").grid(row=4, column=0, padx=10, pady=10, sticky="w")
ch_time_entry = tk.Entry(input_frame, font=("Helvetica", 14), fg="gold", bg="black", bd=2)
ch_time_entry.grid(row=4, column=1, padx=10, pady=10)

# Frame for dynamic process fields
process_frame = tk.Frame(left_frame, bg="black")
process_frame.pack(fill="x", pady=20)

# Buttons for creating process fields and running the simulation
create_button = tk.Button(left_frame, text="Create Process Fields", font=("Helvetica", 14, "bold"), fg="black", bg="gold", command=create_process_fields)
create_button.pack(pady=10)

submit_button = tk.Button(left_frame, text="Run Simulation", font=("Helvetica", 14, "bold"), fg="black", bg="gold", command=run_simulation)
submit_button.pack(pady=10)

# Result Label in the right frame
result_label = tk.Label(right_frame, font=("Helvetica", 14), fg="gold", bg="black")
result_label.pack(pady=20)

root.mainloop()