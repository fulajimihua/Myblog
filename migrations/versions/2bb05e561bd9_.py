"""empty message

Revision ID: 2bb05e561bd9
Revises: 
Create Date: 2019-06-30 17:57:22.179390

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2bb05e561bd9'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('artical', sa.Column('art_descrip', sa.Text(), nullable=True))
    op.add_column('artical', sa.Column('artical_keywords', sa.String(length=100), nullable=True))
    op.add_column('artical', sa.Column('artical_tag', sa.String(length=100), nullable=True))
    op.add_column('classfy', sa.Column('class_description', sa.String(length=1000), nullable=True))
    op.add_column('classfy', sa.Column('class_keywords', sa.String(length=100), nullable=True))
    op.add_column('classfy', sa.Column('class_name2', sa.String(length=100), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('classfy', 'class_name2')
    op.drop_column('classfy', 'class_keywords')
    op.drop_column('classfy', 'class_description')
    op.drop_column('artical', 'artical_tag')
    op.drop_column('artical', 'artical_keywords')
    op.drop_column('artical', 'art_descrip')
    # ### end Alembic commands ###
