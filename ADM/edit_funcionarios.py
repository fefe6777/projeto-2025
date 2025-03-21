import tkinter as tk
from tkinter import messagebox, filedialog
import conf
import requests
import os
import shutil

def criar_tela():
    janela = tk.Toplevel()
    janela.title("Gerenciamento de funcionarios")
    janela.configure(padx=20, pady=20)

    labels = ["ID:", "Nome:", "Cargo:", "Email:", "Telefone:", "Endereço:", "Imagem"]
    entradas = {}

    # Adicionar labels e entradas para os novos campos
    for i, label in enumerate(labels):
        tk.Label(janela, text=label).grid(row=i, column=0, padx=5, pady=5, sticky="e")
        entradas[label] = tk.Entry(janela)
        entradas[label].grid(row=i, column=1, padx=5, pady=5)

    imagem_label = tk.Label(janela)
    imagem_label.grid(row=6, column=1, padx=5, pady=5, sticky="w")

    entradas["ID:"].config(state="normal")
    for campo in ["Nome:", "Cargo:", "Email:", "Telefone:", "Endereço:", "Imagem"]:
        entradas[campo].config(state="disabled")

    def consultar():
        id_produto = entradas["ID:"].get()
        if not id_produto:
            messagebox.showwarning("Erro", "Informe o ID do funcionario para consultar.")
            janela.lift()
            return

        try:
            url = f"{conf.url_api}/funcionario/{id_produto}"
            response = requests.get(url)
            if response.status_code == 200:
                dados = response.json()
                if dados:
                    for campo in ["Nome:", "Cargo:", "Email:", "Telefone:", "Endereço:", "Imagem"]:
                        entradas[campo].config(state="normal")
                        entradas[campo].delete(0, tk.END)
                        entradas[campo].insert(0, dados[campo.lower()])
                    
                    # Habilitar / Desabilitar botões
                    botao_consultar.config(state="normal")
                    botao_atualizar.config(state="normal")
                    botao_novo.config(state="disabled")
                    botao_excluir.config(state="normal")
                else:
                    messagebox.showwarning("Erro", "Funcionario não encontrado.")
                    janela.lift()
            else:
                messagebox.showwarning("Erro", f"Falha ao conectar: {response.status_code}")
                janela.lift()
        except Exception as e:
            messagebox.showwarning("Erro", f"Problemas com o banco de dados: {str(e)}")
            janela.lift()

    def novo():
        for campo in ["ID:", "Nome:", "Cargo:", "Email:", "Telefone:", "Endereço:", "Imagem"]:
            entradas[campo].config(state="normal")
        limpar()
        entradas["ID:"].config(state="disabled")

        # Habilitar/desabilitar botões
        botao_salvar.config(state="normal")
        botao_consultar.config(state="disabled")
        botao_novo.config(state="disabled")

    def salvar():
        dados = {
            "nome": entradas["Nome:"].get(),
            "cargo": entradas["Cargo:"].get(),
            "email": entradas["Email:"].get(),
            "telefone": entradas["Telefone:"].get(),
            "endereco": entradas["Endereço:"].get(),
            "imagem": entradas["Imagem:"].get()
        }

        try:
            url = f"{conf.url_api}/funcionarios"
            response = requests.post(url, json=dados)

            if response.status_code == 201:
                messagebox.showinfo("Sucesso", "Funcionario salvo com sucesso!")
                janela.lift()

                # Habilitar/desabilitar botões
                botao_salvar.config(state="disabled")
                botao_consultar.config(state="disabled")
                botao_novo.config(state="normal")
            else:
                messagebox.showwarning("Erro", f"Falha ao conectar: {response.status_code}")
                janela.lift()
        except Exception as e:
            messagebox.showwarning("Erro", f"Problemas com o banco de dados: {str(e)}")
            janela.lift()

    def atualizar():
        id_funcionario = entradas["ID:"].get()
        if not id_funcionario:
            messagebox.showwarning("Erro", "Informe o ID do funcionario para atualizar.")
            janela.lift()
            return

        dados = {
            "nome": entradas["Nome:"].get(),
            "cargo": entradas["Cargo:"].get(),
            "email": entradas["Email:"].get(),
            "telefone": entradas["Telefone:"].get(),
            "endereco": entradas["Endereço:"].get(),
            "imagem": entradas["Imagem:"].get()
        }

        try:
            url = f"{conf.url_api}/funcionarios/{id_funcionario}"
            response = requests.put(url, json=dados)

            if response.status_code == 200:
                messagebox.showinfo("Sucesso", "Funcionario atualizado com sucesso!")
                janela.lift()
            else:
                messagebox.showwarning("Erro", f"Falha ao conectar: {response.status_code}")
                janela.lift()
        except Exception as e:
            messagebox.showwarning("Erro", f"Problemas com o banco de dados: {str(e)}")
            janela.lift()

    def excluir():
        id_funcionario = entradas["ID:"].get()
        if not id_funcionario:
            messagebox.showwarning("Erro", "Informe o ID do funcionario para excluir.")
            janela.lift()
            return

        resposta = messagebox.askyesno("Excluir", "Tem certeza que deseja excluir o registro?")
        if resposta:
            try:
                url = f"{conf.url_api}/funcionarios/{id_funcionario}"
                response = requests.delete(url)

                if response.status_code == 200:
                    messagebox.showinfo("Sucesso", "Funcionario excluído com sucesso!")
                    limpar()
                    entradas["ID:"].config(state="normal")
                    entradas["Nome:"].config(state="normal")
                    entradas["Cargo:"].config(state="normal")
                    entradas["Email:"].config(state="normal")
                    entradas["Telefone:"].config(state="normal")
                    entradas["Endereço:"].config(state="normal")
                    entradas["Imagem:"].config(state="normal")
                    entradas["ID:"].config(state="disabled")

                    # Habilitar/desabilitar botões
                    botao_salvar.config(state="normal")
                    botao_consultar.config(state="disabled")
                    botao_novo.config(state="disabled")
                    botao_atualizar.config(state="disabled")
                    janela.lift()
                else:
                    messagebox.showwarning("Erro", f"Falha ao conectar: {response.status_code}")
                    janela.lift()
            except Exception as e:
                messagebox.showwarning("Erro", f"Problemas com o banco de dados: {str(e)}")
                janela.lift()

    def limpar():
        for entrada in entradas.values():
            entrada.delete(0, tk.END)

    def sair():
        janela.destroy()

    frame_botoes = tk.Frame(janela)
    frame_botoes.grid(row=len(labels), column=0, columnspan=2, pady=10)

    # Criando os botões
    botao_consultar = tk.Button(frame_botoes, text="Consultar", command=consultar, width=12)
    botao_consultar.pack(side="left", padx=5)
    botao_novo = tk.Button(frame_botoes, text="Novo", command=novo, width=12)
    botao_novo.pack(side="left", padx=5)
    botao_salvar = tk.Button(frame_botoes, text="Salvar", command=salvar, width=12, state="disabled")
    botao_salvar.pack(side="left", padx=5)
    botao_atualizar = tk.Button(frame_botoes, text="Atualizar", command=atualizar, width=12, state="disabled")
    botao_atualizar.pack(side="left", padx=5)
    botao_excluir = tk.Button(frame_botoes, text="Excluir", command=excluir, width=12, state="disabled")
    botao_excluir.pack(side="left", padx=5)
    botao_sair = tk.Button(frame_botoes, text="Sair", command=sair, width=12)
    botao_sair.pack(side="left", padx=5)

    janela.mainloop()
