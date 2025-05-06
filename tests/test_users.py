import uuid

def test_create_user(test_client, init_db):
    unique_id = uuid.uuid4().hex[:6]
    test_data = {
        'username': f'test_{unique_id}',
        'email': f'test_{unique_id}@example.com'
    }

    response = test_client.post('/users', json=test_data)
    assert response.status_code == 201
    assert 'id' in response.json