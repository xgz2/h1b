import json
from flask import Flask, request
from db import db, H1bRow

# define db filename
db_filename = "h1b.db"
app = Flask(__name__)

#setup config
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_filename}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True

# initialize app
db.init_app(app)
with app.app_context():
    db.create_all()

# generalized response formats
def success_response(data, code=200):
    return json.dumps(data), code

def failure_response(message, code=404):
    return json.dumps({'error': message}), code

#-- TASK ROUTES -------------------------------------------------------------------

@app.route("/")
@app.route("/h1b_rows")
def get_h1b_rows():
    """_summary_

    Returns:
        _type_: _description_
    """
    h1b_rows = [h1b_row.serialize() for h1b_row in H1bRow.query.all()]
    return success_response({"h1b_rows": h1b_rows})

@app.route("/h1b_rows/<int:h1b_row_id>/")
def get_h1b_row(h1b_row_id):
    h1b_row = H1bRow.query.filter_by(id=h1b_row_id).first()
    if h1b_row is None:
        return failure_response("H1b row not found!")
    return success_response(h1b_row.serialize())

@app.route("/h1b_rows/", methods=["POST"])
def create_h1b_row():
    body = json.loads(request.data)
    new_h1b_row = H1bRow(
        employer = body.get("employer"),
        job_title = body.get("job_title"),
        base_salary = body.get("base_salary"),
        location = body.get("location")
    )
    db.session.add(new_h1b_row)
    db.session.commit()
    return success_response(new_h1b_row.serialize(), 201)

@app.route("/h1b_rows/<int:h1b_row_id>/", methods=["POST"])
def update_h1b_row(h1b_row_id):
    body = json.loads(request.data)
    h1b_row = H1bRow.query.filter_by(id=h1b_row_id).first()
    if h1b_row is None:
        return failure_response("H1b row not found!")
    h1b_row.employer = body.get("employer", h1b_row.employer)
    h1b_row.job_title = body.get("job_title", h1b_row.job_title)
    h1b_row.base_salary = body.get("base_salary", h1b_row.base_salary)
    h1b_row.location = body.get("location", h1b_row.location)
    db.session.commit()
    return success_response(h1b_row.serialize())

@app.route("/h1b_rows/<int:h1b_row_id>/", methods=["DELETE"])
def delete_h1b_row(h1b_row_id):
    h1b_row = H1bRow.query.filter_by(id=h1b_row_id).first()
    if h1b_row is None:
        return failure_response("H1b row not found!")
    db.session.delete(h1b_row)
    db.session.commit()
    return success_response(h1b_row.serialize())