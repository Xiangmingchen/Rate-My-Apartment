from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
review = Table('review', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('user_name', VARCHAR(length=50), nullable=False),
    Column('content', TEXT, nullable=False),
    Column('apartment_id', INTEGER),
    Column('rating', FLOAT),
    Column('timestamp', VARCHAR),
)

review = Table('review', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('user_name', String(length=50), nullable=False),
    Column('content', Text, nullable=False),
    Column('rating', Float, default=ColumnDefault(0)),
    Column('time_stamp', DateTime),
    Column('apartment_id', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['review'].columns['timestamp'].drop()
    post_meta.tables['review'].columns['time_stamp'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['review'].columns['timestamp'].create()
    post_meta.tables['review'].columns['time_stamp'].drop()
