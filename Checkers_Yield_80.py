import os
from tkinter import *
from tkinter import messagebox
from tkinter import ttk


def password_code(password):
    key = 2
    coded_password = ""
    for i in password:
        coded_password_temp = chr(ord(i) + key)
        coded_password += coded_password_temp
        key = -key + 1
    return coded_password


def open_file():
    try:
        text = open("users_checker_file.txt", "r+")
        return text
    except FileNotFoundError:
        try:
            text = open("users_checker_file.txt", "w")
            text.close()
            text = open("users_checker_file.txt", "r+")
            return text
        except FileNotFoundError:
            text = open("users_checker_file.txt", "r+")
            return text


def dismiss(win):
    win.grab_release()
    win.destroy()


class Checkers:
    def __init__(self, main):
        self.deck = None
        self.first_click = True
        self.main = main
        self.users = {}

        button_style = ttk.Style()
        button_style.configure("my.TButton", font="Arial 12")

        self.label = Label(text="Для игры введите ваш логин и пароль или зарегистрируйтесь", font="Arial 15 bold")
        self.label_login = Label(text="Логин", font="Arial 15")
        self.label_password = Label(text="Пароль", font="Arial 15")
        self.entry_login = ttk.Entry(width=30, justify="center")
        self.entry_password = ttk.Entry(width=30, justify="center")
        self.button_auth = ttk.Button(text="Авторизироваться", style="my.TButton", command=lambda: self.authorization())
        self.button_reg = ttk.Button(text="Зарегистрироваться", style="my.TButton", command=lambda: self.registrate())
        self.button_back = ttk.Button(self.main, text="Выход", style="my.TButton", command=lambda: self.authorization())

        self.label.place(x=40, y=25)
        self.label_login.place(x=320, y=55)
        self.entry_login.place(x=255, y=85)
        self.label_password.place(x=315, y=105)
        self.entry_password.place(x=255, y=135)
        self.button_auth.place(x=260, y=165, width=180)
        self.button_reg.place(x=260, y=195, width=180)

        self.x1 = 0
        self.y1 = 0
        self.x2 = 0
        self.y2 = 0

        self.deck_model = [[0, -1, 0, -1, 0, -1, 0, -1, 0, -1],
                           [-1, 0, -1, 0, -1, 0, -1, 0, -1, 0],
                           [0, -1, 0, -1, 0, -1, 0, -1, 0, -1],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
                           [0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
                           [1, 0, 1, 0, 1, 0, 1, 0, 1, 0]]

        self.white_checker = PhotoImage(file="white_checker.png")
        self.black_checker = PhotoImage(file="black_checker.png")
        self.white_queen = PhotoImage(file="white_queen.png")
        self.black_queen = PhotoImage(file="black_queen.png")
        self.capture_pic = PhotoImage(file="capture.png")

        self.white_move = True
        self.black_move = False
        self.first_move = True
        self.move_without_attack = False

    # Методы для регистрации и авторизации

    def authorization(self):
        login = self.entry_login.get()
        password_raw = self.entry_password.get()
        password = password_code(password_raw)

        if len(login) == 0 and len(password) == 0:
            messagebox.showwarning(title="Ошибка", message="Введите логин и пароль")

        elif len(login) == 0 and len(password) != 0:
            messagebox.showwarning(title="Ошибка", message="Введите логин")

        elif len(login) != 0 and len(password) == 0:
            messagebox.showwarning(title="Ошибка", message="Введите пароль")

        else:
            file = open_file()
            a = file.readline()[:-1].split(" ")

            while True:
                if a != [""]:
                    self.users[a[0]] = a[1]
                    a = file.readline()[:-1].split(" ")
                else:
                    break

            flag_reg = False
            for i in self.users.items():
                login_check, password_check = i
                if login == login_check and password == password_check:
                    flag_reg = True
                    break

            if flag_reg:
                for widget in self.main.winfo_children():
                    widget.destroy()

                Label(self.main, text="Вы успешно авторизировались!", font="Arial 16 bold").place(x=175, y=60)
                button = ttk.Button(self.main, text="Играть", style="my.TButton", command=self.drawing_deck)
                button.place(x=290, y=170)

            else:
                messagebox.showwarning(title="Ошибка", message="Неверный логин или пароль")

    def registrate(self):
        login = self.entry_login.get()
        password_raw = self.entry_password.get()
        password = password_code(password_raw)

        if len(login) == 0 and len(password) == 0:
            messagebox.showwarning(title="Ошибка", message="Введите желаемые логин и пароль")

        elif len(login) == 0 and len(password) != 0:
            messagebox.showwarning(title="Ошибка", message="Введите логин")

        elif len(login) != 0 and len(password) == 0:
            messagebox.showwarning(title="Ошибка", message="Введите пароль")

        else:
            file = open_file()
            temp = file.readline()[:-1].split(' ')

            while True:
                if temp != [""]:
                    self.users[temp[0]] = temp[1]
                    temp = file.readline()[:-1].split(' ')
                else:
                    break

            flag_reg = False

            for i in self.users.items():
                l, p = i
                if login == l:
                    flag_reg = True

            if not flag_reg:
                file = open_file()
                file.seek(0, os.SEEK_END)
                file.write(f'{login} {password}\n')
                file.close()

                for widget in self.main.winfo_children():
                    widget.destroy()

                Label(self.main, text=f"Вы успешно зарегистрировались!\nВаш логин: {login}\nВаш пароль: {password_raw}", font="Arial 16 bold").place(x=155, y=60)
                button = ttk.Button(self.main, text="Играть", style="my.TButton", command=self.drawing_deck)
                button.place(x=290, y=170)
            else:
                messagebox.showwarning(title="Ошибка", message="Такой аккаунт уже существует")

    # Метод для вывода доски

    def drawing_deck(self):
        self.main.title("80-Поддавки")
        self.main.geometry("800x640+100+100")
        cell_sz = 80
        row = 8
        col = 10

        self.deck = Canvas(self.main, width=cell_sz * col, height=cell_sz * row)
        cell_colors = ["#FFDDBB", "#552B00"]
        color_index = 0

        for rows in range(row):
            for cols in range(col):
                x1, y1 = cols * cell_sz, rows * cell_sz
                x2, y2 = cols * cell_sz + cell_sz, rows * cell_sz + cell_sz
                self.deck.create_rectangle(x1, y1, x2, y2, fill=cell_colors[color_index])

                color_index = not color_index

            color_index = not color_index

        for rows in range(row):
            for cols in range(col):
                x1, y1 = cols * cell_sz, rows * cell_sz
                cell = self.deck_model[rows][cols]
                if cell < 0:
                    if cell == -1:
                        self.deck.create_image(x1 + 8, y1 + 8, anchor="nw", image=self.black_checker)
                    else:
                        pass

                elif cell > 0:
                    if cell == 1:
                        self.deck.create_image(x1 + 8, y1 + 8, anchor="nw", image=self.white_checker)
                    else:
                        pass

        self.deck.pack()
        self.user_interact()

    # Метод для отрисовки ходов

    def drawing_move(self):
        self.deck.delete("all")
        cell_colors = ["#FFDDBB", "#552B00"]
        color_index = 0
        cell_sz = 80
        row = 8
        col = 10

        for rows in range(row):
            for cols in range(col):
                x1, y1 = cols * cell_sz, rows * cell_sz
                x2, y2 = cols * cell_sz + cell_sz, rows * cell_sz + cell_sz
                self.deck.create_rectangle(x1, y1, x2, y2, fill=cell_colors[color_index])

                color_index = not color_index

            color_index = not color_index

        for rows in range(row):
            for cols in range(col):
                x1, y1 = cols * cell_sz, rows * cell_sz
                cell = self.deck_model[rows][cols]
                if cell < 0:
                    if cell == -1:
                        self.deck.create_image(x1 + 8, y1 + 8, anchor="nw", image=self.black_checker)
                    elif cell == -2:
                        self.deck.create_image(x1 + 8, y1 + 8, anchor="nw", image=self.black_queen)

                elif cell > 0:
                    if cell == 1:
                        self.deck.create_image(x1 + 8, y1 + 8, anchor="nw", image=self.white_checker)
                    elif cell == 2:
                        self.deck.create_image(x1 + 8, y1 + 8, anchor="nw", image=self.white_queen)

        self.deck.pack()

    # Метод для взаимодействия с пользователями

    def user_interact(self):
        self.x1 = 0
        self.y1 = 0
        self.x2 = 0
        self.y2 = 0

        def queen_check(x2, y2):
            if self.white_move:
                if self.x2 == 0:
                    self.deck_model[x2][y2] = 2
            else:
                if self.x2 == 7:
                    self.deck_model[x2][y2] = -2

        def attack_check(x1, y1, x2, y2):
            coord_checker_user = [x1, y1, x2, y2]
            coord_checker = []
            if self.white_move:
                flag_white_attack = False
                for x in range(8):
                    for y in range(10):
                        if self.deck_model[x][y] == 1:
                            for i, j in (1, -1), (-1, 1), (-1, -1), (1, 1):
                                if 0 <= (x + i) <= 7 and 0 <= (y + j) <= 9:
                                    if self.deck_model[x + i][y + j] == -1 or self.deck_model[x + i][y + j] == -2:
                                        if 0 <= (x + i * 2) <= 7 and 0 <= (y + j * 2) <= 9:
                                            if self.deck_model[x + i + i][y + j + j] == 0:
                                                flag_white_attack = True
                                                coord_checker.append([x, y, x + i + i, y + j + j])

                        elif self.deck_model[x][y] == 2:
                            for d in range(4):
                                h = 0
                                if d == 0:
                                    i = 1
                                    j = 1
                                elif d == 1:
                                    i = 1
                                    j = -1
                                elif d == 2:
                                    i = -1
                                    j = 1
                                elif d == 3:
                                    i = -1
                                    j = -1
                                while 0 <= x + (i * h) + i <= 7 and 0 <= y + (j * h) + j <= 9:
                                    if self.deck_model[x + (i * h)][y + (j * h)] == -1 or \
                                            self.deck_model[x + (i * h)][y + (j * h)] == -2:
                                        if self.deck_model[x + (i * h) + i][y + (j * h) + j] == 0:
                                            flag_white_attack = True
                                            h += 1
                                            while 0 <= x + (i * h) <= 7 and 0 <= y + (j * h) <= 9:
                                                if self.deck_model[x + (i * h)][y + (j * h)] == 0:
                                                    coord_checker.append([x, y, x + (i * h), y + (j * h)])
                                                else:
                                                    break
                                                h += 1
                                        else:
                                            break
                                    h += 1

                if not flag_white_attack:
                    return True
                else:
                    if coord_checker_user in coord_checker:
                        return True

            else:
                flag_black_attack = False
                for x in range(8):
                    for y in range(10):
                        if self.deck_model[x][y] == -1:
                            for i, j in (1, -1), (-1, 1), (-1, -1), (1, 1):
                                if 0 <= (x + i) <= 7 and 0 <= (y + j) <= 9:
                                    if self.deck_model[x + i][y + j] == 1 or self.deck_model[x + i][y + j] == 2:
                                        if 0 <= (x + i * 2) <= 7 and 0 <= (y + j * 2) <= 9:
                                            if self.deck_model[x + i + i][y + j + j] == 0:
                                                flag_black_attack = True
                                                coord_checker.append([x, y, x + i + i, y + j + j])
                        elif self.deck_model[x][y] == -2:
                            for d in range(4):
                                h = 0
                                if d == 0:
                                    i = 1
                                    j = 1
                                elif d == 1:
                                    i = 1
                                    j = -1
                                elif d == 2:
                                    i = -1
                                    j = 1
                                elif d == 3:
                                    i = -1
                                    j = -1
                                while 0 <= x + (i * h) + i <= 7 and 0 <= y + (j * h) + j <= 9:
                                    if self.deck_model[x + (i * h)][y + (j * h)] == 1 or \
                                            self.deck_model[x + (i * h)][y + (j * h)] == 2:
                                        if self.deck_model[x + (i * h) + i][y + (j * h) + j] == 0:
                                            flag_black_attack = True
                                            h += 1
                                            while 0 <= x + (i * h) <= 7 and 0 <= y + (j * h) <= 9:
                                                if self.deck_model[x + (i * h)][y + (j * h)] == 0:
                                                    coord_checker.append([x, y, x + (i * h), y + (j * h)])
                                                else:
                                                    break
                                                h += 1
                                        else:
                                            break
                                    h += 1

                if not flag_black_attack:
                    return True
                else:
                    if coord_checker_user in coord_checker:
                        return True
                    else:
                        return False

        def multijump_check(x2, y2):
            if self.white_move:
                if self.deck_model[x2][y2] == 1:
                    for i, j in (1, -1), (-1, 1), (-1, -1), (1, 1):
                        if 0 < (x2 + i) < 7 and 0 < (y2 + j) < 9:
                            if self.deck_model[x2 + i][y2 + j] == -1 or self.deck_model[x2 + i][y2 + j] == -2:
                                if 0 <= (x2 + i * 2) <= 7 and 0 <= (y2 + j * 2) <= 9:
                                    if self.deck_model[x2 + i + i][y2 + j + j] == 0:
                                        return True
                elif self.deck_model[x2][y2] == 2:
                    for d in range(4):
                        if d == 0:
                            i = 1
                            j = 1
                        elif d == 1:
                            i = 1
                            j = -1
                        elif d == 2:
                            i = -1
                            j = 1
                        elif d == 3:
                            i = -1
                            j = -1
                        for h in range(1, 9):
                            if 0 < x2 + (i * h) < 7 and 0 < y2 + (j * h) < 9:
                                if self.deck_model[x2 + (i * h)][y2 + (j * h)] == -1 or \
                                        self.deck_model[x2 + (i * h)][y2 + (j * h)] == -2:
                                    if self.deck_model[x2 + (i * h) + i][y2 + (j * h) + j] == 0:
                                        return True
                                    else:
                                        break
                            else:
                                break

            else:
                if self.deck_model[x2][y2] == -1:
                    for i, j in (1, -1), (-1, 1), (-1, -1), (1, 1):
                        if 0 < (x2 + i) < 7 and 0 < (y2 + j) < 9:
                            if self.deck_model[x2 + i][y2 + j] == 1 or self.deck_model[x2 + i][y2 + j] == 2:
                                if 0 <= (x2 + i * 2) <= 7 and 0 <= (y2 + j * 2) <= 9:
                                    if self.deck_model[x2 + i + i][y2 + j + j] == 0:
                                        return True
                elif self.deck_model[x2][y2] == -2:
                    for d in range(4):
                        if d == 0:
                            i = 1
                            j = 1
                        elif d == 1:
                            i = 1
                            j = -1
                        elif d == 2:
                            i = -1
                            j = 1
                        elif d == 3:
                            i = -1
                            j = -1
                        for h in range(1, 9):
                            if 0 < x2 + (i * h) < 7 and 0 < y2 + (j * h) < 9:
                                if self.deck_model[x2 + (i * h)][y2 + (j * h)] == 1 or \
                                        self.deck_model[x2 + (i * h)][y2 + (j * h)] == 2:
                                    if self.deck_model[x2 + (i * h) + i][y2 + (j * h) + j] == 0:
                                        return True
                                    else:
                                        break
                            else:
                                break
            return False

        def move_check(x1, y1, x2, y2):
            self.move_without_attack = False
            if self.deck_model[x2][y2] != 0:
                messagebox.showwarning(title="Внимание", message="Такой ход невозможен")
                return False

            if self.deck_model[x1][y1] == 2 or self.deck_model[x1][y1] == -2:
                if abs(x1 - x2) == abs(y1 - y2):
                    count_checker_queen = 0
                    coord_checker = []
                    i = 0
                    j = 0

                    if x1 < x2:
                        i = 1
                    elif x2 < x1:
                        i = -1
                    if y1 < y2:
                        j = 1
                    elif y2 < y1:
                        j = -1

                    for h in range(1, abs(x2 - x1) + 1):
                        if self.deck_model[x1 + (i * h)][y1 + (j * h)] == 1 or self.deck_model[x1 + (i * h)][y1 + (j * h)] == 2:
                            if self.deck_model[x1][y1] == 2:
                                messagebox.showwarning(title="Внимание", message="Такой ход невозможен")
                                return False
                            else:
                                count_checker_queen += 1
                                coord_checker = [x1 + (i * h), y1 + (j * h)]

                        if self.deck_model[x1 + (i * h)][y1 + (j * h)] == -1 or self.deck_model[x1 + (i * h)][y1 + (j * h)] == -2:
                            if self.deck_model[x1][y1] == -2:
                                messagebox.showwarning(title="Внимание", message="Такой ход невозможен")
                                return False
                            else:
                                count_checker_queen += 1
                                coord_checker = [x1 + (i * h), y1 + (j * h)]
                    if count_checker_queen == 1:
                        self.deck_model[coord_checker[0]][coord_checker[1]] = 0
                        self.deck_model[x2][y2] = self.deck_model[x1][y1]
                        self.deck_model[x1][y1] = 0
                        return True

                    elif count_checker_queen > 1:
                        messagebox.showwarning(title="Внимание", message="Такой ход невозможен")
                        return False

                    else:
                        if attack_check(self.x1, self.y1, self.x2, self.y2):
                            self.deck_model[x2][y2] = self.deck_model[x1][y1]
                            self.deck_model[x1][y1] = 0
                            self.move_without_attack = True
                            return True
                        else:
                            messagebox.showwarning(title="Внимание", message="Вы обязаны забрать шашку противника")
                            return False

            else:
                if abs(x2 - x1) == 1 and abs(y2 - y1) == 1:
                    if self.black_move:
                        if x2 < x1 and self.deck_model[x1][y1] == -1:
                            messagebox.showwarning(title="Внимание", message="Такой ход невозможен")
                            return False
                    elif self.white_move:
                        if x1 < x2 and self.deck_model[x1][y1] == 1:
                            messagebox.showwarning(title="Внимание", message="Такой ход невозможен")
                            return False
                    if attack_check(self.x1, self.y1, self.x2, self.y2):
                        self.deck_model[x2][y2] = self.deck_model[x1][y1]
                        self.deck_model[x1][y1] = 0
                        self.move_without_attack = True
                        return True
                    else:
                        messagebox.showwarning(title="Внимание", message="Вы обязаны забрать шашку противника")
                        return False

                elif abs(x2 - x1) == 2 and abs(y2 - y1) == 2:
                    if self.deck_model[(x1 + x2) // 2][(y1 + y2) // 2] == 0 or self.deck_model[(x1 + x2) // 2][(y1 + y2) // 2] == self.deck_model[x1][y1]:
                        messagebox.showwarning(title="Внимание", message="Такой ход невозможен")
                        return False
                    self.deck_model[x2][y2] = self.deck_model[x1][y1]
                    self.deck_model[x1][y1] = 0
                    self.deck_model[(x1 + x2) // 2][(y1 + y2) // 2] = 0
                    return True
            messagebox.showwarning(title="Внимание", message="Такой ход невозможен")
            return False

        def click_event_captured(event):
            if 0 < event.x < 800 and 0 < event.y < 640:
                self.y2 = event.x // 80
                self.x2 = event.y // 80
                if self.first_move:
                    if self.x1 == self.x2 and self.y1 == self.y2:
                        self.main.bind("<Button-1>", click_event)
                        self.drawing_move()

                    else:
                        if move_check(self.x1, self.y1, self.x2, self.y2):
                            queen_check(self.x2, self.y2)
                            self.drawing_move()
                            if not self.move_without_attack:
                                if multijump_check(self.x2, self.y2):
                                    self.check_end()
                                    self.first_move = False
                                    self.x1, self.y1 = self.x2, self.y2
                                    self.deck.create_image(self.y1 * 80, self.x1 * 80, anchor="nw",
                                                           image=self.capture_pic)
                                    self.main.bind("<Button-1>", click_event_captured)
                                else:
                                    self.white_move, self.black_move = not self.white_move, not self.black_move
                                    self.check_end()
                                    self.user_interact()
                            else:
                                self.white_move, self.black_move = not self.white_move, not self.black_move
                                self.check_end()
                                self.user_interact()

                elif not self.first_move:
                    if move_check(self.x1, self.y1, self.x2, self.y2) and not self.move_without_attack:
                        queen_check(self.x2, self.y2)
                        self.drawing_move()
                        if multijump_check(self.x2, self.y2):
                            self.check_end()
                            self.x1, self.y1 = self.x2, self.y2
                            self.deck.create_image(self.y1 * 80, self.x1 * 80, anchor="nw", image=self.capture_pic)
                            self.main.bind("<Button-1>", click_event_captured)
                        else:
                            self.drawing_move()
                            self.first_move = True
                            self.white_move, self.black_move = not self.white_move, not self.black_move
                            self.check_end()
                            self.user_interact()

        def click_event(event):
            if 0 < event.x < 800 and 0 < event.y < 640:

                self.y1 = event.x // 80
                self.x1 = event.y // 80

                if self.white_move and (self.deck_model[self.x1][self.y1] == 1 or self.deck_model[self.x1][self.y1] == 2):
                    self.deck.create_image(self.y1 * 80, self.x1 * 80, anchor="nw", image=self.capture_pic)
                    self.main.bind("<Button-1>", click_event_captured)

                elif self.black_move and (self.deck_model[self.x1][self.y1] == -1 or self.deck_model[self.x1][self.y1] == -2):
                    self.deck.create_image(self.y1 * 80, self.x1 * 80, anchor="nw", image=self.capture_pic)
                    self.main.bind("<Button-1>", click_event_captured)

        self.main.bind("<Button-1>", click_event)

    # Метод для проверки окончания игры

    def check_end(self):
        flag_white_move = False
        flag_black_move = False
        for x in range(8):
            for y in range(10):
                if self.deck_model[x][y] == 1 or self.deck_model[x][y] == 2:
                    for i, j in (1, -1), (-1, 1), (-1, -1), (1, 1):
                        if 0 <= (x + i) <= 7 and 0 <= (y + j) <= 9:

                            if self.deck_model[x + i][y + j] == -1 or self.deck_model[x + i][y + j] == -2:
                                if 0 <= (x + i * 2) <= 7 and 0 < (y + j * 2) <= 9:
                                    if self.deck_model[x + i + i][y + j + j] == 0:
                                        flag_white_move = True
                                        break
                            elif self.deck_model[x + i][y + j] == 0:
                                if self.deck_model[x][y] == 1:
                                    if x > x + i:
                                        flag_white_move = True
                                        break
                                else:
                                    flag_white_move = True
                                    break

                elif self.deck_model[x][y] == -1 or self.deck_model[x][y] == -2:
                    for i, j in (1, -1), (-1, 1), (-1, -1), (1, 1):
                        if 0 <= (x + i) <= 7 and 0 <= (y + j) <= 9:
                            if self.deck_model[x + i][y + j] == 1 or self.deck_model[x + i][y + j] == 2:
                                if 0 <= (x + i * 2) <= 7 and 0 <= (y + j * 2) <= 9:
                                    if self.deck_model[x + i + i][y + j + j] == 0:
                                        flag_black_move = True
                                        break
                            elif self.deck_model[x + i][y + j] == 0:
                                if self.deck_model[x][y] == -1:
                                    if x < x + i:
                                        flag_black_move = True
                                        break
                                else:
                                    flag_black_move = True
                                    break

        if not flag_white_move:
            self.end_game("Белых")
        elif not flag_black_move:
            self.end_game("Чёрных")
        elif not flag_white_move and not flag_black_move:
            self.end_game("Ничья")

    # Метод для вывода результатов окончания игры

    def end_game(self, winner):
        def next_game():
            self.white_move = True
            self.black_move = False
            self.first_move = True

            self.deck_model = [[0, -1, 0, -1, 0, -1, 0, -1, 0, -1],
                               [-1, 0, -1, 0, -1, 0, -1, 0, -1, 0],
                               [0, -1, 0, -1, 0, -1, 0, -1, 0, -1],
                               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                               [1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
                               [0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
                               [1, 0, 1, 0, 1, 0, 1, 0, 1, 0]]

            self.drawing_move()

        winner_window = Tk()
        winner_window.geometry("150x150+150+150")
        winner_window.protocol('WM_DELETE_WINDOW', lambda: dismiss(winner_window))
        winner_window.grab_set()

        if winner == "Ничья":
            Label(winner_window, text="Ничья").pack()
        else:
            Label(winner_window, text=f"Победа {winner}").pack()
        ttk.Button(winner_window, text="Заново", command=lambda: (next_game(), winner_window.grab_release(), winner_window.destroy())).pack()


root = Tk()
root.title("Авторизация")
root.geometry("720x360-100-100")
icon = PhotoImage(file="checkers_icon_app.png")
root.iconphoto(True, icon)
root.resizable(False, False)

Checkers(root)

root.mainloop()
