import socket
import threading
import tkinter as tk
from tkinter import scrolledtext, simpledialog

HOST = '127.0.0.1'
PORT = 55555

nickname = simpledialog.askstring("Nickname", "Choose your nickname:")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

def receive():
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            if message == 'NICK':
                client.send(nickname.encode('utf-8'))
            else:
                chat_area.config(state=tk.NORMAL)
                chat_area.insert(tk.END, message + '\n')
                chat_area.config(state=tk.DISABLED)
                chat_area.see(tk.END)
        except:
            print("An error occurred!")
            client.close()
            break

def write():
    message = f"{nickname}: {input_area.get()}"
    client.send(message.encode('utf-8'))
    input_area.delete(0, tk.END)

# GUI
root = tk.Tk()
root.title(f"Chat - {nickname}")
root.geometry("400x500")

chat_area = scrolledtext.ScrolledText(root)
chat_area.pack(padx=20, pady=5, fill=tk.BOTH, expand=True)
chat_area.config(state=tk.DISABLED)

input_area = tk.Entry(root)
input_area.pack(padx=20, pady=5, fill=tk.X)

send_button = tk.Button(root, text="Send", command=write)
send_button.pack(padx=20, pady=5)

# Threads
receive_thread = threading.Thread(target=receive)
receive_thread.start()

root.mainloop()
