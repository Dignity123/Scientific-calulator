import tkinter as tk
import math
from tkinter import ttk, messagebox

class ScientificCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Scientific Calculator")
        self.root.geometry("400x500")
        self.root.resizable(False, False)
        self.root.configure(bg="#f0f0f0")
        
        # Set the icon (commented out as it requires an icon file)
        # self.root.iconbitmap("calculator_icon.ico")
        
        # Initialize the expression variable
        self.expression = ""
        self.ans = 0
        
        # Create the display frame
        self.create_display()
        
        # Create the buttons frame
        self.create_buttons()
        
        # Apply styling
        self.apply_styling()
    
    def apply_styling(self):
        # Configure styles for buttons
        style = ttk.Style()
        style.configure("TButton", font=('Arial', 12))
        style.configure("Num.TButton", background="#ffffff")
        style.configure("Op.TButton", background="#e1e1e1")
        style.configure("Func.TButton", background="#d0d0d0")
        style.configure("Equal.TButton", background="#4CAF50")
        
    def create_display(self):
        # Create a display frame
        display_frame = tk.Frame(self.root, bg="#f0f0f0")
        display_frame.pack(pady=10)
        
        # Create the input display
        self.input_field = tk.Entry(display_frame, 
                                    font=('Arial', 18), 
                                    justify=tk.RIGHT,
                                    width=22,
                                    bd=5,
                                    relief=tk.RIDGE,
                                    bg="#e0f7fa")
        self.input_field.pack(padx=10, pady=5)
        self.input_field.insert(0, "0")
        self.input_field.configure(state="readonly")
    
    def create_buttons(self):
        # Create a frame for buttons
        buttons_frame = tk.Frame(self.root, bg="#f0f0f0")
        buttons_frame.pack(pady=5)
        
        # Define buttons layout
        buttons = [
            ("sin", 0, 0), ("cos", 0, 1), ("tan", 0, 2), ("√", 0, 3), ("C", 0, 4),
            ("log", 1, 0), ("ln", 1, 1), ("(", 1, 2), (")", 1, 3), ("÷", 1, 4),
            ("x²", 2, 0), ("x³", 2, 1), ("7", 2, 2), ("8", 2, 3), ("9", 2, 4),
            ("x^y", 3, 0), ("1/x", 3, 1), ("4", 3, 2), ("5", 3, 3), ("6", 3, 4),
            ("π", 4, 0), ("e", 4, 1), ("1", 4, 2), ("2", 4, 3), ("3", 4, 4),
            ("Ans", 5, 0), ("DEL", 5, 1), ("0", 5, 2), (".", 5, 3), ("=", 5, 4),
            ("×", 6, 0), ("-", 6, 1), ("+", 6, 2), ("!", 6, 3), ("mod", 6, 4)
        ]
        
        # Create and place buttons
        for (text, row, col) in buttons:
            button = tk.Button(buttons_frame, text=text, 
                               width=5, height=2,
                               font=("Arial", 12, "bold"),
                               bd=3, relief=tk.RAISED)
            
            # Style buttons based on function
            if text in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "."]:
                button.configure(bg="#ffffff")
            elif text in ["+", "-", "×", "÷", "=", "^", "mod"]:
                button.configure(bg="#e1e1e1")
            elif text == "=":
                button.configure(bg="#4CAF50", fg="white")
            elif text in ["C", "DEL"]:
                button.configure(bg="#FF5252", fg="white")
            else:
                button.configure(bg="#d0d0d0")
            
            # Bind button events
            button.configure(command=lambda btn=text: self.button_click(btn))
            
            # Grid layout with padding
            button.grid(row=row, column=col, padx=4, pady=4)
            
        # Add a mode indicator (can be expanded for different calculator modes)
        self.mode_label = tk.Label(self.root, text="Standard Mode", 
                                  font=("Arial", 10), bg="#f0f0f0")
        self.mode_label.pack(pady=5)
            
    def button_click(self, button_text):
        # Get the current displayed text
        current = self.input_field.get()
        
        # Clear the display if it shows "0" or an error
        if current == "0" or current == "Error":
            self.input_field.configure(state="normal")
            self.input_field.delete(0, tk.END)
            self.input_field.configure(state="readonly")
            current = ""
        
        # Handle different button inputs
        if button_text == "C":
            # Clear the display
            self.input_field.configure(state="normal")
            self.input_field.delete(0, tk.END)
            self.input_field.insert(0, "0")
            self.input_field.configure(state="readonly")
            self.expression = ""
        
        elif button_text == "DEL":
            # Delete the last character
            self.input_field.configure(state="normal")
            if len(current) > 0:
                new_text = current[:-1]
                if new_text == "":
                    new_text = "0"
                self.input_field.delete(0, tk.END)
                self.input_field.insert(0, new_text)
                self.expression = new_text if new_text != "0" else ""
            self.input_field.configure(state="readonly")
        
        elif button_text == "=":
            # Evaluate the expression
            try:
                # Replace symbols for evaluation
                expr = current.replace("×", "*").replace("÷", "/").replace("π", str(math.pi))
                expr = expr.replace("e", str(math.e)).replace("mod", "%")
                
                # Handle special functions
                expr = expr.replace("sin", "math.sin").replace("cos", "math.cos")
                expr = expr.replace("tan", "math.tan").replace("log", "math.log10")
                expr = expr.replace("ln", "math.log").replace("√", "math.sqrt")
                
                # Handle square and cube
                expr = expr.replace("x²", "**2").replace("x³", "**3")
                
                # Handle power notation with carets
                while "^" in expr:
                    idx = expr.find("^")
                    expr = expr[:idx] + "**" + expr[idx+1:]
                
                # Handle factorial
                if "!" in expr:
                    parts = expr.split("!")
                    num = float(parts[0])
                    if num.is_integer() and num >= 0:
                        expr = str(math.factorial(int(num))) + "".join(parts[1:])
                    else:
                        raise ValueError("Factorial requires non-negative integer")
                
                # Replace Ans with the last answer
                expr = expr.replace("Ans", str(self.ans))
                
                # Calculate result
                result = eval(expr)
                self.ans = result
                
                # Format and display result
                if result == int(result):
                    result = int(result)
                
                self.input_field.configure(state="normal")
                self.input_field.delete(0, tk.END)
                self.input_field.insert(0, str(result))
                self.input_field.configure(state="readonly")
                self.expression = str(result)
                
            except Exception as e:
                self.input_field.configure(state="normal")
                self.input_field.delete(0, tk.END)
                self.input_field.insert(0, "Error")
                self.input_field.configure(state="readonly")
                self.expression = ""
        
        elif button_text in ["sin", "cos", "tan", "log", "ln", "√"]:
            # Handle scientific functions
            self.input_field.configure(state="normal")
            self.input_field.delete(0, tk.END)
            self.input_field.insert(0, current + button_text + "(")
            self.input_field.configure(state="readonly")
            self.expression = current + button_text + "("
        
        elif button_text in ["x²", "x³"]:
            # Handle powers
            power = "2" if button_text == "x²" else "3"
            self.input_field.configure(state="normal")
            self.input_field.delete(0, tk.END)
            
            # Check if there's content to square/cube
            if current:
                # If the current expression is just a number or ends with a number or closing parenthesis
                if current.isdigit() or (len(current) > 0 and (current[-1].isdigit() or current[-1] == ")")):
                    self.input_field.insert(0, f"({current})^{power}")
                    self.expression = f"({current})**{power}"
                else:
                    self.input_field.insert(0, f"({current})^{power}")
                    self.expression = f"({current})**{power}"
            else:
                # If empty, just put a 0
                self.input_field.insert(0, "0")
                self.expression = ""
            
            self.input_field.configure(state="readonly")
        
        elif button_text == "x^y":
            # Handle power operation
            self.input_field.configure(state="normal")
            self.input_field.delete(0, tk.END)
            self.input_field.insert(0, current + "^")
            self.input_field.configure(state="readonly")
            self.expression = current + "**"
        
        elif button_text == "π":
            # Insert pi
            self.input_field.configure(state="normal")
            self.input_field.delete(0, tk.END)
            self.input_field.insert(0, current + "π")
            self.input_field.configure(state="readonly")
            self.expression = current + "π"
        
        elif button_text == "e":
            # Insert e (Euler's number)
            self.input_field.configure(state="normal")
            self.input_field.delete(0, tk.END)
            self.input_field.insert(0, current + "e")
            self.input_field.configure(state="readonly")
            self.expression = current + "e"
        
        elif button_text == "1/x":
            # Handle reciprocal
            self.input_field.configure(state="normal")
            self.input_field.delete(0, tk.END)
            self.input_field.insert(0, "1/("+current+")")
            self.input_field.configure(state="readonly")
            self.expression = "1/("+current+")"
        
        elif button_text == "!":
            # Handle factorial
            self.input_field.configure(state="normal")
            self.input_field.delete(0, tk.END)
            self.input_field.insert(0, current + "!")
            self.input_field.configure(state="readonly")
            self.expression = current + "!"
        
        elif button_text == "Ans":
            # Insert the last answer
            self.input_field.configure(state="normal")
            self.input_field.delete(0, tk.END)
            self.input_field.insert(0, current + "Ans")
            self.input_field.configure(state="readonly")
            self.expression = current + str(self.ans)
        
        else:
            # Insert the button text
            self.input_field.configure(state="normal")
            self.input_field.delete(0, tk.END)
            self.input_field.insert(0, current + button_text)
            self.input_field.configure(state="readonly")
            self.expression = current + button_text

if __name__ == "__main__":
    root = tk.Tk()
    calculator = ScientificCalculator(root)
    root.mainloop()