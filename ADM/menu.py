import tkinter as tk
from tkinter import messagebox
import edit_usuarios
import relatorio_usuarios
import edit_funcionarios
import adm
from adm import FormularioFuncionario



def janela_usuarios():
    edit_usuarios.criar_tela()

def janela_relatorio():
     relatorio_usuarios.criar_janela()

def janela_funcionarios():
     adm.abrir_tela()


def janela_funcionarios():
    root = tk.Toplevel()  # Cria uma nova janela
    app = FormularioFuncionario(root)
    root.mainloop()
     

def abrir_tela():

    def sair():
            resposta = messagebox.askyesno("Sair", "Tem certeza que deseja sair?")
            if resposta:
                menu.destroy()

    menu = tk.Tk()
    menu.title("Menu Principal")

    # Maximizar a janela
    menu.state('zoomed')

    menu_bar = tk.Menu(menu)
    menu.config(menu=menu_bar)

    menu_usuarios = tk.Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label="Usuários", menu=menu_usuarios)
    menu_usuarios.add_command(label="Edição", command=janela_usuarios)
    menu_usuarios.add_command(label="Relatório", command=janela_relatorio)

    menu_funcionarios = tk.Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label="Funcionarios", menu=menu_funcionarios)
    menu_funcionarios.add_command(label="Edição", command=janela_funcionarios)
    menu_funcionarios.add_command(label="Relatório")

    

    menu_bar.add_command(label="Sair", command=sair)

    menu.mainloop()