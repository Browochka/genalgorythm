import random
import tkinter as tk
from tkinter import ttk
root = tk.Tk()
root.title("Genetic algorithm")
root.geometry("1200x800")
#4(x-5)**2 + (y - 6)**2
population=[]
mutrate=None
minimum=None
maximum=None
best_value=float('inf')
total_gens=0
best_solution=None
modified_mode= False



def set_generations(value):
    generations_entry.delete(0, tk.END)
    generations_entry.insert(0, str(value))




def modified_mode():
    global modified_mode
    modified_mode = not modified_mode
    modified_mode_btn.config(
        text="Модификация: Вкл" if modified_mode else "Модификация: Выкл"
    )
def evaluate_function(parents):
    x,y = parents
    return 4*(x-5)**2 + (y-6) ** 2
def mutation(parent):
    global mutrate
    for i in range(len(parent)):
        if random.randint(0,100) < mutrate:
            parent[i]=random.randint(minimum,maximum)
    return parent
def cross_parents(papa,mama):
    first=(papa[0]+mama[0])/2
    second=(papa[1]+mama[1])/2
    return [first,second]

def selection(generation):
    if modified_mode:
        generation.sort(key=lambda f: evaluate_function(f))
        besties = len(generation) * 0.1
        return generation[:int(besties)]
    else:
        return generation


def create_population(size):
    fpopulation=[]
    if minimum < maximum:
        fpopulation = [[random.randint(minimum, maximum) for i in range(2)] for i in range(size)]
    return fpopulation


def new_population(selected):
    new_generation=selected
    while len(new_generation) < len(population):
        parent1, parent2 = random.sample(selected, 2)
        child = cross_parents(parent1, parent2)
        new_generation.append(mutation(child))
    return new_generation


def genetic_algorihm():
    global total_gens,population,best_value,best_solution,minimum,maximum,mutrate
    num_chromosomes = int(chromosomes_entry.get())
    minimum=int(min_gene_entry.get())
    maximum=int(max_gene_entry.get())
    mutrate=int(mutation_entry.get())
    population=create_population(num_chromosomes)
    current_gen= int(generations_entry.get())
    for i in range(current_gen):
        selected=selection(population)
        population=new_population(selected)
        total_gens+=1
        for gen in population:
            value=evaluate_function(gen)
            if value < best_value:
                best_value=value
                best_solution=gen
            previous_generations_entry.delete(0, tk.END)
            previous_generations_entry.insert(0, str(total_gens))

        best_solution_text.delete(1.0, tk.END)
        if best_solution:
            best_solution_text.insert(tk.END, f"x1 = {best_solution[0]:.6f}\n")
            best_solution_text.insert(tk.END, f"x2 = {best_solution[1]:.6f}\n")

        function_value_entry.delete(0, tk.END)
        function_value_entry.insert(0, str(best_value))

        for item in tree.get_children():
            tree.delete(item)

        for i, chrom in enumerate(population):
            tree.insert("", "end", values=(i + 1, evaluate_function(chrom), *chrom))





left_frame = tk.Frame(root, padx=10, pady=10)
left_frame.pack(side="left", fill="y")

params_label = tk.LabelFrame(left_frame, text="Параметры", padx=10, pady=10)
params_label.pack(fill="x", pady=5)

params_label.grid_columnconfigure(0, weight=1)
params_label.grid_columnconfigure(1, weight=2)

tk.Label(params_label, text="Функция").grid(row=0, column=0, sticky="w")
func_combo = tk.Entry(params_label)
func_combo.grid(row=0, column=1, sticky="ew")
func_combo.insert(0, "4(x-5)**2 + (y - 6)**2")

tk.Label(params_label, text="Вероятность мутации, %:").grid(row=1, column=0, sticky="w")
mutation_entry = tk.Entry(params_label)
mutation_entry.grid(row=1, column=1, sticky="ew")
mutation_entry.insert(0, "25")

