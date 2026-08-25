"""
BUSINESS ASSISTANT PRO 10.0
Коммерческая версия учебного проекта.

Возможности:
- Авторизация
- Роли: admin / manager / cashier
- Товары и склад
- Штрихкод
- Приход товара
- Продажи с корзиной
- Скидка
- Наличные / карта / перевод
- Клиенты
- Расходы
- Возвраты
- Отчёты за период
- CSV экспорт
- Backup базы
- Настройки магазина
- Смена пароля

Первый вход:
admin
admin123
"""

import csv
import hashlib
import sqlite3
import shutil
import tkinter as tk
from datetime import datetime, timedelta
from calendar import monthrange
from tkinter import filedialog, messagebox, simpledialog, ttk
from pathlib import Path


APP_NAME = "Business Assistant PRO 10.0"
DB_NAME = "business_assistant_pro_10.db"

BG = "#f3f6fa"
WHITE = "#ffffff"
DARK = "#16283b"
BLUE = "#2563eb"
GREEN = "#16a34a"
RED = "#dc2626"
ORANGE = "#ea8a00"
PURPLE = "#7c3aed"
GRAY = "#64748b"


def password_hash(value):
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def now():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def display_date(value):
    try:
        return datetime.strptime(
            value, "%Y-%m-%d %H:%M:%S"
        ).strftime("%d.%m.%Y %H:%M")
    except ValueError:
        return value


class DB:
    def __init__(self, filename=DB_NAME):
        self.filename = filename
        self.conn = sqlite3.connect(filename)
        self.conn.row_factory = sqlite3.Row
        self.conn.execute("PRAGMA foreign_keys = ON")
        self.setup()

    def setup(self):
        self.conn.executescript("""
        CREATE TABLE IF NOT EXISTS settings(
            key TEXT PRIMARY KEY,
            value TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT NOT NULL DEFAULT 'cashier'
        );

        CREATE TABLE IF NOT EXISTS products(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            barcode TEXT UNIQUE,
            category TEXT NOT NULL DEFAULT 'Без категории',
            price REAL NOT NULL DEFAULT 0,
            cost REAL NOT NULL DEFAULT 0,
            quantity INTEGER NOT NULL DEFAULT 0,
            min_quantity INTEGER NOT NULL DEFAULT 3
        );

        CREATE TABLE IF NOT EXISTS clients(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT DEFAULT '',
            note TEXT DEFAULT ''
        );

        CREATE TABLE IF NOT EXISTS purchases(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            cost REAL NOT NULL,
            total REAL NOT NULL,
            created_at TEXT NOT NULL,
            user TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS orders(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            client_name TEXT DEFAULT '',
            payment TEXT NOT NULL,
            subtotal REAL NOT NULL,
            discount REAL NOT NULL,
            total REAL NOT NULL,
            created_at TEXT NOT NULL,
            cashier TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS order_items(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            product_name TEXT NOT NULL,
            price REAL NOT NULL,
            quantity INTEGER NOT NULL,
            total REAL NOT NULL,
            FOREIGN KEY(order_id) REFERENCES orders(id) ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS expenses(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            amount REAL NOT NULL,
            description TEXT NOT NULL,
            created_at TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS returns(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            product_name TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            amount REAL NOT NULL,
            reason TEXT NOT NULL,
            created_at TEXT NOT NULL,
            user TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS audit_log(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            action TEXT NOT NULL,
            details TEXT NOT NULL DEFAULT '',
            created_at TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS licenses(
            id INTEGER PRIMARY KEY CHECK(id=1),
            license_key TEXT NOT NULL,
            activated_at TEXT NOT NULL
        );
        """)

        defaults = {
            "shop_name": "Business Assistant PRO",
            "phone": "",
            "address": "",
            "currency": "руб.",
        }

        for key, value in defaults.items():
            self.conn.execute(
                "INSERT OR IGNORE INTO settings(key,value) VALUES(?,?)",
                (key, value)
            )

        self.conn.execute(
            """
            INSERT OR IGNORE INTO users(username,password_hash,role)
            VALUES(?,?,?)
            """,
            ("admin", password_hash("admin123"), "admin")
        )

        self.conn.commit()

    def get(self, key, default=""):
        row = self.conn.execute(
            "SELECT value FROM settings WHERE key=?", (key,)
        ).fetchone()
        return row["value"] if row else default

    def set(self, key, value):
        self.conn.execute(
            """
            INSERT INTO settings(key,value) VALUES(?,?)
            ON CONFLICT(key) DO UPDATE SET value=excluded.value
            """,
            (key, value)
        )
        self.conn.commit()

    def log(self, username, action, details=""):
        self.conn.execute(
            """
            INSERT INTO audit_log(username,action,details,created_at)
            VALUES(?,?,?,?)
            """,
            (username, action, details, now())
        )
        self.conn.commit()

    def close(self):
        self.conn.close()


class LoginWindow:
    def __init__(self, root, db, callback):
        self.root = root
        self.db = db
        self.callback = callback

        self.win = tk.Toplevel(root)
        self.win.title("Вход")
        self.win.geometry("430x420")
        self.win.resizable(False, False)
        self.win.configure(bg=WHITE)
        self.win.protocol("WM_DELETE_WINDOW", root.destroy)

        tk.Label(
            self.win, text="💼",
            bg=WHITE, fg=BLUE,
            font=("Arial", 42)
        ).pack(pady=(30, 0))

        tk.Label(
            self.win, text="Business Assistant",
            bg=WHITE, fg=DARK,
            font=("Arial", 23, "bold")
        ).pack()

        tk.Label(
            self.win, text="PRO 4.0",
            bg=WHITE, fg=BLUE,
            font=("Arial", 12, "bold")
        ).pack(pady=(0, 20))

        form = tk.Frame(self.win, bg=WHITE)
        form.pack(fill=tk.X, padx=55)

        tk.Label(form, text="Логин", bg=WHITE, fg=GRAY).pack(anchor="w")
        self.user = tk.Entry(form, font=("Arial", 11))
        self.user.pack(fill=tk.X, pady=(4, 12))
        self.user.insert(0, "admin")

        tk.Label(form, text="Пароль", bg=WHITE, fg=GRAY).pack(anchor="w")
        self.password = tk.Entry(form, show="•", font=("Arial", 11))
        self.password.pack(fill=tk.X, pady=4)
        self.password.bind("<Return>", lambda e: self.login())

        tk.Button(
            form, text="Войти",
            command=self.login,
            bg=BLUE, fg=WHITE,
            activebackground=BLUE,
            activeforeground=WHITE,
            relief=tk.FLAT,
            font=("Arial", 11, "bold"),
            cursor="hand2",
            pady=9
        ).pack(fill=tk.X, pady=18)

        tk.Label(
            self.win,
            text="Первый вход: admin / admin123",
            bg=WHITE, fg=GRAY,
            font=("Arial", 9)
        ).pack()

    def login(self):
        row = self.db.conn.execute(
            """
            SELECT username, role
            FROM users
            WHERE username=? AND password_hash=?
            """,
            (
                self.user.get().strip(),
                password_hash(self.password.get())
            )
        ).fetchone()

        if not row:
            messagebox.showerror(
                "Ошибка", "Неверный логин или пароль.",
                parent=self.win
            )
            return

        self.win.destroy()
        self.callback(row["username"], row["role"])


