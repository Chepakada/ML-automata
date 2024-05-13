from app import create_app, db
from flask import Flask, jsonify, request
from models import *
app = create_app()

@app.route("/files", methods = ["GET", "POST"], strict_slashes = False )

def files():

    if request.method == "POST":
        file_data = request.get_json()
        new_file = Files(**file_data)
        db.session.add(new_file)
        db.session.commit()

        if new_file.id:
            return jsonify({"message": " File Added Successfilly"}), 201
        else:
            return jsonify({"error":"Failed to add file to database"}), 500
    else:
        files = Files.query.all()
        results = article_schema.dump(files)

        return jsonify(results)


if __name__ == "__main__":
    app.run(debug=True)
