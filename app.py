from flask_openapi3 import OpenAPI, Info , Tag
from flask import Flask, request, Response, jsonify, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import json

info = Info(title="Back End", version="0.1")
app = OpenAPI(__name__, info=info)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///nota.sqlite3'

CORS(app)

db = SQLAlchemy(app)

# A classe Nota vai herdar o db.Model do SQLAlchemy
class Nota(db.Model):
    __tablename__ = "nota"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50))
    descricao = db.Column(db.String(100))
    
    def __init__(self, nome, descricao):
        self.nome = nome
        self.descricao = descricao

    def json(self):
        return {'id': self.id, 'nome': self.nome, 
                'descricao': self.descricao}    

    def obter_todas_notas():
        """Função que obtem todas as notas no banco de dados"""
        return [Nota.json(nota) for nota in Nota.query.all()]
    
    def obter_nota(_id):
        """Funcão para obter a nota usando o id da nota como parametro"""
        Nota.json(Nota.query.filter_by(id=_id).first())

    def adicao_nota(_nome, _descricao):
        """Função para adicionar nota no banco de dados usando _nome e _descricao como parametros"""
        #criando a instancia da noissa Nota como construtor
        nova_nota = Nota(nome=_nome, descricao=_descricao)
        db.session.add(nova_nota) # adiciona nova nota na seção do banco de dados
        db.session.commit() # fazer o commita das mudanças no banco de dados

    def atualizacao_nota(_id, _nome, _descricao):
        """Função para atualizar os detalhes da nota usando o id, nome e descrição como oarametros"""
        nota_a_atualizar = Nota.query.filter_by(id=_id).first()
        nota_a_atualizar = _nome
        nota_a_atualizar = _descricao
        db.session.commit()

    def deletar_nota(_id):
        """Função para deletar a nota do banco de dados usando o id da nota como o parametro"""
        Nota.query.filter_by(id=_id).delete() # Filtrar a nota pelo id e deletar
        db.session.commit() # Fazer o commit da nova mudança no banco de dados

# definindo tags
api_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
tudo_tag = Tag(name="Obter notas", description="Obter todas as nota")
especifico_tag = Tag(name="Obter nota especifica", description="Obter nota especifica")
adicao_tag = Tag(name="Adicao de nota", description="Adicao de nota no bloco")
atualizacao_tag = Tag(name="Atualizacao de nota", description="Atualizacao de nota no bloco")
deletar_tag = Tag(name="Deletar nota", description="Apagar de nota no bloco")
# produto_tag = Tag(name="Produto", description="Adição, visualização e remoção de produtos à base")
# comentario_tag = Tag(name="Comentario", description="Adição de um comentário à um produtos cadastrado na base")

@app.get('/api', tags=[api_tag])
def api():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação.
    """
    return redirect('/openapi')

@app.get('/', methods=['GET'] , tags=[tudo_tag])
def obter_notas():
    """Função que obtem todas as notas no banco de dados"""
    return jsonify({'Notas' : Nota.query.all()})

@app.get('/notas/<int:nota_id>', methods=['GET'] , tags=[especifico_tag])
def obter_nota_por_id(id):
    retorna_valor = Nota.obter_nota(id) 
    return jsonify(retorna_valor)

@app.post('/adicao', methods=['POST'] , tags=[adicao_tag])
def adicao_nota():
    """Função que adiciona nota no banco de dados usando"""
    requisicao_de_dados = request.get_json() # obtendo o dado do cliente
    Nota.adicao_nota(requisicao_de_dados["nome"], requisicao_de_dados["descricao"])
    resposta = Response("Nota adicionada", 201, mimetype='application/json')
    return resposta

@app.put('/notas/<int:nota_id>', methods=['PUT'] , tags=[atualizacao_tag])
def atualizar_nota(id):
    """Função para editar a nota usando o id"""
    requisicao_de_dados = request.get_json()
    Nota.atualizacao_nota(id, requisicao_de_dados['nome'], requisicao_de_dados['descricao'])
    resposta = Response("Nota atualizada", status=200, mimetype='application/json')
    return resposta

@app.delete('/notas/<int:nota_id>', methods=['DELETE'] , tags=[deletar_tag])
def remocao_nota(id):
    """Função para deletar a nota do banco de dados"""
    Nota.deletar_nota(id)
    resposta = Response("Nota deletada", status=200, mimetype='application/json')
    return resposta

@app.before_first_request
def create_table():
    db.create_all()
    app.run(debug=True)