from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
import json, csv, os, datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dbfolder/cars.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


def init_db():
    print "Initializing DB..."
    from models import Car, db
    if not os.path.exists("dbfolder"):
        os.mkdir("dbfolder")
    db.create_all()
    csv_file_ob = open("cars.csv", "r")
    csv_reader = csv.DictReader(csv_file_ob)
    for row in csv_reader:
        # print row
        make = row["make"]
        model = row["model"]
        year = int(row["year"]) if ((row["year"] is not None) and row["year"] != "") else None
        chassis_id = row["chassis_id"]
        price = float(row["price"]) if ((row["price"] is not None) and row["year"] != "") else None
        datetime_object = datetime.datetime.strptime(row["last_updated"], '%d/%m/%Y %H:%M:%S')
        car_obj = Car(make, model, year, chassis_id, price, datetime_object)
        try:
            db.session.add(car_obj)
            db.session.commit()
        except:
            db.session.rollback()
    csv_file_ob.close()
    print "Initializing done..."


@app.route("/car", methods=["GET", "POST"], strict_slashes=False)
def cars():
    from models import Car
    if request.method == "GET":
        res_json = {"cars": []}
        cars = Car.query.all()
        for car in cars:
            res_json["cars"].append({
                "make": car.make,
                "model": car.model,
                "year": car.year,
                "id": car.id,
                "last_updated": car.last_updated.strftime('%d/%m/%Y %H:%M:%S')
            })
        return json.dumps({"res": res_json})
    else:
        make = request.json["make"]
        model = request.json["model"]
        year = request.json["year"]
        chassis_id = request.json["chassis_id"]
        car_obj = Car(make, model, year, chassis_id, None, None)
        try:
            db.session.add(car_obj)
            db.session.commit()
            return "", 201
        except:
            db.session.rollback()
            return "", 500


@app.route("/car/<id>")
def get_car(id):
    from models import Car
    car_obj = Car.query.get(int(id))
    return json.dumps({
        "make": car_obj.make,
        "model": car_obj.model,
        "year": car_obj.year,
        "id": car_obj.id,
        "last_updated": car_obj.last_updated.strftime('%d/%m/%Y %H:%M:%S')
    })


@app.route("/avg_price", methods=["POST"], strict_slashes=False)
def get_car_avg_price():
    from models import Car
    make = request.json["make"]
    model = request.json["model"]
    year = request.json["year"]
    print make, model, year
    cars = db.session.query(Car).filter(Car.make == make, Car.model == model, Car.year == year)
    print cars
    avg = 0
    sum = 0
    num_cars = 0
    for car in cars:
        sum += car.price if car.price is not None else 0
        num_cars += 1
    avg = sum / num_cars
    return json.dumps({"avg_price": avg})


if __name__ == "__main__":
    init_db()
    app.run()
