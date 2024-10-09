import tkinter as tk
from tkinter import simpledialog
import math
import os  # Added for file handling
import webbrowser

# At the start, check and remove the calculations_history.txt file if it exists
history_file = "calculations_history.txt"
if os.path.exists(history_file):
    os.remove(history_file)

# Define global variable to store the last result
last_result = None

# Define functions for standard operations
def add(a, b):
    return a + b

def sub(a, b):
    return a - b

def mult(a, b):
    return a * b

def div(a, b):
    if b == 0:
        return "Error: Division by zero"
    return a / b

def power(a, b):
    return a ** b

def log(a, base=math.e):
    if a <= 0:
        return "Error: Logarithm of non-positive number"
    return math.log(a, base)

def cos(x):
    return math.cos(math.radians(x))

def sin(x):
    return math.sin(math.radians(x))

def tan(x):
    return math.tan(math.radians(x))

# Define functions for matrix operations
def matrix_multiplication(matrix1, matrix2):
    if len(matrix1[0]) != len(matrix2):
        return "Error: Incompatible matrices"
    result = [[sum(a * b for a, b in zip(matrix1_row, matrix2_col)) for matrix2_col in zip(*matrix2)] for matrix1_row in matrix1]
    return result

def matrix_transpose(matrix):
    transpose = list(map(list, zip(*matrix)))
    return transpose

def absolute_value(value):
    return abs(value)

def calculate_mean(values):
    if len(values) == 0:
        return "Error: Empty list"
    return sum(values) / len(values)

def calculate_standard_deviation(values):
    if len(values) == 0:
        return "Error: Empty list"
    mean = calculate_mean(values)
    variance = sum((x - mean) ** 2 for x in values) / len(values)
    return variance ** 0.5

def binary_to_decimal(binary):
    decimal_value = 0
    binary = binary[::-1]
    for i in range(len(binary)):
        if binary[i] == '1':
            decimal_value += 2 ** i
        elif binary[i] != '0':
            return "Error: Invalid binary string"
    return decimal_value

# Function to evaluate the expression entered by the user and save to history
def evaluate_expression():
    global last_result
    expression = entry.get()
    try:
        result = eval(expression)
        last_result = result  # Store the result for the ANS button
    except:
        result = "Error: Invalid expression"
    
    entry.delete(0, tk.END)
    entry.insert(tk.END, str(result))
    
    # Write the expression and result to the history file
    with open("calculations_history.txt", "a") as file:
        file.write(f"{expression} = {result}\n")

# Function to display the calculations history
def show_history():
    history_window = tk.Toplevel(root)
    history_window.title("Calculations History")

    # Add a text widget to display the history
    text_widget = tk.Text(history_window, width=50, height=20, font=("Arial", 14))
    text_widget.pack(pady=10, padx=10)

    # Read the history file and insert the content into the text widget
    try:
        with open("calculations_history.txt", "r") as file:
            history = file.read()
            text_widget.insert(tk.END, history)
    except FileNotFoundError:
        text_widget.insert(tk.END, "No history available.")

    # Add a button to close the history window
    tk.Button(history_window, text="Close", command=history_window.destroy, font=("Arial", 14)).pack(pady=10)

# Function to insert the last result (ANS) into the entry widget
def insert_ans():
    global last_result
    if last_result is not None:
        entry.insert(tk.END, str(last_result))

