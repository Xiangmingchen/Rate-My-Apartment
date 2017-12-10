from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
review = Table('review', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('user_name', String(length=50), nullable=False),
    Column('content', Text, nullable=False),
    Column('rating', Float),
    Column('timestamp', String),
    Column('apartment_id', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['review'].columns['rating'].create()
    post_meta.tables['review'].columns['timestamp'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['review'].columns['rating'].drop()
    post_meta.tables['review'].columns['timestamp'].drop()
