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

O dataset utilizado é o MovieLens ml-latest-small, disponibilizado pelo GroupLens Research da Universidade de Minnesota:
https://grouplens.org/datasets/movielens/


## Screenshots



## Instalação

**Linguagem**: Python 3<br>
**Framework**: Não se aplica<br>

### Pré-requisitos

- Ter o Python 3 instalado.
- Estar na raiz do projeto.
- Ter os arquivos do dataset na mesma pasta do script:
  - `ratings.csv`
  - `movies.csv`

O dataset pode ser baixado em: https://grouplens.org/datasets/movielens/latest/

### Comando para executar

```bash
python3 backend/recomendador.py
```

## Uso

#### Modo Terminal

Ao executar, o programa carrega o dataset e exibe as opções do Menu principal:

```
  [1] Comparar dois usuários
  [2] Ver top compatíveis com um usuário
  [3] Listar usuários
  [0] Sair
```

#### Modo 1 — Comparação entre dois usuários

1. Lista os usuários disponíveis (com nomes fictícios e IDs).
2. Solicita dois usuários (por ID ou nome).
3. Encontra os filmes que ambos avaliaram em comum.
4. Monta o ranking de preferências de cada um.
5. Conta as inversões entre os rankings usando Merge Sort.
6. Exibe a compatibilidade em percentual e recomenda filmes.

#### Modo 2 — Top usuários mais compatíveis

1. Solicita um usuário alvo.
2. Compara com todos os outros usuários do dataset.
3. Ordena pelo menor número de inversões.
4. Exibe o top 5 mais compatíveis.
5. Recomenda filmes com base no perfil mais similar.


## Vídeo de Apresentação


## Outros

- Interface web em desenvolvimento.
- O algoritmo central (Merge Sort com contagem de inversões) está implementado em `recomendador.py` nas funções `merge_sort_inversoes` e `_merge`.
- Apenas usuários com 40 ou mais avaliações são considerados, garantindo interseções significativas entre perfis.
- Fonte do dataset: GroupLens Research — https://grouplens.org/datasets/movielens/