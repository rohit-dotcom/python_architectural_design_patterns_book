from flask import Flask, request
from sqlalchemy import create_engine
from sqlalchemy import sessionmaker

import config
import orm
import model
import repository

orm.start_mapper()
get_sesison=sessionmaker(bind=create_engine('config.get_postgressql_url()'))
app=Flask(__NAME__)/``

@app.route("/allocate", method=["POST"])
def allocate_endpoint():
    session=get_sesison()
    batches=repository.SQLAlchemyRepository.list()
    line=model.Orderline(
        request.json['orderid'],request.json['sku'],request.json['qty']
    )
    batchref=model.Batch.allocate(line,batches)
    return {"batchref":batchref},201
