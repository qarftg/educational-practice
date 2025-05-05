import pytest
from connection import Data
from config import host, user, password, db_name

class TestData:
    @pytest.fixture
    def db_connection(self):
        return Data()

    def test_create_connection(self, db_connection):
        assert db_connection.create_connection() is True

    def test_add_new_transaction(self, db_connection):
        initial_count = db_connection.execute_query_with_params("SELECT COUNT(*) FROM expenses").value(0)
        db_connection.add_new_transaction_query("2023-01-01", "Grocery", "Test", "100", "Outcome")
        new_count = db_connection.execute_query_with_params("SELECT COUNT(*) FROM expenses").value(0)
        assert new_count == initial_count + 1

    def test_update_transaction(self, db_connection):
        # Сначала добавляем тестовую запись
        db_connection.add_new_transaction_query("2023-01-01", "Grocery", "Test", "100", "Outcome")
        last_id = db_connection.execute_query_with_params("SELECT MAX(ID) FROM expenses").value(0)
        
        # Обновляем запись
        db_connection.update_transaction_query("2023-01-02", "Auto", "Updated", "150", "Outcome", last_id)
        
        # Проверяем обновление
        query = db_connection.execute_query_with_params(f"SELECT Description FROM expenses WHERE ID = {last_id}")
        assert query.value(0) == "Updated"

    def test_delete_transaction(self, db_connection):
        # Сначала добавляем тестовую запись
        db_connection.add_new_transaction_query("2023-01-01", "Grocery", "Test", "100", "Outcome")
        last_id = db_connection.execute_query_with_params("SELECT MAX(ID) FROM expenses").value(0)
        
        # Удаляем запись
        db_connection.delete_transaction_query(last_id)
        
        # Проверяем удаление
        query = db_connection.execute_query_with_params(f"SELECT COUNT(*) FROM expenses WHERE ID = {last_id}")
        assert query.value(0) == 0

    def test_total_calculations(self, db_connection):
        # Очищаем тестовые данные
        db_connection.execute_query_with_params("DELETE FROM expenses")
        
        # Добавляем тестовые данные
        db_connection.add_new_transaction_query("2023-01-01", "Grocery", "Test1", "100", "Outcome")
        db_connection.add_new_transaction_query("2023-01-02", "Grocery", "Test2", "200", "Outcome")
        db_connection.add_new_transaction_query("2023-01-03", "Auto", "Test3", "300", "Outcome")
        db_connection.add_new_transaction_query("2023-01-04", "Work", "Test4", "500", "Income")
        
        # Проверяем расчеты
        assert db_connection.total_balance() == "100.0$"  # 500 - (100+200+300)
        assert db_connection.total_income() == "500.0$"
        assert db_connection.total_outcome() == "600.0$"
        assert db_connection.total_groceries() == "300.0$"
        assert db_connection.total_auto() == "300.0$"