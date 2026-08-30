from flask import Flask
from database.db_manager import init_db
from controllers.main_ctrl import main_bp
from controllers.voter_ctrl import voter_bp
from controllers.staff_ctrl import staff_bp

app = Flask(__name__, template_folder='views/templates')
app.secret_key = 'super_secret_key'

with app.app_context():
    init_db()

app.register_blueprint(main_bp)
app.register_blueprint(voter_bp)
app.register_blueprint(staff_bp)

if __name__ == '__main__':
    app.run(debug=True)