tk.Label(params_label, text="Количество хромосом:").grid(row=2, column=0, sticky="w")
chromosomes_entry = tk.Entry(params_label)
chromosomes_entry.grid(row=2, column=1, sticky="ew")
chromosomes_entry.insert(0, "100")

tk.Label(params_label, text="Минимальное значение гена:").grid(row=3, column=0, sticky="w")
min_gene_entry = tk.Entry(params_label)
min_gene_entry.grid(row=3, column=1, sticky="ew")
min_gene_entry.insert(0, "-100")

tk.Label(params_label, text="Максимальное значение гена:").grid(row=4, column=0, sticky="w")
max_gene_entry = tk.Entry(params_label)
max_gene_entry.grid(row=4, column=1, sticky="ew")
max_gene_entry.insert(0, "100")

control_label = tk.LabelFrame(left_frame, text="Управление", padx=10, pady=10)
control_label.pack(fill="x", pady=5)

tk.Label(control_label, text="Количество поколений:").grid(row=1, column=0, sticky="w", pady=0)
generations_entry = tk.Entry(control_label)
generations_entry.grid(row=1, column=1, sticky="ew", pady=0)
generations_entry.insert(0, "5")

tk.Label(control_label, text="Количество прошлых поколений:").grid(row=2, column=0, sticky="w", pady=0)
previous_generations_entry = tk.Entry(control_label)
previous_generations_entry.grid(row=2, column=1, sticky="ew", pady=0)
previous_generations_entry.insert(0, "0")


modified_mode_btn = tk.Button(control_label, text="Модификация: Выкл", command=modified_mode)
modified_mode_btn.grid(row=5, column=0, columnspan=2, sticky="ew", pady=5)


buttons_frame = tk.Frame(control_label)
buttons_frame.grid(row=3, column=0, columnspan=2, pady=5)
tk.Button(buttons_frame, text="1", width=13, command=lambda: set_generations(1)).pack(side="left", padx=0)
tk.Button(buttons_frame, text="10", width=13, command=lambda: set_generations(10)).pack(side="left", padx=0)
tk.Button(buttons_frame, text="100", width=13, command=lambda: set_generations(100)).pack(side="left", padx=0)
tk.Button(buttons_frame, text="1000", width=13, command=lambda: set_generations(1000)).pack(side="left", padx=0)


calculate_btn = tk.Button(control_label, text="Рассчитать", command=genetic_algorihm)
calculate_btn.grid(row=6, column=0, columnspan=2, sticky="ew", pady=5)

results_label = tk.LabelFrame(left_frame, text="Результаты", padx=10, pady=10)
results_label.pack(fill="x", pady=5)

results_label.grid_columnconfigure(0, weight=1)
results_label.grid_columnconfigure(1, weight=1)

best_solution_label = tk.Label(results_label, text="Лучшее решение:")
best_solution_label.grid(row=0, column=0, sticky="w", columnspan=2)

best_solution_text = tk.Text(results_label, width=30, height=5)
best_solution_text.grid(row=1, column=0, columnspan=2, sticky="ew", pady=5)

function_value_label = tk.Label(results_label, text="Значение функции:")
function_value_label.grid(row=2, column=0, sticky="w", padx=(0, 10), pady=5)

function_value_entry = tk.Entry(results_label)
function_value_entry.grid(row=2, column=1, sticky="ew", pady=5)

table_label_frame = tk.LabelFrame(root, text="Хромосомы данного поколения", padx=10, pady=10)
table_label_frame.pack(side="right", fill="both", expand=True, padx=(10, 0), pady=(0, 0))

columns = ("Номер", "Значение функции", "Ген 1", "Ген 2")
tree = ttk.Treeview(table_label_frame, columns=columns, show="headings")
tree.heading("Номер", text="Номер")
tree.heading("Значение функции", text="Значение функции")
tree.heading("Ген 1", text="Ген 1")
tree.heading("Ген 2", text="Ген 2")

tree.column("Номер", width=50)
tree.column("Значение функции", width=150)
tree.column("Ген 1", width=150)
tree.column("Ген 2", width=150)

tree.pack(fill="both", expand=True)

root.mainloop()