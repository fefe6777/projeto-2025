import tkinter as tk
from tkinter import messagebox
import conf
import requests

def criar_tela():
    janela = tk.Toplevel()
    janela.title("Inclusão de Usuário")
    janela.configure(padx=20, pady=20)

    labels = ["Nome:", "Cargo:", "Email:", "Senha:", "Confirmar Senha:"]
    entradas = {}

    for i, texto in enumerate(labels):
        tk.Label(janela, text=texto, width=15, anchor="e").grid(row=i, column=0, padx=5, pady=5, sticky="e")
        entrada = tk.Entry(janela, width=40, show="*" if "Senha" in texto else "")
        entrada.grid(row=i, column=1, padx=5, pady=5, sticky="w")
        entradas[texto] = entrada

    def salvar():
        if entradas["Senha:"].get() != entradas["Confirmar Senha:"].get():
            messagebox.showerror("Erro", "As senhas não coincidem!")
            janela.lift()
            return
        
        dados = {
            "nome": entradas["Nome:"].get(),
            "cargo": entradas["Cargo:"].get(),
            "email": entradas["Email:"].get(),
            "senha": entradas["Senha:"].get()
        }

        try:
            url = f"{conf.url_api}/post/incluir/usuario/"
            response = requests.post(url, json=dados)
            
            if response.status_code == 200:
                data = response.json()
                if data.get("inclusao"):
                    messagebox.showinfo("Sucesso", "Usuário salvo com sucesso!")
                else:
                    messagebox.showwarning("Erro", "Problemas ao incluir o registro")
            else:
                messagebox.showwarning("Erro", f"Falha ao conectar: {response.status_code}")
        except Exception as e:
            messagebox.showwarning("Erro", f"Problemas com o banco de dados: {str(e)}")

    def limpar():
        for entrada in entradas.values():
            entrada.delete(0, tk.END)

    def sair():
        janela.destroy()

    frame_botoes = tk.Frame(janela)
    frame_botoes.grid(row=len(labels), column=0, columnspan=2, pady=10)

    tk.Button(frame_botoes, text="Salvar", command=salvar, width=12).pack(side="left", padx=5)
    tk.Button(frame_botoes, text="Limpar", command=limpar, width=12).pack(side="left", padx=5)
    tk.Button(frame_botoes, text="Sair", command=sair, width=12).pack(side="left", padx=5)

    janela.mainloop()