# Function to open a new window for Matrix mode
def open_matrix_mode():
    matrix_window = tk.Toplevel(root)
    matrix_window.title("Matrix Multiplication Mode")

    rows_a = simpledialog.askinteger("Matrix A Size", "Enter the number of rows for Matrix A:", parent=matrix_window)
    cols_a = simpledialog.askinteger("Matrix A Size", "Enter the number of columns for Matrix A:", parent=matrix_window)
    rows_b = simpledialog.askinteger("Matrix B Size", "Enter the number of rows for Matrix B:", parent=matrix_window)
    cols_b = simpledialog.askinteger("Matrix B Size", "Enter the number of columns for Matrix B:", parent=matrix_window)

    if rows_a and cols_a and rows_b and cols_b:
        if cols_a != rows_b:
            result = "Error: Number of columns in Matrix A must equal the number of rows in Matrix B."
        else:
            # Create labels and input fields for Matrix A and B
            tk.Label(matrix_window, text="Matrix A", font=("Arial", 14)).grid(row=3, column=0, columnspan=cols_a, pady=10)
            matrix_a_entries = create_matrix_entries(matrix_window, rows_a, cols_a, start_row=4)

            tk.Label(matrix_window, text="Matrix B", font=("Arial", 14)).grid(row=3, column=cols_a+1, columnspan=cols_b, pady=10)
            matrix_b_entries = create_matrix_entries(matrix_window, rows_b, cols_b, start_row=4, start_col=cols_a+1)

            def multiply_matrices():
                matrix_a = get_matrix_data(matrix_a_entries)
                matrix_b = get_matrix_data(matrix_b_entries)
                result = matrix_multiplication(matrix_a, matrix_b)
                matrix_window.entry.delete(0, tk.END)
                matrix_window.entry.insert(tk.END, str(result))

            tk.Button(matrix_window, text="Multiply A*B", command=multiply_matrices, font=("Arial", 14)).grid(row=5 + max(rows_a, rows_b), column=0, columnspan=cols_a+cols_b+1, pady=10)
    else:
        result = "Error: Invalid matrix size inputs."

    # Add a label with the name of the mode
    matrix_window.label = tk.Label(matrix_window, text="Matrix Multiplication Mode", font=("Arial", 20), fg="black")
    matrix_window.label.grid(row=0, column=0, columnspan=5, pady=10)

    # Entry widget to display the expression and result
    matrix_window.entry = tk.Entry(matrix_window, width=30, borderwidth=5, font=("Arial", 24))
    matrix_window.entry.grid(row=1, column=0, columnspan=5, pady=15)
    matrix_window.entry.insert(tk.END, str(result))

# Function to open a new window for Transpose mode
def open_transpose_mode():
    transpose_window = tk.Toplevel(root)
    transpose_window.title("Matrix Transpose Mode")

    rows_a = simpledialog.askinteger("Matrix A Size", "Enter the number of rows for Matrix A:", parent=transpose_window)
    cols_a = simpledialog.askinteger("Matrix A Size", "Enter the number of columns for Matrix A:", parent=transpose_window)

    if rows_a and cols_a:
        tk.Label(transpose_window, text="Matrix A", font=("Arial", 14)).grid(row=3, column=0, columnspan=cols_a, pady=10)
        matrix_a_entries = create_matrix_entries(transpose_window, rows_a, cols_a, start_row=4)

        def transpose_matrix():
            matrix_a = get_matrix_data(matrix_a_entries)
            result = matrix_transpose(matrix_a)
            transpose_window.entry.delete(0, tk.END)
            transpose_window.entry.insert(tk.END, str(result))

        tk.Button(transpose_window, text="Transpose Matrix A", command=transpose_matrix, font=("Arial", 14)).grid(row=4, column=cols_a, padx=10, pady=10, sticky="w")
    else:
        result = "Error: Invalid matrix size inputs."

    # Add a label with the name of the mode
    transpose_window.label = tk.Label(transpose_window, text="Matrix Transpose Mode", font=("Arial", 20), fg="black")
    transpose_window.label.grid(row=0, column=0, columnspan=5, pady=10)

    # Entry widget to display the expression and result
    transpose_window.entry = tk.Entry(transpose_window, width=30, borderwidth=5, font=("Arial", 24))
    transpose_window.entry.grid(row=1, column=0, columnspan=5, pady=15)
    transpose_window.entry.insert(tk.END, str(result))

