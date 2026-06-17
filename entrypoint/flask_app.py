from flask import Flask, request
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import config
import adapters.orm as orm
import domain.model as model
import adapters.repository as repository
import services.services as services


orm.start_mapper()
get_session=sessionmaker(bind=create_engine(config.get_postgres_url()))
app=Flask(__name__)


@app.route("/allocate", methods=["POST"])
def allocate_endpoint():
    session=get_session()
    batches=repository.SQLAlchemyRepository(session).list()
    line=model.Orderline(
        request.json['orderid'],request.json['sku'],request.json['qty']
    )

    try :
        batchref=model.allocate(line,batches)
    except (model.OutOfStock,services.InvalidSku) as e:
        return {"message":str(e)},400

    return {"batchref":batchref},201


@app.route("/health", methods=["GET"])
def health():
    return {"status": "ok"}, 200