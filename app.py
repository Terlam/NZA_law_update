from flask_api import app

from faker_seed_db import seedData

if __name__ == "__main__":
    app.run(debug = True)