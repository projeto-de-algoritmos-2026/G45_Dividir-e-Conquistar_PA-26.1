import csv
import os

from nome import gerar_mapa_nomes

def carregar_ratings(caminho: str):

    MIN_RATINGS = 40
    ratings_raw: dict[int, dict[int, float]] = {}

    with open(caminho, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            uid = int(row["userId"])
            mid = int(row["movieId"])
            rating = float(row["rating"])
            if uid not in ratings_raw:
                ratings_raw[uid] = {}
            ratings_raw[uid][mid] = rating

    return {uid: filmes for uid, filmes in ratings_raw.items()
            if len(filmes) >= MIN_RATINGS}


def carregar_filmes(caminho: str):
    filmes = {}
    with open(caminho, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            filmes[int(row["movieId"])] = row["title"]
    return filmes


def merge_sort_inversoes(arr: list):

    if len(arr) <= 1:
        return arr, 0

    meio = len(arr) // 2
    esq, inv_esq = merge_sort_inversoes(arr[:meio])
    dir, inv_dir = merge_sort_inversoes(arr[meio:])
    merged, inv_merge = _merge(esq, dir)

    return merged, inv_esq + inv_dir + inv_merge


def _merge(esq: list, dir: list):

    resultado = []
    inversoes = 0
    i = j = 0

    while i < len(esq) and j < len(dir):
        if esq[i] <= dir[j]:
            resultado.append(esq[i])
            i += 1
        else:
            resultado.append(dir[j])
            inversoes += len(esq) - i
            j += 1

    resultado.extend(esq[i:])
    resultado.extend(dir[j:])
    return resultado, inversoes

def montar_ranking(filmes_usuario: dict[int, float], filmes_comuns: list[int]):

    pares = [(mid, filmes_usuario[mid]) for mid in filmes_comuns]
    pares.sort(key=lambda x: x[1], reverse=True)
    return [mid for mid, _ in pares]


def calcular_inversoes(ratings_a: dict[int, float], ratings_b: dict[int, float]):
    comuns = list(set(ratings_a.keys()) & set(ratings_b.keys()))
    if len(comuns) < 5:
        return -1, len(comuns)  
    ranking_a = montar_ranking(ratings_a, comuns)
    pos_a = {mid: i for i, mid in enumerate(ranking_a)}

    ranking_b = montar_ranking(ratings_b, comuns)
    pos_b = {mid: i for i, mid in enumerate(ranking_b)}
    sequencia = [pos_b[mid] for mid in ranking_a]

    _, inversoes = merge_sort_inversoes(sequencia)
    return inversoes, len(comuns)


def compatibilidade_percentual(inversoes: int, n_filmes: int):

    max_inv = n_filmes * (n_filmes - 1) / 2
    if max_inv == 0:
        return 100.0
    return round((1 - inversoes / max_inv) * 100, 1)

def recomendar_filmes(alvo_id: int,similar_id: int,ratings: dict[int, dict[int, float]],filmes: dict[int, str],top_n: int = 5):

    vistos_alvo = set(ratings[alvo_id].keys())
    candidatos = [
        (mid, rating)
        for mid, rating in ratings[similar_id].items()
        if mid not in vistos_alvo and rating >= 3.5
    ]
    candidatos.sort(key=lambda x: x[1], reverse=True)
    return [(filmes.get(mid, f"Filme #{mid}"), rating)
            for mid, rating in candidatos[:top_n]]


def separador(char="─", n=55):
    print(char * n)


def listar_usuarios(ratings: dict, mapa_nomes: dict):
    separador("═")
    print("  USUÁRIOS DISPONÍVEIS")
    separador("═")
    ids = sorted(ratings.keys())
    for i in range(0, len(ids), 5):
        linha = ids[i:i+5]
        print("  " + "   ".join(
            f"{mapa_nomes[uid]:10s}(#{uid})" for uid in linha
        ))
    separador()


def escolher_usuario(ratings: dict, mapa_nomes: dict, prompt: str):
    ids_validos = set(ratings.keys())
    while True:
        entrada = input(prompt).strip()
        if entrada.isdigit() and int(entrada) in ids_validos:
            return int(entrada)
        for uid, nome in mapa_nomes.items():
            if entrada.lower() == nome.lower() and uid in ids_validos:
                return uid
        print(f"  ✗ ID/nome inválido. Tente novamente.")


def exibir_comparacao(uid_a: int, uid_b: int,ratings: dict, filmes: dict, mapa_nomes: dict):

    inversoes, n_comuns = calcular_inversoes(ratings[uid_a], ratings[uid_b])
    nome_a = mapa_nomes[uid_a]
    nome_b = mapa_nomes[uid_b]

    separador("═")
    print(f"  COMPARAÇÃO: {nome_a} × {nome_b}")
    separador("═")

    if inversoes == -1:
        print(f"  Filmes em comum: {n_comuns} — insuficiente para comparar (mínimo 5).")
        return

    compat = compatibilidade_percentual(inversoes, n_comuns)

    print(f"  Filmes em comum : {n_comuns}")
    print(f"  Inversões       : {inversoes}")
    print(f"  Compatibilidade : {compat}%  \n", end="")

    separador()
    print(f"\n  FILMES RECOMENDADOS PARA {nome_a.upper()}")
    print(f"  (baseado no gosto de {nome_b})\n")

    recomendacoes = recomendar_filmes(uid_a, uid_b, ratings, filmes)
    if not recomendacoes:
        print("  Nenhuma recomendação nova encontrada.")
    for titulo, nota in recomendacoes:
        print(f"  ★ {nota:.1f}  {titulo}")

    separador()


def exibir_top_similares(uid_alvo: int,ratings: dict, filmes: dict, mapa_nomes: dict,top_n: int = 5):
    nome_alvo = mapa_nomes[uid_alvo]

    separador("═")
    print(f"  TOP COMPATÍVEIS COM {nome_alvo.upper()}")
    separador("═")

    resultados = []
    for uid_b, ratings_b in ratings.items():
        if uid_b == uid_alvo:
            continue
        inversoes, n_comuns = calcular_inversoes(ratings[uid_alvo], ratings_b)
        if inversoes == -1:
            continue
        compat = compatibilidade_percentual(inversoes, n_comuns)
        resultados.append((uid_b, inversoes, n_comuns, compat))

    if not resultados:
        print("  Sem usuários comparáveis encontrados.")
        return

    resultados.sort(key=lambda x: x[1]) 
    top = resultados[:top_n]

    for pos, (uid_b, inversoes, n_comuns, compat) in enumerate(top, 1):
        nome_b = mapa_nomes[uid_b]
        print(f"  {pos}. {nome_b:12s}(#{uid_b})  —  {compat}% compatível"
              f"  [{n_comuns} filmes em comum, {inversoes} inversões]")

    separador()

    melhor_id = top[0][0]
    melhor_nome = mapa_nomes[melhor_id]
    print(f"\n  RECOMENDAÇÕES PARA {nome_alvo.upper()}")
    print(f"  (baseado no gosto de {melhor_nome}, seu match mais próximo)\n")

    recomendacoes = recomendar_filmes(uid_alvo, melhor_id, ratings, filmes)
    if not recomendacoes:
        print("  Nenhuma recomendação nova encontrada.")
    for titulo, nota in recomendacoes:
        print(f"  ★ {nota:.1f}  {titulo}")

    separador()


def menu_modo():
    separador("═")
    print("  O QUE DESEJA FAZER?")
    separador()
    print("  [1] Comparar dois usuários")
    print("  [2] Ver top compatíveis com um usuário")
    print("  [3] Listar usuários")
    print("  [0] Sair")
    separador()
    return input("  Escolha: ").strip()


def main():
    base = os.path.dirname(os.path.abspath(__file__))
    path_ratings = os.path.join(base, "ratings.csv")
    path_movies  = os.path.join(base, "movies.csv")

    print("\n  Carregando dataset MovieLens...")
    ratings = carregar_ratings(path_ratings)
    filmes  = carregar_filmes(path_movies)
    mapa_nomes = gerar_mapa_nomes(list(ratings.keys()))

    print(f"  {len(ratings)} usuários ativos carregados.\n")

    while True:
        opcao = menu_modo()

        if opcao == "0":
            print("\n  Até logo!\n")
            break

        elif opcao == "3":
            listar_usuarios(ratings, mapa_nomes)

        elif opcao == "1":
            listar_usuarios(ratings, mapa_nomes)
            uid_a = escolher_usuario(ratings, mapa_nomes,"  Usuário A (ID ou nome): ")
            uid_b = escolher_usuario(ratings, mapa_nomes, "  Usuário B (ID ou nome): ")
            exibir_comparacao(uid_a, uid_b, ratings, filmes, mapa_nomes)

        elif opcao == "2":
            listar_usuarios(ratings, mapa_nomes)
            uid_alvo = escolher_usuario(ratings, mapa_nomes,
                                        "  Usuário alvo (ID ou nome): ")
            exibir_top_similares(uid_alvo, ratings, filmes, mapa_nomes)

        else:
            print("  Opção inválida.\n")


if __name__ == "__main__":
    main()