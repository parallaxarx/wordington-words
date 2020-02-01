
"""
words.py
v 1.0

Программа сделана для поиска слов в играх-кроссвордах с известными буквами,
а не смыслом, таких как Wordington

Автор: Ощепков Евгений
"""

"""
    Доработки:
1) Сделать CheckBox "Словарь" функциональной (исправить)
2) Сделать окно статичным (нельзя расширять и сужать)
3) Добавить строку состояния выполнения в %
4) Добавить проверку на правильность ввода в поля ввода известных букв
"""

from itertools import permutations #............................................

import sys #....................................................................

                                                                               #
from PyQt5.QtWidgets import QApplication,QLabel,QWidget, QPushButton,QMessageBox, QLineEdit, QCheckBox, QComboBox
from PyQt5.QtCore import QSize, Qt #............................................
from PyQt5.QtGui import QFont #.................................................

# Все возможные буквы
model  = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЬЫЪЭЮЯ' #..................................Русский алфавит большых букв
model_ = 'абвгдеёжзийклмнопрстуфхцчщзьыъэюя' #..................................Русский алфавит маленьких букв
# Чтение из файла словаря русских слов
f = open("RUS.txt","r") #.......................................................Открываем файл RUS.txt для чтения
global listRus #................................................................Создание пустого массива для словаря
listRus = [] #..................................................................    (Глобальным)
# Добавление слов в словарь
for word in f:
    listRus.append(word) #......................................................
f.close() #.....................................................................Закрываем файл RUS.txt
# Булева переменная которая проверяет зажатие чекбокса Словарь
global cb #.....................................................................
cb = False #....................................................................
# --------------------------------Константы ------------------------------------
size = 100 #....................................................................Масштаб программы
board = size//10 #..............................................................Ширина отступа
heigthRoot = 6*size #...........................................................Высота окна
widthRoot  = 6*size #...........................................................Ширина окна

countRowABC = 3 #...............................................................Количество строк кнопок алфавита
countColumnABC = 11 #...........................................................Количество столбцов кнопок алфавита
# ----------------------------------- Размеры ----------------------------------
    #-------------------- Buttons -------------------------
                                                                               #Кнопки алфавита:
