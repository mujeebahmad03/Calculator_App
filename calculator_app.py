import tkinter as tk
from tkinter import ttk
import math
from functools import partial
from decimal import Decimal

# Logging Function/Method Decorator
def log_function_call(func):
    def wrapper(*args, **kwargs):
        print(f'calling function: {func.__name__}')
        return func(*args, **kwargs)
    return wrapper

class Calculator:
    """
    A simple calculator class with GUI.
    """

    def __init__(self, root):
        self.root = root
        self.root.title('Calculator')
        self.root.bind('<KeyPress>', self.key_pressed)
        self.text = tk.Text(self.root, width=50, height=5, font=('Arial', 16))
        self.text.grid(row=0, column=0, columnspan=7)
        self.memory = 0
        
        self.style = ttk.Style()
        self.style.configure('Numeric.TButton', background='green')
        self.style.configure('Operator.TButton', background='yellow')
        self.style.configure('Memory.TButton', background='SystemTransparent')
        self.create_buttons()

    @log_function_call
    def create_buttons(self):
        """
        Create calculator buttons with appropriate styling.
        """
        button_texts = [
            'MC','M+','M-','MR','C', '%', '/',
            '√', '^2', '^3', '7', '8', '9', '*',
            'sin', 'cos', 'tan', '4', '5', '6', '+',
            '1/x', '3√', 'log', '1', '2', '3', '-',
            '(', ')', 'x!', '0', '.', '+/-', '='
        ]

        row = 1
        col = 0
        for text in button_texts:
            style_name = self.get_button_style(text)
            button = ttk.Button(self.root, text=text, width=3, style=style_name,
                                command=partial(self.handle_button_click, text))
            button.grid(row=row, column=col)
            col += 1 
            if col > 6:
                col = 0
                row += 1
    
    @log_function_call
    def get_button_style(self, button_text):
        """
        Get the appropriate button style based on the button's text.
        """
        if button_text in ['+', '-', '*', '/']:
            return 'Operator.TButton'
        elif button_text in ['M+', 'M-', 'MC', 'MR']:
            return 'Memory.TButton'
        else: 
            return 'Numeric.TButton'

    @log_function_call
    def perform_operation(self, expression):
        """
        Perform a mathematical operation based on the given expression.
        """
        try:
            result = eval(expression, {'__builtins__': None}, {'Decimal': Decimal})   
            if result == float("inf"):
                raise ZeroDivisionError
            return self.update_text(str(result))
        except ZeroDivisionError:
            self.update_text('Not a number')
        except (SyntaxError, ValueError):
            self.update_text('Invalid Input')
        except Exception as error:
            return self.update_text(f'Error: {error}')
    
    @log_function_call        
    def update_text(self, value):
        """
        Update the text area with the given value.
        """
        self.clear_text()
        self.text.insert(tk.END, value)

    @log_function_call
    def error_handler(self, message):
        """
        Display an error message in the text area.
        """
        self.update_text(f'Error, {message}' )
    
    @log_function_call
    def perform_unary_operation(self, operation, input_type):
        """
        Perform an operation on the current value based on input_type.
        """
        try:
            if input_type == 'unary':
                value = float(self.text.get(1.0, tk.END))
                if (operation == math.sqrt or operation == (lambda x: x ** (1/3))) and value < 0:
                    self.error_handler('Not a number')
                    return
            if input_type == 'integer':
                value = int(self.text.get(1.0, tk.END))
            result = operation(value)
            self.update_text(result)
        except (SyntaxError, ValueError):
            self.update_text('Invalid Input')
        except Exception as error:
            self.error_handler(str(error))

    @log_function_call
    def handle_memory(self, text):
        """
        Handle memory-related operations.
        """
        current_value = self.str_to_num(self.text.get(1.0, tk.END))
        try:
            if text == 'M+':
                self.memory += current_value
                self.update_text(self.memory)
            elif text == 'M-':
                self.memory -= current_value
                self.update_text(self.memory)
            elif text == 'MC':
                self.memory = 0
            elif text == 'MR':
                self.update_text(self.memory)
        except Exception as error:
            self.error_handler(str(error))

    @log_function_call
    def str_to_num(self, str_num):
        """
        Convert a string to a number (integer or float).
        """
        try:
            num = int(str_num)
        except ValueError:
            try:
                num = float(str_num)
            except ValueError:
                num = None
        return num
    
    @log_function_call
    def clear_text(self):
        """
        Clear the text area.
        """
        self.text.delete(1.0, tk.END)
    
    @log_function_call
    def handle_button_click(self, text):
        """
        Handle button clicks.
        """
        current_entry = self.text.get(1.0, 'end').strip()
        
        # Input Validation
        if text.isdigit() or text in '+-/.*()':
            self.text.insert(tk.END, text)
        else:
            # Input Check
            if text == '=':
                self.perform_operation(current_entry)
            elif text == 'C':
                self.clear_text()
            elif text == '√':
                self.perform_unary_operation(math.sqrt, 'unary')
            elif text == '3√':
                self.perform_unary_operation(lambda x: x ** (1/3), 'unary')
            elif text == '^2':
                self.perform_unary_operation(lambda x: x ** 2, 'unary')
            elif text == '^3':
                self.perform_unary_operation(lambda x: x ** 3, 'unary')
            elif text == '%':
                self.perform_unary_operation(lambda x: x / 100, 'unary')
            elif text == '+/-':
                self.perform_unary_operation(lambda x: x * (-1), 'integer')
            elif text == '1/x':
                self.perform_unary_operation(lambda x: 1/x, 'unary')
            elif text == 'log':
                self.perform_unary_operation(math.log10, 'unary')
            elif text == 'sin':
                self.perform_unary_operation(lambda x: math.sin(math.radians(x)), 'unary')
            elif text == 'cos':
                self.perform_unary_operation(lambda x: math.cos(math.radians(x)), 'unary')
            elif text == 'tan':
                self.perform_unary_operation(lambda x: math.tan(math.radians(x)), 'unary')
            elif text == 'x!':
                self.perform_unary_operation(math.factorial, 'integer')
            elif text in ['M+', 'M-', 'MC', 'MR']:
                self.handle_memory(text)
            else:
                self.error_handler('Invalid Input')
        self.text.see('end')

    @log_function_call
    def key_pressed(self, event):
        """
        Handle keyboard key presses.
        """
        current_entry = self.text.get(1.0, tk.END).strip()
        key = event.char
        symbol = event.keysym

        if symbol and symbol in '1234567890':
            self.handle_button_click(key)
        elif key and key in '+-/*()%':
            self.handle_button_click(key)
        elif key == '=' or symbol == 'Return':
            self.perform_operation(current_entry)
        elif key == 'c' or symbol == 'Escape':
            self.clear_text()
        elif symbol == 'BackSpace':
            updated_entry = current_entry[:-1]
            self.update_text(updated_entry)

if __name__ == '__main__':
    root = tk.Tk()
    Calculator(root)
    root.mainloop()
