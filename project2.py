
import tkinter as tk
import math

# ---------------- MAIN WINDOW ----------------

root = tk.Tk()
root.title("Premium Calculator")
root.geometry("430x650")
root.minsize(380, 580)
dark_mode = True
history = []
memory = 0
expression = ""

# ---------------- COLORS ----------------

def get_colors():
    if dark_mode:
        return {
            "bg": "#151821",
            "display": "#222735",
            "button": "#2C3242",
            "text": "#FFFFFF",
            "operator": "#7048E8",
            "special": "#3C4559",
            "equal": "#16A085",
            "history": "#AAB2C5"
        }
    return {
        "bg": "#EDF0F7", 
        "display": "#FFFFFF",
        "button": "#DDE2EF",
        "text": "#153699",
        "operator": "#7048E8",
        "special": "#C9D0E0",
        "equal": "#16A085",
        "history": "#596579"
    }

# ---------------- MAIN LAYOUT ----------------

root.configure(bg="#151821")

header = tk.Frame(root, bg="#151821")
header.pack(fill="x", padx=15, pady=15)

title = tk.Label(
    header,
    text="CALCULATOR PRO",
    font=("Arial", 17, "bold"),
    fg="#A78BFA",
    bg="#151821"
)
title.pack(side="left")

theme_btn = tk.Button(
    header,
    text="☀ / ☾",
    font=("Arial", 12),
    command=lambda: toggle_theme(),
    relief="flat",
    cursor="hand2"
)
theme_btn.pack(side="right")

# ---------------- DISPLAY ----------------

display_frame = tk.Frame(root, bg="#222735")
display_frame.pack(fill="x", padx=15, pady=10)

history_label = tk.Label(
    display_frame,
    text="Welcome!",
    font=("Arial", 11),
    anchor="e",
    bg="#222735",
    fg="#AAB2C5"
)
history_label.pack(fill="x", padx=15, pady=(12, 2))

display = tk.Entry(
    display_frame,
    font=("Arial", 30, "bold"),
    justify="right",
    bd=0,
    relief="flat",
    bg="#222735",
    fg="white",
    insertbackground="white"
)
display.pack(fill="x", padx=15, pady=(5, 15), ipady=8)

# ---------------- BUTTON AREA ----------------

button_frame = tk.Frame(root, bg="#151821")
button_frame.pack(fill="both", expand=True, padx=12, pady=10)

buttons = [
    ["MC", "MR", "M+", "M-"],
    ["AC", "⌫", "%", "÷"],
    ["√", "x²", "xʸ", "×"],
    ["7", "8", "9", "−"],
    ["4", "5", "6", "+"],
    ["1", "2", "3", "="],
    ["00", "0", ".", "0"]
]

# ---------------- FUNCTIONS ----------------

def insert_value(value):
    if display.get() == "Error":
        display.delete(0, tk.END)

    display.insert(tk.END, value)

def clear():
    display.delete(0, tk.END)
    history_label.config(text="Ready")

def backspace():
    current = display.get()
    display.delete(0, tk.END)
    display.insert(0, current[:-1])

def calculate():
    try:
        expr = display.get()

        if not expr:
            return

        # Safe arithmetic parser
        import ast
        import operator

        ops = {
            ast.Add: operator.add,
            ast.Sub: operator.sub,
            ast.Mult: operator.mul,
            ast.Div: operator.truediv,
            ast.Pow: operator.pow,
            ast.USub: operator.neg,
            ast.UAdd: operator.pos
        }

        def safe_eval(node):
            if isinstance(node, ast.Expression):
                return safe_eval(node.body)

            if isinstance(node, ast.Constant):
                if type(node.value) in (int, float):
                    return node.value
                raise ValueError("Invalid number")

            if isinstance(node, ast.BinOp):
                if type(node.op) not in ops:
                    raise ValueError("Invalid operator")
                left = safe_eval(node.left)
                right = safe_eval(node.right)

                if isinstance(node.op, ast.Pow) and abs(right) > 1000:
                    raise ValueError("Exponent too large")

                result = ops[type(node.op)](left, right)

                if isinstance(result, complex):
                    raise ValueError("Complex results unsupported")

                if not math.isfinite(result) or abs(result) > 1e100:
                    raise ValueError("Result out of range")

                return result

            if isinstance(node, ast.UnaryOp):
                if type(node.op) not in ops:
                    raise ValueError("Invalid operator")
                return ops[type(node.op)](safe_eval(node.operand))

            raise ValueError("Invalid expression")

        result = safe_eval(ast.parse(expr, mode="eval"))

        history.append(f"{expr} = {result}")
        history_label.config(text=f"Result: {result}")

        display.delete(0, tk.END)
        display.insert(0, str(result))

    except Exception:
        display.delete(0, tk.END)
        display.insert(0, "Error")
        history_label.config(text="Invalid calculation")

