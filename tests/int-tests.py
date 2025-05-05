class TestIntegration:
    def test_full_flow(self, qtbot):
        # Создаем приложение
        window = ExpenseTracker()
        qtbot.addWidget(window)
        
        # Проверяем начальное состояние
        assert window.model.rowCount() >= 0
        
        # Добавляем новую транзакцию
        initial_count = window.model.rowCount()
        
        # Открываем диалог
        with qtbot.waitSignal(window.ui.btn_new_transaction.clicked, timeout=1000):
            qtbot.mouseClick(window.ui.btn_new_transaction, QtCore.Qt.LeftButton)
        
        # Заполняем форму
        window.ui_window.dateEdit.setDate(QtCore.QDate(2023, 1, 1))
        window.ui_window.cb_choose_category.setCurrentText("Grocery")
        window.ui_window.le_description.setText("Integration Test")
        window.ui_window.le_balance.setText("150")
        window.ui_window.cb_status.setCurrentText("Outcome")
        
        # Сохраняем
        with qtbot.waitSignal(window.ui_window.btn_new_transaction.clicked, timeout=1000):
            qtbot.mouseClick(window.ui_window.btn_new_transaction, QtCore.Qt.LeftButton)
        
        # Проверяем добавление
        assert window.model.rowCount() == initial_count + 1
        
        # Проверяем обновление баланса
        assert window.ui.outcome_balance.text() != "0$"
        assert window.ui.total_groceries.text() != "0$"
        
        # Редактируем транзакцию
        window.ui.tableView.selectRow(0)
        
        # Открываем диалог редактирования
        with qtbot.waitSignal(window.ui.btn_edit_transaction.clicked, timeout=1000):
            qtbot.mouseClick(window.ui.btn_edit_transaction, QtCore.Qt.LeftButton)
        
        # Меняем сумму
        window.ui_window.le_balance.setText("200")
        
        # Сохраняем изменения
        with qtbot.waitSignal(window.ui_window.btn_new_transaction.clicked, timeout=1000):
            qtbot.mouseClick(window.ui_window.btn_new_transaction, QtCore.Qt.LeftButton)
        
        # Проверяем обновление
        assert window.ui.total_groceries.text() == "200.0$"
        
        # Удаляем транзакцию
        window.ui.tableView.selectRow(0)
        
        with qtbot.waitSignal(window.ui.btn_delete_transaction.clicked, timeout=1000):
            qtbot.mouseClick(window.ui.btn_delete_transaction, QtCore.Qt.LeftButton)
        
        # Проверяем удаление
        assert window.model.rowCount() == initial_count