from flask import Flask, request
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import config
import orm
import model
import repository


orm.start_mapper()
get_session=sessionmaker(bind=create_engine(config.get_postgres_url()))
app=Flask(__name__)

@app.route("/allocate", methods=["POST"])
def allocate_endpoint():
    session=get_session()
    batches=repository.SQLAlchemyRepository(session).list()
    print (request)
    line=model.Orderline(
        request.json['orderid'],request.json['sku'],request.json['qty']
    )
    batchref=model.Batch.allocate(line,batches)
    return {"batchref":batchref},201


@app.route("/health", methods=["GET"])
def health():
    return {"status": "ok"}, 200