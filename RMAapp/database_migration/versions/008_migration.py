from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
address = Table('address', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('street', String(length=250)),
    Column('zipcode', Integer, nullable=False),
    Column('city', String(length=50)),
    Column('state', String(length=20)),
    Column('latitude', Float),
    Column('longitude', Float),
    Column('apartment_id', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['address'].columns['latitude'].create()
    post_meta.tables['address'].columns['longitude'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['address'].columns['latitude'].drop()
    post_meta.tables['address'].columns['longitude'].drop()