def special_function(value):
    try:
        number = float(display.get())

        if value == "√":
            result = math.sqrt(number)
        elif value == "x²":
            result = number ** 2
        elif value == "%":
            result = number / 100
        elif value == "xʸ":
            display.insert(tk.END, "**")
            return

        display.delete(0, tk.END)
        display.insert(0, str(result))

    except Exception:
        display.delete(0, tk.END)
        display.insert(0, "Error")

# ---------------- MEMORY FUNCTIONS ----------------

def memory_function(value):
    global memory

    try:
        number = float(display.get() or 0)

        if value == "MC":
            memory = 0
        elif value == "MR":
            display.delete(0, tk.END)
            display.insert(0, str(memory))
        elif value == "M+":
            memory += number
        elif value == "M-":
            memory -= number

    except ValueError:
        pass

# ---------------- BUTTON ACTION ----------------

def button_click(value):
    if value == "=":
        calculate()

    elif value == "AC":
        clear()

    elif value == "⌫":
        backspace()

    elif value in ["√", "x²", "xʸ", "%"]:
        special_function(value)

    elif value in ["MC", "MR", "M+", "M-"]:
        memory_function(value)

    else:
        symbols = {
            "÷": "/",
            "×": "*",
            "−": "-"
        }
        insert_value(symbols.get(value, value))

# ---------------- CREATE BUTTONS ----------------

button_widgets = []

def create_buttons():
    for widget in button_frame.winfo_children():
        widget.destroy()

    colors = get_colors()
    button_widgets.clear()

    for r, row in enumerate(buttons):
        for c, value in enumerate(row):

            if value == "=":
                bg = colors["equal"]
            elif value in ["÷", "×", "−", "+", "xʸ"]:
                bg = colors["operator"]
            elif value in ["AC", "⌫", "%", "√", "x²",
                           "MC", "MR", "M+", "M-"]:
                bg = colors["special"]
            else:
                bg = colors["button"]

            btn = tk.Button(
                button_frame,
                text=value,
                font=("Arial", 16, "bold"),
                bg=bg,
                fg="white" if dark_mode or bg in [
                    colors["operator"], colors["equal"]
                ] else colors["text"],
                activebackground="#9675F5",
                activeforeground="white",
                bd=0,
                relief="flat",
                cursor="hand2",
                command=lambda x=value: button_click(x)
            )

            btn.grid(
                row=r,
                column=c,
                sticky="nsew",
                padx=4,
                pady=4
            )

            button_widgets.append(btn)

    for i in range(4):
        button_frame.columnconfigure(i, weight=1)

    for i in range(len(buttons)):
        button_frame.rowconfigure(i, weight=1)

# ---------------- THEME ----------------

def toggle_theme():
    global dark_mode
    dark_mode = not dark_mode

    colors = get_colors()
    root.configure(bg=colors["bg"])

    header.configure(bg=colors["bg"])
    title.configure(bg=colors["bg"])
    button_frame.configure(bg=colors["bg"])

    display_frame.configure(bg=colors["display"])
    display.configure(
        bg=colors["display"],
        fg=colors["text"],
        insertbackground=colors["text"]
    )

    history_label.configure(
        bg=colors["display"],
        fg=colors["history"]
    )

    theme_btn.configure(
        bg=colors["special"],
        fg=colors["text"],
        activebackground=colors["operator"]
    )

    create_buttons()

# ---------------- KEYBOARD SUPPORT ----------------

def keyboard_input(event):
    key = event.char

    if key in "0123456789.+-*/":
        insert_value(key)

    elif event.keysym == "Return":
        calculate()

    elif event.keysym == "BackSpace":
        backspace()

    elif event.keysym == "Escape":
        clear()

root.bind("<Key>", keyboard_input)

# ---------------- HISTORY WINDOW ----------------

def show_history():
    window = tk.Toplevel(root)
    window.title("Calculation History")
    window.geometry("350x400")
    window.configure(bg="#222735")

    tk.Label(
        window,
        text="CALCULATION HISTORY",
        font=("Arial", 14, "bold"),
        bg="#222735",
        fg="#A78BFA"
    ).pack(pady=15)

    listbox = tk.Listbox(
        window,
        font=("Arial", 12),
        bg="#2C3242",
        fg="white",
        bd=0
    )
    listbox.pack(fill="both", expand=True, padx=15, pady=10)

    for item in reversed(history):
        listbox.insert(tk.END, item)

    tk.Button(
        window,
        text="Clear History",
        bg="#7048E8",
        fg="white",
        command=lambda: (
            history.clear(),
            listbox.delete(0, tk.END)
        )
    ).pack(pady=10)

# ---------------- FOOTER ----------------

footer = tk.Frame(root, bg="#151821")
footer.pack(fill="x", padx=15, pady=8)

history_button = tk.Button(
    footer,
    text="📜 View History",
    font=("Arial", 11, "bold"),
    bg="#7048E8",
    fg="white",
    relief="flat",
    command=show_history,
    cursor="hand2"
)
history_button.pack(fill="x", ipady=8)

# ---------------- START ----------------

create_buttons()
root.mainloop()
