"""Initial migration

Revision ID: 603e56974bf4
Revises: 
Create Date: 2024-10-01 23:59:26.326899

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '603e56974bf4'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('authors',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('image', sa.String(length=50), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('categories',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('lastname', sa.String(length=50), nullable=True),
    sa.Column('firstname', sa.String(length=50), nullable=True),
    sa.Column('image', sa.String(length=50), nullable=True),
    sa.Column('email', sa.String(length=50), nullable=True),
    sa.Column('phone', sa.String(length=50), nullable=True),
    sa.Column('password', sa.String(length=50), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('books',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=255), nullable=True),
    sa.Column('author_id', sa.Integer(), nullable=False),
    sa.Column('publication_date', sa.Date(), nullable=True),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('available', sa.Boolean(), nullable=True),
    sa.Column('image', sa.String(length=250), nullable=True),
    sa.Column('edition', sa.String(length=250), nullable=True),
    sa.Column('isbn', sa.String(length=50), nullable=True),
    sa.Column('publisher', sa.String(length=250), nullable=True),
    sa.ForeignKeyConstraint(['author_id'], ['authors.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('books_categories',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('category_id', sa.Integer(), nullable=True),
    sa.Column('book_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['book_id'], ['books.id'], ),
    sa.ForeignKeyConstraint(['category_id'], ['categories.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('rents',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('book_id', sa.Integer(), nullable=True),
    sa.Column('start_date', sa.Date(), nullable=True),
    sa.Column('return_date', sa.Date(), nullable=True),
    sa.ForeignKeyConstraint(['book_id'], ['books.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('rents')
    op.drop_table('books_categories')
    op.drop_table('books')
    op.drop_table('users')
    op.drop_table('categories')
    op.drop_table('authors')
    # ### end Alembic commands ###
