NOMES = [
    "Alice", "Bruno", "Carla", "Diego", "Elena", "Felipe", "Gabriela",
    "Henrique", "Isabela", "João", "Karen", "Lucas", "Mariana", "Nicolas",
    "Olivia", "Pedro", "Quinn", "Rafael", "Sofia", "Thiago", "Úrsula",
    "Victor", "Wendy", "Xavier", "Yara", "Zeca", "Amanda", "Bernardo",
    "Cecília", "Daniel", "Eduarda", "Fábio", "Giovana", "Hélio", "Iara",
    "Júlio", "Keila", "Leandro", "Mônica", "Nathan", "Olga", "Paulo",
    "Renata", "Samuel", "Tatiana", "Ulisses", "Vanessa", "William",
    "Xênia", "Yasmin", "Zilda", "Arthur", "Beatriz", "Caio", "Diana",
    "Emílio", "Flávia", "Gustavo", "Helena", "Igor", "Juliana", "Klaus",
]
 
 
def gerar_mapa_nomes(user_ids: list[int]) -> dict[int, str]:
    ids_ordenados = sorted(user_ids)
    return {uid: NOMES[i % len(NOMES)] for i, uid in enumerate(ids_ordenados)}
 