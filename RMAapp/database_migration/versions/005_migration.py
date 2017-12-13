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
    Column('apartment_id', Integer),
)

apartment = Table('apartment', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('zpid', Integer, nullable=False),
    Column('rentPerMonth', Float),
)

image = Table('image', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('url', Text, nullable=False),
    Column('apartment_id', Integer),
)

review = Table('review', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('user_name', String(length=50), nullable=False),
    Column('content', Text, nullable=False),
    Column('apartment_id', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['address'].create()
    post_meta.tables['apartment'].create()
    post_meta.tables['image'].create()
    post_meta.tables['review'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['address'].drop()
    post_meta.tables['apartment'].drop()
    post_meta.tables['image'].drop()
    post_meta.tables['review'].drop()
