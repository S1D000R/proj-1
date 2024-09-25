import sys
import os
import csv
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import QPixmap, QAction

APP_STYLE = """
QMainWindow {
    background-color: #f0f0f0;
}

QLabel, QMenuBar, QTextEdit, QListWidget, QComboBox, QLineEdit{
    font-size: 14pt;
}
QComboBox, QLineEdit {
    border: 1px solid #cccccc;
    border-radius: 4px;
    padding: 1px 18px 1px 3px;
    min-height: 27px;
}

QComboBox:focus, QLineEdit:focus {

    border-color: #88aaff;
}
QComboBox {
    margin-bottom: 3px;
}

QComboBox::drop-down {
    width: 15px;
    border-left-width: 1px;
    border-left-color: darkgray;
    border-left-style: solid; 
    border-top-right-radius: 3px; 
    border-bottom-right-radius: 3px;
}
QLineEdit:focus {
    border-color: #88aaff;
}

QListWidget {
    border: none;
    padding: 10px;
    background: #FFFFFF;
}

QListWidget::item {
    border-bottom: 1px solid #eeeeee;
    padding: 5px;
    margin: 0;

}

QListWidget::item:selected {
    background-color: #CCEEEE;
    color: black;
}

QTextEdit {
    background: #FFFFFF;
    border: 1px solid #cccccc;
    padding: 5px;
    margin-top: 10px;
}

QMenuBar {
    background: #FFFFFF;
}

QMenuBar::item {
    background: transparent;
    padding: 5px 10px;
}

QMenuBar::item:selected {
    background: #eeeeee;
}
"""


class RecipeCreationDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setWindowTitle("Новый рецепт")
        self.recipe_image_path = ""
        available_categories = ["Итальянская кухня", "Французская кухня", "Грузинская кухня", "Китайская кухня",
                                "Японская кухня", "Русская кухня", "Индийская кухня"]
        self.setMinimumSize(1000, 600)
        self.setStyleSheet("""
            QDialog {
                background-color: #ffffff; 
            }
            QLabel {
                font-size: 14pt; 
                margin-bottom: 5px; 
            }
            QLineEdit, QTextEdit, QComboBox {
                padding: 5px;
                margin-bottom: 2px; 
                border: 1px solid #ddd; 
                border-radius: 4px; 
            }
            QPushButton {
                padding: 5px 15px; 
                background-color: #5cb85c; 
                border: none; 
                color: white; 
                border-radius: 4px; 
                height:33px;
                font-size:20px;
            }
            QPushButton:hover {
                background-color: #4cae4c; 
            }
        """)

        layout = QVBoxLayout(self)

        form_layout = QFormLayout()
        self.name_edit = QLineEdit()
        self.summary_edit = QTextEdit()
        self.ingredients_edit = QTextEdit()
        self.instructions_edit = QTextEdit()
        self.category_combobox = QComboBox()

        self.image_label = QLabel()
        self.image_label.setFixedSize(250, 168)
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_label.setText("Нет изображения")
        self.image_label.setStyleSheet("border: 1px solid #ddd; background-color: #f0f0f0;")

        if available_categories is not None:
            self.category_combobox.addItems(available_categories)
        else:
            self.category_combobox.addItems(["Без категории"])

        form_layout.addRow("Название:", self.name_edit)
        form_layout.addRow("Краткое описание:", self.summary_edit)
        form_layout.addRow("Категория:", self.category_combobox)
        form_layout.addRow("Ингредиенты:", self.ingredients_edit)
        form_layout.addRow("Инструкции:", self.instructions_edit)
        form_layout.addRow("Изображение:", self.image_label)

        layout.addLayout(form_layout)


        buttons_layout = QHBoxLayout()
        self.save_button = QPushButton("Сохранить")
        self.cancel_button = QPushButton("Отмена")
        self.add_image_button = QPushButton("Добавить изображение")

        spacer_left = QSpacerItem(40, 20)
        spacer_right = QSpacerItem(40, 20)

        buttons_layout.addItem(spacer_left)
        buttons_layout.addWidget(self.add_image_button)
        buttons_layout.addWidget(self.save_button)
        buttons_layout.addWidget(self.cancel_button)
        buttons_layout.addItem(spacer_right)

        layout.addLayout(buttons_layout)

        self.save_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)
        self.add_image_button.clicked.connect(self.add_image)

        buttons_layout.addWidget(self.add_image_button)
        buttons_layout.addWidget(self.save_button)
        buttons_layout.addWidget(self.cancel_button)

        layout.addLayout(buttons_layout)
    def add_image(self):
        options = QFileDialog
        filename, _ = QFileDialog.getOpenFileName(self, "Выберите изображение", "",
                                                  "Image Files (*.png *.jpg *.jpeg *.bmp)")
        if filename:
            self.recipe_image_path = filename
            pixmap = QPixmap(self.recipe_image_path)
            self.image_label.setPixmap(pixmap.scaled(250, 168, Qt.AspectRatioMode.KeepAspectRatio))

    def get_data(self):
        return {
            "name": self.name_edit.text(),
            "summary": self.summary_edit.toPlainText(),
            "category": self.category_combobox.currentText(),
            "ingredients": self.ingredients_edit.toPlainText(),
            "instructions": self.instructions_edit.toPlainText(),
            "image_path": self.recipe_image_path
        }