class App:
    def __init__(self, root):
        self.root = root
        self.root.withdraw()
        self.db = DB()
        self.cart = []
        LoginWindow(root, self.db, self.start)

    def start(self, username, role):
        self.username = username
        self.role = role

        self.root.deiconify()
        self.root.title(APP_NAME)
        self.root.geometry("1380x880")
        self.root.minsize(1120, 740)
        self.root.configure(bg=BG)

        self.setup_style()
        self.build_ui()
        self.refresh_all()
        self.root.protocol("WM_DELETE_WINDOW", self.close)

    def setup_style(self):
        style = ttk.Style()
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        style.configure(
            "Treeview",
            background=WHITE,
            fieldbackground=WHITE,
            foreground=DARK,
            rowheight=31,
            font=("Arial", 10)
        )
        style.configure(
            "Treeview.Heading",
            background=DARK,
            foreground=WHITE,
            font=("Arial", 10, "bold"),
            padding=7
        )
        style.map(
            "Treeview",
            background=[("selected", BLUE)],
            foreground=[("selected", WHITE)]
        )

    def money(self, value):
        return f"{float(value):,.2f} {self.db.get('currency', 'руб.')}"

    def button(self, parent, text, command, color=BLUE, width=15):
        return tk.Button(
            parent,
            text=text,
            command=command,
            bg=color,
            fg=WHITE,
            activebackground=color,
            activeforeground=WHITE,
            relief=tk.FLAT,
            font=("Arial", 10, "bold"),
            cursor="hand2",
            width=width,
            pady=7
        )

    def clear(self, tree):
        for item in tree.get_children():
            tree.delete(item)

    def allowed(self, roles):
        return self.role in roles

    def build_ui(self):
        header = tk.Frame(self.root, bg=DARK, height=70)
        header.pack(fill=tk.X)
        header.pack_propagate(False)

        self.shop_title = tk.Label(
            header, text="",
            bg=DARK, fg=WHITE,
            font=("Arial", 21, "bold")
        )
        self.shop_title.pack(side=tk.LEFT, padx=20)

        tk.Label(
            header,
            text=f"👤 {self.username} • {self.role}",
            bg=DARK, fg="#dbeafe",
            font=("Arial", 10, "bold")
        ).pack(side=tk.RIGHT, padx=20)

        self.button(
            header, "⚙ Настройки",
            self.settings, DARK, 14
        ).pack(side=tk.RIGHT, padx=5)

        cards = tk.Frame(self.root, bg=BG)
        cards.pack(fill=tk.X, padx=18, pady=13)

        self.card_revenue = self.make_card(cards, "💰 Выручка", GREEN)
        self.card_profit = self.make_card(cards, "📈 Прибыль", BLUE)
        self.card_expenses = self.make_card(cards, "💸 Расходы", RED)
        self.card_stock = self.make_card(cards, "📦 Товаров", PURPLE)
        self.card_low = self.make_card(cards, "🔔 Мало", ORANGE)

        notebook = ttk.Notebook(self.root)
        notebook.pack(fill=tk.BOTH, expand=True, padx=18, pady=(0, 7))

        self.home = tk.Frame(notebook, bg=BG)
        self.sales = tk.Frame(notebook, bg=BG)
        self.products = tk.Frame(notebook, bg=BG)
        self.clients = tk.Frame(notebook, bg=BG)
        self.purchases = tk.Frame(notebook, bg=BG)
        self.expenses = tk.Frame(notebook, bg=BG)
        self.history = tk.Frame(notebook, bg=BG)
        self.reports = tk.Frame(notebook, bg=BG)
        self.dashboard = tk.Frame(notebook, bg=BG)
        self.returns = tk.Frame(notebook, bg=BG)
        self.logs = tk.Frame(notebook, bg=BG)

        notebook.add(self.home, text="🏠 Главная")
        notebook.add(self.sales, text="🛒 Продажа")
        notebook.add(self.products, text="📦 Склад")
        notebook.add(self.clients, text="👥 Клиенты")
        notebook.add(self.purchases, text="📥 Приход")
        notebook.add(self.expenses, text="💸 Расходы")
        notebook.add(self.history, text="📜 История")
        notebook.add(self.reports, text="📊 Отчёты")
        notebook.add(self.dashboard, text="📈 Графики")
        notebook.add(self.returns, text="↩ Возвраты")
        if self.role == "admin":
            notebook.add(self.logs, text="📝 Журнал")

        self.build_home()
        self.build_sales()
        self.build_products()
        self.build_clients()
        self.build_purchases()
        self.build_expenses()
        self.build_history()
        self.build_reports()
        self.build_dashboard()
        self.build_returns()
        self.build_logs()

        tk.Label(
            self.root,
            text=f"{APP_NAME} • SQLite",
            bg=BG, fg=GRAY, font=("Arial", 8)
        ).pack(pady=(0, 4))

    def make_card(self, parent, title, color):
        frame = tk.Frame(
            parent, bg=WHITE,
            highlightbackground="#d9e2ec",
            highlightthickness=1
        )
        frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)

        tk.Label(
            frame, text=title,
            bg=WHITE, fg=GRAY,
            font=("Arial", 10, "bold")
        ).pack(pady=(10, 2))

        label = tk.Label(
            frame, text="0",
            bg=WHITE, fg=color,
            font=("Arial", 17, "bold")
        )
        label.pack(pady=(0, 10))
        return label

    # ---------------- HOME ----------------

    def build_home(self):
        box = tk.Frame(self.home, bg=WHITE)
        box.pack(fill=tk.BOTH, expand=True, padx=25, pady=25)

        tk.Label(
            box, text="Панель управления",
            bg=WHITE, fg=DARK,
            font=("Arial", 22, "bold")
        ).pack(anchor="w", padx=25, pady=(25, 5))

        self.home_info = tk.Label(
            box, text="", bg=WHITE, fg=GRAY,
            justify=tk.LEFT, font=("Arial", 11)
        )
        self.home_info.pack(anchor="w", padx=25, pady=8)

        quick = tk.Frame(box, bg=WHITE)
        quick.pack(fill=tk.X, padx=20, pady=12)

        if self.allowed(("admin", "manager", "cashier")):
            self.button(
                quick, "🛒 Продажа",
                self.focus_sale, BLUE, 17
            ).pack(side=tk.LEFT, padx=5)

        if self.allowed(("admin", "manager")):
            self.button(
                quick, "➕ Товар",
                self.product_window, GREEN, 17
            ).pack(side=tk.LEFT, padx=5)

        if self.allowed(("admin", "manager")):
            self.button(
                quick, "📥 Приход",
                self.purchase_window, PURPLE, 17
            ).pack(side=tk.LEFT, padx=5)

        self.button(
            quick, "📄 CSV",
            self.export_csv, ORANGE, 17
        ).pack(side=tk.LEFT, padx=5)

        if self.role == "admin":
            self.button(
                quick, "👨‍💼 Сотрудники",
                self.users_window, DARK, 17
            ).pack(side=tk.LEFT, padx=5)

        tk.Label(
            box,
            text="🔔 Контроль склада",
            bg=WHITE, fg=DARK,
            font=("Arial", 16, "bold")
        ).pack(anchor="w", padx=25, pady=(15, 7))

        self.alert = tk.Text(
            box, height=12,
            bg=WHITE, fg=DARK,
            relief=tk.FLAT,
            font=("Arial", 11)
        )
        self.alert.pack(fill=tk.BOTH, expand=True, padx=25, pady=(0, 25))
        self.alert.configure(state=tk.DISABLED)

    def focus_sale(self):
        self.sale_product.focus_set()

    # ---------------- SALES ----------------

    def build_sales(self):
        main = tk.Frame(self.sales, bg=BG)
        main.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        left = tk.Frame(main, bg=WHITE)
        left.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 8))

        right = tk.Frame(main, bg=WHITE)
        right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(8, 0))

        tk.Label(
            left, text="🛒 Новый заказ",
            bg=WHITE, fg=DARK,
            font=("Arial", 20, "bold")
        ).pack(pady=16)

        form = tk.Frame(left, bg=WHITE)
        form.pack(fill=tk.X, padx=30)

        tk.Label(form, text="Штрихкод или название",
                 bg=WHITE, fg=GRAY).pack(anchor="w")

        self.sale_search = tk.Entry(form)
        self.sale_search.pack(fill=tk.X, pady=5)
        self.sale_search.bind("<Return>", self.search_sale)

        tk.Label(form, text="Товар",
                 bg=WHITE, fg=GRAY).pack(anchor="w")

        self.sale_product = ttk.Combobox(form, state="readonly")
        self.sale_product.pack(fill=tk.X, pady=5)

        tk.Label(form, text="Количество",
                 bg=WHITE, fg=GRAY).pack(anchor="w")

        self.sale_qty = tk.Entry(form)
        self.sale_qty.pack(fill=tk.X, pady=5)
        self.sale_qty.insert(0, "1")

        tk.Label(form, text="Скидка (%)",
                 bg=WHITE, fg=GRAY).pack(anchor="w")

        self.sale_discount = tk.Entry(form)
        self.sale_discount.pack(fill=tk.X, pady=5)
        self.sale_discount.insert(0, "0")
        self.sale_discount.bind(
            "<KeyRelease>",
            lambda e: self.refresh_cart()
        )

        tk.Label(form, text="Оплата",
                 bg=WHITE, fg=GRAY).pack(anchor="w")

        self.sale_payment = ttk.Combobox(
            form,
            state="readonly",
            values=("Наличные", "Карта", "Перевод")
        )
        self.sale_payment.pack(fill=tk.X, pady=5)
        self.sale_payment.set("Наличные")

        tk.Label(form, text="Клиент",
                 bg=WHITE, fg=GRAY).pack(anchor="w")

        self.sale_client = ttk.Combobox(form, state="readonly")
        self.sale_client.pack(fill=tk.X, pady=5)

        self.button(
            form, "➕ Добавить",
            self.add_cart, BLUE, 24
        ).pack(pady=10)

        self.button(
            form, "🗑 Удалить позицию",
            self.remove_cart, RED, 24
        ).pack(pady=3)

        self.button(
            form, "💳 Оформить заказ",
            self.checkout, GREEN, 24
        ).pack(pady=10)

        tk.Label(
            right, text="Состав заказа",
            bg=WHITE, fg=DARK,
            font=("Arial", 18, "bold")
        ).pack(pady=16)

        columns = ("product", "qty", "price", "total")
        self.cart_table = ttk.Treeview(
            right, columns=columns, show="headings"
        )

        for col, title, width in [
            ("product", "Товар", 240),
            ("qty", "Кол.", 70),
            ("price", "Цена", 120),
            ("total", "Сумма", 130)
        ]:
            self.cart_table.heading(col, text=title)
            self.cart_table.column(col, width=width)

        self.cart_table.pack(
            fill=tk.BOTH, expand=True, padx=20
        )

        self.cart_total = tk.Label(
            right, text="",
            bg=WHITE, fg=DARK,
            justify=tk.LEFT,
            font=("Arial", 12, "bold")
        )
        self.cart_total.pack(anchor="w", padx=20, pady=18)

    def search_sale(self, event=None):
        value = self.sale_search.get().strip()
        if not value:
            return

        row = self.db.conn.execute(
            """
            SELECT name
            FROM products
            WHERE barcode=? OR name LIKE ?
            AND quantity > 0
            ORDER BY name
            LIMIT 1
            """,
            (value, f"%{value}%")
        ).fetchone()

        if row:
            self.sale_product.set(row["name"])
            self.add_cart()
            self.sale_search.delete(0, tk.END)
        else:
            messagebox.showinfo(
                "Поиск", "Товар не найден."
            )

    def add_cart(self):
        name = self.sale_product.get().strip()

        try:
            qty = int(self.sale_qty.get())
        except ValueError:
            messagebox.showerror(
                "Ошибка", "Количество должно быть целым."
            )
            return

        if not name or qty <= 0:
            messagebox.showwarning(
                "Ошибка", "Выберите товар и количество."
            )
            return

        row = self.db.conn.execute(
            """
            SELECT id,name,price,quantity
            FROM products
            WHERE name=?
            """,
            (name,)
        ).fetchone()

        if not row:
            return

        existing = sum(
            item["quantity"]
            for item in self.cart
            if item["product_id"] == row["id"]
        )

        if existing + qty > row["quantity"]:
            messagebox.showerror(
                "Ошибка",
                f"Доступно только {row['quantity']} шт."
            )
            return

        self.cart.append({
            "product_id": row["id"],
            "name": row["name"],
            "price": float(row["price"]),
            "quantity": qty
        })

        self.sale_product.set("")
        self.sale_qty.delete(0, tk.END)
        self.sale_qty.insert(0, "1")
        self.refresh_cart()

    def remove_cart(self):
        selected = self.cart_table.selection()
        if not selected:
            return

        index = int(
            self.cart_table.item(
                selected[0], "tags"
            )[0]
        )

        del self.cart[index]
        self.refresh_cart()

    def refresh_cart(self):
        self.clear(self.cart_table)

        subtotal = 0

        for index, item in enumerate(self.cart):
            line = item["price"] * item["quantity"]
            subtotal += line

            self.cart_table.insert(
                "", tk.END,
                values=(
                    item["name"],
                    item["quantity"],
                    self.money(item["price"]),
                    self.money(line)
                ),
                tags=(str(index),)
            )

        try:
            discount_percent = float(
                self.sale_discount.get()
            )
        except (ValueError, tk.TclError):
            discount_percent = 0

        discount_percent = max(
            0, min(100, discount_percent)
        )

        discount = subtotal * discount_percent / 100
        total = subtotal - discount

        self.cart_total.config(
            text=(
                f"Подытог: {self.money(subtotal)}\n"
                f"Скидка: {discount_percent:.2f}% "
                f"({self.money(discount)})\n"
                f"ИТОГО: {self.money(total)}"
            )
        )

    def checkout(self):
        if not self.cart:
            messagebox.showwarning(
                "Заказ", "Корзина пустая."
            )
            return

        try:
            discount_percent = float(
                self.sale_discount.get()
            )
        except ValueError:
            messagebox.showerror(
                "Ошибка", "Скидка должна быть числом."
            )
            return

        if not 0 <= discount_percent <= 100:
            messagebox.showwarning(
                "Ошибка", "Скидка от 0 до 100%."
            )
            return

        subtotal = sum(
            item["price"] * item["quantity"]
            for item in self.cart
        )
        discount = subtotal * discount_percent / 100
        total = subtotal - discount

        payment = self.sale_payment.get() or "Наличные"
        client = self.sale_client.get().strip()
        created = now()

        try:
            cur = self.db.conn.cursor()

            cur.execute(
                """
                INSERT INTO orders(
                    client_name,payment,subtotal,discount,
                    total,created_at,cashier
                )
                VALUES(?,?,?,?,?,?,?)
                """,
                (
                    client, payment, subtotal, discount,
                    total, created, self.username
                )
            )

            order_id = cur.lastrowid

            for item in self.cart:
                cur.execute(
                    """
                    UPDATE products
                    SET quantity=quantity-?
                    WHERE id=? AND quantity>=?
                    """,
                    (
                        item["quantity"],
                        item["product_id"],
                        item["quantity"]
                    )
                )

                if cur.rowcount != 1:
                    raise ValueError(
                        f"Недостаточно товара: {item['name']}"
                    )

                line_total = item["price"] * item["quantity"]

                cur.execute(
                    """
                    INSERT INTO order_items(
                        order_id,product_id,product_name,
                        price,quantity,total
                    )
                    VALUES(?,?,?,?,?,?)
                    """,
                    (
                        order_id,
                        item["product_id"],
                        item["name"],
                        item["price"],
                        item["quantity"],
                        line_total
                    )
                )

            self.db.conn.commit()

        except (sqlite3.Error, ValueError) as error:
            self.db.conn.rollback()
            messagebox.showerror(
                "Ошибка", str(error)
            )
            return

        self.show_receipt(order_id)

        self.cart.clear()
        self.sale_discount.delete(0, tk.END)
        self.sale_discount.insert(0, "0")
        self.sale_client.set("")
        self.refresh_all()

    # ---------------- PRODUCTS ----------------

    def build_products(self):
        top = tk.Frame(self.products, bg=BG)
        top.pack(fill=tk.X, padx=20, pady=12)

        tk.Label(
            top, text="Поиск:",
            bg=BG, fg=DARK
        ).pack(side=tk.LEFT)

        self.product_search = tk.Entry(top, width=30)
        self.product_search.pack(side=tk.LEFT, padx=7)
        self.product_search.bind(
            "<KeyRelease>",
            lambda e: self.refresh_products()
        )

        if self.allowed(("admin", "manager")):
            self.button(
                top, "➕ Товар",
                self.product_window, GREEN, 14
            ).pack(side=tk.RIGHT, padx=4)

            self.button(
                top, "✏ Изменить",
                self.edit_product, BLUE, 14
            ).pack(side=tk.RIGHT, padx=4)

            self.button(
                top, "🗑 Удалить",
                self.delete_product, RED, 14
            ).pack(side=tk.RIGHT, padx=4)

        columns = (
            "id", "name", "barcode",
            "category", "price", "cost",
            "qty", "status"
        )

        self.product_table = ttk.Treeview(
            self.products,
            columns=columns,
            show="headings"
        )

        for col, title, width in [
            ("id", "ID", 50),
            ("name", "Товар", 220),
            ("barcode", "Штрихкод", 140),
            ("category", "Категория", 140),
            ("price", "Цена", 120),
            ("cost", "Себест.", 120),
            ("qty", "Кол.", 70),
            ("status", "Статус", 150)
        ]:
            self.product_table.heading(col, text=title)
            self.product_table.column(col, width=width)

        self.product_table.tag_configure(
            "low", background="#fff2c7"
        )
        self.product_table.tag_configure(
            "empty", background="#ffdede"
        )

        self.product_table.pack(
            fill=tk.BOTH, expand=True,
            padx=20, pady=(0, 20)
        )

    def product_window(self, product_id=None):
        edit = product_id is not None

        win = tk.Toplevel(self.root)
        win.title("Товар")
        win.geometry("480x590")
        win.configure(bg=WHITE)
        win.grab_set()

        tk.Label(
            win,
            text="✏ Редактирование" if edit else "➕ Новый товар",
            bg=WHITE, fg=DARK,
            font=("Arial", 20, "bold")
        ).pack(pady=20)

        form = tk.Frame(win, bg=WHITE)
        form.pack(fill=tk.X, padx=45)

        labels = [
            "Название",
            "Штрихкод",
            "Категория",
            "Цена продажи",
            "Себестоимость",
            "Количество",
            "Минимальный остаток"
        ]

        fields = {}

        for label in labels:
            tk.Label(
                form, text=label,
                bg=WHITE, fg=GRAY
            ).pack(anchor="w")

            entry = tk.Entry(form)
            entry.pack(fill=tk.X, pady=(3, 10))
            fields[label] = entry

        if edit:
            row = self.db.conn.execute(
                "SELECT * FROM products WHERE id=?",
                (product_id,)
            ).fetchone()

            if not row:
                win.destroy()
                return

            fields["Название"].insert(0, row["name"])
            fields["Штрихкод"].insert(0, row["barcode"] or "")
            fields["Категория"].insert(0, row["category"])
            fields["Цена продажи"].insert(0, row["price"])
            fields["Себестоимость"].insert(0, row["cost"])
            fields["Количество"].insert(0, row["quantity"])
            fields["Минимальный остаток"].insert(
                0, row["min_quantity"]
            )
        else:
            fields["Категория"].insert(0, "Без категории")
            fields["Количество"].insert(0, "0")
            fields["Минимальный остаток"].insert(0, "3")

        def save():
            try:
                price = float(
                    fields["Цена продажи"].get()
                )
                cost = float(
                    fields["Себестоимость"].get() or 0
                )
                quantity = int(
                    fields["Количество"].get()
                )
                minimum = int(
                    fields["Минимальный остаток"].get()
                )
            except ValueError:
                messagebox.showerror(
                    "Ошибка",
                    "Цена/себестоимость — числа. "
                    "Количество — целое.",
                    parent=win
                )
                return

            name = fields["Название"].get().strip()
            barcode = fields["Штрихкод"].get().strip() or None
            category = (
                fields["Категория"].get().strip()
                or "Без категории"
            )

            if (
                not name or
                price < 0 or
                cost < 0 or
                quantity < 0 or
                minimum < 0
            ):
                messagebox.showwarning(
                    "Ошибка",
                    "Проверьте данные.",
                    parent=win
                )
                return

            try:
                if edit:
                    self.db.conn.execute(
                        """
                        UPDATE products
                        SET name=?,barcode=?,category=?,
                            price=?,cost=?,quantity=?,
                            min_quantity=?
                        WHERE id=?
                        """,
                        (
                            name, barcode, category,
                            price, cost, quantity,
                            minimum, product_id
                        )
                    )
                else:
                    self.db.conn.execute(
                        """
                        INSERT INTO products(
                            name,barcode,category,
                            price,cost,quantity,min_quantity
                        )
                        VALUES(?,?,?,?,?,?,?)
                        """,
                        (
                            name, barcode, category,
                            price, cost, quantity, minimum
                        )
                    )

                self.db.conn.commit()

            except sqlite3.IntegrityError:
                messagebox.showerror(
                    "Ошибка",
                    "Название или штрихкод уже используется.",
                    parent=win
                )
                return

            win.destroy()
            self.refresh_all()

        self.button(
            win, "💾 Сохранить",
            save, GREEN, 25
        ).pack(pady=8)

    def selected_product(self):
        selected = self.product_table.selection()
        if not selected:
            messagebox.showwarning(
                "Ошибка", "Выберите товар."
            )
            return None

        return int(
            self.product_table.item(
                selected[0], "values"
            )[0]
        )

    def edit_product(self):
        product_id = self.selected_product()
        if product_id:
            self.product_window(product_id)

    def delete_product(self):
        product_id = self.selected_product()
        if not product_id:
            return

        row = self.db.conn.execute(
            "SELECT name FROM products WHERE id=?",
            (product_id,)
        ).fetchone()

        if row and messagebox.askyesno(
            "Удаление",
            f"Удалить «{row['name']}»?"
        ):
            self.db.conn.execute(
                "DELETE FROM products WHERE id=?",
                (product_id,)
            )
            self.db.conn.commit()
            self.refresh_all()

    # ---------------- PURCHASES ----------------

    def build_purchases(self):
        top = tk.Frame(self.purchases, bg=BG)
        top.pack(fill=tk.X, padx=20, pady=12)

        if self.allowed(("admin", "manager")):
            self.button(
                top, "📥 Новый приход",
                self.purchase_window,
                GREEN, 18
            ).pack(side=tk.RIGHT)

        columns = (
            "id", "date", "product",
            "qty", "cost", "total", "user"
        )

        self.purchase_table = ttk.Treeview(
            self.purchases,
            columns=columns,
            show="headings"
        )

        for col, title, width in [
            ("id", "ID", 55),
            ("date", "Дата", 170),
            ("product", "Товар", 250),
            ("qty", "Кол.", 80),
            ("cost", "Цена закупки", 130),
            ("total", "Сумма", 130),
            ("user", "Сотрудник", 130)
        ]:
            self.purchase_table.heading(col, text=title)
            self.purchase_table.column(col, width=width)

        self.purchase_table.pack(
            fill=tk.BOTH, expand=True,
            padx=20, pady=(0, 20)
        )

    def purchase_window(self):
        win = tk.Toplevel(self.root)
        win.title("Приход товара")
        win.geometry("440x390")
        win.configure(bg=WHITE)
        win.grab_set()

        tk.Label(
            win, text="📥 Приход товара",
            bg=WHITE, fg=DARK,
            font=("Arial", 20, "bold")
        ).pack(pady=25)

        form = tk.Frame(win, bg=WHITE)
        form.pack(fill=tk.X, padx=45)

        tk.Label(
            form, text="Товар",
            bg=WHITE, fg=GRAY
        ).pack(anchor="w")

        product = ttk.Combobox(
            form, state="readonly"
        )
        product.pack(fill=tk.X, pady=(3, 12))

        names = [
            row["name"]
            for row in self.db.conn.execute(
                "SELECT name FROM products ORDER BY name"
            ).fetchall()
        ]
        product["values"] = names

        tk.Label(
            form, text="Количество",
            bg=WHITE, fg=GRAY
        ).pack(anchor="w")

        quantity = tk.Entry(form)
        quantity.pack(fill=tk.X, pady=(3, 12))

        tk.Label(
            form, text="Цена закупки",
            bg=WHITE, fg=GRAY
        ).pack(anchor="w")

        cost = tk.Entry(form)
        cost.pack(fill=tk.X, pady=(3, 12))

        def save():
            try:
                qty = int(quantity.get())
                price = float(cost.get())
            except ValueError:
                messagebox.showerror(
                    "Ошибка",
                    "Количество — целое, цена — число.",
                    parent=win
                )
                return

            if not product.get() or qty <= 0 or price < 0:
                messagebox.showwarning(
                    "Ошибка",
                    "Проверьте данные.",
                    parent=win
                )
                return

            row = self.db.conn.execute(
                "SELECT id FROM products WHERE name=?",
                (product.get(),)
            ).fetchone()

            total = qty * price

            self.db.conn.execute(
                """
                UPDATE products
                SET quantity=quantity+?, cost=?
                WHERE id=?
                """,
                (qty, price, row["id"])
            )

            self.db.conn.execute(
                """
                INSERT INTO purchases(
                    product_id,quantity,cost,total,
                    created_at,user
                )
                VALUES(?,?,?,?,?,?)
                """,
                (
                    row["id"], qty, price,
                    total, now(), self.username
                )
            )

            self.db.conn.commit()
            win.destroy()
            self.refresh_all()

        self.button(
            win, "💾 Сохранить приход",
            save, GREEN, 25
        ).pack(pady=10)

    # ---------------- CLIENTS ----------------

    def build_clients(self):
        top = tk.Frame(self.clients, bg=BG)
        top.pack(fill=tk.X, padx=20, pady=12)

        self.button(
            top, "➕ Клиент",
            self.client_window,
            GREEN, 16
        ).pack(side=tk.RIGHT, padx=4)

        if self.allowed(("admin", "manager")):
            self.button(
                top, "🗑 Удалить",
                self.delete_client,
                RED, 16
            ).pack(side=tk.RIGHT, padx=4)

        columns = ("id", "name", "phone", "note")
        self.client_table = ttk.Treeview(
            self.clients,
            columns=columns,
            show="headings"
        )

        for col, title, width in [
            ("id", "ID", 60),
            ("name", "Имя", 300),
            ("phone", "Телефон", 220),
            ("note", "Примечание", 500)
        ]:
            self.client_table.heading(col, text=title)
            self.client_table.column(col, width=width)

        self.client_table.pack(
            fill=tk.BOTH, expand=True,
            padx=20, pady=(0, 20)
        )

    def client_window(self):
        win = tk.Toplevel(self.root)
        win.title("Клиент")
        win.geometry("440x390")
        win.configure(bg=WHITE)
        win.grab_set()

        tk.Label(
            win, text="👥 Новый клиент",
            bg=WHITE, fg=DARK,
            font=("Arial", 20, "bold")
        ).pack(pady=25)

        form = tk.Frame(win, bg=WHITE)
        form.pack(fill=tk.X, padx=45)

        fields = []

        for title in ("Имя", "Телефон", "Примечание"):
            tk.Label(
                form, text=title,
                bg=WHITE, fg=GRAY
            ).pack(anchor="w")

            entry = tk.Entry(form)
            entry.pack(fill=tk.X, pady=(3, 13))
            fields.append(entry)

        def save():
            name, phone, note = [
                x.get().strip() for x in fields
            ]

            if not name:
                messagebox.showwarning(
                    "Ошибка", "Введите имя.",
                    parent=win
                )
                return

            self.db.conn.execute(
                """
                INSERT INTO clients(name,phone,note)
                VALUES(?,?,?)
                """,
                (name, phone, note)
            )
            self.db.conn.commit()

            win.destroy()
            self.refresh_all()

        self.button(
            win, "💾 Сохранить",
            save, GREEN, 24
        ).pack(pady=6)


    def client_history_window(self):
        selected = self.client_table.selection()
        if not selected:
            messagebox.showwarning(
                "Клиенты",
                "Выберите клиента."
            )
            return

        values = self.client_table.item(
            selected[0], "values"
        )
        client_id = int(values[0])
        client_name = values[1]

        win = tk.Toplevel(self.root)
        win.title(f"История — {client_name}")
        win.geometry("900x600")
        win.configure(bg=COLORS["bg"])

        tk.Label(
            win,
            text=f"👤 {client_name}",
            bg=COLORS["bg"],
            fg=COLORS["dark"],
            font=("Arial", 20, "bold"),
        ).pack(pady=18)

        summary = tk.Label(
            win,
            text="",
            bg=COLORS["bg"],
            fg=COLORS["gray"],
            font=("Arial", 11),
        )
        summary.pack(pady=(0, 10))

        columns = ("id", "date", "payment", "total", "cashier")
        table = ttk.Treeview(
            win,
            columns=columns,
            show="headings",
        )

        for col, title, width in [
            ("id", "Заказ", 80),
            ("date", "Дата", 180),
            ("payment", "Оплата", 130),
            ("total", "Сумма", 150),
            ("cashier", "Кассир", 150),
        ]:
            table.heading(col, text=title)
            table.column(col, width=width)

        table.pack(
            fill=tk.BOTH,
            expand=True,
            padx=20,
            pady=10,
        )

        rows = self.db.conn.execute(
            """
            SELECT id, created_at, payment, total, cashier
            FROM orders
            WHERE client_name = ?
            ORDER BY id DESC
            """,
            (client_name,),
        ).fetchall()

        total_spent = sum(float(row["total"]) for row in rows)

        summary.config(
            text=(
                f"Заказов: {len(rows)}    "
                f"Всего покупок: {self.money(total_spent)}"
            )
        )

        for row in rows:
            table.insert(
                "",
                tk.END,
                values=(
                    row["id"],
                    display_date(row["created_at"]),
                    row["payment"],
                    self.money(row["total"]),
                    row["cashier"],
                ),
            )

        self.button(
            win,
            "Закрыть",
            win.destroy,
            COLORS["gray"],
            15,
        ).pack(pady=(0, 16))


    def edit_client(self):
        selected = self.client_table.selection()
        if not selected:
            messagebox.showwarning(
                "Клиенты",
                "Выберите клиента."
            )
            return

        values = self.client_table.item(
            selected[0], "values"
        )
        client_id = int(values[0])

        row = self.db.conn.execute(
            "SELECT * FROM clients WHERE id=?",
            (client_id,)
        ).fetchone()

        if not row:
            return

        win = tk.Toplevel(self.root)
        win.title("Изменить клиента")
        win.geometry("460x420")
        win.configure(bg=COLORS["white"])
        win.grab_set()

        tk.Label(
            win,
            text="✏ Изменить клиента",
            bg=COLORS["white"],
            fg=COLORS["dark"],
            font=("Arial", 20, "bold"),
        ).pack(pady=25)

        form = tk.Frame(win, bg=COLORS["white"])
        form.pack(fill=tk.X, padx=45)

        fields = []
        for label, value in (
            ("Имя", row["name"]),
            ("Телефон", row["phone"]),
            ("Примечание", row["note"]),
        ):
            tk.Label(
                form, text=label,
                bg=COLORS["white"],
                fg=COLORS["gray"]
            ).pack(anchor="w")
            entry = tk.Entry(form)
            entry.insert(0, value or "")
            entry.pack(fill=tk.X, pady=(3, 14))
            fields.append(entry)

        def save():
            name, phone, note = [
                x.get().strip() for x in fields
            ]
            if not name:
                messagebox.showwarning(
                    "Ошибка", "Имя не может быть пустым.",
                    parent=win
                )
                return

            self.db.conn.execute(
                """
                UPDATE clients
                SET name=?, phone=?, note=?
                WHERE id=?
                """,
                (name, phone, note, client_id)
            )
            self.db.conn.commit()
            self.db.log(
                self.username,
                "Клиент",
                f"Изменён ID {client_id}"
            )
            win.destroy()
            self.refresh_all()

        self.button(
            win, "💾 Сохранить",
            save, COLORS["green"], 24
        ).pack(pady=5)

    def delete_client(self):
        selected = self.client_table.selection()
        if not selected:
            return

        client_id = int(
            self.client_table.item(
                selected[0], "values"
            )[0]
        )

        if messagebox.askyesno(
            "Удаление", "Удалить клиента?"
        ):
            self.db.conn.execute(
                "DELETE FROM clients WHERE id=?",
                (client_id,)
            )
            self.db.conn.commit()
            self.refresh_all()

    # ---------------- EXPENSES ----------------

    def build_expenses(self):
        top = tk.Frame(self.expenses, bg=BG)
        top.pack(fill=tk.X, padx=20, pady=12)

        if self.allowed(("admin", "manager")):
            tk.Label(
                top, text="Сумма",
                bg=BG, fg=DARK
            ).pack(side=tk.LEFT)

            self.exp_amount = tk.Entry(top, width=14)
            self.exp_amount.pack(side=tk.LEFT, padx=6)

            tk.Label(
                top, text="Описание",
                bg=BG, fg=DARK
            ).pack(side=tk.LEFT)

            self.exp_desc = tk.Entry(top, width=35)
            self.exp_desc.pack(side=tk.LEFT, padx=6)

            self.button(
                top, "💸 Добавить",
                self.add_expense,
                ORANGE, 15
            ).pack(side=tk.LEFT)

        columns = ("id", "date", "description", "amount")
        self.expense_table = ttk.Treeview(
            self.expenses,
            columns=columns,
            show="headings"
        )

        for col, title, width in [
            ("id", "ID", 60),
            ("date", "Дата", 180),
            ("description", "Описание", 550),
            ("amount", "Сумма", 160)
        ]:
            self.expense_table.heading(col, text=title)
            self.expense_table.column(col, width=width)

        self.expense_table.pack(
            fill=tk.BOTH, expand=True,
            padx=20, pady=(0, 20)
        )

    def add_expense(self):
        try:
            amount = float(self.exp_amount.get())
        except ValueError:
            messagebox.showerror(
                "Ошибка", "Введите сумму."
            )
            return

        if amount <= 0:
            return

        description = (
            self.exp_desc.get().strip()
            or "Без описания"
        )

        self.db.conn.execute(
            """
            INSERT INTO expenses(
                amount,description,created_at
            )
            VALUES(?,?,?)
            """,
            (amount, description, now())
        )
        self.db.conn.commit()

        self.exp_amount.delete(0, tk.END)
        self.exp_desc.delete(0, tk.END)
        self.refresh_all()

    # ---------------- HISTORY ----------------

    def build_history(self):
        top = tk.Frame(self.history, bg=BG)
        top.pack(fill=tk.X, padx=20, pady=12)

        self.button(
            top, "🧾 Чек",
            self.receipt_from_history,
            BLUE, 14
        ).pack(side=tk.RIGHT, padx=4)

        self.button(
            top, "📄 CSV",
            self.export_csv,
            PURPLE, 14
        ).pack(side=tk.RIGHT, padx=4)

        columns = (
            "id", "date", "client",
            "payment", "subtotal",
            "discount", "total", "cashier"
        )

        self.history_table = ttk.Treeview(
            self.history,
            columns=columns,
            show="headings"
        )

        for col, title, width in [
            ("id", "Заказ", 70),
            ("date", "Дата", 170),
            ("client", "Клиент", 170),
            ("payment", "Оплата", 110),
            ("subtotal", "Подытог", 120),
            ("discount", "Скидка", 120),
            ("total", "Итого", 130),
            ("cashier", "Кассир", 130)
        ]:
            self.history_table.heading(col, text=title)
            self.history_table.column(col, width=width)

        self.history_table.pack(
            fill=tk.BOTH, expand=True,
            padx=20, pady=(0, 20)
        )

    def receipt_from_history(self):
        selected = self.history_table.selection()
        if not selected:
            messagebox.showwarning(
                "Чек", "Выберите заказ."
            )
            return

        order_id = int(
            self.history_table.item(
                selected[0], "values"
            )[0]
        )

        self.show_receipt(order_id)

    # ---------------- REPORTS ----------------

    def build_reports(self):
        top = tk.Frame(self.reports, bg=BG)
        top.pack(fill=tk.X, padx=20, pady=15)

        tk.Label(
            top, text="Период:",
            bg=BG, fg=DARK
        ).pack(side=tk.LEFT)

        self.report_period = ttk.Combobox(
            top,
            state="readonly",
            values=(
                "Сегодня",
                "7 дней",
                "30 дней",
                "Весь период"
            ),
            width=18
        )
        self.report_period.pack(side=tk.LEFT, padx=8)
        self.report_period.set("Сегодня")

        self.button(
            top, "📊 Сформировать",
            self.generate_report,
            BLUE, 18
        ).pack(side=tk.LEFT)

        self.button(
            top, "📄 CSV",
            self.export_csv,
            PURPLE, 14
        ).pack(side=tk.RIGHT)

        self.report_text = tk.Text(
            self.reports,
            bg=WHITE,
            fg=DARK,
            relief=tk.FLAT,
            font=("Arial", 12)
        )
        self.report_text.pack(
            fill=tk.BOTH, expand=True,
            padx=20, pady=(0, 20)
        )
        self.report_text.configure(state=tk.DISABLED)

    def report_start(self):
        period = self.report_period.get()

        if period == "Сегодня":
            start = datetime.now().replace(
                hour=0, minute=0, second=0, microsecond=0
            )
        elif period == "7 дней":
            start = datetime.now() - timedelta(days=7)
        elif period == "30 дней":
            start = datetime.now() - timedelta(days=30)
        else:
            return "0000-01-01 00:00:00"

        return start.strftime("%Y-%m-%d %H:%M:%S")


    def report_kpi(self, title, value, color):
        frame = tk.Frame(
            self.reports,
            bg=COLORS["white"],
            highlightbackground=COLORS["border"],
            highlightthickness=1,
        )
        frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=4, pady=4)

        tk.Label(
            frame, text=title,
            bg=COLORS["white"],
            fg=COLORS["gray"],
            font=("Arial", 9, "bold")
        ).pack(pady=(8, 2))

        label = tk.Label(
            frame, text=value,
            bg=COLORS["white"],
            fg=color,
            font=("Arial", 14, "bold")
        )
        label.pack(pady=(0, 8))
        return label

    def generate_report(self):
        start, end = self.report_range()
        if not start or not end:
            return

        revenue = self.db.conn.execute(
            """
            SELECT COALESCE(SUM(total),0) value
            FROM orders
            WHERE created_at >= ?
            """,
            (start,)
        ).fetchone()["value"]

        expenses = self.db.conn.execute(
            """
            SELECT COALESCE(SUM(amount),0) value
            FROM expenses
            WHERE created_at >= ?
            """,
            (start,)
        ).fetchone()["value"]

        orders = self.db.conn.execute(
            """
            SELECT COUNT(*) value
            FROM orders
            WHERE created_at >= ?
            """,
            (start,)
        ).fetchone()["value"]

        purchases = self.db.conn.execute(
            """
            SELECT COALESCE(SUM(total),0) value
            FROM purchases
            WHERE created_at >= ?
            """,
            (start,)
        ).fetchone()["value"]

        top = self.db.conn.execute(
            """
            SELECT
                oi.product_name,
                SUM(oi.quantity) quantity,
                SUM(oi.total) revenue
            FROM order_items oi
            JOIN orders o ON o.id=oi.order_id
            WHERE o.created_at >= ?
            GROUP BY oi.product_name
            ORDER BY revenue DESC
            LIMIT 10
            """,
            (start,)
        ).fetchall()

        text = [
            "📊 BUSINESS REPORT",
            "",
            f"Период: {self.report_period.get()}",
            "",
            f"Выручка: {self.money(revenue)}",
            f"Расходы: {self.money(expenses)}",
            f"Закупки: {self.money(purchases)}",
            f"Прибыль до закупок: {self.money(revenue - expenses)}",
            f"Заказов: {orders}",
            "",
            "🏆 ТОП ТОВАРОВ:"
        ]

        if top:
            for i, row in enumerate(top, 1):
                text.append(
                    f"{i}. {row['product_name']} — "
                    f"{row['quantity']} шт. — "
                    f"{self.money(row['revenue'])}"
                )
        else:
            text.append("Продаж за период нет.")

        self.report_text.configure(state=tk.NORMAL)
        self.report_text.delete("1.0", tk.END)
        self.report_text.insert(tk.END, "\n".join(text))
        self.report_text.configure(state=tk.DISABLED)

    # ---------------- RETURNS ----------------

    def build_returns(self):
        top = tk.Frame(self.returns, bg=BG)
        top.pack(fill=tk.X, padx=20, pady=12)

        tk.Label(
            top, text="Заказ:",
            bg=BG, fg=DARK
        ).pack(side=tk.LEFT)

        self.return_order = ttk.Combobox(
            top, state="readonly", width=30
        )
        self.return_order.pack(side=tk.LEFT, padx=8)

        self.button(
            top, "↩ Вернуть заказ",
            self.return_order_action,
            RED, 18
        ).pack(side=tk.LEFT)

        columns = (
            "id", "order", "product",
            "qty", "amount", "reason", "date"
        )

        self.return_table = ttk.Treeview(
            self.returns,
            columns=columns,
            show="headings"
        )

        for col, title, width in [
            ("id", "ID", 55),
            ("order", "Заказ", 70),
            ("product", "Товар", 230),
            ("qty", "Кол.", 70),
            ("amount", "Сумма", 120),
            ("reason", "Причина", 300),
            ("date", "Дата", 170)
        ]:
            self.return_table.heading(col, text=title)
            self.return_table.column(col, width=width)

        self.return_table.pack(
            fill=tk.BOTH, expand=True,
            padx=20, pady=(0, 20)
        )

    def return_order_action(self):
        value = self.return_order.get().strip()
        if not value:
            return

        order_id = int(value.split(" | ")[0])

        items = self.db.conn.execute(
            """
            SELECT *
            FROM order_items
            WHERE order_id=?
            """,
            (order_id,)
        ).fetchall()

        if not items:
            return

        reason = simpledialog.askstring(
            "Возврат",
            "Причина возврата:",
            parent=self.root
        )

        if reason is None:
            return

        try:
            for item in items:
                self.db.conn.execute(
                    """
                    UPDATE products
                    SET quantity=quantity+?
                    WHERE id=?
                    """,
                    (
                        item["quantity"],
                        item["product_id"]
                    )
                )

                self.db.conn.execute(
                    """
                    INSERT INTO returns(
                        order_id,product_id,product_name,
                        quantity,amount,reason,created_at,user
                    )
                    VALUES(?,?,?,?,?,?,?,?)
                    """,
                    (
                        order_id,
                        item["product_id"],
                        item["product_name"],
                        item["quantity"],
                        item["total"],
                        reason,
                        now(),
                        self.username
                    )
                )

            self.db.conn.commit()

        except sqlite3.Error as error:
            self.db.conn.rollback()
            messagebox.showerror(
                "Ошибка", str(error)
            )
            return

        messagebox.showinfo(
            "Готово",
            f"Заказ #{order_id} возвращён."
        )
        self.refresh_all()

    # ---------------- USERS ----------------

    def users_window(self):
        if self.role != "admin":
            return

        win = tk.Toplevel(self.root)
        win.title("Сотрудники")
        win.geometry("650x520")
        win.configure(bg=BG)

        columns = ("id", "username", "role")
        table = ttk.Treeview(
            win, columns=columns, show="headings"
        )

        for col, title, width in [
            ("id", "ID", 60),
            ("username", "Логин", 240),
            ("role", "Роль", 180)
        ]:
            table.heading(col, text=title)
            table.column(col, width=width)

        table.pack(
            fill=tk.BOTH, expand=True,
            padx=20, pady=20
        )

        def refresh():
            self.clear(table)
            rows = self.db.conn.execute(
                "SELECT id,username,role FROM users ORDER BY id"
            ).fetchall()

            for row in rows:
                table.insert(
                    "", tk.END,
                    values=(
                        row["id"],
                        row["username"],
                        row["role"]
                    )
                )

        def add_user():
            dialog = tk.Toplevel(win)
            dialog.title("Новый сотрудник")
            dialog.geometry("390x330")
            dialog.configure(bg=WHITE)
            dialog.grab_set()

            form = tk.Frame(dialog, bg=WHITE)
            form.pack(fill=tk.X, padx=40, pady=25)

            labels = [
                "Логин",
                "Пароль"
            ]
            entries = []

            for title in labels:
                tk.Label(
                    form, text=title,
                    bg=WHITE, fg=GRAY
                ).pack(anchor="w")

                e = tk.Entry(
                    form,
                    show="•" if title == "Пароль" else ""
                )
                e.pack(fill=tk.X, pady=(3, 12))
                entries.append(e)

            tk.Label(
                form, text="Роль",
                bg=WHITE, fg=GRAY
            ).pack(anchor="w")

            role_box = ttk.Combobox(
                form,
                state="readonly",
                values=("manager", "cashier")
            )
            role_box.pack(fill=tk.X, pady=3)
            role_box.set("cashier")

            def save():
                username = entries[0].get().strip()
                password = entries[1].get()

                if not username or not password:
                    messagebox.showwarning(
                        "Ошибка",
                        "Заполните все поля.",
                        parent=dialog
                    )
                    return

                try:
                    self.db.conn.execute(
                        """
                        INSERT INTO users(
                            username,password_hash,role
                        )
                        VALUES(?,?,?)
                        """,
                        (
                            username,
                            password_hash(password),
                            role_box.get()
                        )
                    )
                    self.db.conn.commit()
                except sqlite3.IntegrityError:
                    messagebox.showerror(
                        "Ошибка",
                        "Такой логин уже существует.",
                        parent=dialog
                    )
                    return

                dialog.destroy()
                refresh()

            self.button(
                dialog, "💾 Создать",
                save, GREEN, 20
            ).pack()

        self.button(
            win, "➕ Добавить сотрудника",
            add_user, GREEN, 20
        ).pack(pady=(0, 20))

        refresh()

    # ---------------- DASHBOARD ----------------

    def build_dashboard(self):
        top = tk.Frame(self.dashboard, bg=BG)
        top.pack(fill=tk.X, padx=20, pady=12)

        tk.Label(
            top,
            text="📈 Продажи по дням",
            bg=BG,
            fg=DARK,
            font=("Arial", 18, "bold")
        ).pack(side=tk.LEFT)

        self.button(
            top, "🔄 Обновить",
            self.refresh_dashboard_chart,
            BLUE, 15
        ).pack(side=tk.RIGHT)

        self.chart_canvas = tk.Canvas(
            self.dashboard,
            bg=WHITE,
            highlightthickness=0
        )
        self.chart_canvas.pack(
            fill=tk.BOTH,
            expand=True,
            padx=20,
            pady=(0, 20)
        )
        self.chart_canvas.bind(
            "<Configure>",
            lambda e: self.refresh_dashboard_chart()
        )

    def refresh_dashboard_chart(self):
        if not hasattr(self, "chart_canvas"):
            return

        self.chart_canvas.delete("all")

        width = max(self.chart_canvas.winfo_width(), 700)
        height = max(self.chart_canvas.winfo_height(), 400)

        start = datetime.now() - timedelta(days=6)
        data = []

        for i in range(7):
            day = start + timedelta(days=i)
            day_start = day.strftime("%Y-%m-%d 00:00:00")
            day_end = (day + timedelta(days=1)).strftime("%Y-%m-%d 00:00:00")

            value = self.db.conn.execute(
                """
                SELECT COALESCE(SUM(total),0) v
                FROM orders
                WHERE created_at >= ? AND created_at < ?
                """,
                (day_start, day_end)
            ).fetchone()["v"]

            data.append((day.strftime("%d.%m"), float(value)))

        left = 65
        right = width - 30
        top = 40
        bottom = height - 65

        self.chart_canvas.create_text(
            left, 18,
            text="Выручка, " + self.db.get("currency", "руб."),
            anchor="w",
            fill=DARK,
            font=("Arial", 11, "bold")
        )

        max_value = max([v for _, v in data] + [1])

        self.chart_canvas.create_line(
            left, bottom, right, bottom,
            fill="#9ca3af"
        )
        self.chart_canvas.create_line(
            left, top, left, bottom,
            fill="#9ca3af"
        )

        bar_space = (right - left) / len(data)
        bar_width = bar_space * 0.55

        for i, (label, value) in enumerate(data):
            x_center = left + bar_space * i + bar_space / 2
            bar_height = (bottom - top) * value / max_value
            y1 = bottom - bar_height

            self.chart_canvas.create_rectangle(
                x_center - bar_width / 2,
                y1,
                x_center + bar_width / 2,
                bottom,
                fill=BLUE,
                outline=BLUE
            )

            self.chart_canvas.create_text(
                x_center,
                bottom + 18,
                text=label,
                fill=GRAY,
                font=("Arial", 9)
            )

            self.chart_canvas.create_text(
                x_center,
                y1 - 10,
                text=f"{value:,.0f}",
                fill=DARK,
                font=("Arial", 9, "bold")
            )

    # ---------------- AUDIT LOG ----------------

    def build_logs(self):
        if self.role != "admin":
            return

        top = tk.Frame(self.logs, bg=BG)
        top.pack(fill=tk.X, padx=20, pady=12)

        self.button(
            top, "🔄 Обновить",
            self.refresh_logs,
            BLUE, 15
        ).pack(side=tk.RIGHT)

        columns = ("id", "user", "action", "details", "date")
        self.log_table = ttk.Treeview(
            self.logs,
            columns=columns,
            show="headings"
        )

        for col, title, width in [
            ("id", "ID", 55),
            ("user", "Пользователь", 150),
            ("action", "Действие", 180),
            ("details", "Подробности", 500),
            ("date", "Дата", 170)
        ]:
            self.log_table.heading(col, text=title)
            self.log_table.column(col, width=width)

        self.log_table.pack(
            fill=tk.BOTH,
            expand=True,
            padx=20,
            pady=(0, 20)
        )

    def refresh_logs(self):
        if self.role != "admin" or not hasattr(self, "log_table"):
            return

        self.clear(self.log_table)

        rows = self.db.conn.execute(
            """
            SELECT *
            FROM audit_log
            ORDER BY id DESC
            LIMIT 500
            """
        ).fetchall()

        for row in rows:
            self.log_table.insert(
                "",
                tk.END,
                values=(
                    row["id"],
                    row["username"],
                    row["action"],
                    row["details"],
                    display_date(row["created_at"])
                )
            )

    # ---------------- RECEIPT ----------------

    def show_receipt(self, order_id):
        order = self.db.conn.execute(
            "SELECT * FROM orders WHERE id=?",
            (order_id,)
        ).fetchone()

        items = self.db.conn.execute(
            """
            SELECT *
            FROM order_items
            WHERE order_id=?
            """,
            (order_id,)
        ).fetchall()

        win = tk.Toplevel(self.root)
        win.title(f"Чек #{order_id}")
        win.geometry("520x650")
        win.configure(bg=WHITE)

        text = tk.Text(
            win,
            bg=WHITE,
            fg=DARK,
            font=("Courier New", 10),
            relief=tk.FLAT
        )
        text.pack(
            fill=tk.BOTH,
            expand=True,
            padx=20, pady=20
        )

        lines = [
            self.db.get(
                "shop_name",
                "Business Assistant PRO"
            ).center(44),
            "КАССОВЫЙ ЧЕК".center(44),
            "-" * 44,
            f"Заказ: #{order_id}",
            f"Дата: {display_date(order['created_at'])}",
            f"Кассир: {order['cashier']}",
            "-" * 44
        ]

        for item in items:
            lines.append(
                f"{item['product_name'][:20]:20} "
                f"{item['quantity']:>3} x "
                f"{item['price']:>8.2f} = "
                f"{item['total']:>9.2f}"
            )

        lines.extend([
            "-" * 44,
            f"Подытог: {self.money(order['subtotal'])}",
            f"Скидка: {self.money(order['discount'])}",
            f"ИТОГО: {self.money(order['total'])}",
            f"Оплата: {order['payment']}",
            "-" * 44,
            "Спасибо за покупку!"
        ])

        text.insert("1.0", "\n".join(lines))
        text.configure(state=tk.DISABLED)

        self.button(
            win, "Закрыть",
            win.destroy, GRAY, 16
        ).pack(pady=(0, 20))

    # ---------------- SETTINGS ----------------

    def settings(self):
        win = tk.Toplevel(self.root)
        win.title("Настройки")
        win.geometry("500x600")
        win.configure(bg=WHITE)
        win.grab_set()

        tk.Label(
            win, text="⚙ Настройки магазина",
            bg=WHITE, fg=DARK,
            font=("Arial", 21, "bold")
        ).pack(pady=25)

        form = tk.Frame(win, bg=WHITE)
        form.pack(fill=tk.X, padx=50)

        fields = {}

        for key, label in [
            ("shop_name", "Название"),
            ("phone", "Телефон"),
            ("address", "Адрес"),
            ("currency", "Валюта")
        ]:
            tk.Label(
                form, text=label,
                bg=WHITE, fg=GRAY
            ).pack(anchor="w")

            entry = tk.Entry(form)
            entry.pack(fill=tk.X, pady=(3, 14))
            entry.insert(0, self.db.get(key))
            fields[key] = entry

        tk.Label(
            form, text="Новый пароль текущего пользователя",
            bg=WHITE, fg=GRAY
        ).pack(anchor="w")

        password = tk.Entry(
            form, show="•"
        )
        password.pack(fill=tk.X, pady=(3, 20))

        def save():
            for key, entry in fields.items():
                value = entry.get().strip()

                if key == "shop_name" and not value:
                    value = "Business Assistant PRO"

                if key == "currency" and not value:
                    value = "руб."

                self.db.set(key, value)

            if password.get():
                self.db.conn.execute(
                    """
                    UPDATE users
                    SET password_hash=?
                    WHERE username=?
                    """,
                    (
                        password_hash(password.get()),
                        self.username
                    )
                )
                self.db.conn.commit()

            win.destroy()
            self.refresh_all()

        self.button(
            win, "💾 Сохранить",
            save, GREEN, 25
        ).pack(pady=(0, 8))

        self.button(
            win, "🔑 Лицензия",
            self.license_window,
            PURPLE, 25
        ).pack()

    # ---------------- LICENSE ----------------

    def license_window(self):
        win = tk.Toplevel(self.root)
        win.title("Лицензия")
        win.geometry("480x350")
        win.configure(bg=WHITE)
        win.grab_set()

        tk.Label(
            win,
            text="🔑 Лицензия программы",
            bg=WHITE,
            fg=DARK,
            font=("Arial", 20, "bold")
        ).pack(pady=25)

        current = self.db.conn.execute(
            "SELECT license_key, activated_at FROM licenses WHERE id=1"
        ).fetchone()

        status = (
            "Лицензия активна"
            if current
            else
            "Демо-режим"
        )

        tk.Label(
            win,
            text=status,
            bg=WHITE,
            fg=GREEN if current else ORANGE,
            font=("Arial", 12, "bold")
        ).pack(pady=5)

        key_entry = tk.Entry(win, width=35)
        key_entry.pack(pady=15)

        def activate():
            key = key_entry.get().strip()

            if not key:
                messagebox.showwarning(
                    "Лицензия",
                    "Введите лицензионный ключ.",
                    parent=win
                )
                return

            # Для серверной коммерческой версии эту проверку можно заменить
            # на серверную активацию.
            if len(key) < 8:
                messagebox.showerror(
                    "Лицензия",
                    "Ключ слишком короткий.",
                    parent=win
                )
                return

            self.db.conn.execute(
                """
                INSERT INTO licenses(id,license_key,activated_at)
                VALUES(1,?,?)
                ON CONFLICT(id) DO UPDATE SET
                    license_key=excluded.license_key,
                    activated_at=excluded.activated_at
                """,
                (key, now())
            )
            self.db.conn.commit()
            self.db.log(
                self.username,
                "Лицензия",
                "Лицензионный ключ активирован"
            )

            messagebox.showinfo(
                "Лицензия",
                "Лицензия сохранена.",
                parent=win
            )
            win.destroy()

        self.button(
            win,
            "🔓 Активировать",
            activate,
            GREEN,
            22
        ).pack(pady=5)

        self.button(
            win,
            "Закрыть",
            win.destroy,
            GRAY,
            15
        ).pack(pady=5)

    # ---------------- REFRESH ----------------

    def refresh_all(self):
        self.refresh_header()
        self.refresh_dashboard()
        self.refresh_products()
        self.refresh_clients()
        self.refresh_purchases()
        self.refresh_expenses()
        self.refresh_history()
        self.refresh_return_choices()
        self.refresh_returns()
        self.refresh_sale_choices()
        self.refresh_cart()
        self.generate_report()
        self.refresh_dashboard_chart()
        self.refresh_logs()

    def refresh_header(self):
        self.shop_title.config(
            text="💼 " + self.db.get(
                "shop_name",
                "Business Assistant PRO"
            )
        )

    def refresh_dashboard(self):
        revenue = self.db.conn.execute(
            "SELECT COALESCE(SUM(total),0) v FROM orders"
        ).fetchone()["v"]

        expenses = self.db.conn.execute(
            "SELECT COALESCE(SUM(amount),0) v FROM expenses"
        ).fetchone()["v"]

        products = self.db.conn.execute(
            "SELECT COUNT(*) v FROM products"
        ).fetchone()["v"]

        low = self.db.conn.execute(
            """
            SELECT COUNT(*) v
            FROM products
            WHERE quantity <= min_quantity
            """
        ).fetchone()["v"]

        self.card_revenue.config(
            text=self.money(revenue)
        )
        self.card_expenses.config(
            text=self.money(expenses)
        )
        self.card_profit.config(
            text=self.money(revenue - expenses)
        )
        self.card_stock.config(
            text=str(products)
        )
        self.card_low.config(
            text=str(low)
        )

        self.home_info.config(
            text=(
                f"Пользователь: {self.username} ({self.role})\n"
                f"Выручка: {self.money(revenue)}\n"
                f"Расходы: {self.money(expenses)}\n"
                f"Прибыль: {self.money(revenue - expenses)}"
            )
        )

        rows = self.db.conn.execute(
            """
            SELECT name,quantity,min_quantity
            FROM products
            WHERE quantity <= min_quantity
            ORDER BY quantity
            """
        ).fetchall()

        self.alert.configure(state=tk.NORMAL)
        self.alert.delete("1.0", tk.END)

        if not rows:
            self.alert.insert(
                tk.END,
                "✅ Все основные товары в наличии."
            )
        else:
            for row in rows:
                self.alert.insert(
                    tk.END,
                    f"⚠ {row['name']} — "
                    f"{row['quantity']} шт. "
                    f"(минимум {row['min_quantity']})\n"
                )

        self.alert.configure(state=tk.DISABLED)

    def refresh_products(self):
        self.clear(self.product_table)

        search = (
            self.product_search.get()
            .strip()
            .lower()
        )

        rows = self.db.conn.execute(
            "SELECT * FROM products ORDER BY name"
        ).fetchall()

        for row in rows:
            combined = (
                f"{row['name']} "
                f"{row['barcode'] or ''} "
                f"{row['category']}"
            ).lower()

            if search and search not in combined:
                continue

            if row["quantity"] == 0:
                status = "Нет"
                tag = "empty"
            elif row["quantity"] <= row["min_quantity"]:
                status = "Мало"
                tag = "low"
            else:
                status = "В наличии"
                tag = ""

            self.product_table.insert(
                "", tk.END,
                values=(
                    row["id"],
                    row["name"],
                    row["barcode"] or "",
                    row["category"],
                    self.money(row["price"]),
                    self.money(row["cost"]),
                    row["quantity"],
                    status
                ),
                tags=(tag,)
            )

    def refresh_clients(self):
        self.clear(self.client_table)

        rows = self.db.conn.execute(
            "SELECT * FROM clients ORDER BY name"
        ).fetchall()

        self.sale_client["values"] = [
            row["name"] for row in rows
        ]

        for row in rows:
            self.client_table.insert(
                "", tk.END,
                values=(
                    row["id"],
                    row["name"],
                    row["phone"],
                    row["note"]
                )
            )

    def refresh_purchases(self):
        self.clear(self.purchase_table)

        rows = self.db.conn.execute(
            """
            SELECT
                purchases.*,
                products.name product
            FROM purchases
            JOIN products
                ON products.id=purchases.product_id
            ORDER BY purchases.id DESC
            """
        ).fetchall()

        for row in rows:
            self.purchase_table.insert(
                "", tk.END,
                values=(
                    row["id"],
                    display_date(row["created_at"]),
                    row["product"],
                    row["quantity"],
                    self.money(row["cost"]),
                    self.money(row["total"]),
                    row["user"]
                )
            )

    def refresh_expenses(self):
        self.clear(self.expense_table)

        rows = self.db.conn.execute(
            """
            SELECT *
            FROM expenses
            ORDER BY id DESC
            """
        ).fetchall()

        for row in rows:
            self.expense_table.insert(
                "", tk.END,
                values=(
                    row["id"],
                    display_date(row["created_at"]),
                    row["description"],
                    self.money(row["amount"])
                )
            )

    def refresh_history(self):
        self.clear(self.history_table)

        rows = self.db.conn.execute(
            """
            SELECT *
            FROM orders
            ORDER BY id DESC
            """
        ).fetchall()

        for row in rows:
            self.history_table.insert(
                "", tk.END,
                values=(
                    row["id"],
                    display_date(row["created_at"]),
                    row["client_name"],
                    row["payment"],
                    self.money(row["subtotal"]),
                    self.money(row["discount"]),
                    self.money(row["total"]),
                    row["cashier"]
                )
            )

    def refresh_sale_choices(self):
        names = [
            row["name"]
            for row in self.db.conn.execute(
                """
                SELECT name
                FROM products
                WHERE quantity > 0
                ORDER BY name
                """
            ).fetchall()
        ]

        self.sale_product["values"] = names

    def refresh_return_choices(self):
        rows = self.db.conn.execute(
            """
            SELECT id
            FROM orders
            ORDER BY id DESC
            """
        ).fetchall()

        self.return_order["values"] = [
            f"{row['id']} | заказ"
            for row in rows
        ]

    def refresh_returns(self):
        self.clear(self.return_table)

        rows = self.db.conn.execute(
            """
            SELECT *
            FROM returns
            ORDER BY id DESC
            """
        ).fetchall()

        for row in rows:
            self.return_table.insert(
                "", tk.END,
                values=(
                    row["id"],
                    row["order_id"],
                    row["product_name"],
                    row["quantity"],
                    self.money(row["amount"]),
                    row["reason"],
                    display_date(row["created_at"])
                )
            )

    # ---------------- CSV ----------------

    def export_csv(self):
        rows = self.db.conn.execute(
            """
            SELECT
                id,client_name,payment,
                subtotal,discount,total,
                created_at,cashier
            FROM orders
            ORDER BY id DESC
            """
        ).fetchall()

        if not rows:
            messagebox.showinfo(
                "CSV", "Продаж пока нет."
            )
            return

        path = filedialog.asksaveasfilename(
            title="Экспорт заказов",
            defaultextension=".csv",
            filetypes=[("CSV", "*.csv")],
            initialfile="business_report.csv"
        )

        if not path:
            return

        with open(
            path,
            "w",
            newline="",
            encoding="utf-8-sig"
        ) as file:
            writer = csv.writer(file)

            writer.writerow([
                "Заказ", "Клиент", "Оплата",
                "Подытог", "Скидка", "Итого",
                "Дата", "Кассир"
            ])

            for row in rows:
                writer.writerow([
                    row["id"],
                    row["client_name"],
                    row["payment"],
                    row["subtotal"],
                    row["discount"],
                    row["total"],
                    row["created_at"],
                    row["cashier"]
                ])

        messagebox.showinfo(
            "Готово",
            f"CSV сохранён:\n{path}"
        )

    # ---------------- BACKUP ----------------

    def backup(self):
        path = filedialog.asksaveasfilename(
            title="Backup базы",
            defaultextension=".db",
            filetypes=[("SQLite DB", "*.db")],
            initialfile="business_backup.db"
        )

        if not path:
            return

        self.db.conn.commit()

        try:
            shutil.copy2(
                self.db.filename,
                path
            )
            messagebox.showinfo(
                "Backup",
                f"Копия сохранена:\n{path}"
            )
        except OSError as error:
            messagebox.showerror(
                "Ошибка", str(error)
            )

    def close(self):
        self.db.close()
        self.root.destroy()


def main():
    root = tk.Tk()
    App(root)
    root.mainloop()


if __name__ == "__main__":
    main()