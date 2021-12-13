from emobpy import DataBase

def temp():
    DB = DataBase('../../../data/emobpy_data/db')
    DB.loadfiles()
    PLT = NBplot(DB)