heigthButtonABC = (heigthRoot//3 - 2*board)//countRowABC #......................Высота кнопок abc
widthButtonABC  = (widthRoot - 2*board)//countColumnABC #.......................Ширина кнопок abc
                                                                               #Кнопка обнуления программы:
heigthButtonNew = heigthRoot//6 - board #.......................................Высота кнопки New
widthButtonNew  = widthRoot//3 - 2*board #......................................Ширина кнопки New
                                                                               #Кнопка удаления последнего символа из поля букв:
heigthButtonDel = heigthRoot//6 - 2*board #.....................................Высота кнопки Del
widthButtonDel  = widthRoot//6 - 2*board #......................................Ширина кнопки Del
                                                                               #Кнопка поиска слов:
heigthButtonOK = heigthRoot//12 - 2*board #.....................................Высота кнопки OK
widthButtonOK  = widthRoot//3 - 2*board #.......................................Ширина кнопки OK
                                                                               #Кнопка очистки поля вывода слов:
heigthButtonClear = heigthRoot//12 - 2*board #..................................Высота кнопки Clear
widthButtonClear  = widthRoot//6 - 2*board #....................................Ширина кнопки Clear

    #-------------------- Labels -------------------------
                                                                               #Поле вывода слов:
heigthLabelWords = heigthRoot//3 - board #......................................Высота Label Words
widthLabelWords  = widthRoot - 2*board #........................................Ширина Label Words
                                                                               #Поле вывода букв:
heigthLabelLetters = heigthRoot//6 - board #....................................Высота Label Letters
widthLabelLetters  = widthRoot //2 - board #....................................Ширина Label Letters
                                                                               #Поле c надписью "Кол-во букв:"
heigthLabelCount = heigthRoot//12 - board #.....................................Высота Label Count
widthLabelCount  = widthRoot //6 - board #......................................Ширина Label Count

    #-------------------- Edits ---------------------------
                                                                               #Поля ввода известных букв
heigthLineEditLetters = heigthRoot//12 - board #................................Высота Edit`ов Letters
widthLineEditLetters  = widthRoot //12 - board #................................Ширина Edit`ов Letters

    #-------------------- CheckBox -------------------------
                                                                               #Выбор делать ли через словарь
heigthCheckBoxDict = heigthRoot//12 - board #...................................Высота CheckBox Dict
widthCheckBoxDict  = widthRoot //6 - board #....................................Ширина CheckBox Dict

    #-------------------- ComboBox -------------------------
                                                                               #Выпадающий список количества букв в слове
heigthComboBoxLetters = heigthRoot//12 - board #................................Высота ComboBox Letters
widthComboBoxLetters  = widthRoot //6 - board #.................................Ширина ComboBox Letters

    #-------------------------------------------------------
#
class Main(QWidget):
    #
    def __init__(self):
        super().__init__() #....................................................
        self.initUI() #.........................................................
        self.resize(QSize(widthRoot, heigthRoot)) #.............................Размер окна
        self.setWindowTitle('Слова') #..........................................Заголовок
#------------------------------ Функционал -------------------------------------
    # Переключение выбора словаря (Не работает)
    def fCheckBoxDict(self, state):
        #Проверка наличие на галочку в окне
        if state == Qt.Checked:
            cb = True #.........................................................
        #Отсутствие...
        else:
            cb = False #........................................................
    # Очищает вывод слов в labelWords (Работает)
    def fClear(self):
        self.labelWords.setText('') #...........................................
    # Нажатие на букву (Работает)
    def fABC(self):
        sender = self.sender() #................................................Нажатая клавиша
        # Если буква первая
        if self.labelLetters.text() == '':
                                                                               #Просто добавить букву
            self.labelLetters.setText(self.labelLetters.text() + sender.text())
        # Если буква уже не первая
        else:
                                                                               #Добавить букву с запятой в начале
            self.labelLetters.setText(self.labelLetters.text() + ', ' + sender.text())
    # Функция выполнения вывода
    def fGO(self):
                                                                               #Список возможных букв без запятых и пробелов
        listLetters = ''.join((''.join(self.labelLetters.text().split(','))).split())
        listWords = permutations(listLetters, len(self.lineEditLetters)) #......Перебор всех перестановок возможных букв
        listWordsNoRepeat = [] #................................................Создание списка слов без подстановок
        # Вывод слов в поле вывода слов
        for i in list(listWords):
            check = True #......................................................Булева переменная для проверки включения известных букв в слово
            #Перебор известных букв
            for j in range(len(self.lineEditLetters)):
                #Условие проверки на наличие буквы в поле ввода
                if self.lineEditLetters[j].text() != '':
                    #Условие проверки отсутствие известной буквы в слове на нужном месте
                    if i[j] != self.lineEditLetters[j].text():
                        check = False #.........................................

            #Проверка на правильность слова
            if check:
                #Исключение повторений в списке
                if ''.join(i) not in listWordsNoRepeat:
                    #Условие проверки на наличие слов в русском языке из словаря RUS.txt
                    if ((''.join(i)+'\n') in listRus):# or not (cb):
                        listWordsNoRepeat.append(''.join(i)) #..................Добавление слова в список
                        print(''.join(i)) #.....................................//// Вывод слова в консоль (Для разработки)
        countWordsInLine = 0 #..................................................Переменная для содержания в себе количества слов в строке
        #Перебор слов по списку для вывода
        for i in listWordsNoRepeat:
            #Если слово первое
            if self.labelWords.text() == '':
                self.labelWords.setText(i) #....................................Просто вывод слова
                countWordsInLine += 1 #......................................... +1 к количеству слов в строке
            #Последующие слова
            else:
                #Если слов в строке меньше 10
                if countWordsInLine < 10:
                    self.labelWords.setText(self.labelWords.text() + ', ' + i) #Вывод слова с запятой в начале
                    countWordsInLine += 1 #..................................... +1 к количеству слов в строке
                #Если слов в строке становится 10
                else:
                                                                               #Вывод слова с переносом на новую строку
                    self.labelWords.setText(self.labelWords.text() + ', ' + '\n'+ i)
                    countWordsInLine = 1 #......................................Онулирование количества слов в строке
        #Если после вывода слов пусто
        if self.labelWords.text() == '':
            self.labelWords.setText('Не найдено') #.............................Вывести текст "Не найдено"
        print() #...............................................................////Вывод в консоль пустой строки для удобства (Для разработки)
    # Онулирование программы (Работает)
    def fNew(self):
        #Перебор всех окон ввода
        for i in range(len(self.lineEditLetters)):
            self.lineEditLetters[i].hide() #....................................Скрытыие полей ввода
        self.lineEditLetters.clear() #..........................................Очищение списка полей ввода
        self.labelWords.setText('') #...........................................Очищение поля вывода слов
        self.labelLetters.setText('') #.........................................Очищение поля вывода известных букв
    # Удаление символа из поля возможных букв (Работает)
    def fDel(self):
        self.labelLetters.setText(self.labelLetters.text()[:-3]) #..............Удаление последних трёх символов (буква, запятая, полбел)
    # Создание n-го количества Edit для ввода известных букв (Работает)
    def onActivated(self, cnt):
        #Перебор старых полей ввода известных букв
        for i in range(len(self.lineEditLetters)):
            self.lineEditLetters[i].hide() #....................................Скрытие полей
        self.lineEditLetters.clear() #..........................................Очищение списка
        #Создание полей cnt штук
        for i in range(int(cnt)):
            editLetters = QLineEdit(self) #.....................................Создание поля
            self.lineEditLetters.append(editLetters) #..........................Добавление в список полей
                                                                               #Установка размера полей
            self.lineEditLetters[i].resize(widthLineEditLetters,heigthLineEditLetters)
                                                                               #Смещение полей
            self.lineEditLetters[i].move(board + widthRoot//12 + i*widthLineEditLetters,board + 5*heigthRoot//12)
            self.lineEditLetters[i].show() #....................................Размещение в окне
#-------------------------------------------------------------------------------
    #
    def initUI(self):
        # ---------------Список кнопок--------------------------
        # Алфавит в порядке как на клавиатуре (маленькими)
        abcList = [['й','ц','у','к','е','н','г','ш','щ','з','х'],
                   ['ф','ы','в','а','п','р','о','л','д','ж','э'],
                   ['я','ч','с','м','и','т','ь','б','ю','ъ','ё']]
                   # Большими
                   # [['Й','Ц','У','К','Е','Н','Г','Ш','Щ','З','Х'],
                   #  ['Ф','Ы','В','А','П','Р','О','Л','Д','Ж','Э'],
                   #  ['Я','Ч','С','М','И','Т','Ь','Б','Ю','Ъ','Ё']]
                   # в алфавитном порядке:
                   # Большими
                   # [['А','Б','В','Г','Д','Е','Ё','Ж','З','И','Й'],
                   #  ['К','Л','М','Н','О','П','Р','С','Т','У','Ф'],
                   #  ['Х','Ц','Ч','Ш','Щ','Ь','Ы','Ъ','Э','Ю','Я']]
                   # Маленькими
                   # [['а','б','в','г','д','е','ё','ж','з','и','й'],
                   #  ['к','л','м','н','о','п','р','с','т','у','ф'],
                   #  ['х','ц','ч','ш','щ','ь','ы','ъ','э','ю','я']]

        # Стили
        self.setStyleSheet("""
            QWidget {
                background-color: #9932CC;
                color: #FFF;
                position:relative;
                text-align: center;
            }
            QPushButton {
                background-color: #BC8F8F;
                color: #123;
            }

            #buttonABC {
                background-color: #BC8F8F;
                color: #123;
            }
            #buttonNew {
                background-color: #BC8F8F;
                color: #123;

            }
            #buttonDel {
                background-color: #BC8F8F;
                color: #123;

            }
            #buttonOK {
                background-color: #BC8F8F;
                color: #123;

            }
            #buttonClear {
                background-color: #BC8F8F;
                color: #123;

            }
            QLabel {
                background-color: #9932CC;
                color: #FFF;

            }
            #labelWords {
                background-color: #8A2BE2;
                color: #FFF;
                border: 1px solid  #FFF;
            }
            #labelLetters {
                background-color: #8A2BE2;
                color: #FFF;
                border: 1px solid  #FFF;
            }


            QComboBox {
                background-color: #8A2BE2;
                color: #FFF;
            }

            QLineEdit {
                background-color: #8A2BE2;
                color: #FFF;
            }

            QCheckBox {
                background-color: #9932CC;
                color: #FFF;
            }
        """)

# ------------------------- Создание элементов ---------------------------------
    # Кнопки
        # Алфавит
        self.btnABC = [] #......................................................Создание пустого списка кнопок Алфавита
        #
        for r in range(countRowABC):
            self.btnABC.append([]) #............................................Добавление строк в список
            #
            for c in range(countColumnABC):
                                                                               #Создание кнопки
                button = QPushButton(abcList[r][c],self,objectName = 'buttonABC')
                self.btnABC[r].append(button) #.................................Добавление кнопки в строку
                self.btnABC[r][c].resize(widthButtonABC, heigthButtonABC) #.....Размер кнопки
                                                                               #Положение кнопки
                self.btnABC[r][c].move(board + c*widthButtonABC , 2*heigthRoot//3 + board + r*heigthButtonABC)
                self.btnABC[r][c].clicked.connect(self.fABC) #..................Привязка нажатия к кнопке
        # New
        self.btnNew = QPushButton("NEW",self,objectName = 'buttonNew') #........Создание кнопки
        self.btnNew.resize(widthButtonNew, heigthButtonNew) #...................Размер кнопки
        self.btnNew.move(board , heigthRoot//2 + board) #.......................Положение кнопки
        self.btnNew.clicked.connect(self.fNew) #................................Привязка нажатия к кнопке
        # Del
        self.btnDel = QPushButton("<",self,objectName = 'buttonDel') #..........Создание кнопки
        self.btnDel.resize(widthButtonDel, heigthButtonDel) #...................Размер кнопки
        self.btnDel.move( 5*widthRoot//6 , heigthRoot//2 + 3*board//2) #........Положение кнопки
        self.btnDel.clicked.connect(self.fDel) #................................Привязка нажатия к кнопке
        # OK
        self.btnOK = QPushButton("Найти слова",self,objectName = 'buttonOK') #..Создание кнопки
        self.btnOK.resize(widthButtonOK, heigthButtonOK) #......................Размер кнопки
        self.btnOK.move( board + widthRoot//2 , 3*board//2 + heigthRoot//3 ) #..Положение кнопки
        self.btnOK.clicked.connect(self.fGO) #..................................Привязка нажатия к кнопке
        # Clear
                                                                               #Создание кнопки
        self.btnClear = QPushButton("Очистить поле",self,objectName = 'buttonClear')
        self.btnClear.resize(widthButtonClear, heigthButtonClear) #.............Размер кнопки
        self.btnClear.move( board , 3*board//2 + heigthRoot//3 ) #..............Положение кнопки
        self.btnClear.clicked.connect(self.fClear) #............................Привязка нажатия к кнопке
    # Label
        # Words
        self.labelWords = QLabel("",self,objectName = 'labelWords') #...........Создание поля вывода слов
        self.labelWords.resize(widthLabelWords, heigthLabelWords) #.............Размер поля вывода слов
        self.labelWords.move(board, board) #....................................Положение поля вывода слов
        # Letters
        self.labelLetters = QLabel("",self,objectName = 'labelLetters') #.......Создание поля вывода возможных букв
        self.labelLetters.resize(widthLabelLetters, heigthLabelLetters) #.......Размер поля вывода возможных букв
        self.labelLetters.move(widthRoot//3, board + heigthRoot//2) #...........Положение поля вывода возможных букв
        # Count
        self.labelCount = QLabel("Кол-во букв:",self,objectName = 'labelCount')#Создание поля с надписью
        self.labelCount.resize(widthLabelCount, heigthLabelCount) #.............Размер поля с надписью
        self.labelCount.move(board + widthRoot//6, board + heigthRoot//3) #.....Положение поля с надписью
    # Edit
        # Letters
        startChar= 2 #..........................................................Минимальное количество букв
        endChar = 10 #..........................................................Максимальное количество букв (до 12)
        self.lineEditLetters = [] #.............................................Пустой список полей ввода для известных букв
        #
        for i in range(int(startChar)):
            editLetters = QLineEdit(self) #.....................................Создание поля ввода известных букв
            self.lineEditLetters.append(editLetters) #..........................Добавление поля в список
                                                                               #Размер полей
            self.lineEditLetters[i].resize(widthLineEditLetters,heigthLineEditLetters)
                                                                               #Положение полей
            self.lineEditLetters[i].move(board + widthRoot//12 + i*widthLineEditLetters,board + 5*heigthRoot//12)
            self.lineEditLetters[i].show() #....................................Размещение в окне
    # ComboBox
        # Количество известных букв
        self.comboBoxCountLetters = QComboBox(self) #...........................Создание списка количества букв в слове
        #
        for i in range(startChar,endChar+1):
            self.comboBoxCountLetters.addItem(str(i)) #.........................Добавление чисел в список
                                                                               #Размер списка
        self.comboBoxCountLetters.resize(widthComboBoxLetters,heigthComboBoxLetters)
                                                                               #Положение списка
        self.comboBoxCountLetters.move(board + widthRoot//3, board + heigthRoot//3)
        self.comboBoxCountLetters.activated[str].connect(self.onActivated) #....Привязка изменения списка к функции, создающей окна ввода известных букв

    # CheckBox
        # Словарь
                                                                               #Создание ЧекБокса Словарь
        self.checkBoxDict = QCheckBox('Словарь',self,objectName = 'checkBoxDict')
        self.checkBoxDict.resize(widthCheckBoxDict,heigthCheckBoxDict) #........Размер ЧекБокса
        self.checkBoxDict.move(board + 5*widthRoot//6, board + heigthRoot//3) #.Положение ЧекБокса
        self.checkBoxDict.stateChanged.connect(self.fCheckBoxDict) #............Привязка к функции меняющей булево значение переменной cb
#
if __name__ == '__main__':
    app = QApplication(sys.argv) #..............................................
    ex = Main() #...............................................................
    ex.show() #.................................................................
    sys.exit(app.exec_()) #.....................................................
