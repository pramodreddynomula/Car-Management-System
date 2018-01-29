curl http://localhost:5000/car/1
curl http://localhost:5000/car/
curl -d '{"make":"Seat","model":"Cordoba", "year":"2003"}' -H "Content-Type:application/json" -X POST http://localhost:5000/avgprice
curl -d '{"make":"Seat","model":"Cordoba", "year":"2003","chassis_id":"12345F"}' -H "Content-Type: application/json" -X POST http://localhost:5000/car