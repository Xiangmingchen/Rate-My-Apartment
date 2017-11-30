from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
address = Table('address', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('street', VARCHAR(length=250)),
    Column('zipcode', INTEGER, nullable=False),
    Column('city', VARCHAR(length=50)),
    Column('state', VARCHAR(length=20)),
    Column('apartment_id', INTEGER),
)

apartment = Table('apartment', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('zpid', INTEGER, nullable=False),
    Column('rentPerMonth', FLOAT),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['address'].drop()
    pre_meta.tables['apartment'].drop()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['address'].create()
    pre_meta.tables['apartment'].create()
