import sys
import os
from PyQt6.QtWidgets import (QApplication, QMainWindow, QGridLayout, 
                            QWidget, QLabel, QPushButton, QVBoxLayout, 
                            QHBoxLayout, QDialog, QSpinBox, QLineEdit,
                            QComboBox, QMessageBox, QMenu)
from PyQt6.QtGui import QPixmap, QFont
from PyQt6.QtCore import Qt
##from supabase import create_client, Client
##rom dotenv import load_dotenv

from mockdb import MockSupabaseClient 

class Product:
    def __init__(self, id, name, price, quantity, image_url):
        self.id = id
        self.name = name
        self.price = price
        self.quantity = quantity
        self.image_url = image_url


class AdminDialog(QDialog):
    def __init__(self, products, parent=None):
        super().__init__(parent)
        self.products = products  # Referenz auf Hauptliste
        self.setWindowTitle("Admin-Modus - Automat auffüllen")
        self.setFixedSize(400, 300)
        layout = QVBoxLayout()
        
        # Produkt-Auswahl
        self.product_combo = QComboBox()
        product_names = [f"{p.name} (ID: {p.id}) - Vorrat: {p.quantity}" for p in products]
        self.product_combo.addItems(product_names)
        layout.addWidget(self.product_combo)
        
        # Menge
        layout.addWidget(QLabel("Neue Menge:"))
        self.quantity_spin = QSpinBox()
        self.quantity_spin.setRange(0, 100)
        layout.addWidget(self.quantity_spin)
        
        # Preis
        layout.addWidget(QLabel("Neuer Preis (€):"))
        self.price_edit = QLineEdit()
        self.price_edit.setPlaceholderText("z.B. 1.50")
        layout.addWidget(self.price_edit)
        
        # Buttons
        save_btn = QPushButton("Speichern")
        save_btn.clicked.connect(self.save_product)
        cancel_btn = QPushButton("Schließen")
        cancel_btn.clicked.connect(self.reject)
        
        btn_layout = QHBoxLayout()
        btn_layout.addWidget(save_btn)
        btn_layout.addWidget(cancel_btn)
        layout.addLayout(btn_layout)
        
        self.setLayout(layout)
    
    def save_product(self):
        index = self.product_combo.currentIndex()
        if index < 0:
            return
            
        # LOKAL speichern - direkt die Product-Objekte ändern
        product = self.products[index]
        product.quantity = self.quantity_spin.value()
        
        # Preis nur ändern wenn etwas eingegeben wurde
        if self.price_edit.text().strip():
            try:
                product.price = float(self.price_edit.text())
            except ValueError:
                QMessageBox.warning(self, "Fehler", "Ungültiger Preis!")
                return
        
        QMessageBox.information(self, "Erfolg", f"{product.name} aktualisiert!")
        self.accept()

class CoinDialog(QDialog):
    def __init__(self, current_balance, needed_amount, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Münzen einwerfen")
        self.setFixedSize(300, 200)
        self.balance = current_balance
        
        layout = QVBoxLayout()
        layout.addWidget(QLabel(f"Aktueller Stand: {current_balance:.2f}€"))
        layout.addWidget(QLabel(f"Benötigt: {needed_amount:.2f}€"))
        
        self.coins = [
            ("2€", 2.0), ("1€", 1.0), ("0.50€", 0.5), 
            ("0.20€", 0.2), ("0.10€", 0.1), ("0.05€", 0.05), ("0.02€", 0.02), ("0.01€", 0.01)
        ]
        
        self.coin_counts = {}
        for coin_name, value in self.coins:
            layout.addWidget(QLabel(f"{coin_name}:"))
            spin = QSpinBox()
            spin.setMaximum(50)
            spin.valueChanged.connect(lambda v, n=coin_name: self.update_balance(n, v))
            layout.addWidget(spin)
            self.coin_counts[coin_name] = spin
        
        insert_btn = QPushButton("Einwerfen")
        insert_btn.clicked.connect(self.accept)
        layout.addWidget(insert_btn)
        
        self.setLayout(layout)
    
    def get_inserted_amount(self):
        total = 0
        for coin_name, spin in self.coin_counts.items():
            value = next(v for n, v in self.coins if n == coin_name)
            total += spin.value() * value
        return total
    
class SnackAutomat(QMainWindow):
    def __init__(self):
        super().__init__()
        # statt echtem Supabase-Client:
        self.supabase = MockSupabaseClient()
        self.products = []
        self.balance = 0.0
        ##self.init_ui()
        self.load_products()

    def load_products(self):
        """Lädt Produkte aus der Mock-DB (später Supabase)"""
        try:
            response = self.supabase.table('snacks').select("*").eq('active', True).execute()
            self.products = []
            for data in response.data:
                product = Product(data['id'], data['name'], data['price'],
                                  data['quantity'], data.get('image_url', ''))
                self.products.append(product)

            self.update_display()
        except Exception as e:
            print(f"Fehler beim Laden: {e}")
            ##self.show_sample_products()

    def buy_product(self, product):
        price = product.price
        if self.balance < price:
            needed = price - self.balance
            self.open_coin_dialog(needed)
            return

        self.balance -= price
        new_qty = product.quantity - 1
        product.quantity = new_qty

        # Update in Mock-DB
        self.supabase.table('snacks').update({'quantity': new_qty}).eq('id', product.id).execute()

        self.dispense_label.setText(f"🎉 {product.name} fällt heraus!")
        self.update_display()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = SnackAutomat()
    window.show()
    sys.exit(app.exec())