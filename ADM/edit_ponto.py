import tkinter as tk
from tkinter import ttk, messagebox
import cv2
import os
import numpy as np
from PIL import Image, ImageTk
import requests
from datetime import datetime
import geocoder


class PontoEletronico:
    def __init__(self, root):
        self.root = root
        self.root.title("Ponto Eletrônico")
        self.root.geometry("800x600")

        # Frame principal
        self.frame = ttk.Frame(self.root, padding="10")
        self.frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Frame para login
        frame_login = ttk.Frame(self.frame)
        frame_login.grid(row=0, column=0, columnspan=2, pady=10)

        # Campos de login
        ttk.Label(frame_login, text="ID:").pack(side=tk.LEFT, padx=5)
        self.id_entry = ttk.Entry(frame_login)
        self.id_entry.pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_login, text="Login", command=self.login).pack(side=tk.LEFT, padx=5)

        # Frame para identificação facial
        frame_identificacao = ttk.Frame(self.frame)
        frame_identificacao.grid(row=1, column=0, columnspan=2, pady=10)

        # Botão para iniciar identificação facial
        ttk.Button(frame_identificacao, text="Iniciar Identificação Facial", command=self.iniciar_identificacao).pack(side=tk.LEFT, padx=5)

    def login(self):
        
            id = self.id_entry.get()
            if not id:
                messagebox.showwarning("Aviso", "Digite o ID do funcionário para login!")
                self.root.lift()
                return

            # Requisição à API para pegar os dados do funcionário
            response = requests.get(f'http://127.0.0.1:5000/ponto/{id}')
            if response.status_code == 200:
                funcionario = response.json()
                print(funcionario)
                self.funcionario_atual = funcionario  # Armazenando dados do funcionário para uso posterior
                messagebox.showinfo("Sucesso", f"Bem-vindo {funcionario['nome']}!")
                self.root.lift()
            else:
                messagebox.showerror("Erro", "Funcionário não encontrado!")
                self.root.lift()
        

    def iniciar_identificacao(self):
        try:
            # Verifica se o funcionário foi autenticado antes de iniciar a identificação facial
            if not hasattr(self, 'funcionario_atual'):
                messagebox.showwarning("Aviso", "Realize o login primeiro!")
                return

            # Criar uma nova janela para visualização da câmera
            janela_camera = tk.Toplevel(self.root)
            janela_camera.title("Identificação Facial")
            janela_camera.geometry("640x480")

            # Label para exibir a imagem da câmera
            label_camera = ttk.Label(janela_camera)
            label_camera.pack(pady=10)

            # Inicializar a câmera
            self.cap = cv2.VideoCapture(0)

            if not self.cap.isOpened():
                messagebox.showerror("Erro", "Não foi possível acessar a webcam!")
                janela_camera.destroy()
                return

            def atualizar_camera():
                ret, frame = self.cap.read()
                if ret:
                    # Converter frame para formato PIL
                    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    imagem_pil = Image.fromarray(frame_rgb)
                    # Redimensionar para caber na janela
                    imagem_pil = imagem_pil.resize((640, 360), Image.Resampling.LANCZOS)
                    # Converter para PhotoImage
                    imagem_tk = ImageTk.PhotoImage(image=imagem_pil)
                    label_camera.configure(image=imagem_tk)
                    label_camera.image = imagem_tk
                    janela_camera.after(10, atualizar_camera)

            atualizar_camera()

            # Configurar o que acontece quando a janela é fechada
            def on_closing():
                self.cap.release()
                janela_camera.destroy()

            janela_camera.protocol("WM_DELETE_WINDOW", on_closing)

            # Botão para capturar a foto e realizar identificação facial
            btn_capturar = ttk.Button(janela_camera, text="Capturar Foto e Identificar", command=lambda: self.identificar_face(janela_camera))
            btn_capturar.pack(pady=10)

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao iniciar identificação facial: {str(e)}")
            self.root.lift()

    def identificar_face(self, janela_camera):
        try:
            ret, frame = self.cap.read()

            if ret:
                # Converter frame para escala de cinza
                gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

                # Carregar fotos cadastradas do funcionário atual
                fotos_cadastradas = []
                for i in range(1, 6):
                    nome_foto = self.funcionario_atual[f'foto{i}']
                    caminho_foto = os.path.join("IMGS", nome_foto)
                    if os.path.exists(caminho_foto):
                        foto_cadastrada = cv2.imread(caminho_foto, cv2.IMREAD_GRAYSCALE)
                        fotos_cadastradas.append(foto_cadastrada)

                if not fotos_cadastradas:
                    messagebox.showerror("Erro", "Nenhuma foto cadastrada encontrada!")
                    return

                # Inicializar o reconhecedor facial LBPH
                recognizer = cv2.face.LBPHFaceRecognizer_create()

                # Treinar o reconhecedor com as fotos cadastradas
                labels = [self.funcionario_atual['id']] * len(fotos_cadastradas)
                recognizer.train(fotos_cadastradas, np.array(labels))

                # Realizar a identificação facial na foto capturada
                id_predicted, confidence = recognizer.predict(gray_frame)

                if id_predicted == self.funcionario_atual['id'] and confidence > 55:
                    messagebox.showinfo("Sucesso", "Identificação facial bem-sucedida!")
                    self.root.lift()

                    # Armazenar data e hora atuais e geolocalização do usuário
                    data_hora_atual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    g = geocoder.ip('me')
                    geolocalizacao = g.latlng

                    registros_ponto = {
                        'id_funcionario': self.funcionario_atual['id'],
                        'data_hora': data_hora_atual,
                        'geolocalizacao': geolocalizacao
                    }

                    response = requests.post('http://127.0.0.1:5000/registros_ponto', json=registros_ponto)
                    if response.status_code == 201:
                        messagebox.showinfo("Sucesso", "Registro de ponto armazenado com sucesso!")
                        self.root.lift()
                    else:
                        messagebox.showerror("Erro", "Falha ao armazenar registro de ponto!")
                        self.root.lift()

                else:
                    messagebox.showerror("Erro", "Identificação facial falhou!")
                    self.root.lift()

                # Liberar a câmera e fechar a janela
                self.cap.release()
                janela_camera.destroy()

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao realizar identificação facial: {str(e)}")
            self.root.lift()

if __name__ == "__main__":
    root = tk.Tk()
    app = PontoEletronico(root)
    root.mainloop()