# Function to open a new window for Stat mode
def open_stat_mode():
    stat_window = tk.Toplevel(root)
    stat_window.title("Stat Mode")

    def calculate_mean_trigger():
        values = eval(stat_window.entry.get())
        if isinstance(values, list):
            result = calculate_mean(values)
        else:
            result = "Error: Input should be a list of numbers."
        stat_window.entry.delete(0, tk.END)
        stat_window.entry.insert(tk.END, str(result))

    def calculate_standard_deviation_trigger():
        values = eval(stat_window.entry.get())
        if isinstance(values, list):
            result = calculate_standard_deviation(values)
        else:
            result = "Error: Input should be a list of numbers."
        stat_window.entry.delete(0, tk.END)
        stat_window.entry.insert(tk.END, str(result))

    # Add a label with the name of the mode
    stat_window.label = tk.Label(stat_window, text="Stat Mode", font=("Arial", 20), fg="black")
    stat_window.label.grid(row=0, column=0, columnspan=5, pady=10)

    # Entry widget to display the expression and result
    stat_window.entry = tk.Entry(stat_window, width=30, borderwidth=5, font=("Arial", 24))
    stat_window.entry.grid(row=1, column=0, columnspan=5, pady=15)

    # Stat mode buttons
    tk.Button(stat_window, text='Mean', padx=10, pady=10, command=calculate_mean_trigger, font=("Arial", 14)).grid(row=2, column=0, pady=10)
    tk.Button(stat_window, text='Std Dev', padx=10, pady=10, command=calculate_standard_deviation_trigger, font=("Arial", 14)).grid(row=2, column=1, pady=10)

# Function to open a new window for Base_N mode
def open_base_n_mode():
    base_n_window = tk.Toplevel(root)
    base_n_window.title("Base_N Mode")

    def convert_bin_to_dec():
        binary = base_n_window.entry.get()
        result = binary_to_decimal(binary)
        base_n_window.entry.delete(0, tk.END)
        base_n_window.entry.insert(tk.END, str(result))

    # Add a label with the name of the mode
    base_n_window.label = tk.Label(base_n_window, text="Base_N Mode", font=("Arial", 20), fg="black")
    base_n_window.label.grid(row=0, column=0, columnspan=5, pady=10)

    # Entry widget to display the binary input
    base_n_window.entry = tk.Entry(base_n_window, width=30, borderwidth=5, font=("Arial", 24))
    base_n_window.entry.grid(row=1, column=0, columnspan=5, pady=15)

    # Base_N mode button
    tk.Button(base_n_window, text='Bin to Dec', padx=10, pady=10, command=convert_bin_to_dec, font=("Arial", 14)).grid(row=2, column=0, pady=10)

# Function to create matrix input grid
def create_matrix_entries(parent_window, rows, cols, start_row, start_col=0):
    entries = []
    for i in range(rows):
        current_row = []
        for j in range(cols):
            entry = tk.Entry(parent_window, width=5, font=("Arial", 14))
            entry.grid(row=start_row + i, column=start_col + j, padx=5, pady=5)
            current_row.append(entry)
        entries.append(current_row)
    return entries

# Function to get matrix data from entries
def get_matrix_data(entries):
    return [[float(entry.get()) for entry in row_entries] for row_entries in entries]

# Function to evaluate the expression entered by the user
def evaluate_expression():
    global last_result
    expression = entry.get()
    try:
        result = eval(expression)
        last_result = result  # Store the result for the ANS button
    except:
        result = "Error: Invalid expression"
    entry.delete(0, tk.END)
    entry.insert(tk.END, str(result))

    # Save to history file
    with open("calculations_history.txt", "a") as file:
        file.write(f"{expression} = {result}\n")

# Function to insert text into the entry widget
def insert_text(text):
    entry.insert(tk.END, text)

# Function to clear the entry widget
def clear_entry():
    entry.delete(0, tk.END)

# Function to delete the last character
def delete_last():
    entry.delete(len(entry.get())-1, tk.END)

# Function to display mode options on button click
def show_mode_options():
    mode_button_frame.grid(row=row+1, column=0, padx=20, pady=20, columnspan=4, sticky="nsew")

# Function to open the Casio support website
def open_casio_support():
    webbrowser.open("https://www.casio.com/intl/support/contact/")

# Create the main window
root = tk.Tk()
root.title("Casio Calculator")  # Update the window title

# Set the shape of the calculator window to be tall and narrow, like the Casio FX-570ES PLUS
root.geometry("400x700")

# Set background color
root.configure(bg="#1e3d59")  # Dark Blue background

# Add a label with the name of the calculator in bold and white color, centered
label = tk.Label(root, text="CASIO CALCULATOR", font=("Arial", 20, "bold"), fg="white", bg="#1e3d59")
label.grid(row=0, column=0, columnspan=5, pady=10)

