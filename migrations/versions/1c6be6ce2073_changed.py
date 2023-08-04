"""changed

Revision ID: 1c6be6ce2073
Revises: bba88c8743af
Create Date: 2023-08-04 15:13:26.449902

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1c6be6ce2073'
down_revision = 'bba88c8743af'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_superusers_id', table_name='superusers')
    op.drop_table('superusers')
    op.drop_index('ix_musics_id', table_name='musics')
    op.drop_index('ix_musics_title', table_name='musics')
    op.drop_table('musics')
    op.drop_index('ix_favorites_id', table_name='favorites')
    op.drop_table('favorites')
    op.drop_index('ix_users_id', table_name='users')
    op.drop_index('ix_users_username', table_name='users')
    op.drop_table('users')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.INTEGER(), server_default=sa.text("nextval('users_id_seq'::regclass)"), autoincrement=True, nullable=False),
    sa.Column('username', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('password', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('name', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('lastname', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='users_pkey'),
    postgresql_ignore_search_path=False
    )
    op.create_index('ix_users_username', 'users', ['username'], unique=False)
    op.create_index('ix_users_id', 'users', ['id'], unique=False)
    op.create_table('favorites',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('music_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['music_id'], ['musics.id'], name='favorites_music_id_fkey'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name='favorites_user_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='favorites_pkey')
    )
    op.create_index('ix_favorites_id', 'favorites', ['id'], unique=False)
    op.create_table('musics',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('title', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('artist', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('genre', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('photo', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('music', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name='musics_user_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='musics_pkey')
    )
    op.create_index('ix_musics_title', 'musics', ['title'], unique=False)
    op.create_index('ix_musics_id', 'musics', ['id'], unique=False)
    op.create_table('superusers',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name='superusers_user_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='superusers_pkey'),
    sa.UniqueConstraint('user_id', name='superusers_user_id_key')
    )
    op.create_index('ix_superusers_id', 'superusers', ['id'], unique=False)
    # ### end Alembic commands ###