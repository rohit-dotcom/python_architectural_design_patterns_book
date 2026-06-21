from flask import Flask, request
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import config
import adapters.orm as orm
import domain.model as model
import adapters.repository as repository
import services.services as services
from datetime import datetime



orm.start_mapper()
get_session=sessionmaker(bind=create_engine(config.get_postgres_url()))
app=Flask(__name__)

@app.route("/add_batch",methods=["POST"])
def add_batch():
    session=get_session()
    repo=repository.SQLAlchemyRepository(session)
    eta=request.json['eta']
    if eta is not None:
        eta=datetime.fromisoformat(eta).date()
    services.add_batch(
        request.json['batch_ref'],
        request.json['sku'],
        request.json['qty'],
        eta,
        repo,
        session
    )

    return "OK",201

@app.route("/allocate", methods=["POST"])
def allocate_endpoint():
    session=get_session()

    repo=repository.SQLAlchemyRepository(session)

    try :
        batchref=services.allocate(request.json['orderid'],
                                   request.json['sku'],
                                   request.json['qty'],
                                   repo,
                                   session)
    except (model.OutOfStock,services.InvalidSku) as e:
        return {"message":str(e)},400

    return {"batchref":batchref},201




@app.route("/health", methods=["GET"])
def health():
    return {"status": "ok"}, 200