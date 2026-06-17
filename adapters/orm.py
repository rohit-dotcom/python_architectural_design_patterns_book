from sqlalchemy.orm import registry,relationship
from sqlalchemy import String,Column,MetaData,Integer,Table,Date,ForeignKey
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

batches=Table("batches",
            metadata,
            Column("id",Integer,autoincrement=True,primary_key=True),
            Column("batch_ref",String(255)),
            Column("sku",String(255)),
            Column("_purchased_quantity",Integer,nullable=False),
            Column("eta",Date,nullable=True),

            )

allocations=Table(
              "allocations",
              metadata,
              Column("id",Integer,primary_key=True,autoincrement=True),
              Column("orderline_id",ForeignKey("order_lines.id")),
              Column("batch_id",ForeignKey("batches.id"))
)


def start_mapper():
    lines_mapper=mapper_registry.map_imperatively(model.Orderline,order_lines)
    mapper_registry.map_imperatively(model.Batch,batches,
                                     properties={
                                         "_allocations":relationship(
                                             lines_mapper,secondary=allocations,collection_class=set
                                         )
                                     }
                                     )