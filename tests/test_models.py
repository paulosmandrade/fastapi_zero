from sqlalchemy import select

from fast_zero.models import User


def test_create_user(session):
    user = User(
        username='paulo',
        email='paulo.andrade@email.com',
        password='123Mudar',
    )
    session.add(user)
    session.commit()

    result = session.scalar(select(User).where(User.username == 'paulo'))

    assert result.email == 'paulo.andrade@email.com'
