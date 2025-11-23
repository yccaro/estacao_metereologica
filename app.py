from config import app
from controllers import auth_controller, user_controller, leitura_controller

if __name__ == "__main__":
    app.run(debug=True)
