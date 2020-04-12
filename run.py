from shop import app
from werkzeug.utils import secure_filename

if __name__ == "__main__":
    app.run(debug=True)