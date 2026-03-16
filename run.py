from flask import Flask
from config import Config

# Import Blueprints
from app.routes.auth_routes import auth_bp
from app.routes.dashboard_routes import dashboard_bp
from app.routes.ticket_routes import ticket_bp
from app.routes.comment_routes import comment_bp
from app.routes.user_routes import user_bp 
from app.routes.developer_routes import developer_bp 


def create_app():

    app = Flask(__name__)
    app.config.from_object(Config)

    # Register Blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(ticket_bp)
    app.register_blueprint(comment_bp)
    app.register_blueprint(user_bp) 
    app.register_blueprint(developer_bp)

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)