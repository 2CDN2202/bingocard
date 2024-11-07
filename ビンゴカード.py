import tkinter as tk
import random

def generate_bingo_numbers():
    bingo_card = []
    for i in range(5):
        column_numbers = random.sample(range(1 + i * 15, 16 + i * 15), 5)
        bingo_card.append(column_numbers)
    
    bingo_card[2][2] = "FREE"
    return bingo_card

def check_bingo():
    bingo_lines = 0
    reach_lines = 0

    for i in range(5):
        row_count = sum(selected[i][j] for j in range(5))
        if row_count == 5:
            bingo_lines += 1
        elif row_count == 4:
            reach_lines += 1

        col_count = sum(selected[j][i] for j in range(5))
        if col_count == 5:
            bingo_lines += 1
        elif col_count == 4:
            reach_lines += 1

    diag1_count = sum(selected[i][i] for i in range(5))
    diag2_count = sum(selected[i][4 - i] for i in range(5))
    
    if diag1_count == 5:
        bingo_lines += 1
    elif diag1_count == 4:
        reach_lines += 1

    if diag2_count == 5:
        bingo_lines += 1
    elif diag2_count == 4:
        reach_lines += 1

    if bingo_lines > 0:
        result_label.config(text=f"ビンゴ！ {bingo_lines}ライン！")
    elif reach_lines > 0:
        result_label.config(text=f"{reach_lines}リーチ！")
    else:
        result_label.config(text="")

def on_cell_click(i, j, button):
    if not selected[j][i]:  
        selected[j][i] = True
        button.config(bg="lightblue")
        check_bingo()  

def reset_bingo_card():
    global selected
    selected = [[False] * 5 for _ in range(5)]
    result_label.config(text="")  
    bingo_numbers = generate_bingo_numbers()
    for i in range(5):
        for j in range(5):
            button = buttons[i][j]
            number = bingo_numbers[j][i]
            button.config(text=str(number), bg="SystemButtonFace", state="normal")
            if i == 2 and j == 2:
                selected[j][i] = True
                button.config(text="FREE", bg="lightgray", state="disabled")

def create_bingo_card():
    bingo_numbers = generate_bingo_numbers()
    for i in range(5):
        row = []
        for j in range(5):
            number = bingo_numbers[j][i]
            btn = tk.Button(root, text=str(number), width=8, height=4)
            btn.grid(row=i, column=j, padx=5, pady=5)
            if i == 2 and j == 2:
                selected[j][i] = True
                btn.config(text="FREE", bg="lightgray", state="disabled")
            else:
                btn.config(command=lambda i=i, j=j, b=btn: on_cell_click(i, j, b))
            row.append(btn)
        buttons.append(row)

root = tk.Tk()
root.title("ビンゴカード")

selected = [[False] * 5 for _ in range(5)]
buttons = []  

create_bingo_card()

result_label = tk.Label(root, text="", font=("Arial", 16))
result_label.grid(row=5, column=0, columnspan=5, pady=10)

reset_button = tk.Button(root, text="リセット", command=reset_bingo_card, font=("Arial", 14))
reset_button.grid(row=6, column=0, columnspan=5, pady=10)

root.mainloop()