class Recipe:
    def __init__(self, name, summary, category, image_path, ingredients=None, instructions=None):
        self.name = name
        self.summary = summary
        self.image_path = image_path
        self.category = category
        self.ingredients = ingredients or "Ингредиенты отсутствуют"
        self.instructions = instructions or "Инструкция отсутствует"


class RecipeDetailWindow(QDialog):
    def __init__(self, recipe, parent=None):
        super().__init__(parent)
        self.recipe = recipe
        self.initUI()

    def initUI(self):
        self.setWindowTitle(f"Рецепт: {self.recipe.name}")
        self.setGeometry(200, 100, 800, 900)
        self.setStyleSheet("""
                    QDialog {
                        background-color: #ffffff;
                    }
                    QLabel {
                        font-size: 12pt;
                        padding: 10px;
                    }
                    QScrollArea {
                        border: 1px solid #cccccc;
                    }
                """)
        layout = QVBoxLayout()
        name_label = QLabel(f"<h1>{self.recipe.name}</h1>")
        name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(name_label)
        name_label.setStyleSheet("""
        font-family:'Montserrat';
        """)
        self.image_label = QLabel()
        image_pixmap = QPixmap(self.recipe.image_path)
        self.image_label.setPixmap(image_pixmap.scaled(400, 300, Qt.AspectRatioMode.KeepAspectRatio))
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.image_label)

        # Список ингредиентов
        self.ingredients_label = QLabel(self.recipe.ingredients)
        self.ingredients_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        self.ingredients_label.setWordWrap(True)

        ingredients_scroll_area = QScrollArea()
        ingredients_scroll_area.setWidgetResizable(True)
        ingredients_scroll_area.setWidget(self.ingredients_label)
        layout.addWidget(ingredients_scroll_area)

        # Инструкции по приготовлению
        self.instructions_label = QLabel(self.recipe.instructions)
        self.instructions_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        self.instructions_label.setWordWrap(True)
        self.instructions_label.setStyleSheet("""
            QLabel {
                background-color: #f0f0f0;
                margin: 5px;
                padding:10px;
                border-radius: 2px;
            }""")

        instructions_scroll_area = QScrollArea()
        instructions_scroll_area.setWidgetResizable(True)
        instructions_scroll_area.setWidget(self.instructions_label)
        layout.addWidget(instructions_scroll_area)

        self.setLayout(layout)