# Add a label with the version "FX-570" under the title
version_label = tk.Label(root, text="FX-570", font=("Arial", 14), fg="white", bg="#1e3d59")
version_label.grid(row=1, column=0, columnspan=5)

# Entry widget to display the expression and result
entry = tk.Entry(root, width=22, borderwidth=5, font=("Arial", 24), bg="white", fg="black")
entry.grid(row=2, column=0, columnspan=5, pady=15)

# Define the standard buttons with updated styling
button_color = "#4f6d7a"  # Light Blue color for buttons
button_text_color = "white"  # White text for buttons

standard_buttons = [
    tk.Button(root, text='SHIFT', padx=10, pady=10, command=None, font=("Arial", 14), bg=button_color, fg=button_text_color),
    tk.Button(root, text='ALPHA', padx=10, pady=10, command=None, font=("Arial", 14), bg=button_color, fg=button_text_color),
    tk.Button(root, text='MODE', padx=10, pady=10, command=show_mode_options, font=("Arial", 14), bg=button_color, fg=button_text_color),
    tk.Button(root, text='DEL', padx=10, pady=10, command=delete_last, font=("Arial", 14), bg=button_color, fg=button_text_color),
    tk.Button(root, text='AC', padx=10, pady=10, command=clear_entry, font=("Arial", 14), bg=button_color, fg=button_text_color),
    tk.Button(root, text='x^2', padx=10, pady=10, command=lambda: insert_text('**2'), font=("Arial", 14), bg=button_color, fg=button_text_color),
    tk.Button(root, text='x^3', padx=10, pady=10, command=lambda: insert_text('**3'), font=("Arial", 14), bg=button_color, fg=button_text_color),
    tk.Button(root, text='x^y', padx=10, pady=10, command=lambda: insert_text('**'), font=("Arial", 14), bg=button_color, fg=button_text_color),
    tk.Button(root, text='sqrt', padx=10, pady=10, command=lambda: insert_text('math.sqrt('), font=("Arial", 14), bg=button_color, fg=button_text_color),
    tk.Button(root, text='log', padx=10, pady=10, command=lambda: insert_text('log('), font=("Arial", 14), bg=button_color, fg=button_text_color),
    tk.Button(root, text='sin', padx=10, pady=10, command=lambda: insert_text('sin('), font=("Arial", 14), bg=button_color, fg=button_text_color),
    tk.Button(root, text='cos', padx=10, pady=10, command=lambda: insert_text('cos('), font=("Arial", 14), bg=button_color, fg=button_text_color),
    tk.Button(root, text='tan', padx=10, pady=10, command=lambda: insert_text('tan('), font=("Arial", 14), bg=button_color, fg=button_text_color),
    tk.Button(root, text='(', padx=10, pady=10, command=lambda: insert_text('('), font=("Arial", 14), bg=button_color, fg=button_text_color),
    tk.Button(root, text=')', padx=10, pady=10, command=lambda: insert_text(')'), font=("Arial", 14), bg=button_color, fg=button_text_color),
    tk.Button(root, text='7', padx=10, pady=10, command=lambda: insert_text('7'), font=("Arial", 14), bg=button_color, fg=button_text_color),
    tk.Button(root, text='8', padx=10, pady=10, command=lambda: insert_text('8'), font=("Arial", 14), bg=button_color, fg=button_text_color),
    tk.Button(root, text='9', padx=10, pady=10, command=lambda: insert_text('9'), font=("Arial", 14), bg=button_color, fg=button_text_color),
    tk.Button(root, text='*', padx=10, pady=10, command=lambda: insert_text('*'), font=("Arial", 14), bg=button_color, fg=button_text_color),
    tk.Button(root, text='/', padx=10, pady=10, command=lambda: insert_text('/'), font=("Arial", 14), bg=button_color, fg=button_text_color),  # Added division button
    tk.Button(root, text='%', padx=10, pady=10, command=lambda: insert_text('%'), font=("Arial", 14), bg=button_color, fg=button_text_color),
    tk.Button(root, text='4', padx=10, pady=10, command=lambda: insert_text('4'), font=("Arial", 14), bg=button_color, fg=button_text_color),
    tk.Button(root, text='5', padx=10, pady=10, command=lambda: insert_text('5'), font=("Arial", 14), bg=button_color, fg=button_text_color),
    tk.Button(root, text='6', padx=10, pady=10, command=lambda: insert_text('6'), font=("Arial", 14), bg=button_color, fg=button_text_color),
    tk.Button(root, text='-', padx=10, pady=10, command=lambda: insert_text('-'), font=("Arial", 14), bg=button_color, fg=button_text_color),
    tk.Button(root, text='EXP', padx=10, pady=10, command=lambda: insert_text('math.exp('), font=("Arial", 14), bg=button_color, fg=button_text_color),
    tk.Button(root, text='1', padx=10, pady=10, command=lambda: insert_text('1'), font=("Arial", 14), bg=button_color, fg=button_text_color),
    tk.Button(root, text='2', padx=10, pady=10, command=lambda: insert_text('2'), font=("Arial", 14), bg=button_color, fg=button_text_color),
    tk.Button(root, text='3', padx=10, pady=10, command=lambda: insert_text('3'), font=("Arial", 14), bg=button_color, fg=button_text_color),
    tk.Button(root, text='+', padx=10, pady=10, command=lambda: insert_text('+'), font=("Arial", 14), bg=button_color, fg=button_text_color),
    tk.Button(root, text='ANS', padx=10, pady=10, command=insert_ans, font=("Arial", 14), bg=button_color, fg=button_text_color),  # Added ANS functionality
    tk.Button(root, text='0', padx=10, pady=10, command=lambda: insert_text('0'), font=("Arial", 14), bg=button_color, fg=button_text_color),
    tk.Button(root, text='.', padx=10, pady=10, command=lambda: insert_text('.'), font=("Arial", 14), bg=button_color, fg=button_text_color),
    tk.Button(root, text='=', padx=10, pady=10, command=evaluate_expression, font=("Arial", 14), bg=button_color, fg=button_text_color),
]

