import requests
import tkinter as tk
from tkinter import ttk
import conf

class RelatorioUsuario:
    def criar_janela():
        janela = tk.Toplevel()
        janela.title("Relatorio de funcionarios")
        janela.configure(padx=20, pady=20)

        # URL da API Flask
        API_URL = f"{conf.url_api}/funcionarios" 

        # Criar janela principal
        root = tk.Tk()
        root.title("Relatório de funcionarios")

        # Criar frame para organizar a tabela e a barra de rolagem
        frame = tk.Frame(root)
        frame.pack(fill=tk.BOTH, expand=True)

        # Criar Treeview para exibir os dados
        tree = ttk.Treeview(frame, columns=("ID", "Nome", "Cargo", "Email", "Telefone", "Endereço", "Salario", "Data Cont", "Foto1", "Foto2", "Foto3", "Foto4", "Foto5"), show="headings")

    # Definir os cabeçalhos das colunas
        tree.heading("ID", text="ID")
        tree.heading("Nome", text="Nome")
        tree.heading("Cargo", text="Cargo")
        tree.heading("Email", text="Email")
        tree.heading("Telefone", text="Telefone")
        tree.heading("Endereço", text="Endereço")
        tree.heading("Salario", text="Salario")
        tree.heading("Data Cont", text="Data Cont")
        tree.heading("Foto1", text="Foto1")
        tree.heading("Foto2", text="Foto2")
        tree.heading("Foto3", text="Foto3")
        tree.heading("Foto4", text="Foto4")
        tree.heading("Foto5", text="Foto5")


        # Ajustar tamanho das colunas
        tree.column("ID", width=50)
        tree.column("Nome", width=150)
        tree.column("Cargo", width=100)
        tree.column("Email", width=150)
        tree.column("Telefone", width=100)
        tree.column("Endereço", width=200)
        tree.column("Salario", width=100)
        tree.column("Data Cont", width=100)
        tree.column("Foto1", width=80)
        tree.column("Foto2", width=80)
        tree.column("Foto3", width=80)
        tree.column("Foto4", width=80)
        tree.column("Foto5", width=80)

        # Adicionar barra de rolagem vertical
        scroll_y = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scroll_y.set)

        # Posicionar os widgets
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll_y.pack(side=tk.RIGHT, fill=tk.Y)

        # Buscar dados da API e preencher a tabela
        try:
            response = requests.get(API_URL)
            if response.status_code == 200:
                usuarios = response.json()
                for usuario in usuarios:
                    tree.insert("", tk.END, values=usuario)
            else:
                print("Erro ao buscar dados:", response.json())
        except Exception as e:
            print("Erro na requisição:", e)

        # Rodar a interface gráfica
        root.mainloop()