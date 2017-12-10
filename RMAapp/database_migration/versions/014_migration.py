from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
details = Table('details', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('apartment_id', Integer),
    Column('bedrooms', Integer),
    Column('bathrooms', Float),
    Column('area', Integer),
    Column('lot_area', Integer),
    Column('year_built', Integer),
    Column('year_update', Integer),
    Column('num_floor', Integer),
    Column('basement', String(length=20)),
    Column('view', String(length=100)),
    Column('parking_type', String(length=20)),
    Column('heating_source', String(length=20)),
    Column('heating_system', String(length=20)),
    Column('cooling_system', String(length=20)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['details'].columns['cooling_system'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['details'].columns['cooling_system'].drop()
