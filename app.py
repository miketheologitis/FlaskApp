from flaskr import app
from json import load

if __name__ == '__main__':
    with open('conf.json', 'r') as f:
        conf = load(f)

    app.run(
        host=conf['APP']['HOST'],
        port=conf['APP']['PORT'],
        debug=True
    )


