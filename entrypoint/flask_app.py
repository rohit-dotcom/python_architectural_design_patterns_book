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
    line=model.Orderline(
        request.json['orderid'],request.json['sku'],request.json['qty']
    )
    repo=repository.SQLAlchemyRepository(session)

    try :
        batchref=services.allocate(line,repo,session)
    except (model.OutOfStock,services.InvalidSku) as e:
        return {"message":str(e)},400

    return {"batchref":batchref},201


@app.route("/health", methods=["GET"])
def health():
    return {"status": "ok"}, 200