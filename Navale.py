import tkinter as tk
from tkinter import messagebox
import random

# Constants
GRID_SIZE = 10
SHIP_SIZES = {"Porte-avions": 5, "Croiseur": 4, "Destroyer": 3, "Sous-marin": 2}
NUM_SHIPS = {"Porte-avions": 1, "Croiseur": 1, "Destroyer": 2, "Sous-marin": 2}

class BattleShipGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Jeu de la Bataille Navale")
        
        self.player_grid = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]
        self.computer_grid = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]
        self.player_ships = []
        self.computer_ships = []
        self.current_ship = None
        self.current_orientation = "H"
        
        self.create_widgets()
        self.reset_game()

    def create_widgets(self):
        # Create player grid
        self.player_buttons = [[None] * GRID_SIZE for _ in range(GRID_SIZE)]
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                btn = tk.Button(self.root, width=2, height=1, command=lambda i=i, j=j: self.player_place_ship(i, j))
                btn.grid(row=i, column=j)
                self.player_buttons[i][j] = btn
        
        # Create computer grid
        self.computer_buttons = [[None] * GRID_SIZE for _ in range(GRID_SIZE)]
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                btn = tk.Button(self.root, width=2, height=1, command=lambda i=i, j=j: self.player_shoot(i, j))
                btn.grid(row=i, column=j + GRID_SIZE + 1)
                self.computer_buttons[i][j] = btn
        
        # Control panel
        self.control_panel = tk.Frame(self.root)
        self.control_panel.grid(row=GRID_SIZE + 1, columnspan=GRID_SIZE * 2 + 1)
        
        self.new_game_button = tk.Button(self.control_panel, text="Nouvelle Partie", command=self.reset_game)
        self.new_game_button.pack(side=tk.LEFT)
        
        self.turn_label = tk.Label(self.control_panel, text="Tour: Joueur")
        self.turn_label.pack(side=tk.LEFT)
        
        self.orientation_button = tk.Button(self.control_panel, text="Orientation: Horizontal", command=self.toggle_orientation)
        self.orientation_button.pack(side=tk.LEFT)

    def reset_game(self):
        # Reset grids and ships
        self.player_grid = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]
        self.computer_grid = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]
        self.player_ships = []
        self.computer_ships = []
        self.current_ship = None
        
        # Reset buttons
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                self.player_buttons[i][j].config(bg="SystemButtonFace", state=tk.NORMAL)
                self.computer_buttons[i][j].config(bg="SystemButtonFace", state=tk.NORMAL)
        
        # Place computer ships
        self.place_computer_ships()
        
    def toggle_orientation(self):
        if self.current_orientation == "H":
            self.current_orientation = "V"
            self.orientation_button.config(text="Orientation: Vertical")
        else:
            self.current_orientation = "H"
            self.orientation_button.config(text="Orientation: Horizontal")
    
    def player_place_ship(self, row, col):
        if self.current_ship is None:
            self.current_ship = list(SHIP_SIZES.keys())[len(self.player_ships)]
        
        size = SHIP_SIZES[self.current_ship]
        if self.current_orientation == "H":
            if col + size > GRID_SIZE or any(self.player_grid[row][col + i] != 0 for i in range(size)):
                messagebox.showerror("Erreur", "Impossible de placer le navire ici.")
                return
            for i in range(size):
                self.player_grid[row][col + i] = 1
                self.player_buttons[row][col + i].config(bg="gray")
        else:
            if row + size > GRID_SIZE or any(self.player_grid[row + i][col] != 0 for i in range(size)):
                messagebox.showerror("Erreur", "Impossible de placer le navire ici.")
                return
            for i in range(size):
                self.player_grid[row + i][col] = 1
                self.player_buttons[row + i][col].config(bg="gray")
        
        self.player_ships.append(self.current_ship)
        if len(self.player_ships) == sum(NUM_SHIPS.values()):
            messagebox.showinfo("Placement terminé", "Tous les navires ont été placés.")
            for i in range(GRID_SIZE):
                for j in range(GRID_SIZE):
                    self.player_buttons[i][j].config(state=tk.DISABLED)
            self.turn_label.config(text="Tour: Joueur")
        else:
            self.current_ship = None
    
    def place_computer_ships(self):
        for ship, size in SHIP_SIZES.items():
            num_ships = NUM_SHIPS[ship]
            while num_ships > 0:
                orientation = random.choice(["H", "V"])
                if orientation == "H":
                    row = random.randint(0, GRID_SIZE - 1)
                    col = random.randint(0, GRID_SIZE - size)
                    if all(self.computer_grid[row][col + i] == 0 for i in range(size)):
                        for i in range(size):
                            self.computer_grid[row][col + i] = 1
                        num_ships -= 1
                else:
                    row = random.randint(0, GRID_SIZE - size)
                    col = random.randint(0, GRID_SIZE - 1)
                    if all(self.computer_grid[row + i][col] == 0 for i in range(size)):
                        for i in range(size):
                            self.computer_grid[row + i][col] = 1
                        num_ships -= 1
    
    def player_shoot(self, row, col):
        if self.computer_grid[row][col] == 1:
            self.computer_buttons[row][col].config(bg="red")
            messagebox.showinfo("Touché!", "Vous avez touché un navire!")
            self.computer_grid[row][col] = -1
            if not any(1 in row for row in self.computer_grid):
                messagebox.showinfo("Gagné!", "Vous avez coulé tous les navires de l'ordinateur!")
                self.reset_game()
        else:
            self.computer_buttons[row][col].config(bg="blue")
            messagebox.showinfo("Manqué!", "Vous avez manqué votre tir.")
            self.computer_turn()
    
    def computer_turn(self):
        while True:
            row = random.randint(0, GRID_SIZE - 1)
            col = random.randint(0, GRID_SIZE - 1)
            if self.player_grid[row][col] == 0:
                if any(1 in row for row in self.player_grid):
                    if random.choice([True, False]):
                        continue
                break
        
        if self.player_grid[row][col] == 1:
            messagebox.showinfo("Touché!", "L'ordinateur a touché votre navire!")
            self.player_buttons[row][col].config(bg="red")
            self.player_grid[row][col] = -1
            if not any(1 in row for row in self.player_grid):
                messagebox.showinfo("Perdu!", "Tous vos navires ont été coulés par l'ordinateur.")
                self.reset_game()
        else:
            messagebox.showinfo("Manqué!", "L'ordinateur a manqué son tir.")
            self.player_buttons[row][col].config(bg="blue")

if __name__ == "__main__":
    root = tk.Tk()
    game = BattleShipGame(root)
    root.mainloop()