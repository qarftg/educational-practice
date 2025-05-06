def test_home_page(test_client):
    response = test_client.get('/nonexistent')
    assert response.status_code == 404