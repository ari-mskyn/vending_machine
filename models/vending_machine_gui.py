import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QLineEdit
)

from vending_machine import VendingMachine

class VendingMachineWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.vm = VendingMachine()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Vending Machine")

        main_layout = QVBoxLayout()

        # Balance label
        self.balance_label = QLabel(f"Balance: €{self.vm.balance:.2f}")
        main_layout.addWidget(self.balance_label)

        # Status label
        self.status_label = QLabel("Insert money or choose an item.")
        main_layout.addWidget(self.status_label)

        # Money input and button
        money_layout = QHBoxLayout()
        self.money_input = QLineEdit()
        self.money_input.setPlaceholderText("Amount (e.g. 2 or 1.50)")
        money_button = QPushButton("Insert Money")
        money_button.clicked.connect(self.handle_insert_money)

        money_layout.addWidget(self.money_input)
        money_layout.addWidget(money_button)
        main_layout.addLayout(money_layout)

        # Item buttons
        items_layout = QHBoxLayout()
        for name in self.vm.items:
            btn = QPushButton(f"{name} (€{self.vm.items[name]:.2f})")
            btn.clicked.connect(lambda checked, n=name: self.handle_purchase(n))
            items_layout.addWidget(btn)
        main_layout.addLayout(items_layout)

        # Refund button
        refund_button = QPushButton("Refund")
        refund_button.clicked.connect(self.handle_refund)
        main_layout.addWidget(refund_button)

        self.setLayout(main_layout)

    def update_balance_label(self):
        self.balance_label.setText(f"Balance: €{self.vm.balance:.2f}")

    def handle_insert_money(self):
        text = self.money_input.text().strip()
        try:
            amount = float(text)
        except ValueError:
            self.status_label.setText("Please enter a valid number.")
            return
        message = self.vm.insertmoney(amount)
        self.status_label.setText(message)
        self.update_balance_label()
        self.money_input.clear()

    def handle_purchase(self, item_name):
        message = self.vm.purchase(item_name)
        self.status_label.setText(message)
        self.update_balance_label()

    def handle_refund(self):
        message = self.vm.refund()
        self.status_label.setText(message)
        self.update_balance_label()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = VendingMachineWindow()
    window.show()
    sys.exit(app.exec())