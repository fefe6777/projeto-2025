import tkinter as tk
from tkinter import messagebox
import edit_usuarios
import relatorio_usuarios
from edit_funcionarios import FormularioFuncionario
import relatorio_funcionarios
from edit_ponto import PontoEletronico

def janela_usuarios():
    edit_usuarios.criar_tela()

def janela_relatorio():
    relatorio_usuarios.criar_janela()

def janela_funcionarios():
    root = tk.Toplevel()  # Cria uma nova janela
    app = FormularioFuncionario(root)
    root.mainloop()

def janela_relatorio_funcionario():
    relatorio_funcionarios.criar_janela()

def janela_ponto():
    root = tk.Toplevel()  # Cria uma nova janela para a tela de ponto
    app = PontoEletronico(root)  # Supondo que PontoEletronico seja a classe que você já tem
    root.mainloop()

def abrir_tela():

    def sair():
        resposta = messagebox.askyesno("Sair", "Tem certeza que deseja sair?")
        if resposta:
            menu.destroy()

    menu = tk.Tk()
    menu.title("Menu Principal")

    imagem = tk.PhotoImage(file="ADM/imgs/cocacola.png")
    tk.Label(menu, image=imagem).pack(pady=50)

     
    # Maximizar a janela
    menu.state('zoomed')

    menu_bar = tk.Menu(menu)
    menu.config(menu=menu_bar)

    # Menu de Usuários
    menu_usuarios = tk.Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label="Usuários", menu=menu_usuarios)
    menu_usuarios.add_command(label="Edição", command=janela_usuarios)
    menu_usuarios.add_command(label="Relatório", command=janela_relatorio)

    # Menu de Funcionários
    menu_funcionarios = tk.Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label="Funcionarios", menu=menu_funcionarios)
    menu_funcionarios.add_command(label="Edição", command=janela_funcionarios)
    menu_funcionarios.add_command(label="Relatório", command=janela_relatorio_funcionario)  # Chama a função do relatório de funcionários

    menu_bate_ponto = tk.Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label="Bater ponto", menu=menu_bate_ponto)
    menu_bate_ponto.add_command(label="Iniciar Reconhecimento", command=janela_ponto)

    


    # Botão de Sair
    menu_bar.add_command(label="Sair", command=sair)

    menu.mainloop()

# Chama a função para abrir o menu principal
if __name__ == "__main__":
    abrir_tela()
