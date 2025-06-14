"""
Learning Quest - Code in Place Final Project

A comprehensive educational game that demonstrates Python programming concepts
learned in Stanford's Code in Place course.

Author: Code in Place Student
Date: June 2025

This project demonstrates:
- Object-oriented programming with classes
- Graphics programming with tkinter
- Game logic and state management
- User input and event handling
- Randomization for game elements
- Data structures (lists, dictionaries)
- File I/O for saving scores
- Interactive educational content
"""

import tkinter as tk
from tkinter import messagebox, simpledialog
import random
import time

class LearningQuestGame:
    """
    Learning Quest: An educational game where players answer questions to advance
    through different levels while collecting points and unlocking achievements.

    This game demonstrates various concepts from Code in Place:
    - Object-oriented programming (classes)
    - Graphics with tkinter
    - Randomization
    - Lists and dictionaries
    - User input and interaction
    - Game logic and state management
    """

    def __init__(self, root):
        """Initialize the game with the main window and setup"""
        self.root = root
        self.root.title("Learning Quest - Code in Place Final Project")
        self.root.geometry("800x600")
        self.root.resizable(False, False)

        # Game state variables
        self.score = 0
        self.level = 1
        self.time_remaining = 60
        self.game_active = False
        self.character_position = [400, 500]
        self.achievements = []
        self.obstacles = []
        self.collectibles = []

        # Store questions in a dictionary where the key is the difficulty level
        self.questions = {
            1: [
                {"question": "What does the 'print' function do in Python?", 
                 "options": ["Displays text on the screen", "Prints to a printer", "Creates a PDF file", "Takes a screenshot"], 
                 "answer": 0},
                {"question": "Which symbol is used for comments in Python?", 
                 "options": ["//", "/*", "#", "<!--"], 
                 "answer": 2},
                {"question": "What is the correct way to create a variable named 'age' with the value 25?", 
                 "options": ["variable age = 25", "age = 25", "int age = 25", "age := 25"], 
                 "answer": 1},
                {"question": "What type of data can a Python list contain?", 
                 "options": ["Only numbers", "Only strings", "Any type of data", "Only booleans"], 
                 "answer": 2},
                {"question": "How do you get user input in Python?", 
                 "options": ["get()", "input()", "read()", "scan()"], 
                 "answer": 1},
            ],
            2: [
                {"question": "What does the 'len()' function return?", 
                 "options": ["The longest item in a list", "The number of items in a list", "The memory size of an object", "The length of a string in pixels"], 
                 "answer": 1},
                {"question": "How do you create a list in Python?", 
                 "options": ["list = (1, 2, 3)", "list = [1, 2, 3]", "list = {1, 2, 3}", "list = <1, 2, 3>"], 
                 "answer": 1},
                {"question": "What is the correct way to start a for loop in Python?", 
                 "options": ["for i in range(10):", "for(i=0; i<10; i++)", "for i = 1 to 10", "foreach i in 10"], 
                 "answer": 0},
                {"question": "How do you add an item to the end of a list?", 
                 "options": ["list.add(item)", "list.append(item)", "list.insert(item)", "list.push(item)"], 
                 "answer": 1},
                {"question": "What does 'random.randint(1, 10)' return?", 
                 "options": ["A random decimal between 1 and 10", "A random integer between 1 and 9", "A random integer between 1 and 10", "Always returns 5"], 
                 "answer": 2},
            ],
            3: [
                {"question": "What does the 'append()' method do to a list?", 
                 "options": ["Removes an item", "Adds an item to the end", "Sorts the list", "Reverses the list"], 
                 "answer": 1},
                {"question": "How do you open a file named 'data.txt' for reading in Python?", 
                 "options": ["file = open('data.txt', 'r')", "file = open('data.txt', 'w')", "file = read('data.txt')", "file = load('data.txt')"], 
                 "answer": 0},
                {"question": "Which of these is NOT a valid way to create a dictionary?", 
                 "options": ["dict = {}", "dict = dict()", "dict = {1, 2, 3}", "dict = {'a': 1, 'b': 2}"], 
                 "answer": 2},
                {"question": "What is the purpose of the '__init__' method in a Python class?", 
                 "options": ["To delete the object", "To initialize object attributes", "To print object information", "To copy the object"], 
                 "answer": 1},
                {"question": "How do you handle exceptions in Python?", 
                 "options": ["try/catch", "try/except", "handle/error", "check/fail"], 
                 "answer": 1},
            ]
        }

        # Create and place UI elements
        self.create_widgets()

        # Bind keyboard events for character movement
        self.root.bind("<Left>", self.move_left)
        self.root.bind("<Right>", self.move_right)
        self.root.bind("<Up>", self.move_up)
        self.root.bind("<Down>", self.move_down)
        self.root.focus_set()  # Make sure window has focus for key events

    def create_widgets(self):
        """Set up all the UI elements for the game"""
        # Create a frame for the header
        header_frame = tk.Frame(self.root, bg="#3498db", height=50)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)

        # Score and level labels
        self.score_label = tk.Label(header_frame, text="Score: 0", font=("Arial", 14, "bold"), 
                                   bg="#3498db", fg="white")
        self.score_label.pack(side=tk.LEFT, padx=20, pady=10)

        self.level_label = tk.Label(header_frame, text="Level: 1", font=("Arial", 14, "bold"), 
                                   bg="#3498db", fg="white")
        self.level_label.pack(side=tk.LEFT, padx=20, pady=10)

        self.time_label = tk.Label(header_frame, text="Time: 60", font=("Arial", 14, "bold"), 
                                  bg="#3498db", fg="white")
        self.time_label.pack(side=tk.RIGHT, padx=20, pady=10)

        # Create the game canvas
        self.canvas = tk.Canvas(self.root, bg="#ecf0f1", width=800, height=450)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Create a frame for the bottom controls
        control_frame = tk.Frame(self.root, bg="#2c3e50", height=50)
        control_frame.pack(fill=tk.X)
        control_frame.pack_propagate(False)

        # Start button
        self.start_button = tk.Button(control_frame, text="🎮 Start Game", font=("Arial", 12, "bold"), 
                                      command=self.start_game, bg="#2ecc71", fg="white",
                                      padx=20, pady=5)
        self.start_button.pack(side=tk.LEFT, padx=20, pady=10)

        # Question button
        self.question_button = tk.Button(control_frame, text="🧠 Answer Question", font=("Arial", 12, "bold"), 
                                        command=self.show_question, state=tk.DISABLED, 
                                        bg="#e74c3c", fg="white", padx=20, pady=5)
        self.question_button.pack(side=tk.LEFT, padx=20, pady=10)

        # High scores button
        self.scores_button = tk.Button(control_frame, text="🏆 High Scores", font=("Arial", 12, "bold"), 
                                      command=self.show_high_scores, bg="#9b59b6", fg="white",
                                      padx=20, pady=5)
        self.scores_button.pack(side=tk.LEFT, padx=20, pady=10)

        # Help button
        self.help_button = tk.Button(control_frame, text="❓ Help", font=("Arial", 12, "bold"), 
                                    command=self.show_help, bg="#f39c12", fg="white",
                                    padx=20, pady=5)
        self.help_button.pack(side=tk.RIGHT, padx=20, pady=10)

        # Welcome screen
        self.show_welcome_screen()

    def show_welcome_screen(self):
        """Display the welcome screen"""
        self.canvas.delete("all")

        # Title
        self.canvas.create_text(400, 100, text="🎓 Learning Quest", 
                              font=("Arial", 32, "bold"), fill="#2c3e50")

        # Subtitle
        self.canvas.create_text(400, 150, text="Code in Place Final Project", 
                              font=("Arial", 18), fill="#7f8c8d")

        # Instructions
        instructions = [
            "Welcome to your Python learning adventure!",
            "",
            "🎯 How to Play:",
            "• Use arrow keys to move your character",
            "• Collect 🟡 yellow circles for +10 points",
            "• Avoid 🟥 red squares (they cost you 5 points)",
            "• Answer questions to earn +20 points",
            "• Reach the target score to advance levels",
            "",
            "🏆 Level Goals:",
            "Level 1: Reach 50 points to advance",
            "Level 2: Reach 100 points to advance",
            "Level 3: Reach 150+ points to win!",
            "",
            "Press 'Start Game' when you're ready!"
        ]

        y_position = 200
        for instruction in instructions:
            self.canvas.create_text(400, y_position, text=instruction, 
                                  font=("Arial", 12), fill="#2c3e50")
            y_position += 20

    def start_game(self):
        """Start or restart the game"""
        # Reset game state
        self.score = 0
        self.level = 1
        self.time_remaining = 60
        self.game_active = True
        self.character_position = [400, 400]
        self.achievements = []
        self.obstacles = []
        self.collectibles = []

        # Update UI
        self.score_label.config(text=f"Score: {self.score}")
        self.level_label.config(text=f"Level: {self.level}")
        self.time_label.config(text=f"Time: {self.time_remaining}")

        # Enable question button
        self.question_button.config(state=tk.NORMAL)

        # Clear canvas and draw game elements
        self.canvas.delete("all")
        self.draw_game()

        # Start the timer
        self.update_timer()

        # Generate initial obstacles and collectibles
        self.generate_obstacles()
        self.generate_collectibles()

    def draw_game(self):
        """Draw all game elements on the canvas"""
        # Clear canvas
        self.canvas.delete("all")

        # Draw background based on level
        level_colors = {
            1: "#e8f4fd",  # Light blue for level 1
            2: "#e8f5e8",  # Light green for level 2
            3: "#fde8e8"   # Light red for level 3
        }
        bg_color = level_colors.get(self.level, "#ecf0f1")
        self.canvas.config(bg=bg_color)

        # Draw level indicator
        self.canvas.create_text(400, 30, text=f"🌟 Level {self.level} 🌟", 
                              font=("Arial", 18, "bold"), fill="#2c3e50")

        # Draw obstacles
        for obstacle in self.obstacles:
            # Red squares for obstacles
            self.canvas.create_rectangle(obstacle[0], obstacle[1], 
                                       obstacle[0] + 40, obstacle[1] + 40, 
                                       fill="#e74c3c", outline="#c0392b", width=2)
            # Add emoji-style decoration
            self.canvas.create_text(obstacle[0] + 20, obstacle[1] + 20, 
                                  text="⚠️", font=("Arial", 16))

        # Draw collectibles
        for collectible in self.collectibles:
            # Yellow circles for collectibles
            self.canvas.create_oval(collectible[0], collectible[1], 
                                  collectible[0] + 30, collectible[1] + 30, 
                                  fill="#f1c40f", outline="#f39c12", width=2)
            # Add sparkle effect
            self.canvas.create_text(collectible[0] + 15, collectible[1] + 15, 
                                  text="✨", font=("Arial", 12))

        # Draw character
        x, y = self.character_position
        # Main character body
        self.canvas.create_oval(x - 20, y - 20, x + 20, y + 20, 
                              fill="#3498db", outline="#2980b9", width=3)
        # Character face
        self.canvas.create_text(x, y, text="😊", font=("Arial", 16))

        # Draw goal text
        target_score = self.level * 50
        goal_text = f"Goal: Reach {target_score} points to advance!"
        if self.level == 3:
            goal_text = "Goal: Reach 150+ points to win the game!"

        self.canvas.create_text(400, 420, text=goal_text, 
                              font=("Arial", 14, "bold"), fill="#27ae60")

        # Draw progress bar
        progress_width = 300
        progress_height = 20
        progress_x = 250
        progress_y = 60

        # Background of progress bar
        self.canvas.create_rectangle(progress_x, progress_y, 
                                   progress_x + progress_width, progress_y + progress_height,
                                   fill="#bdc3c7", outline="#95a5a6")

        # Fill of progress bar
        progress_percent = min(self.score / target_score, 1.0)
        fill_width = progress_width * progress_percent
        if fill_width > 0:
            self.canvas.create_rectangle(progress_x, progress_y, 
                                       progress_x + fill_width, progress_y + progress_height,
                                       fill="#2ecc71", outline="")

        # Progress text
        self.canvas.create_text(400, 70, text=f"{self.score}/{target_score}", 
                              font=("Arial", 10, "bold"), fill="white")

    def generate_obstacles(self):
        """Generate random obstacles based on the current level"""
        self.obstacles = []
        # More obstacles as level increases
        num_obstacles = 2 + self.level * 2

        for _ in range(num_obstacles):
            x = random.randint(50, 710)
            y = random.randint(100, 350)
            # Make sure obstacles don't spawn too close to character start
            if abs(x - 400) > 60 or abs(y - 400) > 60:
                self.obstacles.append([x, y])

        self.draw_game()

    def generate_collectibles(self):
        """Generate random collectibles (bonus points)"""
        self.collectibles = []
        # Consistent number of collectibles
        num_collectibles = 6

        for _ in range(num_collectibles):
            x = random.randint(50, 720)
            y = random.randint(100, 350)
            # Make sure collectibles don't spawn inside obstacles
            collision = False
            for obstacle in self.obstacles:
                if (abs(x - obstacle[0]) < 50 and abs(y - obstacle[1]) < 50):
                    collision = True
                    break

            if not collision:
                self.collectibles.append([x, y])

        self.draw_game()

    def move_left(self, event):
        """Move character left"""
        if not self.game_active:
            return

        self.character_position[0] = max(20, self.character_position[0] - 25)
        self.check_collisions()
        self.draw_game()

    def move_right(self, event):
        """Move character right"""
        if not self.game_active:
            return

        self.character_position[0] = min(780, self.character_position[0] + 25)
        self.check_collisions()
        self.draw_game()

    def move_up(self, event):
        """Move character up"""
        if not self.game_active:
            return

        self.character_position[1] = max(90, self.character_position[1] - 25)
        self.check_collisions()
        self.draw_game()

    def move_down(self, event):
        """Move character down"""
        if not self.game_active:
            return

        self.character_position[1] = min(400, self.character_position[1] + 25)
        self.check_collisions()
        self.draw_game()

    def check_collisions(self):
        """Check if character collides with obstacles or collectibles"""
        x, y = self.character_position

        # Check obstacle collisions
        for obstacle in self.obstacles[:]:
            if (abs(x - (obstacle[0] + 20)) < 35 and 
                abs(y - (obstacle[1] + 20)) < 35):
                # Collision with obstacle - lose points
                self.score = max(0, self.score - 5)
                self.score_label.config(text=f"Score: {self.score}")
                self.obstacles.remove(obstacle)
                messagebox.showwarning("Oops! 💥", "You hit an obstacle! -5 points.")
                break

        # Check collectible collisions
        for collectible in self.collectibles[:]:
            if (abs(x - (collectible[0] + 15)) < 30 and 
                abs(y - (collectible[1] + 15)) < 30):
                # Collected a point - gain points
                self.score += 10
                self.score_label.config(text=f"Score: {self.score}")
                self.collectibles.remove(collectible)

                # Generate new collectible to replace the collected one
                self.generate_new_collectible()
                break

    def generate_new_collectible(self):
        """Generate a single new collectible"""
        for _ in range(10):  # Try up to 10 times to find a good position
            x = random.randint(50, 720)
            y = random.randint(100, 350)

            # Check if position is clear of obstacles and character
            collision = False
            for obstacle in self.obstacles:
                if (abs(x - obstacle[0]) < 50 and abs(y - obstacle[1]) < 50):
                    collision = True
                    break

            if not collision and abs(x - self.character_position[0]) > 40:
                self.collectibles.append([x, y])
                break

        self.draw_game()

    def show_question(self):
        """Display a random question based on the current level"""
        if not self.game_active:
            return

        # Get a random question for the current level
        level_questions = self.questions.get(self.level, self.questions[1])
        question_data = random.choice(level_questions)

        # Create a custom dialog for the question
        question_window = tk.Toplevel(self.root)
        question_window.title(f"🧠 Level {self.level} Question")
        question_window.geometry("600x400")
        question_window.resizable(False, False)
        question_window.configure(bg="#ecf0f1")

        # Center the window
        question_window.transient(self.root)
        question_window.grab_set()

        # Question header
        header_frame = tk.Frame(question_window, bg="#3498db", height=60)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)

        header_label = tk.Label(header_frame, text=f"🎯 Level {self.level} Challenge", 
                               font=("Arial", 18, "bold"), bg="#3498db", fg="white")
        header_label.pack(pady=15)

        # Question label
        question_frame = tk.Frame(question_window, bg="#ecf0f1")
        question_frame.pack(fill=tk.X, padx=20, pady=20)

        question_label = tk.Label(question_frame, text=question_data["question"], 
                                wraplength=550, font=("Arial", 16), bg="#ecf0f1",
                                justify=tk.CENTER)
        question_label.pack()

        # Answer frame
        answer_frame = tk.Frame(question_window, bg="#ecf0f1")
        answer_frame.pack(pady=10, fill=tk.X, padx=40)

        # Variable to store the selected answer
        selected_answer = tk.IntVar()
        selected_answer.set(-1)  # Default: no selection

        # Create radio buttons for options
        for i, option in enumerate(question_data["options"]):
            radio_frame = tk.Frame(answer_frame, bg="#ffffff", relief=tk.RAISED, bd=1)
            radio_frame.pack(fill=tk.X, pady=5)

            radio = tk.Radiobutton(radio_frame, text=f"{chr(65+i)}. {option}", 
                                 variable=selected_answer, value=i, 
                                 font=("Arial", 12), bg="#ffffff",
                                 padx=10, pady=8, anchor=tk.W)
            radio.pack(fill=tk.X)

        # Function to check the answer
        def check_answer():
            if selected_answer.get() == -1:
                messagebox.showwarning("No Selection", "Please select an answer!")
                return

            if selected_answer.get() == question_data["answer"]:
                # Correct answer
                self.score += 20
                self.score_label.config(text=f"Score: {self.score}")
                messagebox.showinfo("Correct! 🎉", "That's right! +20 points\n\nGreat job!")

                # Check if score is high enough to advance to next level
                if self.score >= self.level * 50:
                    self.advance_level()
            else:
                # Incorrect answer
                self.score = max(0, self.score - 10)
                self.score_label.config(text=f"Score: {self.score}")
                correct_option = question_data["options"][question_data["answer"]]
                messagebox.showinfo("Incorrect 😔", 
                                  f"Sorry, that's wrong.\n\nThe correct answer was:\n{correct_option}\n\n-10 points")

            question_window.destroy()

        def skip_question():
            """Allow player to skip question without penalty"""
            result = messagebox.askyesno("Skip Question", 
                                       "Are you sure you want to skip this question?\nNo points will be gained or lost.")
            if result:
                question_window.destroy()

        # Button frame
        button_frame = tk.Frame(question_window, bg="#ecf0f1")
        button_frame.pack(pady=20)

        # Submit button
        submit_button = tk.Button(button_frame, text="✅ Submit Answer", 
                                command=check_answer, font=("Arial", 14, "bold"),
                                bg="#2ecc71", fg="white", padx=20, pady=10)
        submit_button.pack(side=tk.LEFT, padx=10)

        # Skip button
        skip_button = tk.Button(button_frame, text="⏭️ Skip", 
                              command=skip_question, font=("Arial", 14, "bold"),
                              bg="#95a5a6", fg="white", padx=20, pady=10)
        skip_button.pack(side=tk.LEFT, padx=10)

    def advance_level(self):
        """Advance to the next level"""
        if self.level < 3:
            self.level += 1
            self.level_label.config(text=f"Level: {self.level}")

            # Bonus time for advancing
            self.time_remaining += 30
            self.time_label.config(text=f"Time: {self.time_remaining}")

            # Generate new obstacles and collectibles
            self.generate_obstacles()
            self.generate_collectibles()

            messagebox.showinfo("Level Up! 🎊", 
                              f"Congratulations! You've advanced to Level {self.level}!\n\n" +
                              f"🎯 New Goal: Reach {self.level * 50} points\n" +
                              f"⏰ +30 seconds added to your timer!")

            # Achievement for reaching a new level
            achievement = f"Reached Level {self.level}"
            if achievement not in self.achievements:
                self.achievements.append(achievement)
        else:
            # Player has completed all levels
            self.game_active = False
            self.question_button.config(state=tk.DISABLED)

            messagebox.showinfo("🏆 VICTORY! 🏆", 
                              f"Amazing! You've completed all levels!\n\n" +
                              f"Final Score: {self.score} points\n" +
                              f"Time Remaining: {self.time_remaining} seconds\n\n" +
                              f"You're a Python learning champion!")

            # Ask for player name to save score
            player_name = simpledialog.askstring("🏆 High Score", 
                                                "Enter your name for the high score:")
            if player_name:
                self.save_high_score(player_name, self.score)

    def update_timer(self):
        """Update the game timer"""
        if self.game_active and self.time_remaining > 0:
            self.time_remaining -= 1
            self.time_label.config(text=f"Time: {self.time_remaining}")

            # Change color when time is running low
            if self.time_remaining <= 10:
                self.time_label.config(fg="#e74c3c")
            elif self.time_remaining <= 30:
                self.time_label.config(fg="#f39c12")
            else:
                self.time_label.config(fg="white")

            self.root.after(1000, self.update_timer)
        elif self.game_active:
            # Time's up
            self.game_active = False
            self.question_button.config(state=tk.DISABLED)
            messagebox.showinfo("⏰ Time's Up!", 
                              f"Game over! You reached Level {self.level} with {self.score} points.\n\n" +
                              f"Thanks for playing Learning Quest!")

            # Ask for player name to save score
            player_name = simpledialog.askstring("Game Over", 
                                                "Enter your name for the high score:")
            if player_name:
                self.save_high_score(player_name, self.score)

    def save_high_score(self, name, score):
        """Save the player's score to a file"""
        try:
            timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
            score_entry = f"{name},{score},{self.level},{timestamp}\n"

            with open("learning_quest_scores.txt", "a") as file:
                file.write(score_entry)

            messagebox.showinfo("💾 Score Saved", 
                              f"Your score has been saved!\n\n" +
                              f"Player: {name}\n" +
                              f"Score: {score}\n" +
                              f"Level: {self.level}")
        except Exception as e:
            messagebox.showerror("Error", f"Could not save score: {str(e)}")

    def show_high_scores(self):
        """Display the high scores"""
        try:
            scores = []
            with open("learning_quest_scores.txt", "r") as file:
                for line in file:
                    if line.strip():
                        parts = line.strip().split(",")
                        if len(parts) >= 4:
                            name, score, level, timestamp = parts[0], int(parts[1]), int(parts[2]), parts[3]
                            scores.append((name, score, level, timestamp))

            # Sort by score (descending)
            scores.sort(key=lambda x: x[1], reverse=True)

            # Create high scores window
            scores_window = tk.Toplevel(self.root)
            scores_window.title("🏆 High Scores")
            scores_window.geometry("500x400")
            scores_window.configure(bg="#ecf0f1")

            # Header
            header = tk.Label(scores_window, text="🏆 Learning Quest High Scores", 
                            font=("Arial", 18, "bold"), bg="#3498db", fg="white")
            header.pack(fill=tk.X, pady=(0, 20))

            # Scores frame with scrollbar
            scores_frame = tk.Frame(scores_window, bg="#ecf0f1")
            scores_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

            if scores:
                # Display top 10 scores
                for i, (name, score, level, timestamp) in enumerate(scores[:10]):
                    rank = i + 1
                    medal = "🥇" if rank == 1 else "🥈" if rank == 2 else "🥉" if rank == 3 else f"{rank}."

                    score_text = f"{medal} {name} - {score} pts (Level {level})"

                    score_label = tk.Label(scores_frame, text=score_text, 
                                         font=("Arial", 12), bg="#ffffff", 
                                         relief=tk.RAISED, bd=1, pady=5)
                    score_label.pack(fill=tk.X, pady=2)
            else:
                no_scores_label = tk.Label(scores_frame, text="No high scores yet!\nBe the first to play!", 
                                         font=("Arial", 14), bg="#ecf0f1")
                no_scores_label.pack(pady=50)

        except FileNotFoundError:
            messagebox.showinfo("No Scores", "No high scores found yet!\nPlay the game to set the first record!")
        except Exception as e:
            messagebox.showerror("Error", f"Could not load high scores: {str(e)}")

    def show_help(self):
        """Display help information"""
        help_window = tk.Toplevel(self.root)
        help_window.title("❓ Help - Learning Quest")
        help_window.geometry("600x500")
        help_window.configure(bg="#ecf0f1")

        # Header
        header = tk.Label(help_window, text="❓ How to Play Learning Quest", 
                        font=("Arial", 18, "bold"), bg="#3498db", fg="white")
        header.pack(fill=tk.X, pady=(0, 20))

        # Help content frame
        content_frame = tk.Frame(help_window, bg="#ffffff", relief=tk.RAISED, bd=2)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        help_text = """
🎯 OBJECTIVE:
Learn Python programming concepts while playing a fun adventure game!

🎮 CONTROLS:
• Use ← → ↑ ↓ arrow keys to move your character
• Click 'Answer Question' to solve programming challenges

🏆 SCORING:
• Collect 🟡 yellow circles: +10 points each
• Answer questions correctly: +20 points
• Hit 🟥 red obstacles: -5 points  
• Answer questions wrong: -10 points

📈 LEVELS:
• Level 1: Basic Python concepts (need 50 points to advance)
• Level 2: Intermediate topics (need 100 points to advance)  
• Level 3: Advanced concepts (need 150+ points to win)

⏰ TIME LIMIT:
• Start with 60 seconds
• Gain +30 seconds when you level up
• Game ends when time runs out

💡 TIPS:
• Focus on answering questions for the most points
• Avoid obstacles while collecting coins
• Questions get harder but give the same points
• You can skip questions if you're unsure

🏅 ACHIEVEMENTS:
• Your scores are saved automatically
• Check the High Scores to see how you rank
• Try to beat your personal best!

Good luck on your learning adventure! 🚀
        """

        help_label = tk.Label(content_frame, text=help_text, font=("Arial", 10), 
                            bg="#ffffff", justify=tk.LEFT, anchor=tk.NW)
        help_label.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

def main():
    """Main function to run the Learning Quest game"""
    print("🎮 Starting Learning Quest - Code in Place Final Project")
    print()
    print("This game demonstrates the following Python concepts from Code in Place:")
    print("✓ Object-oriented programming with classes")
    print("✓ Graphics programming with tkinter")
    print("✓ Event handling and user input")
    print("✓ Randomization with the random module")
    print("✓ Data structures: lists and dictionaries")
    print("✓ File I/O for saving high scores")
    print("✓ Game logic and state management")
    print("✓ Functions and methods")
    print("✓ Conditional statements and loops")
    print()
    print("Launching game window...")

    # Create the main window and game instance
    root = tk.Tk()

    # Set window icon (if available)
    try:
        root.iconbitmap('icon.ico')  # Optional: add a game icon
    except:
        pass  # Icon file not found, continue without it

    # Create the game
    game = LearningQuestGame(root)

    # Start the tkinter event loop
    root.mainloop()

    print("Thanks for playing Learning Quest! 🎓")

# Run the game if this script is executed directly
if __name__ == "__main__":
    main()
