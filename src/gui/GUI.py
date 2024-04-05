import tkinter as tk
from tkinter.simpledialog import askstring
from tkinter.messagebox import showinfo

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import numpy as np  
import random 

from src.cromosome import Cromosome
from src.codification.coder import Coder
from src.selection.selector import Selector
from src.combination.combination import Combinator
from src.mutation.mutation import Mutator

class GUI:
    
     def __init__(
          self: object,
          population_size: int,
          generations: int,
          lower_bound: float,
          upper_bound: float,
          precision: int,
          f_arguments: list[float],
          combination_rate: float,
          mutation_rate: float
     ):
          self.population_size = population_size
          self.generations = 1
          self.initial_generations = generations
          self.lower_bound = lower_bound
          self.upper_bound = upper_bound
          self.precision = precision
          self.f_arguments = f_arguments
          self.f = lambda x: f_arguments[0] * (x ** 2) + f_arguments[1] * x + f_arguments[2]
          self.combination_rate = combination_rate
          self.mutation_rate = mutation_rate

          # initialize population
          values = [round(random.uniform(lower_bound, upper_bound), precision) for _ in range(population_size)]
          self.coder = Coder(lower_bound, upper_bound, precision)
          binaries = [self.coder.encoder.encode(x)for x in values]
          fitnesses = [self.f(x) for x in values]
          Cromosome.init(self.coder, self.f)
          self.population = [Cromosome(values[i], binaries[i], fitnesses[i]) for i in range(len(values))]

          self.selector = Selector(self.population)
          self.combinator = Combinator(self.population, combination_rate)
          self.mutator = Mutator(self.population, mutation_rate)

          # no printing
          self.coder.should_print = False
          self.selector.should_print = False
          self.combinator.should_print = False
          self.mutator.should_print = False

          self.best_value = max(self.population, key=lambda c: c.fitness).fitness


     def display_window(self):
          self.__init_window()
          self.__display_helper_buttons()
          self.__display_graph()
          self.__display_info_label()
          self.__display_population_listbox()
          self.__display_population_side_label()
          self.__display_menu()
          self.__open_settings_window()
     
     def run(self):
          self.root.mainloop()

     ##################################### MENU SETTINGS #####################################

     def __display_menu(self):
          self.menu = tk.Menu(self.root)
          self.root.config(menu=self.menu)

          self.settings_menu = tk.Menu(self.menu, tearoff=0)
          self.menu.add_cascade(label="Settings", menu=self.settings_menu)
          self.settings_menu.add_command(label="Change Settings", command=self.__open_settings_window)


     def __open_settings_window(self):

          # create a new Toplevel window
          self.settings_window = tk.Toplevel(self.root)
          self.settings_window.title("Settings")
          # set the settings window to be on top of the main window
          self.settings_window.attributes('-topmost', 'true')
          self.settings_window.grab_set()
          self.settings_window.update()

          settings_frame = tk.Frame(self.settings_window)
          settings_frame.pack(padx=10, pady=10)

          settings_labels = [
               "Population Size:", "Initial Generations:", "Lower Bound:", "Upper Bound:",
               "Precision:", "F Arguments:", "Combination Rate:", "Mutation Rate:"
          ]

          self.settings_entries = []
          for i, label_text in enumerate(settings_labels):
               label = tk.Label(settings_frame, text=label_text)
               label.grid(row=i, column=0, sticky='e', padx=5, pady=5)

               default_value = getattr(self, label_text.replace(":", "").replace(" ", "_").lower())
               entry = tk.Entry(settings_frame)
               entry.insert(tk.END, str(default_value))
               entry.grid(row=i, column=1, padx=5, pady=5)
               self.settings_entries.append(entry)

          continue_button = tk.Button(self.settings_window, text="Continue", command=self.__save_settings_and_update_ui)
          continue_button.pack(pady=10)


     def __save_settings_and_update_ui(self):
          try:
               population_size = int(self.settings_entries[0].get())
               initial_generations = int(self.settings_entries[1].get())
               lower_bound = float(self.settings_entries[2].get())
               upper_bound = float(self.settings_entries[3].get())
               precision = int(self.settings_entries[4].get())
               f_arguments = [float(arg) for arg in self.settings_entries[5].get().strip("[]").split(",")]
               combination_rate = float(self.settings_entries[6].get())
               mutation_rate = float(self.settings_entries[7].get())

               if population_size < 1  or\
               initial_generations < 2 or\
               lower_bound >= upper_bound or\
               precision < 1 or\
               f_arguments[0] >= 0 or\
               combination_rate < 0 or\
               combination_rate > 1 or\
               mutation_rate < 0 or\
               mutation_rate > 1:
                    raise Exception("Wrong init arguments")

               self.__init__(
                    population_size, 
                    initial_generations, 
                    lower_bound, 
                    upper_bound,
                    precision,
                    f_arguments,
                    combination_rate,
                    mutation_rate
               )

          except Exception as e:
               showinfo("Invalid settings", f"Please enter only valid numbers in the settings fields")
               return

          # updates
          self.__update_population_listbox()
          self.__update_info_label()
          self.__update_graph()
          self.__update_population_side_label()

          self.settings_window.destroy()

     ##################################### DISPLAY WIDGETS #####################################

     def __init_window(self):
          self.root = tk.Tk()
          self.root.geometry("1400x600")
          self.root.resizable(False, False)
          self.root.title("Maximum quadratic function")

          self.frame = tk.Frame(self.root)
          self.title_label = tk.Label(self.frame, text="Genetic Algorithm")
          self.title_label.config(font=("Courier", 32))
          self.title_label.pack()
          self.frame.pack()


     def __display_info_label(self):

          self.info_frame = tk.Frame(self.root, borderwidth=2, relief=tk.GROOVE, background='white')
          self.info_frame.pack(side=tk.TOP, anchor=tk.NW, padx=10, pady=10)

          labels_text = [
               f"Population Size: {self.population_size}",
               f"Generations: {self.initial_generations}",
               f"Bounds: [{self.lower_bound}, {self.upper_bound}]",
               f"Precision: {self.precision}",
               f"Function Arguments: {self.f_arguments[0]} * x^2 + {self.f_arguments[1]} * x + {self.f_arguments[2]}",
               f"Combination Rate: {self.combination_rate}",
               f"Mutation Rate: {self.mutation_rate}",
               f"Current Generation: {self.generations}/ {self.initial_generations}"
          ]

          for text in labels_text:
               label = tk.Label(self.info_frame, text=text, background='white', foreground='black', font=('Courier', 12))
               label.pack(anchor=tk.W)


     def __display_population_listbox(self):
          self.population_frame = tk.Frame(self.root, borderwidth=2, relief=tk.GROOVE, background='white')
          self.population_frame.pack(side=tk.TOP, anchor=tk.NW, padx=10, pady=10)
          
          header_text = f"{'ID': >3} | {'Value': >{self.precision + 3}} | {'Binary': >30} | {'Fitness': >20}"
          header_label = tk.Label(self.population_frame, text=header_text, background='white', foreground='black', font=('Courier', 12))
          header_label.pack(anchor=tk.W)

          separator = tk.Frame(self.population_frame, height=2, bd=1, relief=tk.SUNKEN)
          separator.pack(fill=tk.X, padx=5, pady=5)

          self.population_listbox = tk.Listbox(self.population_frame, width=80, height=20, font=('Courier', 12))
          scrollbar = tk.Scrollbar(self.population_frame, orient="vertical", command=self.population_listbox.yview)
          self.population_listbox.config(yscrollcommand=scrollbar.set)

          self.population_listbox.pack(side="left", fill="both", expand=True)
          scrollbar.pack(side="right", fill="y")

          for c in self.population:
               id_str = f"{c.id: >3}"
               value_str = f"{c.value:>{self.precision + 3}}"
               binary_str = f"{c.binary: >30}"
               fitness_str = f"{c.fitness: >20}"

               item_text = f"{id_str} | {value_str} | {binary_str} | {fitness_str}"
               self.population_listbox.insert(tk.END, item_text)


     def __display_population_side_label(self):
          best = max(self.population, key=lambda c: c.fitness)
          mean = sum([c.fitness for c in self.population]) / len(self.population)

          separator = tk.Frame(self.population_frame, height=2, bd=1, relief=tk.SUNKEN)
          separator.pack(fill=tk.X, padx=5, pady=5)

          self.best_label = tk.Label(self.population_frame, text=f"Best: {best.fitness}", background='white', foreground='black', font=('Courier', 12))
          self.best_label.pack(anchor=tk.W)

          self.mean_label = tk.Label(self.population_frame, text=f"Mean: {mean}", background='white', foreground='black', font=('Courier', 12))
          self.mean_label.pack(anchor=tk.W)

          separator = tk.Frame(self.population_frame, height=2, bd=1, relief=tk.SUNKEN)
          separator.pack(fill=tk.X, padx=5, pady=5)

          max_function_x = -1 * self.f_arguments[1] / (2 * self.f_arguments[0])
          max_function_y = self.f(max_function_x)
          
          self.max_function_y_label = tk.Label(self.population_frame, text=f"Max function value: {max_function_y}", background='white', foreground='black', font=('Courier', 12))
          self.max_function_y_label.pack(anchor=tk.W)

          self.max_function_x_label = tk.Label(self.population_frame, text=f"X value: {max_function_x}", background='white', foreground='black', font=('Courier', 12))
          self.max_function_x_label.pack(anchor=tk.W)

          separator = tk.Frame(self.population_frame, height=2, bd=1, relief=tk.SUNKEN)
          separator.pack(fill=tk.X, padx=5, pady=5)

          self.best_value_label = tk.Label(self.population_frame, text=f"Best value found: {self.best_value}", background='white', foreground='black', font=('Courier', 12))
          self.best_value_label.pack(anchor=tk.W)


     def __display_graph(self):
          self.graph_frame = tk.Frame(self.root)
          self.graph_frame.pack(side=tk.TOP, anchor=tk.NE, padx=10, pady=10)

          x = [c.value for c in self.population]
          y = [c.fitness for c in self.population]

          self.fig = plt.Figure(figsize=(5, 5))
          self.ax = self.fig.add_subplot(111)

          self.ax.scatter(x, y, color='yellow', edgecolors='black')

          self.ax.set_xlabel('X')
          self.ax.set_ylabel('Y')
          self.ax.set_title('Population')

          self.ax.grid(True)

          x_func = np.linspace(self.lower_bound, self.upper_bound, 100)
          y_func = self.f(x_func)
          self.ax.plot(x_func, y_func, color='blue')

          max_function_x = -1 * self.f_arguments[1] / (2 * self.f_arguments[0])
          max_function_y = self.f(max_function_x)
          self.ax.scatter(max_function_x, max_function_y, color='red')

          self.canvas = FigureCanvasTkAgg(self.fig, master=self.graph_frame)
          self.canvas.draw()
          self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

          self.graph_frame.place(relx=1, y=50, anchor=tk.NE, width=500, height=500)

     ##################################### HELPER BUTTONS #####################################

     def __display_helper_buttons(self):

          self.button_frame = tk.Frame(self.root)
          self.button_frame.pack(side=tk.TOP, anchor=tk.NW, padx=5, pady=5)

          self.next_button = tk.Button(self.button_frame, text="Next", command=self.__next_button_action)
          self.next_button.pack(side=tk.LEFT, padx=5, pady=5)

          self.auto_button = tk.Button(self.button_frame, text="Auto", command=self.__auto_button_action)
          self.auto_button.pack(side=tk.LEFT, padx=5, pady=5)

          self.reset_button = tk.Button(self.button_frame, text="Reset", command=self.__reset_button_action)
          self.reset_button.pack(side=tk.LEFT, padx=5, pady=5)

          self.go_to_generation_button = tk.Button(self.button_frame, text="Go to generation", command=self.__go_to_generation_button_action)
          self.go_to_generation_button.pack(side=tk.LEFT, padx=5, pady=5)


     def __go_to_generation_button_action(self):
          try:
               generation = askstring("Go to generation", "Enter the generation number:")
               generation = int(generation)
               if generation < self.generations or generation > self.initial_generations:
                    showinfo("Invalid generation", f"Generation must be between {self.generations} and {self.initial_generations}")
                    return
               
               self.next_button.config(state=tk.DISABLED)
               self.reset_button.config(state=tk.DISABLED)
               self.auto_button.config(state=tk.DISABLED)
               self.go_to_generation_button.config(text="Wait...", state=tk.DISABLED)

               while self.generations < generation and generation <= self.initial_generations:
                    self.generations += 1
                    self.__next_generation()
                    self.__update_info_label()
               
               self.__update_population_listbox()
               self.__update_graph()
               self.__update_population_side_label()
               self.__update_info_label()

               self.next_button.config(state=tk.NORMAL)
               self.reset_button.config(state=tk.NORMAL)
               self.auto_button.config(state=tk.NORMAL)
               self.go_to_generation_button.config(text="Go to generation", state=tk.NORMAL)
          except:
               showinfo("Invalid generation", "Generation must be a number")


     def __auto_button_action(self):
          self.shoud_continue_generations = True
          
          while self.generations < self.initial_generations and self.shoud_continue_generations:
               self.next_button.config(state=tk.DISABLED)
               self.reset_button.config(state=tk.DISABLED)
               self.auto_button.config(text="Stop", command=self.__stop_button_action)
               self.go_to_generation_button.config(state=tk.DISABLED)

               self.__next_generation()
               self.__update_population_listbox()
               self.__update_graph()
               self.__update_population_side_label()
               self.__update_info_label()

               self.root.update()
               self.root.after(10)
          
          self.next_button.config(state=tk.NORMAL)
          self.reset_button.config(state=tk.NORMAL)
          self.auto_button.config(text="Auto", command=self.__auto_button_action)
          self.go_to_generation_button.config(state=tk.NORMAL)


     def __stop_button_action(self):

          self.shoud_continue_generations = False

          self.next_button.config(state=tk.NORMAL)
          self.reset_button.config(state=tk.NORMAL)
          self.auto_button.config(text="Auto", command=self.__auto_button_action)


     def __reset_button_action(self):
          values = [round(random.uniform(self.lower_bound, self.upper_bound), self.precision) for _ in range(self.population_size)]
          binaries = [self.coder.encoder.encode(x)for x in values]
          fitnesses = [self.f(x) for x in values]
          self.population = [Cromosome(values[i], binaries[i], fitnesses[i]) for i in range(len(values))]
          self.generations = 1


          self.__update_population_listbox()
          self.__update_graph()
          self.__update_population_side_label()
          self.__update_info_label()


     def __next_button_action(self):
          self.__next_generation()

          self.__update_population_listbox()
          self.__update_graph()
          self.__update_population_side_label()
          self.__update_info_label()

     ##################################### UPDATES #####################################

     def __next_generation(self):

          if self.generations >= self.initial_generations:
               return

          self.population = self.selector.select()
          self.population = self.combinator.combine()
          self.population = self.mutator.mutate()

          self.generations += 1


     def __update_population_listbox(self):
          self.population_listbox.delete(0, tk.END)

          for c in self.population:
               id_str = f"{c.id: >3}"
               value_str = f"{c.value:>{self.precision + 3}}"
               binary_str = f"{c.binary: >30}"
               fitness_str = f"{c.fitness: >20}"

               item_text = f"{id_str} | {value_str} | {binary_str} | {fitness_str}"
               self.population_listbox.insert(tk.END, item_text)


     def __update_info_label(self):
          for widget in self.info_frame.winfo_children():
               widget.destroy()

          labels_text = [
               f"Population Size: {self.population_size}",
               f"Generations: {self.initial_generations}",
               f"Bounds: [{self.lower_bound}, {self.upper_bound}]",
               f"Precision: {self.precision}",
               f"Function Arguments: {self.f_arguments[0]} * x^2 + {self.f_arguments[1]} * x + {self.f_arguments[2]}",
               f"Combination Rate: {self.combination_rate}",
               f"Mutation Rate: {self.mutation_rate}",
               f"Current Generation: {self.generations}/ {self.initial_generations}"
          ]

          for text in labels_text:
               label = tk.Label(self.info_frame, text=text, background='white', foreground='black', font=('Courier', 12))
               label.pack(anchor=tk.W)


     def __update_graph(self):
          self.ax.clear()

          x = [c.value for c in self.population]
          y = [c.fitness for c in self.population]

          self.ax.scatter(x, y, color='yellow', edgecolors='black')
          self.ax.set_xlabel('X')
          self.ax.set_ylabel('Y')
          self.ax.set_title('Population')
          self.ax.grid(True)

          x = np.linspace(self.lower_bound, self.upper_bound, 100)
          y = self.f(x)
          self.ax.plot(x, y, color='blue')

          max_function_x = -1 * self.f_arguments[1] / (2 * self.f_arguments[0])
          max_function_y = self.f(max_function_x)
          self.ax.scatter(max_function_x, max_function_y, color='red')

          self.canvas.draw()


     def __update_population_side_label(self):
          best = max(self.population, key=lambda c: c.fitness)
          mean = sum([c.fitness for c in self.population]) / len(self.population)

          max_function_x = -1 * self.f_arguments[1] / (2 * self.f_arguments[0])
          max_function_y = self.f(max_function_x)

          self.best_value = max(self.best_value, best.fitness)
          
          self.best_label.config(text=f"Best: {best.fitness}")
          self.mean_label.config(text=f"Mean: {mean}")
          self.max_function_y_label.config(text=f"Max function value: {max_function_y}")
          self.max_function_x_label.config(text=f"X value: {max_function_x}")
          self.best_value_label.config(text=f"Best value found: {self.best_value}")

