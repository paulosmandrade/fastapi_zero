from sqlalchemy import select

from fast_zero.models import User


def test_create_user(session):
    new_user = User(
        username='Paulo', password='secret', email='paulo@test.com.br'
    )
    session.add(new_user)
    session.commit()

    user = session.scalar(select(User).where(User.username == 'Paulo'))

    assert user.username == 'Paulo'
