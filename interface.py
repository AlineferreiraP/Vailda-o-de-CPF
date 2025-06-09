import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import requests

class App(ttk.Window):
    def __init__(self):
        super().__init__(title="Validador de CPF", size=(400, 300))
        self.frames = {}

        for F in (PaginaInicial, PaginaSucesso):
            frame = F(self)
            self.frames[F] = frame
            frame.place(x=0, y=0, relwidth=1, relheight=1)

        self.mostrar_pagina(PaginaInicial)

    def mostrar_pagina(self, pagina):
        self.frames[pagina].tkraise()

class PaginaInicial(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master

        ttk.Label(self, text="Digite um CPF:", font=("Helvetica", 14)).pack(pady=20)

        self.cpf_entry = ttk.Entry(self, font=("Helvetica", 12))
        self.cpf_entry.pack(pady=10)

        self.mensagem = ttk.Label(self, text="", font=("Helvetica", 11))
        self.mensagem.pack(pady=5)

        ttk.Button(self, text="Validar CPF", bootstyle=PRIMARY, command=self.validar_cpf).pack(pady=10)

    def validar_cpf(self):
        cpf = self.cpf_entry.get().strip()
        self.mensagem.config(text="", foreground="")

        try:
            response = requests.post('http://127.0.0.1:5000/validar_cpf', json={'cpf': cpf})
            if response.status_code == 200:
                data = response.json()
                if data.get('valido'):
                    self.master.mostrar_pagina(PaginaSucesso)
                else:
                    self.mensagem.config(text="❌ CPF inválido!", foreground="red")
            else:
                self.mensagem.config(text="⚠️ Erro no servidor.", foreground="orange")
        except Exception as e:
            self.mensagem.config(text="🚫 Erro de conexão com o servidor.", foreground="orange")
            print("Erro:", e)

class PaginaSucesso(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)

        ttk.Label(self, text="✅ CPF Válido!", font=("Helvetica", 16), foreground="green").pack(pady=40)

        ttk.Button(self, text="Voltar", bootstyle=SECONDARY, command=lambda: master.mostrar_pagina(PaginaInicial)).pack(pady=10)

if __name__ == "__main__":
    app = App()
    app.mainloop()

