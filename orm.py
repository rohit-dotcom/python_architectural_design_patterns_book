from sqlalchemy.orm import registry
from sqlalchemy import String,Column,MetaData,Integer,Table
import model


mapper_registry = registry()
metadata = mapper_registry.metadata


order_lines=Table("order_lines",
                  metadata,
                  Column("id",Integer,autoincrement=True,primary_key=True),
                  Column("sku",String(255)),
                  Column("qty",Integer,nullable=False),
                  Column("orderid",String(255))
                    )

def start_mapper():
    lines_mapper=mapper_registry.map_imperatively(model.Orderline,order_lines)