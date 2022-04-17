"""empty message

Revision ID: 1f151d39a98d
Revises: 
Create Date: 2022-04-17 20:04:38.278869

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1f151d39a98d'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('actors',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('age', sa.Integer(), nullable=False),
    sa.Column('gender', sa.String(length=1), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('movies',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('year', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('casts',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('movie_id', sa.Integer(), nullable=False),
    sa.Column('actor_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['actor_id'], ['actors.id'], ),
    sa.ForeignKeyConstraint(['movie_id'], ['movies.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('movie_id', 'actor_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('casts')
    op.drop_table('movies')
    op.drop_table('actors')
    # ### end Alembic commands ###