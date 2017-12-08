from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
apartment = Table('apartment', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('zpid', Integer, nullable=False),
    Column('rentPerMonth', Float),
    Column('image_count', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['apartment'].columns['image_count'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['apartment'].columns['image_count'].drop()
