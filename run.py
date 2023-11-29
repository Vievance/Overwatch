from fancii import create_app, db
from flask_migrate import Migrate

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = create_app()
migrate = Migrate(app, db)


with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)

    