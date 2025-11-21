from app.models import UserCreate, TaskCreate


def test_user_create_model():
    payload = UserCreate(name='Alice', email='alice@example.com')
    assert payload.name == 'Alice'


def test_task_create_model():
    payload = TaskCreate(title='Task 1', description='a')
    assert payload.title == 'Task 1'
