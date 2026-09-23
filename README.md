# MVP-DBA - *Book Review API*

#### 1. Descrição

API criada para o projeto [Book Review](https://github.com/thelunacodes/MVP-DBA-Front-End), uma plataforma que permite o usuário pesquisar e avaliar uma vasta seleção de livros, fornecidas pela [API pública da OpenLibrary](https://openlibrary.org/dev/docs/api/search). 

Essa API possui as seguintes funcionalidades:

1. Cadastro de usuários, com autenticação e hash de senha usando o algoritmo **argon2**
2. Cadastro de reviews de livros, fazendo uso das chaves fornecidas pela API da Open Library
3. Registro de likes vinculados às reviews

#### 2. Pré-Requisitos

1. Uma IDE de sua escolha (exemplo: Visual Studio Code)
2. [Git](https://git-scm.com/)
3. [Python](https://www.python.org/)
4. [Docker](https://www.docker.com/)

#### 3. Instalação e execução 

(TODO: INCLUIR INSTRUÇÕES PARA EXECUÇÃO DO DOCKER E TALS)

**Passo 1 - Clone o repositório para sua máquina**

Em um terminal, execute os comandos:
 
    git clone https://github.com/thelunacodes/MVP-DBA-Back-End.git

**Passo 2 - Navegue para a pasta do projeto**

    cd MVP-DBA-Back-End

**Passo 3 - Instale as dependências do projeto**

    pip install -r requirements.txt

**Passo 4 - Inicie o servidor**

    flask run --host 0.0.0.0 --port 5000 --debug

Você pode acessar a interface da API por meio do link:

    http://localhost:<port>

*Obs: Nesse caso, o "port" é 5000, o número que passamos na hora de iniciar o servidor*

**Como o projeto é executado em um servidor de desenvolvimento local, ele só pode ser acessado pela sua máquina.**

