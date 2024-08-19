import tkinter as tk
from tkinter import messagebox, font, Menu, ttk
import sv_ttk
from calc import calculate_avg, ranks


class SniperCalcApp:
    def __init__(self, root):
        self.root = root
        root.resizable(False, False)
        self.root.title("spinercalc")
        self.root.geometry("250x330")
        sv_ttk.set_theme("dark")

        self.entries = []
        self.input_ranks = []

        self.setup_menu()
        self.setup_widgets()
        self.bind_events()

    def open_window(self):
        # Create a new window
        new_window = tk.Toplevel(root)
        new_window.title("Small Window")
        
        # Set the size of the window (optional)
        new_window.geometry("300x300")
        
        # Add a label with text inside the window
        label = tk.Label(new_window, 
                         text="Format for the calculator is rank letter, rank number, points.  Such as 'g1 900'.\n\nUse the Quick Add option to add or remove 200 points from the entire party.", 
                         font=self.smaller_font, 
                         wraplength=275, 
                         anchor="w", 
                         justify="left")
        label.pack(pady=20)

    def setup_menu(self):
        menu_bar = Menu(self.root)
        self.root.config(menu=menu_bar)
        points_menu = Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Quick Add", menu=points_menu)
        points_menu.add_command(label="Add a win", command=self.add_fixed_number)
        points_menu.add_command(label="Add a loss", command=self.remove_fixed_number)
        theme_menu = Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Theme", menu=theme_menu)
        theme_menu.add_command(label="Light", command=self.toggle_light)
        theme_menu.add_command(label="Dark", command=self.toggle_dark)
        placeholder_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label=" ", menu=placeholder_menu)
        placeholder_menu.add_command(label=" ", state="disabled")
        help_menu = Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="Help", command=self.open_window)
        
    def setup_widgets(self):
        """Setup the main widgets."""
        self.reg_font = font.Font(family="Open Sans", size=12)
        self.bold_font = font.Font(family="Open Sans", size=12, weight="bold")
        self.smaller_font = font.Font(family="Open Sans", size=10, weight="bold")

        # Create a style for the separator
        style = ttk.Style()
        style.configure("Thick.TSeparator", thickness=10)  # Set the thickness here

        tk.Label(self.root, text="Enter ranks and points.", font=self.smaller_font).grid(row=0, column=0, columnspan=3, padx=1, pady=(15,10))

        # Button to add more input fields
        add_button = tk.Button(self.root, text="+", font=self.smaller_font, command=self.add_entry, width=3)
        add_button.grid(row=1, column=1, padx=(5, 0), pady=5)

        # Button to remove input fields
        self.remove_button = tk.Button(self.root, text="-", font=self.smaller_font, command=self.remove_entry, width=3)
        self.remove_button.grid(row=1, column=2, padx=(0, 5), pady=5)

        # Clear & calculate button position
        self.clear_button = tk.Button(self.root, text="Reset", font=self.smaller_font, command=self.clear_all)
        self.clear_button.grid(row=4, column=0, padx=(0, 10), pady=10)
        self.calculate_button = tk.Button(self.root, text="Calculate", font=self.smaller_font, command=self.calculate, width=9)
        self.calculate_button.grid(row=3, column=1, columnspan=2, padx=(1, 40), pady=5)

        # Separator & results position
        self.bot_separator = ttk.Separator(self.root, orient="horizontal", style="Thick.TSeparator")
        self.bot_separator.grid(row=5, column=0, columnspan=3, sticky="ew", padx=10, pady=10)       
        self.result_label = tk.Label(self.root, text="", font=self.bold_font, justify=tk.LEFT)
        self.result_label.grid(row=4, column=1, padx=10, pady=10)

        # Add initial input field
        self.add_entry()

        # Configure grid weights for resizing behavior
        for i in range(3):
            self.root.grid_columnconfigure(i, weight=1)

        self.update_widgets_position()

    def bind_events(self):
        """Bind events to widgets."""
        self.root.bind("<Return>", self.on_enter)

    def toggle_light(self):
        sv_ttk.set_theme("light")

    def toggle_dark(self):
        sv_ttk.set_theme("dark")

    def add_entry(self):
        if len(self.entries) >= 5:
            messagebox.showinfo("Limit reached!", "You can only add up to 5 ranks.")
            return  # Stop adding more entries if the limit is reached

        entry = tk.Entry(self.root, font=self.reg_font, width=14)
        entry.grid(row=len(self.entries) + 1, column=0, padx=(10, 1), pady=5)  # Unique row number
        self.entries.append(entry)

        self.update_widgets_position()

        if not self.remove_button.winfo_ismapped():
            self.remove_button.grid(row=1, column=2, padx=(0, 5), pady=5)

    def remove_entry(self):
        if len(self.entries) <= 1:
            messagebox.showinfo("Error", "You need at least 1 rank")
            return
        
        # Remove the last entry
        last_entry = self.entries.pop()  # Get the last entry and remove it from the list
        last_entry.grid_forget()  # Remove it from the grid

        self.update_widgets_position()
        
        if not self.entries:
            self.remove_button.grid_forget()

    def update_widgets_position(self):
        """Update the positions of calculate button, separator, and result label."""
        num_entries = len(self.entries)
        self.clear_button.grid(row=num_entries + 2, column=0, padx=(0, 10), pady=10)
        self.calculate_button.grid(row=num_entries + 2, column=1, columnspan=2, padx=(1, 40), pady=5)
        self.bot_separator.grid(row=num_entries + 3, column=0, columnspan=3, sticky="ew", padx=10, pady=10)
        self.result_label.grid(row=num_entries + 4, column=0, columnspan=3, padx=10, pady=10)

    def clear_all(self):
        """Clear all entry fields and the result label."""
        # Clear all entry fields
        for entry in self.entries:
            entry.delete(0, tk.END)
        
        # Clear the result label
        self.result_label.config(text="")
        
        # Optionally, remove all entries (if you want to reset to a fresh state)
        while len(self.entries) > 1:
            self.remove_entry()
            
    def on_enter(self, event=None):
        self.calculate()

    def calculate(self):
        self.input_ranks.clear()  # Clear previous input ranks

        for entry in self.entries:
            user_input = entry.get().strip()
            
            if not user_input:
                continue  # Skip empty entries
            
            try:
                # Split the input by spaces
                parts = user_input.split()
                
                # Check if the input has the correct number of parts
                if len(parts) < 2:
                    messagebox.showerror("Input Error", f"Invalid input format: {user_input.strip()}. Please use 'RankName Level Points' format or 'RankLevel Points'.")
                    return
                
                # Handle the case where rank and level are combined (e.g., G1)
                rank_and_level = parts[0]  # First part is rank (and possibly level)
                points_str = parts[1]  # Second part should be points
                
                # Check if rank_and_level is in the format G1 or G 1
                if len(rank_and_level) < 2 or not rank_and_level[:-1].isalpha() or not rank_and_level[-1].isdigit():
                    messagebox.showerror("Input Error", f"Invalid rank format: {rank_and_level.strip()}. Please use 'RankName Level Points' format or 'RankLevel Points'.")
                    return
                
                rank_name = rank_and_level[:-1].upper()  # Get the rank and convert to uppercase
                level = rank_and_level[-1]  # Get the last character as the level

                points = int(points_str)  # Convert points to integer

                # Check if rank and level are valid
                if rank_name in ranks and level in ranks[rank_name]:
                    base_points = ranks[rank_name][level][0]  # Get base points for that rank
                    total_points = base_points + points  # Add input points to base points
                    self.input_ranks.append((rank_name, total_points))  # Append to input_ranks
                else:
                    messagebox.showerror("Input Error", f"Invalid rank or level: {user_input.strip()}.")
            except (ValueError, IndexError):
                messagebox.showerror("Input Error", f"Invalid input format: {user_input.strip()}. Please use 'RankName Level Points' format or 'RankLevel Points'.")
        
        average_rank = calculate_avg(self.input_ranks)
        self.result_label.config(text=average_rank)

    def add_fixed_number(self):
        """Add 200 points to all entries"""
        fixed_points = 200
        for entry in self.entries:
            current_value = entry.get().strip()
            if current_value:
                try:
                    # Assuming the input format is 'RankLevel Points'
                    parts = current_value.split()
                    if len(parts) == 2:  # If format is 'RankLevel Points'
                        rank_level = parts[0].upper()
                        points = int(parts[1])


                        # Extract the rank and level
                        rank_name = rank_level[:-1]  # Everything except the last character is the rank
                        level = rank_level[-1]  # The last character is the level

                        if rank_name in ranks and level in ranks[rank_name]:
                            new_points = points + fixed_points

                            # Check if new points exceed the upper bound of the current level
                            if new_points > ranks[rank_name][level][1] - ranks[rank_name][level][0]:
                                new_points = new_points - 1000
                                # Promote to the next rank level
                                next_level = str(int(level) - 1)
                                if next_level == "0":  # If it's already at level 1, promote to the next rank
                                    if rank_name == "D":
                                        messagebox.showerror("Error", "We don't have calculations for Master")
                                    next_rank_name = list(ranks.keys())[list(ranks.keys()).index(rank_name) + 1]
                                    rank_name = next_rank_name
                                    next_level = "5"  # Reset to the highest level of the new rank
                                rank_level = rank_name + next_level
                            
                            entry.delete(0, tk.END)
                            entry.insert(0, f"{rank_level} {new_points}")
                        else:
                            messagebox.showerror("Rank Error", "Invalid rank or level.")
                    else:
                        messagebox.showerror("Format Error", "Input must be in 'RankLevel Points' format.")
                except ValueError:
                    messagebox.showerror("Value Error", "Invalid number format in entry.")
            else:
                continue  # Skip empty entries

    def remove_fixed_number(self):
        RANKS = ['D', 'P', 'G', 'S', 'B']
        LEVELS = ['1', '2', '3', '4', '5']
        
        """Remove 200 points from all entries."""
        fixed_points = 200
        for entry in self.entries:
            current_value = entry.get().strip()
            if current_value:
                try:
                    # Split the input into rank_level and points
                    parts = current_value.split()
                    if len(parts) == 2:  # If format is 'RankLevel Points'
                        rank_level = parts[0].upper()
                        points = int(parts[1])

                        # Extract rank and level
                        level_index = next((i for i, c in enumerate(rank_level) if c.isdigit()), len(rank_level))
                        rank_name = rank_level[:level_index].upper()  # Rank is all characters before digits
                        level = rank_level[level_index:]  # Level is digits part

                        # Validate rank and level
                        if rank_name in RANKS and level in LEVELS:
                            # Deduct points
                            new_points = points - fixed_points

                            # Roll over if needed
                            while new_points < 0:
                                # Move to the previous level
                                if level != LEVELS[-1]:
                                    # Decrease level
                                    level_index = LEVELS.index(level)
                                    level = LEVELS[level_index + 1]
                                    new_points += 1000  # Adjust based on your level points increment
                                else:
                                    # Move to the previous rank
                                    if rank_name != RANKS[-1]:
                                        rank_index = RANKS.index(rank_name)
                                        rank_name = RANKS[rank_index + 1]
                                        level = LEVELS[0]  # Reset to the highest level of the new rank
                                        new_points += 1000  # Adjust based on your rank points increment
                                    else:
                                        new_points = 0  # If at the lowest rank and level, set points to 0
                                        break

                            # Ensure points are non-negative
                            new_points = max(new_points, 0)

                            # Update the entry with the new rank, level, and points
                            rank_level = rank_name + level
                            entry.delete(0, tk.END)
                            entry.insert(0, f"{rank_level} {new_points}")
                        else:
                            messagebox.showerror("Rank Error", f"Invalid rank or level: {rank_name} {level}")
                    else:
                        messagebox.showerror("Format Error", "Input must be in 'RankLevel Points' format.")
                except ValueError:
                    messagebox.showerror("Value Error", "Invalid number format in entry.")
            else:
                continue  # Skip empty entries

if __name__ == "__main__":
    root = tk.Tk()
    app = SniperCalcApp(root)
    root.mainloop()