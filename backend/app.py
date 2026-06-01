from flask import Flask, jsonify, request, send_from_directory
import os
from recomendador import carregar_ratings, carregar_filmes, calcular_inversoes, compatibilidade_percentual, recomendar_filmes
from nome import gerar_mapa_nomes


def create_app():
    base = os.path.dirname(os.path.abspath(__file__))
    frontend_dir = os.path.normpath(os.path.join(base, '..', 'frontend'))
    app = Flask(__name__, static_folder=frontend_dir, static_url_path='')
    path_ratings = os.path.join(base, 'ratings.csv')
    path_movies = os.path.join(base, 'movies.csv')

    ratings = carregar_ratings(path_ratings)
    filmes = carregar_filmes(path_movies)
    mapa_nomes = gerar_mapa_nomes(list(ratings.keys()))

    app.config['RATINGS'] = ratings
    app.config['FILMES'] = filmes
    app.config['MAPA_NOMES'] = mapa_nomes


    @app.route('/api/users')
    def users():
        mapa = app.config['MAPA_NOMES']
        users_list = [{'id': uid, 'name': nome} for uid, nome in sorted(mapa.items())]
        return jsonify(users_list)


    @app.route('/')
    def index():
        return send_from_directory(app.static_folder, 'index.html')


    @app.route('/api/top')
    def top():
        try:
            uid = int(request.args.get('user', ''))
        except Exception:
            return jsonify({'error': 'user param required'}), 400
        n = int(request.args.get('n', '5'))
        ratings = app.config['RATINGS']
        mapa = app.config['MAPA_NOMES']

        if uid not in ratings:
            return jsonify({'error': 'user not found'}), 404

        resultados = []
        for uid_b, ratings_b in ratings.items():
            if uid_b == uid:
                continue
            inversoes, n_comuns = calcular_inversoes(ratings[uid], ratings_b)
            if inversoes == -1:
                continue
            compat = compatibilidade_percentual(inversoes, n_comuns)
            resultados.append({'id': uid_b, 'name': mapa.get(uid_b, str(uid_b)), 'inversions': inversoes, 'common': n_comuns, 'compat': compat})

        resultados.sort(key=lambda x: x['inversions'])
        return jsonify({'top': resultados[:n]})


    @app.route('/api/recommend')
    def recommend():
        try:
            uid = int(request.args.get('user', ''))
        except Exception:
            return jsonify({'error': 'user param required'}), 400

        ratings = app.config['RATINGS']
        filmes = app.config['FILMES']
        mapa = app.config['MAPA_NOMES']

        if uid not in ratings:
            return jsonify({'error': 'user not found'}), 404

        # if client provided a specific similar user, use it
        similar = request.args.get('similar')
        if similar:
            try:
                sid = int(similar)
            except Exception:
                return jsonify({'error': 'invalid similar id'}), 400
            if sid not in ratings:
                return jsonify({'error': 'similar user not found'}), 404
            recs = recomendar_filmes(uid, sid, ratings, filmes, top_n=int(request.args.get('n', '5')))
            return jsonify({'based_on': mapa.get(sid, str(sid)), 'recommendations': [{'title': t, 'rating': r} for t, r in recs]})

        # otherwise pick best match
        resultados = []
        for uid_b, ratings_b in ratings.items():
            if uid_b == uid:
                continue
            inversoes, n_comuns = calcular_inversoes(ratings[uid], ratings_b)
            if inversoes == -1:
                continue
            compat = compatibilidade_percentual(inversoes, n_comuns)
            resultados.append((uid_b, inversoes, n_comuns, compat))

        if not resultados:
            return jsonify({'recommendations': []})

        resultados.sort(key=lambda x: x[1])
        melhor = resultados[0][0]
        recs = recomendar_filmes(uid, melhor, ratings, filmes, top_n=int(request.args.get('n', '5')))
        return jsonify({'based_on': mapa.get(melhor, str(melhor)), 'recommendations': [{'title': t, 'rating': r} for t, r in recs]})


    @app.route('/api/compare')
    def compare():
        try:
            a = int(request.args.get('user_a', ''))
            b = int(request.args.get('user_b', ''))
        except Exception:
            return jsonify({'error': 'user_a and user_b params required'}), 400

        ratings = app.config['RATINGS']
        filmes = app.config['FILMES']

        if a not in ratings or b not in ratings:
            return jsonify({'error': 'one or both users not found'}), 404

        inversoes, n_comuns = calcular_inversoes(ratings[a], ratings[b])
        if inversoes == -1:
            return jsonify({'inversions': -1, 'common': n_comuns, 'compat': None, 'shared': []})

        compat = compatibilidade_percentual(inversoes, n_comuns)
        comuns = sorted(set(ratings[a].keys()) & set(ratings[b].keys()))
        shared = [
            {
                'movieId': mid,
                'title': filmes.get(mid, f"Filme #{mid}"),
                'rating_a': ratings[a][mid],
                'rating_b': ratings[b][mid]
            }
            for mid in comuns
        ]

        return jsonify({'inversions': inversoes, 'common': n_comuns, 'compat': compat, 'shared': shared})

    return app


if __name__ == '__main__':
    application = create_app()
    application.run(host='0.0.0.0', port=5000, debug=True)