# Add standard buttons to the grid with appropriate positioning
row = 4  # Start at row 3 since row 0 is the label, row 1 is the version, and row 2 is the entry
col = 0
for button in standard_buttons:
    button.grid(row=row, column=col, sticky="nsew")
    col += 1
    if col > 4:
        col = 0
        row += 1

# Create a frame for mode buttons that is initially hidden
mode_button_frame = tk.Frame(root, bg="#1e3d59")  # Match background color

tk.Button(mode_button_frame, text="Matrix Mode", command=open_matrix_mode, font=("Arial", 14), bg=button_color, fg=button_text_color).grid(row=0, column=0, padx=20, pady=20, columnspan=2, sticky="nsew")
tk.Button(mode_button_frame, text="Transpose Mode", command=open_transpose_mode, font=("Arial", 14), bg=button_color, fg=button_text_color).grid(row=0, column=2, padx=20, pady=20, columnspan=2, sticky="nsew")
tk.Button(mode_button_frame, text="Stat Mode", command=open_stat_mode, font=("Arial", 14), bg=button_color, fg=button_text_color).grid(row=1, column=0, padx=20, pady=20, columnspan=2, sticky="nsew")
tk.Button(mode_button_frame, text="Base_N Mode", command=open_base_n_mode, font=("Arial", 14), bg=button_color, fg=button_text_color).grid(row=1, column=2, padx=20, pady=20, columnspan=2, sticky="nsew")

# Add a button for showing history
history_button = tk.Button(root, text="History", padx=10, pady=10, command=show_history, font=("Arial", 14), bg=button_color, fg=button_text_color)
history_button.grid(row=row+1, column=0, columnspan=5, pady=10)

# Position the "Contact Us" label and email
contact_label = tk.Label(root, text="Contact Us", font=("Arial", 12, "bold"), fg="white", bg="#1e3d59", cursor="hand2")
contact_label.grid(row=row+2, column=0, columnspan=5, pady=10)
contact_label.bind("<Button-1>", lambda e: open_casio_support())

email_label = tk.Label(root, text="cms@casio.com", font=("Arial", 12), fg="white", bg="#1e3d59")
email_label.grid(row=row+3, column=0, columnspan=5)

# Make the buttons and entry widget expand with the window
for i in range(5):
    root.grid_columnconfigure(i, weight=1)
for i in range(row+4):
    root.grid_rowconfigure(i, weight=1)

# Start the main event loop
root.mainloop()
