from flask import Flask, request, jsonify
from flask_mysqldb import MySQL
from flask_cors import CORS
from datetime import datetime
import os
basedir = os.path.dirname(os.path.abspath(__file__))


app = Flask(__name__)

CORS(app)

# Configuração do banco de dados MySQL
app.config['MYSQL_HOST'] = '192.168.127.244'
app.config['MYSQL_USER'] = 'App'
app.config['MYSQL_PASSWORD'] = 'Senha123'
app.config['MYSQL_DB'] = 'RH'

mysql = MySQL(app)

# Rotas de Funcionários
@app.route('/funcionarios', methods=['POST'])
def criar_funcionario():
    try:
        data = request.json
        
        # Validar dados obrigatórios
        campos_obrigatorios = ['nome', 'cargo', 'email', 'senha','telefone', 'endereco', 'data_contratacao', 'salario', 'foto1', 'foto2', 'foto3', 'foto4', 'foto5']
        for campo in campos_obrigatorios:
            if campo not in data:
                return jsonify({'erro': f'Campo {campo} é obrigatório'}), 400
        
        cur = mysql.connection.cursor()
        
        # Inserir funcionário
        query = """
        INSERT INTO funcionarios 
        (nome, cargo, email, senha, telefone, endereco, data_cont, salario, foto1, foto2, foto3, foto4, foto5)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        valores = (
            data['nome'],
            data['cargo'],
            data['email'],
            data['senha'],
            data['telefone'],
            data['endereco'],
            data['data_contratacao'],
            data['salario'],
            data['foto1'],
            data['foto2'],
            data['foto3'],
            data['foto4'],
            data['foto5']
        )
        
        cur.execute(query, valores)
        mysql.connection.commit()
        
        return jsonify({
            'mensagem': 'Funcionário criado com sucesso',
            'id': cur.lastrowid
        }), 201
        
    except Exception as e:
        return jsonify({'erro': str(e)}), 500
    finally:
        if 'cur' in locals():
            cur.close()

        

@app.route('/funcionarios/<int:id>', methods=['GET'])
def obter_funcionario(id):
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM funcionarios WHERE id = %s", (id,))
        dado = cur.fetchone()
        cur.close()
        
        if dado:
            funcionario = {
                'id': dado[0],
                'nome': dado[1],
                'cargo': dado[2],
                'email': dado[3],
                'senha': dado[4],
                'telefone': dado[5],
                'endereco': dado[6],
                'salario': dado[7],
                'data_cont': dado[8],
                'foto1': dado[9],
                'foto2': dado[10],
                'foto3': dado[11],
                'foto4': dado[12],
                'foto5': dado[13]
            }
            return jsonify(funcionario)
        else:
            return jsonify({'erro': 'Funcionário não encontrado'}), 404
            
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

@app.route('/funcionarios/<int:id>', methods=['PUT'])
def atualizar_funcionario(id):
    try:
        # Obter os dados do corpo da requisição
        data = request.json
        
        # Validar dados obrigatórios
        campos_obrigatorios = ['nome', 'cargo', 'email', 'senha', 'telefone', 'endereco', 'salario', 'data_cont', 'foto1', 'foto2', 'foto3', 'foto4', 'foto5']
        for campo in campos_obrigatorios:
            if campo not in data:
                return jsonify({'erro': f'Campo {campo} é obrigatório'}), 400
        
        # Conectar ao banco de dados
        cur = mysql.connection.cursor()

        # Verificar se o funcionário existe
        cur.execute("SELECT id FROM funcionarios WHERE id = %s", (id,))
        if not cur.fetchone():
            return jsonify({'erro': 'Funcionário não encontrado'}), 404
        
        # Query para atualizar os dados do funcionário
        query = """
        UPDATE funcionarios 
        SET 
            nome = %s, 
            cargo = %s, 
            email = %s, 
            senha = %s, 
            telefone = %s, 
            endereco = %s, 
            salario = %s, 
            data_cont = %s, 
            foto1 = %s, 
            foto2 = %s, 
            foto3 = %s, 
            foto4 = %s, 
            foto5 = %s
        WHERE id = %s
        """

        # Valores que serão passados para a query
        valores = (
            data['nome'],
            data['cargo'],
            data['email'],
            data['senha'],  # Adicionando o campo 'senha'
            data['telefone'],
            data['endereco'],
            data['salario'],
            data['data_cont'],  # Corrigindo o nome da chave
            data['foto1'],
            data['foto2'],
            data['foto3'],
            data['foto4'],
            data['foto5'],
            id  # O id do funcionário a ser atualizado
        )

        # Executar a query com os valores passados
        cur.execute(query, valores)
        mysql.connection.commit()

        # Resposta de sucesso
        return jsonify({'mensagem': 'Funcionário atualizado com sucesso'})

    except Exception as e:
        # Retorna erro detalhado caso algo falhe
        return jsonify({'erro': f'Erro ao atualizar o funcionário: {str(e)}'}), 500
    
    finally:
        # Fechar o cursor no final, independentemente de ocorrer erro ou não
        if 'cur' in locals():
            cur.close()


@app.route('/funcionarios/<int:id>', methods=['DELETE'])
def deletar_funcionario(id):
    try:
        cur = mysql.connection.cursor()
        
        # Verificar se o funcionário existe
        cur.execute("SELECT id FROM funcionarios WHERE id = %s", (id,))
        if not cur.fetchone():
            return jsonify({'erro': 'Funcionário não encontrado'}), 404
        
        # Deletar funcionário
        cur.execute("DELETE FROM funcionarios WHERE id = %s", (id,))
        mysql.connection.commit()
        
        return jsonify({'mensagem': 'Funcionário deletado com sucesso'})
        
    except Exception as e:
        return jsonify({'erro': str(e)}), 500
    finally:
        if 'cur' in locals():
            cur.close()

            
# Rota para consultar todos os registros de funcionarios
@app.route('/funcionarios', methods=['GET'])
def listar_funcionarioss():
    try:
        cur = mysql.connection.cursor()
        # Alteração da consulta SQL para incluir as novas colunas
        cur.execute("SELECT id, nome, cargo, email, telefone, endereco, salario, data_cont, foto1, foto2, foto3, foto4, foto5 FROM funcionarios")
        dados = cur.fetchall()
        cur.close()
        return jsonify(dados)
    except Exception as e:
        return jsonify({'mensagem': str(e)}), 500



# Rota para consultar todos os registros
@app.route('/usuarios', methods=['GET'])
def listar_usuarios():
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT id, nome, cargo, email, telefone, endereco FROM usuarios")
        dados = cur.fetchall()
        cur.close()
        return jsonify(dados)
    except Exception as e:
        return jsonify({'mensagem': str(e)}), 500

# Rota para consultar um usuário pelo ID
@app.route('/usuarios/<int:id>', methods=['GET'])
def obter_usuario(id):
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT id, nome, cargo, email, telefone, endereco FROM usuarios WHERE id = %s", (id,))
        dado = cur.fetchone()
        cur.close()
        
        if dado:
            # Verificação adicional para garantir que 'dado' é uma tupla
            if isinstance(dado, tuple):
                # Converta a tupla para um dicionário para facilitar o retorno em JSON
                usuario = {
                    'id': dado[0],
                    'nome': dado[1],
                    'cargo': dado[2],
                    'email': dado[3],
                    'telefone': dado[4],
                    'endereco': dado [5]
                }
                return jsonify(usuario), 200
            else:
                return jsonify({'mensagem': 'Erro inesperado: dado não é uma tupla'}), 500
        else:
            return jsonify({'mensagem': 'Usuário não encontrado'}), 401
    except Exception as e:
        return jsonify({'mensagem': str(e)}), 500


# Rota para verificar se um usuário existe pelo e-mail e senha
@app.route('/usuarios/login', methods=['POST'])
def verificar_usuario():
    dados = request.json
    email = dados.get('email')
    senha = dados.get('senha')
    
    if not email or not senha:
        return jsonify({'mensagem': 'Email e senha são obrigatórios'}), 400
    
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT id FROM usuarios WHERE email = %s AND senha = %s", (email, senha))
        usuario = cur.fetchone()
        cur.close()
        
        if usuario:
            return jsonify({'mensagem': 'Login bem-sucedido'})
        else:
            return jsonify({'mensagem': 'Usuário ou senha inválidos'}), 401
    except Exception as e:
        return jsonify({'mensagem': str(e)}), 500

# Rota para incluir um novo usuário
@app.route('/usuarios', methods=['POST'])
def criar_usuario():
    dados = request.json
    nome = dados.get('nome')
    cargo = dados.get('cargo')
    email = dados.get('email')
    senha = dados.get('senha')
    telefone = dados.get('telefone')
    endereco = dados.get('endereco')
    

    if not nome or not cargo or not email or not senha or not telefone or not endereco:
        return jsonify({'mensagem': 'Todos os campos são obrigatórios'}), 400

    try:
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO usuarios (nome, cargo, email, senha, telefone, endereco) VALUES (%s, %s, %s, %s,%s,%s)",
                    (nome, cargo, email, senha))
        mysql.connection.commit()
        cur.close()
        return jsonify({'mensagem': 'Usuário criado com sucesso'}), 201
    except Exception as e:
        return jsonify({'mensagem': str(e)}), 500

# Rota para atualizar um usuário existente
@app.route('/usuarios/<int:id>', methods=['PUT'])
def atualizar_usuario(id):
    dados = request.json
    nome = dados.get('nome')
    cargo = dados.get('cargo')
    email = dados.get('email')
    telefone = dados.get('telefone')
    endereco = dados.get('endereco')

    if not nome or not cargo or not email or not telefone or not endereco:
        return jsonify({'mensagem': 'Todos os campos são obrigatórios'}), 400

    try:
        cur = mysql.connection.cursor()
        cur.execute("UPDATE usuarios SET nome=%s, cargo=%s, email=%s, telefone=%s, email=%s WHERE id=%s",
                    (nome, cargo, email, telefone, endereco, id))
        mysql.connection.commit()
        cur.close()
        return jsonify({'mensagem': 'Usuário atualizado com sucesso'})
    except Exception as e:
        return jsonify({'mensagem': str(e)}), 500

# Rota para deletar um usuário
@app.route('/usuarios/<int:id>', methods=['DELETE'])
def deletar_usuario(id):
    try:
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM usuarios WHERE id = %s", (id,))
        mysql.connection.commit()
        cur.close()
        return jsonify({'mensagem': 'Usuário deletado com sucesso'})
    except Exception as e:
        return jsonify({'mensagem': str(e)}), 500
    
@app.route('/ponto/<int:id>', methods=['GET'])
def bater_ponto(id):  # Agora o id é passado como parâmetro da URL
    try:
        # Conectando ao banco de dados
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM funcionarios WHERE id = %s", (id,))
        dado = cur.fetchone()  # Busca o primeiro resultado (funcionário)

        cur.close()  # Fecha o cursor após a consulta
        #print (dado)
        if dado:
            # Criando o dicionário com as informações do funcionário
            funcionario = {
                'id': dado[0],
                'nome': dado[1],
                'cargo': dado[2],
                'email': dado[3],
                'senha': dado[4],
                'telefone': dado[5],
                'endereco': dado[6],
                'salario': dado[7],
                'data_cont': dado[8],
                'foto1': dado[9],
                'foto2': dado[10],
                'foto3': dado[11],
                'foto4': dado[12],
                'foto5': dado[13]
            }
            return jsonify(funcionario), 200  # Retorna as informações do funcionário em formato JSON
        else:
            return jsonify({'erro': 'Funcionário não encontrado'}), 404  # Caso o funcionário não seja encontrado
            
    except Exception as e:
        return jsonify({'erro': str(e)}), 500  # Caso ocorra um erro no servidor
    

@app.route('/registros_ponto', methods=['POST'])
def obter_registros():
    dados = request.json  # Obtém os dados enviados no corpo da requisição

    print(dados)

    # Extrair os dados da requisição
    id_funcionario = dados.get('id_funcionario')

    if(dados.get('data_hora')):
        data_hora = datetime.strptime(dados.get('data_hora'), '%Y-%m-%d %H:%M:%S')
    else: 
        data_hora = datetime.now()
    
    geolocalizacao = dados.get('geolocalizacao')

    # Verificar se todos os campos obrigatórios estão presentes
    if not id_funcionario or not data_hora or not geolocalizacao:
        return jsonify({'mensagem': 'Todos os campos são obrigatórios'}), 400

    try:
        # Inserir os dados no banco de dados
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO registros (id, data_hora, geolocalizacao) VALUES (%s, %s, %s)",
            (id_funcionario, data_hora, str(geolocalizacao)))
        mysql.connection.commit()
        cur.close()

        # Retornar uma resposta de sucesso
        return jsonify({'mensagem': 'Registro criado com sucesso'}), 201

    except Exception as e:
        # Em caso de erro, retornar uma mensagem de erro
        return jsonify({'mensagem': f'Erro ao criar o registro: {str(e)}'}), 500


# Rota para verificar se um usuário existe pelo e-mail e senha
@app.route('/funcionarios/login', methods=['POST'])
def verificar_funcionario_login():
    dados = request.json
    email = dados.get('email')
    senha = dados.get('senha')
    
    if not email or not senha:
        return jsonify({'mensagem': 'Email e senha são obrigatórios'}), 400
    
    try:
        cur = mysql.connection.cursor()
        cur.execute("""
            SELECT id, nome, email, senha, foto1 
            FROM funcionarios 
            WHERE email = %s AND senha = %s
        """, (email, senha))
        usuario = cur.fetchone()
        cur.close()
        
        if usuario:
            funcionario = {
                'mensagem': 'Login bem-sucedido',
                'id': usuario[0],
                'nome': usuario[1],
                'email': usuario[2],
                'foto1': usuario[4]
            }
            return jsonify(funcionario)
        else:
            return jsonify({'mensagem': 'Usuário ou senha inválidos'}), 401
    except Exception as e:
        return jsonify({'mensagem': 'Erro no servidor: ' + str(e)}), 500


@app.route('/reconhecer_face', methods=['POST'])
def reconhecer_face():
    try:
        dados = request.json
        id_funcionario = dados.get('id_funcionario')
        imagem_base64 = dados.get('imagem')

        
        if not id_funcionario or not imagem_base64:
            return jsonify({'mensagem': 'Campos obrigatórios ausentes'}), 400

        import cv2
        import numpy as np
        import base64
        import os

        # Decodificar imagem base64 recebida
        imagem_bytes = base64.b64decode(imagem_base64.split(",")[1])
        nparr = np.frombuffer(imagem_bytes, np.uint8)
        imagem_recebida = cv2.imdecode(nparr, cv2.IMREAD_GRAYSCALE)

        # Buscar fotos cadastradas
        cur = mysql.connection.cursor()
        cur.execute("SELECT foto1, foto2, foto3, foto4, foto5 FROM funcionarios WHERE id = %s", (id_funcionario,))
        fotos = cur.fetchone()
        cur.close()
        if not fotos:
            return jsonify({'mensagem': 'Funcionário não encontrado'}), 404

        # Carregar as imagens cadastradas
        fotos_cadastradas = []
        for nome_foto in fotos:
            if nome_foto:
                nome_foto = nome_foto.strip()
                caminho = os.path.join(basedir, '../IMGS', nome_foto)
                print(f"Verificando: {caminho}")
                if os.path.exists(caminho):
                    img = cv2.imread(caminho, cv2.IMREAD_GRAYSCALE)
                    if img is not None:
                        print(f"Imagem carregada: {caminho}, shape: {img.shape}")
                        fotos_cadastradas.append(img)
                    else:
                        print(f"Erro ao carregar imagem: {caminho}")
                else:
                    print(f"Imagem não encontrada no caminho: {caminho}")
                    
        if not fotos_cadastradas:
            return jsonify({'mensagem': 'Fotos do funcionário não encontradas'}), 400
        

        # Treinar reconhecedor
        recognizer = cv2.face.LBPHFaceRecognizer_create()
        labels = [id_funcionario] * len(fotos_cadastradas)
        recognizer.train(fotos_cadastradas, np.array(labels))

        # Realizar predição
        id_predito, confianca = recognizer.predict(imagem_recebida)

        if id_predito == id_funcionario and confianca < 90:
            print(confianca)
            return jsonify({'reconhecido': True, 'confianca': confianca})
        else:
            print(confianca)
            return jsonify({'reconhecido': False, 'confianca': confianca})

    except Exception as e:
        return jsonify({'mensagem': str(e)}), 500



if __name__ == '__main__':
    app.run(debug=True)
