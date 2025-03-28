from flask import Flask, request, jsonify
from flask_mysqldb import MySQL
from flask_cors import CORS


app = Flask(__name__)

CORS(app)

# Configuração do banco de dados MySQL
app.config['MYSQL_HOST'] = '192.168.127.244'
app.config['MYSQL_USER'] = 'App'
app.config['MYSQL_PASSWORD'] = 'Senha123'
app.config['MYSQL_DB'] = 'RH'

mysql = MySQL(app)



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
    telefone = dados.get('telefone')
    endereco = dados.get('endereco')
    senha = dados.get('senha')

    if not nome or not cargo or not email or not senha:
        return jsonify({'mensagem': 'Todos os campos são obrigatórios'}), 400

    try:
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO usuarios (nome, cargo, email, telefone, endereco, senha) VALUES (%s, %s, %s, %s, %s, %s)",
                    (nome, cargo, email, telefone, endereco, senha))
        mysql.connection.commit()
        cur.close()
        return jsonify({'mensagem': 'Usuário criado com sucesso'}), 201
    except Exception as e:
        return jsonify({'mensagem': str(e)}), 500
    
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
    

@app.route('/usuarios/<int:id>', methods=['GET'])
def consultar_usuarios(id):
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT id, nome, cargo, email, senha, telefone, endereco FROM usuarios WHERE id = %s", (id,))
        dado = cur.fetchone()
        cur.close()
        
        if dado:
            usuario = {
                'id': dado[0],
                'nome': dado[1],
                'cargo': dado[2],
                'email': dado[3],
                'senha': dado[4],
                'telefone': dado[5],
                'endereco': dado[6],

            }
            return jsonify(usuario), 200
        else:
            return jsonify({'mensagem': 'Produto não encontrado'}), 404
    except Exception as e:
        return jsonify({'mensagem': str(e)}), 500
    
@app.route('/usuarios/<int:id>', methods=['PUT'])
def atualizar_usuario(id):
    dados = request.json
    nome = dados.get('nome')
    cargo = dados.get('cargo')
    email = dados.get('email')
    senha = dados.get('senha')
    telefone = dados.get('telefone')
    endereco = dados.get('endereco')

   # if not nome or not cargo or not email or not senha:
    #    return jsonify({'mensagem': 'Todos os campos são obrigatórios'}), 400

    try:
        cur = mysql.connection.cursor()
        cur.execute("UPDATE usuarios SET nome=%s, cargo=%s, email=%s, senha=%s, telefone=%s, endereco=%s WHERE id=%s",
                    (nome, cargo, email, senha, telefone, endereco, id))
        mysql.connection.commit()
        cur.close()
        return jsonify({'mensagem': 'Usuário atualizado com sucesso'})
    except Exception as e:
        return jsonify({'mensagem': str(e)}), 500

    

@app.route('/funcionarios', methods=['POST'])
def criar_funcionario():
    try:
        data = request.json
        
        # Validar dados obrigatórios
        campos_obrigatorios = ['funcionario', 'cargo', 'data_contratacao', 'salario', 'foto1', 'foto2', 'foto3', 'foto4', 'foto5']
        for campo in campos_obrigatorios:
            if campo not in data:
                return jsonify({'erro': f'Campo {campo} é obrigatório'}), 400
        
        cur = mysql.connection.cursor()
        
        # Inserir funcionário
        query = """
        INSERT INTO funcionarios 
        (nome, cargo, email, senha, telefone, endereco, salario,  data_cont,  foto1, foto2, foto3, foto4, foto5)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s,%s,%s,%s,%s)
        """
        valores = (
            data['nome'],
            data['cargo'],
            data['email'],
            data['senha'],
            data['telefone'],
            data['endereco'],
            data['salaro'],
            data['data_contratacao'],
            data['foto1'],
            data['foto2'],
            data['foto3'],
            data['foto4'],
            data['foto5'],
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

@app.route('/funcionarios', methods=['GET'])
def listar_funcionarios():
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM funcionarios")
        dados = cur.fetchall()
        cur.close()
        
        # Converter os resultados para dicionários
        funcionarios = []
        for dado in dados:
            funcionario = {
                 'id': dado[0],
                'nome': dado[1],
                'cargo': dado[2],
                'email': dado[3],
                'senha': dado[4],
                'telefone': dado[6],
                'endereco': dado[7],
                'salario': dado[8],
                'data_contratacao': dado[9],
                'foto1': dado[10],
                'foto2': dado[11],
                'foto3': dado[12],
                'foto4': dado[13],
                'foto5': dado[14]
            }
            funcionarios.append(funcionario)
            
        return jsonify(funcionarios)
        
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

@app.route('/funcionario/<int:id>', methods=['GET'])
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
                'telefone': dado[6],
                'endereco': dado[7],
                'salario': dado[8],
                'data_contratacao': dado[9],
                'foto1': dado[10],
                'foto2': dado[11],
                'foto3': dado[12],
                'foto4': dado[13],
                'foto5': dado[14]
            }
            return jsonify(funcionario)
        else:
            return jsonify({'erro': 'Funcionário não encontrado'}), 404
            
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

@app.route('/funcionario/<int:id>', methods=['PUT'])
def atualizar_funcionario(id):
    try:
        data = request.json
        
        # Validar dados obrigatórios
        campos_obrigatorios = ['nome', 'cargo','email', 'senha', 'telefone', 'endereco', 'salario', 'data_contratacao', 'foto1', 'foto2', 'foto3', 'foto4', 'foto5']
        for campo in campos_obrigatorios:
            if campo not in data:
                return jsonify({'erro': f'Campo {campo} é obrigatório'}), 400
        
        cur = mysql.connection.cursor()
        
        # Verificar se o funcionário existe
        cur.execute("SELECT id FROM funcionarios WHERE id = %s", (id,))
        if not cur.fetchone():
            return jsonify({'erro': 'Funcionário não encontrado'}), 404
        
        # Atualizar funcionário
        query = """
        UPDATE funcionarios 
        SET nome = %s, cargo = %s, email = %s, senha = %s, telefone = %s, endereco = %s, salario = %s, data_cont = %s, 
             foto1 = %s, foto2 = %s, foto3 = %s, 
            foto4 = %s, foto5 = %s
        WHERE id = %s
        """
        valores = (
            data['nome'],
            data['cargo'],
            data['email'],
            data['senha'],
            data['telefone'],
            data['endereco'],
            data['salario'],
            data['data_contratacao'],
            data['foto1'],
            data['foto2'],
            data['foto3'],
            data['foto4'],
            data['foto5'],
            id
        )
        
        cur.execute(query, valores)
        mysql.connection.commit()
        
        return jsonify({'mensagem': 'Funcionário atualizado com sucesso'})
        
    except Exception as e:
        return jsonify({'erro': str(e)}), 500
    finally:
        if 'cur' in locals():
            cur.close()

@app.route('/funcionario/<int:id>', methods=['DELETE'])
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
    

    

if __name__ == '__main__':
    app.run(debug=True)