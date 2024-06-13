from flask_openapi3 import OpenAPI, Info , Tag
from flask import Flask, request, Response, jsonify, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import json

info = Info(title="Api o bloco de notas", version="1.0")
app = OpenAPI(__name__, info=info)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///nota.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

CORS(app)

db = SQLAlchemy(app)

"""Classe de definição do banco de dados e os métodos de manipulação dele,
 a classe Nota vai herdar o db.Model do SQLAlchemy"""
class Nota(db.Model):
    __tablename__ = "nota"

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(50))
    texto = db.Column(db.String(100))
    
    def __init__(self, titulo, texto):
        """Função inicia o banco de dados"""
        self.titulo = titulo
        self.texto = texto

    def json(self):
        """Função define o id, titulo e texto como json"""
        return {'id': self.id, 'titulo': self.titulo, 
                'texto': self.texto}    

    def obter_todas_notas():
        """Função que obtem todas as notas no banco de dados"""
        return [Nota.json(nota) for nota in Nota.query.all()] # Retorna a busca te todas as notas
    
    #def obter_nota(id):
        #"""Funcão para obter a nota usando o id da nota como parametro"""
        #Nota.json(Nota.query.filter_by(id=id).first().json()) # Procura a a nota no banco de dados pelo id como json

    def adicao_nota(titulo, texto):
        """Função para adicionar nota no banco de dados usando titulo e texto como parametros"""
        nova_nota = Nota(titulo=titulo, texto=texto) # Criação da instancia da nossa Nota como um construtor
        db.session.add(nova_nota) # Adiciona nova nota na seção do banco de dados
        db.session.commit() # Fazer o commit das mudanças no banco de dados
        return nova_nota # Retorna a nova nota

    def edicao_nota(id, titulo, texto):
        """Função para atualizar os detalhes da nota usando o id, titulo e descrição como parametros"""
        nota_a_atualizar = Nota.query.filter_by(id=id).first() # Procura a a nota no banco de dados pelo id
        nota_a_atualizar.titulo = titulo # Atualiza no banco de dados o novo titulo
        nota_a_atualizar.texto = texto # Atualiza no banco de dados o novo texto
        db.session.commit() # Faz o commit das mudanças no banco de dados

    def deletar_nota():
        """Função para deletar a nota do banco de dados usando o id da nota como o parametro"""
        # Definição do id da requisição como um json
        id_de_requisicao = request.get_json()
        id = id_de_requisicao['id']
        nota_a_deletar = Nota.query.filter_by(id=id).first() # Procurar a a nota no banco de dados pelo id
        db.session.delete(nota_a_deletar) # Deleta a nota no banco de dados
        db.session.commit() # Fazer o commit da nova mudança no banco de dados

# definindo as tags
api_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
tudo_tag = Tag(name="Obter notas", description="Obter todas as nota")
#especifico_tag = Tag(name="Obter nota especifica", description="Obter nota especifica")
adicao_tag = Tag(name="Adicao de nota", description="Adicao de nota no bloco")
atualizacao_tag = Tag(name="Atualizacao de nota", description="Atualizacao de nota no bloco")
deletar_tag = Tag(name="Deletar nota", description="Apagar de nota no bloco")

@app.get('/api', tags=[api_tag])
def api():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação."""
    return redirect('/openapi')

@app.get('/', methods=['GET'] , tags=[tudo_tag])
def obter_notas():
    """Função que obtem todas as notas no banco de dados"""
    return jsonify({'Notas' : Nota.obter_todas_notas()})

#@app.get('/', methods=['GET'] , tags=[especifico_tag])
#def obter_nota_por_id():
    #"""Função que obtem nota específica no banco de dados"""
    #requisicao_de_dados = request.get_json() # Obtem o dado do cliente
    #id = requisicao_de_dados.get('id')
    #return jsonify(Nota.obter_nota(id))

@app.post('/', methods=['POST'] , tags=[adicao_tag])
def adicao_nota():
    """Função que adiciona nota no banco de dados usando"""
    requisicao_de_dados = request.get_json() # Obtem o dado do cliente
    nova_nota = Nota.adicao_nota(requisicao_de_dados["titulo"], requisicao_de_dados["texto"])
    resposta = jsonify(nova_nota.json())
    return resposta

@app.put('/', methods=['PUT'] , tags=[atualizacao_tag])
def editar_nota():
    """Função para editar a nota usando o id"""
    requisicao_de_dados = request.get_json() # Obtem o dado do cliente
    id = requisicao_de_dados.get('id')
    titulo = requisicao_de_dados.get('titulo')
    texto = requisicao_de_dados.get('texto')
    resposta = Nota.edicao_nota(id, titulo, texto)
    return jsonify(resposta)

@app.delete('/', methods=['DELETE'] , tags=[deletar_tag])
def remocao_nota():
    """Função para deletar a nota do banco de dados"""
    Nota.deletar_nota()
    resposta = Response("Nota deletada", status=200, mimetype='application/json')
    return resposta

"""Criação do banco de dados"""
@app.before_first_request
def create_table():
    db.create_all()
    app.run(debug=True)