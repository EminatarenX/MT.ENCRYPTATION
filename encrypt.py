import tkinter as tk
from tkinter import messagebox

class TuringEncryption:
    def __init__(self):
        self.key_array = [7, 13, 17, 23, 29, 31, 37, 41, 43, 47]
        self.chars = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
        self.substitution_map = {
            self.chars[i]: self.chars[(i + 7) % len(self.chars)] 
            for i in range(len(self.chars))
        }
    def is_valid_input(self, text):
        return all(char in self.chars for char in text)

    def apply_transformation(self, char, position):
        if char in self.chars:
            idx = self.chars.index(char)
            key = self.key_array[position % 10]
            new_idx = (idx + key) % len(self.chars)
            return self.chars[new_idx]
        return char

    def reverse_transformation(self, char, position):
        if char in self.chars:
            idx = self.chars.index(char)
            key = self.key_array[position % 10]
            new_idx = (idx - key) % len(self.chars)
            return self.chars[new_idx]
        return char

    def encrypt(self, text):
        if not text or not self.is_valid_input(text):
            raise ValueError("El texto solo debe contener letras y números")
        transformed = ""
        for i, char in enumerate(text):
            transformed += self.apply_transformation(char, i)
        encrypted = ""
        for char in transformed:
            encrypted += self.substitution_map.get(char, char)
        final = "E#" + encrypted + "#E"
        return final

    def decrypt(self, encrypted):
        if not encrypted or len(encrypted) < 4:
            raise ValueError("Texto encriptado inválido")
        if not (encrypted.startswith("E#") and encrypted.endswith("#E")):
            raise ValueError("Formato de encriptación inválido")
        encrypted = encrypted[2:-2]
        reverse_sub_map = {v: k for k, v in self.substitution_map.items()}
        unsubstituted = ""
        for char in encrypted:
            unsubstituted += reverse_sub_map.get(char, char)
        final = ""
        for i, char in enumerate(unsubstituted):
            final += self.reverse_transformation(char, i)

        return final

class EncryptionGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Encriptador MT Alfanumérico")
        self.encryptor = TuringEncryption()
        self.setup_gui()

    def setup_gui(self):
        main_frame = tk.Frame(self.root, padx=20, pady=20)
        main_frame.pack(expand=True, fill='both')

        tk.Label(main_frame, text="Ingrese texto (solo letras y números):").grid(row=0, column=0, sticky='w', pady=5)
        self.entry_password = tk.Entry(main_frame, width=40, show="*")
        self.entry_password.grid(row=0, column=1, columnspan=2, pady=5)

        self.show_password_var = tk.BooleanVar()
        tk.Checkbutton(main_frame, text="Mostrar texto", 
                      variable=self.show_password_var, 
                      command=self.toggle_password_visibility).grid(row=1, column=0, pady=5)

        btn_frame = tk.Frame(main_frame)
        btn_frame.grid(row=2, column=0, columnspan=3, pady=10)
        
        tk.Button(btn_frame, text="Encriptar", 
                 command=self.encrypt_action, width=15).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Desencriptar", 
                 command=self.decrypt_action, width=15).pack(side=tk.LEFT, padx=5)

        tk.Label(main_frame, text="Resultado:").grid(row=3, column=0, sticky='w', pady=5)
        self.entry_result = tk.Entry(main_frame, width=40)
        self.entry_result.grid(row=3, column=1, columnspan=2, pady=5)

        tk.Button(main_frame, text="Copiar Resultado", 
                 command=self.copy_result).grid(row=4, column=1, pady=10)

    def toggle_password_visibility(self):
        if self.show_password_var.get():
            self.entry_password.config(show="")
        else:
            self.entry_password.config(show="*")

    def encrypt_action(self):
        try:
            text = self.entry_password.get().strip()
            if not text:
                messagebox.showwarning("Advertencia", "Por favor ingrese texto para encriptar.")
                return
            encrypted = self.encryptor.encrypt(text)
            self.entry_result.delete(0, tk.END)
            self.entry_result.insert(0, encrypted)
        except ValueError as ve:
            messagebox.showerror("Error", str(ve))
        except Exception as e:
            messagebox.showerror("Error", f"Error durante la encriptación: {str(e)}")

    def decrypt_action(self):
        try:
            text = self.entry_password.get().strip()
            if not text:
                messagebox.showwarning("Advertencia", "Por favor ingrese texto para desencriptar.")
                return
            decrypted = self.encryptor.decrypt(text)
            self.entry_result.delete(0, tk.END)
            self.entry_result.insert(0, decrypted)
        except ValueError as ve:
            messagebox.showerror("Error", str(ve))
        except Exception as e:
            messagebox.showerror("Error", f"Error durante la desencriptación: {str(e)}")

    def copy_result(self):
        result = self.entry_result.get()
        if result:
            self.root.clipboard_clear()
            self.root.clipboard_append(result)
            messagebox.showinfo("Éxito", "Resultado copiado al portapapeles")
        else:
            messagebox.showwarning("Advertencia", "No hay resultado para copiar")

if __name__ == "__main__":
    root = tk.Tk()
    app = EncryptionGUI(root)
    root.mainloop()
