from src.app import app


if __name__ == '__main__':
    app.run(debug=app.config['DEBUG'], port=4990)