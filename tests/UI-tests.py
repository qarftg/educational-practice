class TestUI:
    def test_labels(self, app):
        # Проверяем, что все основные элементы интерфейса существуют
        assert app.ui.lbl_current_balance is not None
        assert app.ui.current_balance is not None
        assert app.ui.lbl_income is not None
        assert app.ui.income_balance is not None
        assert app.ui.lbl_outcome is not None
        assert app.ui.outcome_balance is not None
        assert app.ui.lbl_expenses_categories is not None
        assert app.ui.tableView is not None
        
        # Проверяем текст меток
        assert app.ui.lbl_current_balance.text() == "Current Balance"
        assert app.ui.lbl_income.text() == "Income"
        assert app.ui.lbl_outcome.text() == "Outcome"
        assert app.ui.lbl_expenses_categories.text() == "Expenses categories"
        
        # Проверяем кнопки
        assert app.ui.btn_new_transaction.text() == "New transaction"
        assert app.ui.btn_edit_transaction.text() == "Edit transaction"
        assert app.ui.btn_delete_transaction.text() == "Delete transaction"

    def test_table_view(self, app):
        # Проверяем настройки таблицы
        assert app.ui.tableView.verticalScrollBarPolicy() == QtCore.Qt.ScrollBarAlwaysOff
        assert app.ui.tableView.horizontalScrollBarPolicy() == QtCore.Qt.ScrollBarAlwaysOff
        assert not app.ui.tableView.showGrid()
        assert app.ui.tableView.isSortingEnabled()