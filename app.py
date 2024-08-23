from flask import Flask, jsonify, request, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_swagger_ui import get_swaggerui_blueprint
import logging

app = Flask(__name__)
app.secret_key = "4321Lupa"

# Database configuration for production
app.config["SQLALCHEMY_DATABASE_URI"] = (
    "postgresql://data_catcleango:8d0f9d00c202580dfdde988d310e3cf60c82295b@twu.h.filess.io:5433/data_catcleango"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

# Enable SQLAlchemy logging
logging.basicConfig()
logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)

# Swagger setup
SWAGGER_URL = "/swagger"
API_URL = "/swagger/swagger.yaml"
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL, API_URL, config={"app_name": "DIGIPAN"}
)
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)


# Models
class Family(db.Model):
    __tablename__ = "family"
    __table_args__ = {"schema": "data_keluarga"}
    id = db.Column(db.Integer, primary_key=True)
    nama_keluarga = db.Column(db.String(100), nullable=False)
    nama = db.Column(db.String(100), nullable=False)
    tempat_lahir = db.Column(db.String(100), nullable=False)
    tanggal_lahir = db.Column(db.Date, nullable=False)
    nomor_keluarga = db.Column(db.String(20), nullable=False)
    hubungan_keluarga = db.Column(db.String(50), nullable=False)


class User(db.Model):
    __tablename__ = "user"
    __table_args__ = {"schema": "data_keluarga"}
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)


class SuratPengantar(db.Model):
    __tablename__ = "surat_pengantar"
    __table_args__ = {"schema": "data_keluarga"}
    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(50))
    tanggal = db.Column(db.Date)
    tempatlahir = db.Column(db.String(100))
    jeniskelamin = db.Column(db.String(255))
    pekerjaan = db.Column(db.String(100))
    alamatktp = db.Column(db.String(255))
    tujuan = db.Column(db.Text)

    def __init__(
        self, nama, tanggal, tempatlahir, jeniskelamin, pekerjaan, alamatktp, tujuan
    ):
        self.nama = nama
        self.tanggal = tanggal
        self.tempatlahir = tempatlahir
        self.jeniskelamin = jeniskelamin
        self.pekerjaan = pekerjaan
        self.alamatktp = alamatktp
        self.tujuan = tujuan


@app.route("/swagger/swagger.yaml")
def swagger_spec():
    return send_from_directory("swagger", "swagger.yaml")


# Routes for testing
@app.route("/families", methods=["GET"])
def get_families():
    families = Family.query.all()
    return jsonify(
        [
            {
                "id": family.id,
                "nama_keluarga": family.nama_keluarga,
                "nama": family.nama,
                "tempat_lahir": family.tempat_lahir,
                "tanggal_lahir": family.tanggal_lahir.isoformat(),
                "nomor_keluarga": family.nomor_keluarga,
                "hubungan_keluarga": family.hubungan_keluarga,
            }
            for family in families
        ]
    )


@app.route("/families/by-name/<string:nama_keluarga>", methods=["GET"])
def get_family_by_name(nama_keluarga):
    families = Family.query.filter(Family.nama_keluarga.ilike(nama_keluarga)).all()
    if not families:
        return jsonify({"message": "No families found with the given name"}), 404
    return jsonify(
        [
            {
                "id": family.id,
                "nama_keluarga": family.nama_keluarga,
                "nama": family.nama,
                "tempat_lahir": family.tempat_lahir,
                "tanggal_lahir": family.tanggal_lahir.isoformat(),
                "nomor_keluarga": family.nomor_keluarga,
                "hubungan_keluarga": family.hubungan_keluarga,
            }
            for family in families
        ]
    )


if __name__ == "__main__":
    app.run(debug=True)
