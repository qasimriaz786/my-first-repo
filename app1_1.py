from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout,
    QPushButton, QTextEdit, QLineEdit, QLabel, QComboBox
)
from PyQt5.QtCore import Qt

# -------------------------
# ORIGINAL FUNCTION (UNCHANGED)
# -------------------------
def statement(invoice, plays):
    total_amount = 0
    volume_credits = 0
    result = f"Statement for {invoice['customer']}\n"

    f0

        # Calculate amount
        if play['type'] == "tragedy":
            this_amount = 40000
            if perf['audience'] > 30:
                this_amount += 1000 * (perf['audience'] - 30)

        elif play['type'] == "comedy":
            this_amount = 30000
            if perf['audience'] > 20:
                this_amount += 10000 + 500 * (perf['audience'] - 20)
            this_amount += 300 * perf['audience']

        else:
            raise ValueError(f"Unknown type: {play['type']}")

        # Add volume credits
        volume_credits += max(perf['audience'] - 30, 0)

        if play['type'] == "comedy":
            volume_credits += perf['audience'] // 5

        # Append result
        result += f"  {play['name']}: {this_amount/100:.2f} ({perf['audience']} seats)\n"
        total_amount += this_amount

    result += f"Amount owed is {total_amount/100:.2f}\n"
    result += f"You earned {volume_credits} credits\n"

    return result


# -------------------------
# PLAY DATA
# -------------------------
plays = {
    "hamlet": {"name": "Hamlet", "type": "tragedy"},
    "as-like": {"name": "As You Like It", "type": "comedy"},
    "othello": {"name": "Othello", "type": "tragedy"}
}


# -------------------------
# GUI
# -------------------------
class MyWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Invoice Generator with Step-by-Step Logic")

        # 🌈 Styling for beautiful UI
        self.setStyleSheet("""
            QWidget {
                background-color: #e6f7ff;
                font-family: Arial;
                font-size: 12pt;
            }
            QLabel {
                color: #003366;
                font-weight: bold;
            }
            QLineEdit, QComboBox, QTextEdit {
                background-color: #ffffff;
                border: 2px solid #3399ff;
                border-radius: 6px;
                padding: 4px;
            }
            QPushButton {
                background-color: #4CAF50;
                color: white;
                font-weight: bold;
                border-radius: 8px;
                padding: 6px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #2e7031;
            }
        """)

        self.performances = []
        layout = QVBoxLayout()

        # 🔥 Banner Heading
        banner = QLabel("✨ INVOICE SYSTEM BY M.BILAL ✨")
        banner.setAlignment(Qt.AlignCenter)
        banner.setStyleSheet("""
            QLabel {
                background-color: #003366;
                color: #ffffff;
                font-size: 16pt;
                font-weight: bold;
                padding: 10px;
                border-radius: 8px;
            }
        """)
        layout.addWidget(banner)

        # Customer name
        layout.addWidget(QLabel("Customer Name:"))
        self.customer_input = QLineEdit()
        self.customer_input.setText("BigCo")
        layout.addWidget(self.customer_input)

        # Play selection
        layout.addWidget(QLabel("Select Play:"))
        self.play_select = QComboBox()
        self.play_select.addItems(plays.keys())
        layout.addWidget(self.play_select)

        # Audience input
        layout.addWidget(QLabel("Audience Count:"))
        self.audience_input = QLineEdit()
        layout.addWidget(self.audience_input)

        # Add performance button
        add_btn = QPushButton("➕ Add Performance")
        add_btn.clicked.connect(self.add_performance)
        layout.addWidget(add_btn)

        # Step-by-step calculation area
        layout.addWidget(QLabel("📊 Step-by-Step Calculation:"))
        self.calc_area = QTextEdit()
        layout.addWidget(self.calc_area)

        # Final invoice area
        layout.addWidget(QLabel("🧾 Final Invoice:"))
        self.invoice_area = QTextEdit()
        layout.addWidget(self.invoice_area)

        # Generate invoice button
        gen_btn = QPushButton("✅ Generate Invoice")
        gen_btn.clicked.connect(self.generate_invoice)
        layout.addWidget(gen_btn)

        self.setLayout(layout)

    def add_performance(self):
        play_id = self.play_select.currentText()
        audience_text = self.audience_input.text()

        if not audience_text.isdigit():
            self.calc_area.setText("Audience must be a number")
            return

        audience = int(audience_text)
        play = plays[play_id]

        # Step-by-step calculation
        calc_text = f"Play: {play['name']} ({play['type']})\n"
        calc_text += f"Audience: {audience}\n"

        if play["type"] == "tragedy":
            base = 40000
            calc_text += f"Base price: 400.00\n"
            if audience > 30:
                extra = (audience - 30) * 1000
                calc_text += f"Extra (1000 × {audience - 30}): {extra/100:.2f}\n"
            else:
                extra = 0
            total = base + extra

        elif play["type"] == "comedy":
            base = 30000
            calc_text += f"Base price: 300.00\n"
            if audience > 20:
                extra = 10000 + 500 * (audience - 20)
                calc_text += f"Extra (10000 + 500 × {audience - 20}): {extra/100:.2f}\n"
            else:
                extra = 0
            per_seat = 300 * audience
            calc_text += f"Per-seat (300 × {audience}): {per_seat/100:.2f}\n"
            total = base + extra + per_seat

        calc_text += f"Total for this play: {total/100:.2f}\n\n"

        # Credits
        credits = max(audience - 30, 0)
        calc_text += f"Credits from audience: {credits}\n"
        if play["type"] == "comedy":
            comedy_bonus = audience // 5
            calc_text += f"Comedy bonus: {comedy_bonus}\n"
            credits += comedy_bonus

        calc_text += f"Total credits for this play: {credits}\n\n"

        self.calc_area.append(calc_text)

        # Add to performance list
        self.performances.append({"playID": play_id, "audience": audience})

        self.audience_input.clear()

    def generate_invoice(self):
        customer = self.customer_input.text().strip()

        invoice = {
            "customer": customer,
            "performances": self.performances
        }

        result = statement(invoice, plays)
        self.invoice_area.setText(result)

        # ✅ Reset after generating invoice
        self.performances = []
        self.calc_area.clear()


# -------------------------
# RUN APP
# -------------------------
app = QApplication([])
window = MyWindow()
window.show()
app.exec_()