class RecipeListItem(QWidget):
    def __init__(self, recipe, parent=None):
        super().__init__(parent)
        self.recipe = recipe
        layout = QHBoxLayout(self)
        layout.setSpacing(5)
        if recipe.image_path:
            image_label = QLabel()
            pixmap = QPixmap(recipe.image_path)
            image_label.setPixmap(pixmap.scaled(270, 270, Qt.AspectRatioMode.KeepAspectRatio))
            layout.addWidget(image_label)

        text_layout = QVBoxLayout()
        text_layout.setSpacing(2)
        text_layout.setContentsMargins(1, 0, 0, 0)
        self.name_label = QLabel(f"<b>{recipe.name}</b>")
        text_layout.addWidget(self.name_label)

        summary_label = QLabel(recipe.summary)
        summary_label.setWordWrap(True)
        text_layout.addWidget(summary_label)

        layout.addLayout(text_layout)
        self.setLayout(layout)

    def sizeHint(self):
        return QSize(300, 160)



class RecipesApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.addrecipes = []
        self.headers = ["name", "summary", "image_path", "category", "ingredients", "instructions"]
        self.recipes = []
        self.load_recipes_from_csv("recipes.csv")
        self.initUI()

    def load_recipes_from_csv(self, filepath):
        image_dir = os.path.join(os.getcwd(), 'Image')
        with open(filepath, encoding='utf-8') as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                # Обновляем путь к изображению, чтобы он был абсолютным
                image_path = os.path.join(image_dir, row["image_path"])
                self.recipes.append(
                    Recipe(
                        name=row["name"],
                        summary=row["summary"],
                        category=row["category"],
                        image_path=image_path,
                        ingredients=row["ingredients"],
                        instructions=row["instructions"]
                    )
                )

    def initUI(self):
        self.setWindowTitle('Рецепты')
        self.setMinimumSize(QSize(1480, 850))
        self.setStyleSheet(APP_STYLE)

        self.central_widget = QWidget()
        self.main_layout = QVBoxLayout(self.central_widget)
        self.top_layout = QHBoxLayout()

        self.search_line_edit = QLineEdit()
        self.search_line_edit.setPlaceholderText("Поиск блюда...")
        self.search_line_edit.textChanged.connect(self.filter_recipes)
        self.top_layout.addWidget(self.search_line_edit)

        self.current_category = "Все категории"
        self.category_combobox = QComboBox()
        self.category_combobox.addItem("Все категории")
        self.category_combobox.addItems(set(recipe.category for recipe in self.recipes))
        self.category_combobox.currentTextChanged.connect(self.update_recipe_list)

        self.top_layout.addWidget(self.category_combobox)

        self.main_layout.addLayout(self.top_layout)

        self.content_layout = QHBoxLayout()
        self.recipes_list_widget = QListWidget()
        self.content_layout.addWidget(self.recipes_list_widget)

        self.details_layout = QVBoxLayout()
        self.recipe_image_label = QLabel()
        self.recipe_image_label.setFixedSize(700, 400)
        self.recipe_detail_textedit = QTextEdit()
        self.recipe_detail_textedit.setReadOnly(True)
        self.details_layout.addWidget(self.recipe_image_label)
        self.details_layout.addWidget(self.recipe_detail_textedit)
        self.content_layout.addLayout(self.details_layout)

        self.main_layout.addLayout(self.content_layout)

        self.setCentralWidget(self.central_widget)

        self.create_menu()
        self.recipes_list_widget.currentRowChanged.connect(self.display_recipe_details)
        self.recipes_list_widget.itemDoubleClicked.connect(self.open_recipe_detail)

        for recipe in self.recipes:
            item_widget = RecipeListItem(recipe)
            item = QListWidgetItem(self.recipes_list_widget)
            item.setSizeHint(item_widget.sizeHint())
            self.recipes_list_widget.addItem(item)
            self.recipes_list_widget.setItemWidget(item, item_widget)

    def update_recipe_list(self, category):
        self.current_category = category
        self.filter_recipes(self.search_line_edit.text())
        self.recipes_list_widget.clear()
        for recipe in self.recipes:
            if self.current_category == "Все категории" or recipe.category == self.current_category:
                item_widget = RecipeListItem(recipe)
                item = QListWidgetItem(self.recipes_list_widget)
                item.setSizeHint(item_widget.sizeHint())
                self.recipes_list_widget.addItem(item)
                self.recipes_list_widget.setItemWidget(item, item_widget)

    def filter_recipes(self, text):
        self.recipes_list_widget.clear()
        for recipe in self.recipes:
            if text.lower() in recipe.name.lower() and (
                    self.current_category == "Все категории" or recipe.category == self.current_category):
                item_widget = RecipeListItem(recipe)
                item = QListWidgetItem(self.recipes_list_widget)
                item.setSizeHint(item_widget.sizeHint())
                self.recipes_list_widget.addItem(item)
                self.recipes_list_widget.setItemWidget(item, item_widget)
    def create_menu(self):
        main_menu = self.menuBar()
        file_menu = main_menu.addMenu('Рецепты')

        action_add_recipe = QAction('Добавить новый рецепт', self)
        action_add_recipe.triggered.connect(self.show_add_recipe_dialog)
        file_menu.addAction(action_add_recipe)

    def show_add_recipe_dialog(self):
        dialog = RecipeCreationDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            new_recipe_data = dialog.get_data()
            # Проверка, существует ли уже рецепт с таким именем
            if any(recipe.name == new_recipe_data["name"] for recipe in self.recipes):
                QMessageBox.warning(self, "Ошибка", f"Рецепт с именем '{new_recipe_data['name']}' уже существует.")
            else:
                # Проверка, заполнены ли обязательные поля
                if not all([new_recipe_data["name"], new_recipe_data["summary"],
                            new_recipe_data["category"], new_recipe_data["ingredients"],
                            new_recipe_data["instructions"]]):
                    QMessageBox.warning(self, "Ошибка", "Заполните все поля!")
                else:
                    new_recipe = Recipe(new_recipe_data["name"], new_recipe_data["summary"],
                                        new_recipe_data["category"], new_recipe_data["image_path"],
                                        new_recipe_data["ingredients"],
                                        new_recipe_data["instructions"])
                    self.recipes.append(new_recipe)
                    self.append_recipe_to_csv(new_recipe_data)

        self.recipes_list_widget.clear()

        for recipe in self.recipes:
            item_widget = RecipeListItem(recipe)
            item = QListWidgetItem(self.recipes_list_widget)
            item.setSizeHint(item_widget.sizeHint())
            self.recipes_list_widget.addItem(item)
            self.recipes_list_widget.setItemWidget(item, item_widget)

    def append_recipe_to_csv(self, new_recipe, storage_filename="recipes.csv"):
        with open(storage_filename, 'a', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=self.headers)
            if file.tell() == 0:
                writer.writeheader()
            writer.writerow(new_recipe)

    def set_recipe_image(self, image_path):
        if os.path.exists(image_path) and image_path:
            pixmap = QPixmap(image_path)
            scaled_pixmap = pixmap.scaled(
                self.recipe_image_label.width(),
                self.recipe_image_label.height(),
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
            self.recipe_image_label.setPixmap(scaled_pixmap)
            self.recipe_image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        else:
            self.recipe_image_label.clear()
            self.recipe_image_label.setText("Изображение недоступно")
            self.recipe_image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def display_recipe_details(self, current_index):
        current_item = self.recipes_list_widget.item(current_index)
        item_widget = self.recipes_list_widget.itemWidget(current_item)
        if hasattr(item_widget, 'recipe'):
            recipe = item_widget.recipe
            self.recipe_detail_textedit.setHtml(
                f"<h1>{recipe.name}</h1><p><b>Описание:</b><br>{recipe.summary}</p>"
                f"<p><b>Ингредиенты:</b><br>{recipe.ingredients}</p>"
            )
            self.set_recipe_image(recipe.image_path)
        else:
            self.recipe_detail_textedit.clear()
            self.set_recipe_image("")

    def open_recipe_detail(self, item):
        selected_item = self.recipes_list_widget.currentItem()
        item_widget = self.recipes_list_widget.itemWidget(selected_item)
        if hasattr(item_widget, 'recipe'):
            recipe_name = item_widget.recipe.name
        recipe = next((r for r in self.recipes if r.name == recipe_name), None)
        if recipe:
            self.detail_window = RecipeDetailWindow(recipe, self)
            self.detail_window.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_win = RecipesApp()
    main_win.show()
    sys.exit(app.exec())
