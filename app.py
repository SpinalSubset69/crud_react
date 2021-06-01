from flask import Flask
from flask_cors import CORS
from routes import Routes

app = Flask(__name__)

# Cargamos archivo de rutas desde donde se manejara todo
routes = Routes(app)

# Configurando CORS
CORS(app)


# Runing Server
if __name__ == '__main__':
    app.run(port=3200, debug=True)
