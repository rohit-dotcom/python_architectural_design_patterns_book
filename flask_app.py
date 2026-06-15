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


def is_valid_sku(sku,batches):
    return sku in {b.sku for b in batches}


@app.route("/allocate", methods=["POST"])
def allocate_endpoint():
    session=get_session()
    batches=repository.SQLAlchemyRepository(session).list()
    print (request)
    line=model.Orderline(
        request.json['orderid'],request.json['sku'],request.json['qty']
    )
    if not is_valid_sku(line.sku,batches):
        return {"message": f"Invalid sku {line.sku}"},400
    
    try :
        batchref=model.allocate(line,batches)
    except model.OutOfStock as e:
        return {"message":str(e)},400

    session.commit()
    return {"batchref":batchref},201


@app.route("/health", methods=["GET"])
def health():
    return {"status": "ok"}, 200