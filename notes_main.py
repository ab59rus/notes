#подключение библиотек
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication, 
    QWidget, 
    QPushButton, 
    QLabel, 
    QVBoxLayout, 
    QHBoxLayout, 
    QListWidget,
    QLineEdit,
    QTextEdit,
    QInputDialog, 
    QMessageBox)
import json

'''notes = {
    "Добро пожаловать!" : {
        "текст" : "Это самое лучшее приложение для заметок в мире!",
        "теги" : ["добро", "инструкция"]
    }
}
with open("notes_data.json", "w", encoding = 'utf-8') as file:
    json.dump(notes, file)'''

def show_note():
    #получаем текст из заметки с выделенным названием и отображаем его в поле редактирования
    key = list_notes.selectedItems()[0].text()
    field_text.setText(notes[key]["текст"])
    list_tags.clear()
    list_tags.addItems(notes[key]["теги"])

def add_note():
    note_name, ok = QInputDialog.getText(main_win, "Добавить заметку", "Название заметки: ")
    if ok and note_name != "":
        notes[note_name] = {"текст" : "", "теги" : []}
        list_notes.addItem(note_name)
        list_tags.addItems(notes[note_name]["теги"])

def save_note():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        notes[key]["текст"] = field_text.toPlainText()
        with open("notes_data.json", "w", encoding = 'utf-8') as file:
            json.dump(notes, file, sort_keys=True, ensure_ascii=False)
    else:
        info("Заметка для сохранения не выбрана!")

def del_note():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        del notes[key]
        list_notes.clear()
        list_tags.clear()
        field_text.clear()
        list_notes.addItems(notes)
        with open("notes_data.json", "w", encoding = 'utf-8') as file:
            json.dump(notes, file, sort_keys=True, ensure_ascii=False)
    else:
        info("Заметка для удаления не выбрана!")

def info(txt):
    mes = QMessageBox()
    mes.setWindowTitle("Message")
    mes.setText(txt)
    mes.show()
    mes.exec_()

def add_tag():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        tag = field_tag.text()
        if not tag in notes[key]["теги"]:
            notes[key]["теги"].append(tag)
            list_tags.addItem(tag)
            field_tag.clear()
        with open("notes_data.json", "w", encoding = 'utf-8') as file:
            json.dump(notes, file, sort_keys=True, ensure_ascii=False)
    else:
        info("Заметка для добавления тега не выбрана!")

def del_tag():
    if list_tags.selectedItems():
        key = list_notes.selectedItems()[0].text()
        tag = list_tags.selectedItems()[0].text()
        notes[key]["теги"].remove(tag)
        list_tags.clear()
        list_tags.addItems(notes[key]["теги"])
        with open("notes_data.json", "w", encoding = 'utf-8') as file:
            json.dump(notes, file, sort_keys=True, ensure_ascii=False)
    else:
        info("Тег для удаления не выбран!")

def search_tag():
    tag = field_tag.text()
    if btn6.text() == "Искать заметки по тегу" and tag:
        notes_filtered = {} #тут будут заметки с выделенным тегом
        for note in notes:
            if tag in notes[note]["теги"]: 
                notes_filtered[note]=notes[note]
        btn6.setText("Сбросить поиск")
        list_notes.clear()
        list_tags.clear()
        list_notes.addItems(notes_filtered)
    elif btn6.text() == "Сбросить поиск":
        field_tag.clear()
        list_notes.clear()
        list_tags.clear()
        list_notes.addItems(notes)
        btn6.setText("Искать заметки по тегу")
    else:
        pass


#главное окно
app = QApplication([])
main_win = QWidget()
main_win.resize(700,500)
main_win.setWindowTitle('Умные заметки')

#список виджетов
text1 = QLabel('Список заметок:')
text2 = QLabel('Список тегов:')

btn1 = QPushButton('Создать заметку')
btn2 = QPushButton('Удалить заметку')
btn3 = QPushButton('Сохранить заметку')
btn4 = QPushButton('Добавить к заметке')
btn5 = QPushButton('Открепить от заметки')
btn6 = QPushButton('Искать заметки по тегу')

list_notes = QListWidget()
list_tags = QListWidget()

field_text = QTextEdit()

field_tag = QLineEdit()

#список лэйаутов
line1 = QHBoxLayout()
line2 = QHBoxLayout()
line3 = QHBoxLayout()

r_line = QVBoxLayout()
l_line = QVBoxLayout()

main_line = QHBoxLayout()

line1.addWidget(btn1)
line1.addWidget(btn2)
line2.addWidget(btn4)
line2.addWidget(btn5)

r_line.addWidget(text1)
r_line.addWidget(list_notes)
r_line.addLayout(line1)
r_line.addWidget(btn3)
r_line.addWidget(text2)
r_line.addWidget(list_tags)
r_line.addWidget(field_tag)
r_line.addLayout(line2)
r_line.addWidget(btn6)

l_line.addWidget(field_text)

main_line.addLayout(l_line, stretch = 1)
main_line.addLayout(r_line, stretch = 1)

main_win.setLayout(main_line)

#обработка событий
list_notes.itemClicked.connect(show_note)
btn1.clicked.connect(add_note)
btn3.clicked.connect(save_note)
btn2.clicked.connect(del_note)
btn4.clicked.connect(add_tag)
btn5.clicked.connect(del_tag)
btn6.clicked.connect(search_tag)

#запуск приложения
main_win.show()

with open("notes_data.json", "r", encoding = 'utf-8') as file:
    notes = json.load(file)
list_notes.addItems(notes)

app.exec_()
