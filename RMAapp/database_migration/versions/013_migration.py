from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
amentities = Table('amentities', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('apartment_id', Integer),
    Column('name', String(length=30)),
)

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
)

rooms = Table('rooms', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('apartment_id', Integer),
    Column('name', String(length=30)),
)

apartment = Table('apartment', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('zpid', Integer, nullable=False),
    Column('rentPerMonth', Float),
    Column('image_count', Integer),
    Column('comps', Boolean, default=ColumnDefault(False)),
    Column('descripion', String(length=2500)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['amentities'].create()
    post_meta.tables['details'].create()
    post_meta.tables['rooms'].create()
    post_meta.tables['apartment'].columns['descripion'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['amentities'].drop()
    post_meta.tables['details'].drop()
    post_meta.tables['rooms'].drop()
    post_meta.tables['apartment'].columns['descripion'].drop()
