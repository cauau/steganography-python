from tkinter import Tk, Label, Button, Entry, Text, filedialog
import os

from Source_code import encode_in_image, extract_from_image


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Steganography Tool")
        self.root.geometry("650x520")

        self.image_path = ""

        Label(root, text="Mensagem:").pack(pady=5)
        self.message_entry = Entry(root, width=70)
        self.message_entry.pack(pady=5)

        Label(root, text="Senha:").pack(pady=5)
        self.password_entry = Entry(root, width=70, show="*")
        self.password_entry.pack(pady=5)

        Button(root, text="Selecionar Imagem PNG", command=self.select_image).pack(pady=8)
        Button(root, text="Criptografar", command=self.encrypt).pack(pady=8)

        self.status = Label(root, text="")
        self.status.pack(pady=8)

        Button(root, text="Selecionar Imagem Criptografada", command=self.select_image).pack(pady=8)
        Button(root, text="Descriptografar", command=self.decrypt).pack(pady=8)

        Label(root, text="Mensagem recuperada:").pack(pady=5)
        self.output = Text(root, height=8, width=70)
        self.output.pack(pady=10)

    def select_image(self):
        path = filedialog.askopenfilename(
            title="Selecione uma imagem PNG",
            filetypes=[("PNG files", "*.png")]
        )
        if path:
            self.image_path = path
            self.status.config(text=f"Imagem selecionada: {os.path.basename(path)}")

    def encrypt(self):
        try:
            message = self.message_entry.get()
            password = self.password_entry.get()

            if not message:
                self.status.config(text="Digite uma mensagem.")
                return

            if not password:
                self.status.config(text="Digite uma senha.")
                return

            if not self.image_path:
                self.status.config(text="Selecione uma imagem PNG.")
                return

            folder, name = os.path.split(self.image_path)
            new_name = os.path.splitext(name)[0] + "_encoded.png"
            output_path = os.path.join(folder, new_name)

            encoded_image = encode_in_image(self.image_path, message, password)
            encoded_image.save(output_path, "PNG")

            self.status.config(text=f"Imagem salva como: {new_name}")

        except Exception as e:
            self.status.config(text=f"Erro: {e}")

    def decrypt(self):
        try:
            password = self.password_entry.get()

            if not password:
                self.status.config(text="Digite a senha para descriptografar.")
                return

            if not self.image_path:
                self.status.config(text="Selecione a imagem criptografada.")
                return

            message = extract_from_image(self.image_path, password)

            self.output.delete("1.0", "end")
            self.output.insert("end", message)

            self.status.config(text="Mensagem recuperada com sucesso.")

        except Exception as e:
            self.status.config(text=f"Erro: {e}")


if __name__ == "__main__":
    root = Tk()
    app = App(root)
    root.mainloop()