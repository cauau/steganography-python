# 🔐 Steganography Tool (Python)

Aplicação em Python para esconder mensagens dentro de imagens PNG utilizando esteganografia (LSB) com criptografia baseada em senha.

---

## 🚀 Funcionalidades

* Esconde mensagens em imagens PNG
* Criptografa a mensagem com senha (Fernet + SHA256)
* Recupera e descriptografa a mensagem
* Interface gráfica com Tkinter

---

## 🧠 Como funciona

1. A mensagem é criptografada usando uma senha
2. O texto criptografado é convertido em bits
3. Os bits são inseridos nos pixels da imagem (LSB)
4. Para recuperar:

   * Os bits são lidos da imagem
   * A mensagem é reconstruída
   * A senha descriptografa o conteúdo

---

## ⚙️ Como usar

```bash
git clone https://github.com/cauau/steganography-python.git
cd steganography-python

pip install -r requirements.txt
python main.py
```

---

## 🛠 Tecnologias

* Python
* Pillow
* NumPy
* Cryptography
* Tkinter

---

## ⚠️ Observações

* Funciona apenas com imagens PNG
* A mensagem deve caber no tamanho da imagem
* Senha incorreta gera erro na descriptografia

---

## 📄 Licença

MIT
