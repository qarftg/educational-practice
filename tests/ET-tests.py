from PySide6 import QtCore
from main import ExpenseTracker
import pytest

@pytest.fixture
def app(qtbot):
    test_app = ExpenseTracker()
    qtbot.addWidget(test_app)
    return test_app

class TestExpenseTracker:
    def test_initial_state(self, app):
        # Проверяем начальное состояние интерфейса
        assert app.ui.current_balance.text() == "0$"
        assert app.ui.income_balance.text() == "0$"
        assert app.ui.outcome_balance.text() == "0$"
        assert app.model is not None
        assert app.ui.tableView.model() == app.model

    def test_reload_data(self, app, qtbot):
        # Тестируем обновление данных
        app.conn.execute_query_with_params("DELETE FROM expenses")
        app.conn.add_new_transaction_query("2023-01-01", "Grocery", "Test", "100", "Outcome")
        
        with qtbot.waitSignal(app.model.dataChanged, timeout=1000):
            app.reload_data()
        
        assert app.ui.outcome_balance.text() == "100.0$"
        assert app.ui.total_groceries.text() == "100.0$"

    def test_add_transaction(self, app, qtbot):
        initial_count = app.model.rowCount()
        
        # Открываем диалог добавления
        with qtbot.waitSignal(app.ui.btn_new_transaction.clicked, timeout=1000):
            qtbot.mouseClick(app.ui.btn_new_transaction, QtCore.Qt.LeftButton)
        
        # Заполняем форму
        app.ui_window.dateEdit.setDate(QtCore.QDate(2023, 1, 1))
        app.ui_window.cb_choose_category.setCurrentText("Grocery")
        app.ui_window.le_description.setText("Test")
        app.ui_window.le_balance.setText("100")
        app.ui_window.cb_status.setCurrentText("Outcome")
        
        # Нажимаем кнопку сохранения
        with qtbot.waitSignal(app.ui_window.btn_new_transaction.clicked, timeout=1000):
            qtbot.mouseClick(app.ui_window.btn_new_transaction, QtCore.Qt.LeftButton)
        
        # Проверяем, что запись добавилась
        assert app.model.rowCount() == initial_count + 1

    def test_delete_transaction(self, app, qtbot):
        # Сначала добавляем тестовую запись
        app.conn.add_new_transaction_query("2023-01-01", "Grocery", "Test", "100", "Outcome")
        app.view_data()  # Обновляем модель
        
        initial_count = app.model.rowCount()
        
        # Выбираем первую строку
        app.ui.tableView.selectRow(0)
        
        # Удаляем запись
        with qtbot.waitSignal(app.ui.btn_delete_transaction.clicked, timeout=1000):
            qtbot.mouseClick(app.ui.btn_delete_transaction, QtCore.Qt.LeftButton)
        
        # Проверяем, что запись удалилась
        assert app.model.rowCount() == initial_count - 1