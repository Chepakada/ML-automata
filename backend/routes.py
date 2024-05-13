from app import create_app
from flask import Flask, jsonify
from models import *
app = create_app()

@app.route("/files", methods = ["GET", "POST"], strict_slashes = False )

def files():
    
    files = Files.query.all()
    results = FilesShema.dump(files)

    return jsonify(results)


if __name__ == "__main__":
    app.run(debug=True)
