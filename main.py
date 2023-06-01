import tkinter as tk
from tkinter import messagebox

root = tk.Tk()
root.title("Программа с окном авторизации")
root.geometry("300x100")


def check_password():
    login = login_entry.get()
    password = password_entry.get()
    with open("passwords.txt", "r") as file:
        lines = file.readlines()
        for line in lines:
            line_login, line_password = line.split()
            if login == line_login and password == line_password:
                root.destroy()
                main_window = tk.Tk()
                main_window.title("Главное окно")
                main_window.geometry("500x400")
                label = tk.Label(main_window, text=f"Добро пожаловать, {login}!")
                label.pack()

                def open_history():
                    history_window = tk.Toplevel(main_window)
                    history_window.title("История")
                    history_window.geometry("300x200")

                    def go_back():
                        history_window.destroy()
                        main_window.deiconify()

                    def open_details(data):
                        details_window = tk.Toplevel(history_window)
                        details_window.title("Подробности заявления")
                        details_window.geometry("300x200")

                        category, room_number, email, reason = data.split("; ")

                        category_label = tk.Label(details_window, text=f"Категория: {category}")
                        category_label.pack()
                        room_number_label = tk.Label(details_window, text=f"Номер комнаты: {room_number}")
                        room_number_label.pack()
                        email_label = tk.Label(details_window, text=f"Электронная почта: {email}")
                        email_label.pack()
                        reason_label = tk.Label(details_window, text=f"Причина заявления: {reason}")
                        reason_label.pack()

                    with open("applications.txt", "r") as file:
                        lines = file.readlines()
                        for line in lines:
                            line = line.strip()
                            category, room_number = line.split("; ")[:2]
                            application_button = tk.Button(history_window, text=f"{room_number} {category}", command=lambda d=line: open_details(d))
                            application_button.pack()
                    instruction_label = tk.Label(history_window, text="Нажмите на кнопку с нужным заявлением для просмотра подробностей")
                    instruction_label.pack()
                    back_button = tk.Button(history_window, text="Назад", command=go_back)
                    back_button.pack(side=tk.BOTTOM)

                def log_out():
                    main_window.destroy()
                    root.deiconify()

                def open_application(work):
                    application_window = tk.Toplevel(main_window)
                    application_window.title(f"Заявление на проведение {work}")
                    application_window.geometry("500x400")

                    def go_back():
                        application_window.destroy()
                        main_window.deiconify()

                    def send_application():

                        reason = reason_entry.get()
                        email = email_entry.get()
                        room_number = room_number_entry.get()
                        if len(room_number) == 5 and room_number[2] == "-":
                            with open("applications.txt", "a") as file:
                                file.write(f"{work}; {room_number}; {email}; {reason}\n")
                            application_window.destroy()
                            main_window.deiconify()
                            messagebox.showinfo("Успех", "Ваше заявление успешно отправлено")
                        else:
                            messagebox.showerror("Ошибка", "Неверный формат номера комнаты. Должно быть 00-00")
                    instruction_label = tk.Label(application_window, text="Заполните форму заявления")
                    instruction_label.pack()
                    reason_label = tk.Label(application_window, text="Причина заявления:")
                    reason_label.pack()
                    reason_entry = tk.Entry(application_window, width=60)
                    reason_entry.pack()
                    email_label = tk.Label(application_window, text="Электронная почта:")
                    email_label.pack()
                    email_entry = tk.Entry(application_window)
                    email_entry.pack()
                    room_number_label = tk.Label(application_window, text="Номер комнаты:")
                    room_number_label.pack()
                    room_number_entry = tk.Entry(application_window)
                    room_number_entry.pack()
                    send_button = tk.Button(application_window, text="Отправить", command=send_application)
                    send_button.pack(side=tk.RIGHT)
                    back_button = tk.Button(application_window, text="Назад", command=go_back)
                    back_button.pack(side=tk.LEFT)
                history_button = tk.Button(main_window, text="История", command=open_history)
                history_button.pack(side=tk.LEFT)
                logout_button = tk.Button(main_window, text="Выйти", command=log_out)
                logout_button.pack(side=tk.RIGHT)
                works = ["сантехнических", "электромонтажных", "дезинфекции", "дератизации", "столярных", "других"]
                for work in works:
                    application_button = tk.Button(main_window, text=f"Оставить заявление на проведение {work} работ", command=lambda w=work: open_application(w))
                    application_button.pack()
                return
    messagebox.showerror("Ошибка", "Неверный логин или пароль")


instruction_label = tk.Label(root, text="Введите логин и пароль")
instruction_label.pack()

login_entry = tk.Entry(root)
login_entry.pack()

password_entry = tk.Entry(root, show="*")
password_entry.pack()

login_button = tk.Button(root, text="Войти", command=check_password)
login_button.pack()

root.mainloop()
