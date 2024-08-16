# Meu Back-End

Back-end do MVP **Bloco de Notas**

---
## Como executar

Após clonar o repositório, é necessário ir ao diretório raiz, pelo terminal, para poder executar os comandos descritos abaixo.

> É fortemente indicado o uso de ambientes virtuais do tipo [virtualenv](https://virtualenv.pypa.io/en/latest/installation.html).


Será necessário a criação doo diretório do virtual enviroment, o myvenv.

```
$ mkdir myvenv
```

Será criado o virtual enviroment propriamente, através do comando:

```
$ virtualenv myvenv
```

Para utilização do virtual enviroment ele deverá ser acessado com o comando abaixo:

```
$ source myvenv/bin/activate
```

Será necessário ter todas as libs python listadas no `requirements.txt` instaladas.

```
(myenv)$ pip install -r requirements.txt
```

Este comando instala as dependências/bibliotecas, descritas no arquivo `requirements.txt`.

Para executar a API  basta executar:

```
(myenv)$ flask run --host 0.0.0.0 --port 5000
```

Em modo de desenvolvimento é recomendado executar utilizando o parâmetro reload, que reiniciará o servidor automaticamente após uma mudança no código fonte. 

```
(myenv)$ flask run --host 0.0.0.0 --port 5000 --reload
```

Abra o [http://localhost:5000/api/#/](http://localhost:5000/api/#/) no navegador para verificar o status da API em execução.

---
## Como executar em docker

```
$ docker-compose up
```
