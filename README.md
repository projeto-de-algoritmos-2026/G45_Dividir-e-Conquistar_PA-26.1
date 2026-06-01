# G45_Dividir-e-Conquistar_PA-26.1
## Recomendação por Contagem de Inversões
**Número da Lista**: 45<br>
**Conteúdo da Disciplina**: Dividir e Conquistar<br>

## Alunos
|Matrícula | Aluno |
| -- | -- |
| 20/2016909  | Marcelo Adrian Ribeiro de Araujo |
| 24/2015924  | Maria Eduarda de Jezus Guimarães |

## Sobre

Este projeto implementa um sistema de recomendação de filmes utilizando **contagem de inversões** como métrica de similaridade entre usuários, aplicando o paradigma de **Dividir e Conquistar** por meio de uma adaptação do Merge Sort.

A ideia central é: dado dois usuários que assistiram filmes em comum, monta o ranking de preferências de cada um e conta-se quantas inversões existem entre eles. A partir disso, o sistema identifica os usuários mais similares e recomenda filmes que o perfil mais compatível curtiu e o usuário alvo ainda não viu.

Na versão atual, o projeto possui uma interface web em `frontend/` e um wrapper Flask em `backend/app.py` que expõe os dados por HTTP. A interface permite listar usuários, ver os perfis mais compatíveis e comparar duas pessoas com métricas objetivas como filmes em comum, inversões e compatibilidade percentual.

O dataset utilizado é o MovieLens ml-latest-small, disponibilizado pelo GroupLens Research da Universidade de Minnesota:
https://grouplens.org/datasets/movielens/


## Screenshots

O frontend web foi construído com um layout leve e parecido com os trabalhos anteriores, usando um painel central para seleção de usuários e exibição dos resultados.


## Instalação

**Linguagem**: Python 3<br>
**Framework**: Flask<br>

### Pré-requisitos

- Ter o Python 3 instalado.
- Estar na raiz do projeto.
- Ter os arquivos do dataset dentro de `backend/`:
  - `backend/ratings.csv`
  - `backend/movies.csv`
- Instalar as dependências listadas em `backend/requirements.txt`.

O dataset usado é o MovieLens `ml-latest-small`, disponibilizado pelo GroupLens Research da Universidade de Minnesota:
https://grouplens.org/datasets/movielens/

### Comando para executar

Modo terminal no backend:

```bash
cd backend
python3 recomendador.py
```

Modo web com frontend e API:

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

## Uso

#### Modo Terminal

Ao executar `backend/recomendador.py`, o programa roda no terminal com menu interativo e não depende do navegador.

Fluxo de uso:

1. O programa carrega os arquivos `ratings.csv` e `movies.csv`.
2. Exibe o menu principal no console.
3. Escolha uma das opções:

```
  [1] Comparar dois usuários
  [2] Ver top compatíveis com um usuário
  [3] Listar usuários
  [0] Sair
```

4. Siga as instruções na tela para informar IDs ou nomes.

#### Modo Web

Ao executar `backend/app.py`, o servidor Flask carrega o dataset, disponibiliza a API e também serve o frontend web na raiz `http://127.0.0.1:5000/`.

O menu principal da interface web oferece:

```
  [1] Top compatíveis (pessoas)
  [2] Recomendar filmes para um usuário
  [3] Comparar duas pessoas
```

Como usar o frontend:

1. Abra `http://127.0.0.1:5000/` no navegador.
2. Selecione um usuário no primeiro dropdown.
3. Clique em `Top compatíveis (pessoas)` para ver quem tem gostos parecidos.
4. Clique em `Recomendar filmes` para ver sugestões com base no perfil mais parecido.
5. Clique em `Comparar duas pessoas` para mostrar o segundo dropdown, escolha outro usuário e depois clique em `Executar comparação`.
6. A comparação exibe filmes em comum, número de inversões e a compatibilidade percentual.

#### Modo 1 — Comparação entre dois usuários

1. Lista os usuários disponíveis (com nomes fictícios e IDs).
2. Permite escolher um usuário alvo e, quando ativado, um segundo usuário para comparação.
3. Encontra os filmes que ambos avaliaram em comum.
4. Monta o ranking de preferências de cada um.
5. Conta as inversões entre os rankings usando Merge Sort.
6. Exibe filmes em comum, inversões, compatibilidade em percentual e as notas lado a lado.

#### Modo 2 — Top usuários mais compatíveis

1. Solicita um usuário alvo.
2. Compara com todos os outros usuários do dataset.
3. Ordena pelo menor número de inversões.
4. Exibe o top 5 de pessoas mais compatíveis.
5. Recomenda filmes com base no perfil mais similar.


## Vídeo de Apresentação

Ainda não adicionado.

## Outros

- A interface web está disponível em `frontend/` e é servida pelo Flask em `backend/app.py`.
- O backend expõe os endpoints `GET /api/users`, `GET /api/top`, `GET /api/recommend` e `GET /api/compare`.
- O algoritmo central (Merge Sort com contagem de inversões) está implementado em `recomendador.py` nas funções `merge_sort_inversoes` e `_merge`.
- Apenas usuários com 40 ou mais avaliações são considerados, garantindo interseções significativas entre perfis.
- Fonte do dataset: GroupLens Research — https://grouplens.org/datasets/movielens/