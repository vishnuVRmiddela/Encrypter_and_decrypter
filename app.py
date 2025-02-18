import os
import base64
from cryptography.fernet import Fernet
from tkinter import Tk, Label, Entry, Button, filedialog, messagebox

class FileEncrypterDecrypter:
    def __init__(self, root):
        self.root = root
        self.root.title("File Encrypter and Decrypter")

        # Key Entry
        self.label_key = Label(root, text="Encryption Key:")
        self.label_key.grid(row=0, column=0, padx=10, pady=10)
        self.entry_key = Entry(root, width=50, show="*")
        self.entry_key.grid(row=0, column=1, padx=10, pady=10)

        # Generate Key Button
        self.generate_key_button = Button(root, text="Generate Key", command=self.generate_key)
        self.generate_key_button.grid(row=0, column=2, padx=10, pady=10)

        # File Path Entry
        self.label_file = Label(root, text="File Path:")
        self.label_file.grid(row=1, column=0, padx=10, pady=10)
        self.entry_file = Entry(root, width=50)
        self.entry_file.grid(row=1, column=1, padx=10, pady=10)
        self.browse_button = Button(root, text="Browse", command=self.browse_file)
        self.browse_button.grid(row=1, column=2, padx=10, pady=10)

        # Encrypt Button
        self.encrypt_button = Button(root, text="Encrypt File", command=self.encrypt_file)
        self.encrypt_button.grid(row=2, column=0, columnspan=3, pady=10)

        # Decrypt Button
        self.decrypt_button = Button(root, text="Decrypt File", command=self.decrypt_file)
        self.decrypt_button.grid(row=3, column=0, columnspan=3, pady=10)

    def generate_key(self):
        key = Fernet.generate_key()
        self.entry_key.delete(0, 'end')
        self.entry_key.insert(0, base64.urlsafe_b64encode(key).decode())

    def browse_file(self):
        file_path = filedialog.askopenfilename()
        self.entry_file.delete(0, 'end')
        self.entry_file.insert(0, file_path)

    def encrypt_file(self):
        key = self.entry_key.get()
        file_path = self.entry_file.get()

        if not key or not file_path:
            messagebox.showwarning("Warning", "Please fill in both fields.")
            return

        try:
            fernet = Fernet(base64.urlsafe_b64decode(key))
            with open(file_path, 'rb') as file:
                original = file.read()
            encrypted = fernet.encrypt(original)
            with open(file_path, 'wb') as encrypted_file:
                encrypted_file.write(encrypted)
            messagebox.showinfo("Success", "File encrypted successfully.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def decrypt_file(self):
        key = self.entry_key.get()
        file_path = self.entry_file.get()

        if not key or not file_path:
            messagebox.showwarning("Warning", "Please fill in both fields.")
            return

        try:
            fernet = Fernet(base64.urlsafe_b64decode(key))
            with open(file_path, 'rb') as encrypted_file:
                encrypted = encrypted_file.read()
            decrypted = fernet.decrypt(encrypted)
            with open(file_path, 'wb') as decrypted_file:
                decrypted_file.write(decrypted)
            messagebox.showinfo("Success", "File decrypted successfully.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

if __name__ == "__main__":
    root = Tk()
    app = FileEncrypterDecrypter(root)
    root.mainloop()