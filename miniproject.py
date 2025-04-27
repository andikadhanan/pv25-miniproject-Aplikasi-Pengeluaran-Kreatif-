import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QComboBox, QSpinBox, QPushButton, QListWidget, QListWidgetItem,
    QMessageBox, QDateEdit, QGroupBox
)
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtGui import QFont, QColor, QPalette, QBrush, QLinearGradient

class AplikasiPengeluaranKreatif(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("\ud83d\udcb0 Pencatat Pengeluaran Kreatif")
        self.setGeometry(200, 200, 500, 650)
        self.total_pengeluaran = 0

        self.initUI()
        self.setGradientBackground()

    def initUI(self):
        widget = QWidget()
        self.setCentralWidget(widget)

        layout = QVBoxLayout()

        identitas_box = QGroupBox("\ud83d\udc64 Identitas")
        identitas_layout = QVBoxLayout()
        nama_label = QLabel("Nama: Andika Dhanan Jaya")
        nama_label.setFont(QFont("Segoe UI", 11))
        nim_label = QLabel("NIM: F1D022111")
        nim_label.setFont(QFont("Segoe UI", 11))
        identitas_layout.addWidget(nama_label)
        identitas_layout.addWidget(nim_label)
        identitas_box.setLayout(identitas_layout)
        layout.addWidget(identitas_box)

        input_box = QGroupBox("\ud83d\udcdd Form Pengeluaran")
        input_layout = QVBoxLayout()

        desc_layout = QHBoxLayout()
        desc_label = QLabel("Deskripsi:")
        self.desc_input = QLineEdit()
        desc_layout.addWidget(desc_label)
        desc_layout.addWidget(self.desc_input)
        input_layout.addLayout(desc_layout)

        amount_layout = QHBoxLayout()
        amount_label = QLabel("Jumlah:")
        self.amount_input = QSpinBox()
        self.amount_input.setRange(1, 10000000)
        amount_layout.addWidget(amount_label)
        amount_layout.addWidget(self.amount_input)
        input_layout.addLayout(amount_layout)

        category_layout = QHBoxLayout()
        category_label = QLabel("Kategori:")
        self.category_input = QComboBox()
        self.category_input.addItems(["Makanan", "Transportasi", "Belanja", "Hiburan", "Tagihan", "Lainnya"])
        category_layout.addWidget(category_label)
        category_layout.addWidget(self.category_input)
        input_layout.addLayout(category_layout)

        date_layout = QHBoxLayout()
        date_label = QLabel("Tanggal:")
        self.date_input = QDateEdit()
        self.date_input.setDate(QDate.currentDate())
        self.date_input.setCalendarPopup(True)
        date_layout.addWidget(date_label)
        date_layout.addWidget(self.date_input)
        input_layout.addLayout(date_layout)

        input_box.setLayout(input_layout)
        layout.addWidget(input_box)

        btn_layout = QHBoxLayout()
        add_btn = QPushButton("\u2795 Tambah")
        add_btn.clicked.connect(self.tambah_pengeluaran)
        clear_btn = QPushButton("\ud83d\uddd1\ufe0f Hapus Semua")
        clear_btn.clicked.connect(self.hapus_semua)

        for btn in [add_btn, clear_btn]:
            btn.setCursor(Qt.PointingHandCursor)
            btn.setMinimumHeight(40)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #ffb6b9;
                    border-radius: 20px;
                    font-weight: bold;
                    color: white;
                }
                QPushButton:hover {
                    background-color: #ff929f;
                }
            """)

        btn_layout.addWidget(add_btn)
        btn_layout.addWidget(clear_btn)
        layout.addLayout(btn_layout)

        list_box = QGroupBox("\ud83d\udccb Daftar Pengeluaran")
        list_layout = QVBoxLayout()
        self.expense_list = QListWidget()
        self.expense_list.itemClicked.connect(self.detail_pengeluaran)
        list_layout.addWidget(self.expense_list)
        list_box.setLayout(list_layout)
        layout.addWidget(list_box)

        self.statistik_label = QLabel("\ud83d\udcb0 Total: Rp0 | \ud83d\udcca Transaksi: 0")
        self.statistik_label.setFont(QFont("Segoe UI", 11, QFont.Bold))
        self.statistik_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.statistik_label)

        widget.setLayout(layout)

    def emoji_kategori(self, kategori):
        mapping = {
            "Makanan": "\ud83c\udf54",
            "Transportasi": "\ud83d\ude97",
            "Belanja": "\ud83d\udecb\ufe0f",
            "Hiburan": "\ud83c\udfa5",
            "Tagihan": "\ud83d\udcc8",
            "Lainnya": "\ud83d\udd39"
        }
        return mapping.get(kategori, "\ud83d\udd39")

    def tambah_pengeluaran(self):
        deskripsi = self.desc_input.text().strip()
        if not deskripsi:
            QMessageBox.warning(self, "Peringatan", "Harap masukkan deskripsi.")
            return

        jumlah = self.amount_input.value()
        kategori = self.category_input.currentText()
        tanggal = self.date_input.date().toString("yyyy-MM-dd")

        emoji = self.emoji_kategori(kategori)
        text = f"{emoji} {kategori}\n{tanggal}\n{deskripsi} - Rp{jumlah}"

        item = QListWidgetItem(text)
        item.setFont(QFont("Segoe UI", 10))
        item.setBackground(QColor("#ffe0f0"))
        item.setData(Qt.UserRole, {"jumlah": jumlah, "kategori": kategori, "deskripsi": deskripsi, "tanggal": tanggal})
        self.expense_list.addItem(item)

        self.total_pengeluaran += jumlah
        self.update_statistik()
        self.desc_input.clear()

    def update_statistik(self):
        transaksi = self.expense_list.count()
        self.statistik_label.setText(f"\ud83d\udcb0 Total: Rp{self.total_pengeluaran} | \ud83d\udcca Transaksi: {transaksi}")

    def detail_pengeluaran(self, item):
        data = item.data(Qt.UserRole)
        if data:
            detail = (f"Kategori: {data['kategori']}\n"
                      f"Tanggal: {data['tanggal']}\n"
                      f"Deskripsi: {data['deskripsi']}\n"
                      f"Jumlah: Rp{data['jumlah']}")
            QMessageBox.information(self, "Detail Pengeluaran", detail)

    def hapus_semua(self):
        konfirmasi = QMessageBox.question(
            self, "Konfirmasi", "Apakah kamu yakin ingin menghapus semua pengeluaran?",
            QMessageBox.Yes | QMessageBox.No
        )
        if konfirmasi == QMessageBox.Yes:
            self.expense_list.clear()
            self.total_pengeluaran = 0
            self.update_statistik()

    def setGradientBackground(self):
        p = self.palette()
        gradient = QLinearGradient(0, 0, 0, self.height())
        gradient.setColorAt(0.0, QColor("#f0f8ff"))
        gradient.setColorAt(1.0, QColor("#ffe0f0"))
        p.setBrush(QPalette.Window, QBrush(gradient))
        self.setPalette(p)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = AplikasiPengeluaranKreatif()
    win.show()
    sys.exit(app.exec_())
