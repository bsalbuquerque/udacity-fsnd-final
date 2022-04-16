from flask import Flask, abort, jsonify, request
from flask_cors import CORS
from src.database.models import setup_db, Actor, Movie
from src.auth.auth0 import AuthError, requires_auth

PAGINATE = 3

'''
App creation

'''


def create_app():

    app = Flask(__name__)
    setup_db(app)
    CORS(app, resources={r"*": {"origins": "*"}})

    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS"
        )

        return response

    '''
    Pagination

    '''
    def paginate_actors(request, selection):
        page = request.args.get('page', 1, type=int)
        start = (page - 1) * PAGINATE
        end = start + PAGINATE

        actors = [actor.format() for actor in selection]
        current_actors = actors[start:end]

        return current_actors

    def paginate_movies(request, selection):
        page = request.args.get('page', 1, type=int)
        start = (page - 1) * PAGINATE
        end = start + PAGINATE

        movies = [movie.format() for movie in selection]
        current_movies = movies[start:end]

        return current_movies

    '''
    Home with Hello Reviewer

    '''
    @app.route('/')
    def index():
        return "Hello FSND Reviewer! :)"

    '''
    Actors endpoints

    '''
    @app.route('/actors')
    @requires_auth('get:actors')
    def list_actors(payload):
        selection = Actor.query.order_by(Actor.id.desc()).all()
        current_actors = paginate_actors(request, selection)

        if len(current_actors) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'actors': current_actors,
            'total_actors': len(Actor.query.all())
        })

    @app.route('/actors/<int:actor_id>', methods=['GET'])
    @requires_auth('get:actors')
    def get_actor(payload, actor_id):
        actor = Actor.query.filter(Actor.id == actor_id).one_or_none()

        if actor is None:
            abort(404)

        return jsonify({
            'success': True,
            'actor': actor.format()
        })

    @app.route('/actors', methods=['POST'])
    @requires_auth('post:actors')
    def new_actor(payload):
        body = request.get_json()

        name = body.get('name')
        age = body.get('age')
        gender = body.get('gender')

        try:
            actor = Actor(name=name, age=age, gender=gender)
            actor.insert()

            return jsonify({
                'success': True,
                'actor': actor.format()
            })

        except():
            abort(422)

    @app.route('/actors/<int:actor_id>', methods=['DELETE'])
    @requires_auth('delete:actors')
    def delete_actor(payload, actor_id):
        try:
            actor = Actor.query.filter(Actor.id == actor_id).one_or_none()

            if actor is None:
                abort(404)

            actor.delete()

            return jsonify({
                'success': True,
                'deletedId': actor_id
            })

        except():
            abort(404)

    @app.route('/actors/<int:actor_id>', methods=['PATCH'])
    @requires_auth('patch:actors')
    def update_actor(payload, actor_id):
        body = request.get_json()

        if body is None:
            abort(400)

        try:
            actor = Actor.query.filter(Actor.id == actor_id).one_or_none()

            if actor is None:
                abort(404)

            if 'name' in body:
                actor.name = str(body.get('name'))

            if 'age' in body:
                actor.age = int(body.get('age'))

            if 'gender' in body:
                actor.gender = str(body.get('gender'))

            actor.update()

            return jsonify({
                'success': True,
                'actorId': actor.id
            })

        except():
            abort(400)

    '''
    Movies endpoints

    '''
    @app.route('/movies')
    @requires_auth('get:movies')
    def list_movies(payload):
        selection = Movie.query.order_by(Movie.id.desc()).all()
        current_movies = paginate_movies(request, selection)

        if len(current_movies) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'movies': current_movies,
            'total_movies': len(Movie.query.all())
        })

    @app.route('/movies/<int:movie_id>', methods=['GET'])
    @requires_auth('get:movies')
    def get_movie(payload, movie_id):
        movie = Movie.query.filter(Movie.id == movie_id).one_or_none()

        if movie is None:
            abort(404)

        return jsonify({
            'success': True,
            'movie': movie.format()
        })

    @app.route('/movies', methods=['POST'])
    @requires_auth('post:movies')
    def new_movie(payload):
        body = request.get_json()

        name = body.get('name')
        year = body.get('year')

        try:
            movie = Movie(name=name, year=year)
            movie.insert()

            return jsonify({
                'success': True,
                'movie': movie.format()
            })

        except():
            abort(422)

    @app.route('/movies/<int:movie_id>', methods=['DELETE'])
    @requires_auth('delete:movies')
    def delete_movie(payload, movie_id):
        try:
            movie = Movie.query.filter(Movie.id == movie_id).one_or_none()

            if movie is None:
                abort(404)

            movie.delete()

            return jsonify({
                'success': True,
                'deletedId': movie_id
            })

        except():
            abort(404)

    @app.route('/movies/<int:movie_id>', methods=['PATCH'])
    @requires_auth('patch:movies')
    def update_movie(payload, movie_id):
        body = request.get_json()

        if body is None:
            abort(400)

        try:
            movie = Movie.query.filter(Movie.id == movie_id).one_or_none()

            if movie is None:
                abort(404)

            if 'name' in body:
                movie.name = str(body.get('name'))

            if 'release' in body:
                movie.year = int(body.get('release'))

            movie.update()

            return jsonify({
                'success': True,
                'movieId': movie.id
            })

        except():
            abort(400)

    '''
    Error handlers

    '''
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "bad request"
        }), 400

    @app.errorhandler(401)
    def unauthorized(error):
        return jsonify({
            "success": False,
            "error": 401,
            "message": "unauthorized"
        }), 401

    @app.errorhandler(405)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 405,
            "message": "method not allowed"
        }), 405

    @app.errorhandler(AuthError)
    def handle_auth_error(ex):
        response = jsonify(ex.error)
        response.status_code = ex.status_code

        return response

    return app

