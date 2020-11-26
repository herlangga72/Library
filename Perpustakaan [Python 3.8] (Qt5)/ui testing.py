from PyQt5 import QtWidgets, uic
import mysql.connector as db
from datetime import date,timedelta
#Activate Loger
Logger   = False
#Load the Appp?
Load     = True
#bypasser
session  = None
#For loginto db
userDB     ="pmauser"
passwordDB ="password_here"
# Universal function
def Out(x):
    global Logger 
    if Logger :print(f"working {x}")
def connect(query):
    cnx     = db.connect(user=userDB, password=passwordDB, database='perpus' )
    cursor  = cnx.cursor()
    cursor.execute(query)
    data=list(cursor)
    column=cursor.column_names
    cursor.close()
    cnx.close()
    print(query,data, sep="\n")
    return data,column
def Level(session):
    global window
    if session[0][3]==1:
        window=Menu_1()
    elif session[0][3]==2:
        window=Menu_2()
def selectdb(target,query):    
    data,column = connect(query)
    insertTable(target,column,data)
def insertTable(target,column,data):
    target.setColumnCount(len(column))
    target.setRowCount(0)
    target.setHorizontalHeaderLabels(column)
    target.insertRow(1)
    row_number = 0
    for i in data:
        target.insertRow(row_number)
        column_number =0
        for j in i:
            if j is None:
                j=""
            target.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(j)))
            column_number+=1
        row_number += 1
    target.resizeColumnsToContents()
def update(query):
    print(query)
    cnx     = db.connect(user=userDB, password=passwordDB, database='perpus' )
    cursor  = cnx.cursor()
    cursor.execute(query)
    cnx.commit()
    cursor.close()
    cnx.close()
#Bagian ini diakses semua
class Login(QtWidgets.QMainWindow):
    def __init__(self):
        super(Login, self).__init__()
        uic.loadUi    ('gui/Main menu.ui', self) 
        self.setWindowTitle("Login")
        self.status = self.findChild(QtWidgets.QStatusBar, 'statusbar')
        self.button = self.findChild(QtWidgets.QPushButton, 'b_Login')
        self.button.clicked.connect(self.login)
        self.Login  = self.findChild(QtWidgets.QLineEdit, 'Q_Login')
        self.Pass   = self.findChild(QtWidgets.QLineEdit, 'Q_Pass')
        self.Pass.setEchoMode(QtWidgets.QLineEdit.Password)
        self.show()
    def login(self):
        global Logger, window, session
        if Logger: Out(f"{self.Login.text()}, {self.Pass.text()}")
        try:
            sim = connect(f"SELECT `UserID_Usr`, `UserID_Pwd`,Member_ID FROM UserID WHERE UserID_Usr='{self.Login.text()}' AND UserID_Pwd='{self.Pass.text()}'")[0]
            # ini jelas merupakan bug, bila data banyak maka yg di cek atas saja?? anda bercanda
            if self.Login.text()==sim[0][0] and self.Pass.text()==sim[0][1]:
                session = connect(f"SELECT * FROM Member WHERE Member_ID='{sim[0][2]}'")[0]
                Level(session)
                self.close()
            #end
        except:
            self.status.showMessage("Login Failed : Member Not Found")
class Profile(QtWidgets.QMainWindow):
    def __init__(self):
        super(Profile, self).__init__()
        uic.loadUi('gui/Main_Login_Member.ui', self)
        global session
        self.setWindowTitle("Profile - Info")
        self.b_Back= self.findChild(QtWidgets.QPushButton, 'b_Back')
        self.b_Back.clicked.connect(self.Back)
        #config on Info
        self.Tab    = self.findChild(QtWidgets.QTabWidget, 'Tab')
        self.Nama   = self.findChild(QtWidgets.QLabel, 'Nama')
        self.Id     = self.findChild(QtWidgets.QLabel, 'ID')
        self.Alamat = self.findChild(QtWidgets.QLabel, 'Alamat')
        #setting value
        self.Nama.setText(session[0][1])
        self.Id.setText(session[0][0])
        self.Alamat.setText(session[0][2])
        #config on Transaksi
        self.Table  = self.findChild(QtWidgets.QTableWidget, 'tabel')
        self.Tab.currentChanged.connect(self.onChange)
        self.show()
    def onChange(self,i):
        if i==0:
            self.setWindowTitle("Profile - Transaksi")
        elif i==1:
            self.setWindowTitle("Profile - Transaksi")
            selectdb(self.Table,f"Select ID,Buku_Judul as Judul ,'Tanggal Dipinjam','Tanggal Kembali',Status FROM (SELECT Transaksi_ID AS ID, Transaksi_F_Time AS 'Tanggal Dipinjam', Transaksi_R_Time AS 'Tanggal Kembali',Status,Buku_ID,Member_ID  FROM Transaksi) AS A INNER JOIN (SELECT Buku_ID, Buku_Judul From Buku)AS B ON A.Buku_ID=B.Buku_ID WHERE A.Member_ID='{session[0][0]}'")
    def Back(self):
        global Logger,session
        if Logger: Out(f"Back")
        Level(session)
        self.close()
class Pencarian(QtWidgets.QMainWindow):
    def __init__(self):
        super(Pencarian, self).__init__()
        uic.loadUi('gui/main_pencarian_Buku.ui', self) 
        self.setWindowTitle("Pencarian Buku")

        self.Judul       = self.findChild(QtWidgets.QLineEdit,   's_Judul')
        self.Pengarang   = self.findChild(QtWidgets.QLineEdit,   's_Pengarang')
        self.Penerbit    = self.findChild(QtWidgets.QLineEdit,   's_Penerbit')
        self.b_Back      = self.findChild(QtWidgets.QPushButton, 'b_Back')
        self.b_Search    = self.findChild(QtWidgets.QPushButton, 'b_Search')
        self.Tabel       = self.findChild(QtWidgets.QTableWidget,'Tabel' )
        
        self.b_Back.clicked.connect(self.Back)
        self.b_Search.clicked.connect(self.Search)
    
        self.show()
    def Back(self):
        global Logger,session
        if Logger: Out(f"Back")
        Level(session)
        self.close()
    def Search(self):
        List        = list()
        List.append(self.Judul.text())
        List.append(self.Pengarang.text())
        List.append(self.Penerbit.text())
        combined=""
        if List[0]!='':
            combined+=f"AND Buku_Judul LIKE '%{List[0]}%' "
        if List[1]!='':
            combined+=f"AND Buku_Pengarang LIKE '%{List[1]}%' "
        if List[2]!='':
            combined+=f"AND Buku_Penerbitan LIKE '%{List[2]}%' "
        if combined!='':
            combined=f"WHERE {combined[4:]}"
        combined=f"SELECT `Buku_ID` AS ID, `Buku_Judul` AS Judul, `Buku_Pengarang` AS Pengarang, `Buku_Penerbitan` AS Penerbit, `Buku_Fisik`AS 'Wujud Fisik', `Buku_Media` AS 'Media Tersimpan', `Buku_Subjek` AS Subjek, `Buku_Catatan` AS Catatan, `Buku_Rak` AS 'Lokasi Rak', `Buku_Copy` AS 'Jumlah Copy' FROM `Buku` {combined}"
        selectdb(self.Tabel,combined)
#bagian member level 1 (Member)
class Menu_1(QtWidgets.QMainWindow):
    def __init__(self):
        super(Menu_1, self).__init__()
        uic.loadUi('gui/Main_SearchBook.ui', self)
        self.setWindowTitle("Main Menu") 
        
        self.b_Pencarian = self.findChild(QtWidgets.QPushButton, 'b_Pencarian')
        self.b_Profile = self.findChild(QtWidgets.QPushButton, 'b_Profile')
        self.b_Logout = self.findChild(QtWidgets.QPushButton, 'b_Logout')
        
        self.b_Pencarian.clicked.connect(self.LoadPencarian)
        self.b_Profile.clicked.connect(self.LoadProfile)
        self.b_Logout.clicked.connect(self.close)
        
        self.show()
    def LoadPencarian(self):
        global Logger,window
        if Logger: Out(f"Pencarian")
        window=Pencarian()
        self.close()
    def LoadProfile(self):
        global Logger,window
        if Logger: Out(f"Profile")
        window = Profile()
        self.close()
#bagian member level 2 (Admin)
class Menu_2(QtWidgets.QMainWindow):
    def __init__(self):
        super(Menu_2, self).__init__()
        uic.loadUi('gui/Main_SearchBook_Admin.ui', self)
        self.setWindowTitle("Main Menu") 
        #get component
        self.b_Pencarian    = self.findChild(QtWidgets.QPushButton, 'b_Pencarian')
        self.b_Profile      = self.findChild(QtWidgets.QPushButton, 'b_Profile')
        self.b_AnggotaPlus  = self.findChild(QtWidgets.QPushButton, 'b_AnggotaPlus')
        self.b_Buku         = self.findChild(QtWidgets.QPushButton, 'b_Buku')
        self.b_Peminjaman   = self.findChild(QtWidgets.QPushButton, 'b_Peminjaman')
        self.b_Logout       = self.findChild(QtWidgets.QPushButton, 'b_Logout')
        #make event handler
        self.b_Pencarian.clicked.connect(self.LoadPencarian)
        self.b_Profile.clicked.connect(self.LoadProfile)
        self.b_AnggotaPlus.clicked.connect(self.LoadAnggotaPlus)
        self.b_Buku.clicked.connect(self.LoadBuku)
        self.b_Peminjaman.clicked.connect(self.LoadPeminjaman)
        self.b_Logout.clicked.connect(self.close)
        #load gui
        self.show()
    def LoadPencarian(self):
        global Logger,window
        if Logger: Out(f"Pencarian")
        window=Pencarian()
        self.close()
    def LoadProfile(self):
        global Logger,window
        if Logger: Out(f"Profile")
        window = Profile()
        self.close()
    def LoadAnggotaPlus(self):
        global Logger,window
        if Logger: Out(f"AnggotaPlus")
        window = MemberEdit()
        self.close()
    def LoadBuku(self):
        global Logger,window
        if Logger: Out(f"Buku")
        window = Inv()
        self.close()
    def LoadPeminjaman(self):
        global Logger,window
        if Logger: Out(f"Peminjam")
        window = Peminjaman()
        self.close()
class MemberEdit(QtWidgets.QMainWindow):
    def __init__(self):
        super(MemberEdit, self).__init__()
        uic.loadUi('gui/Menu_Member.ui', self)
        self.setWindowTitle("Member Editor") 
        self.status = self.findChild(QtWidgets.QStatusBar, 'statusbar')
        
        #get component
        self.b_Update        = self.findChild(QtWidgets.QPushButton, 'b_Update')
        self.b_Cari          = self.findChild(QtWidgets.QPushButton, 'b_Cari')
        self.b_Tambah        = self.findChild(QtWidgets.QPushButton, 'b_Tambah')
        self.b_Hapus         = self.findChild(QtWidgets.QPushButton, 'b_Hapus')
        self.b_Back         = self.findChild(QtWidgets.QPushButton, 'b_Back')
        
        self.s_Member_ID     = self.findChild(QtWidgets.QLineEdit,   's_Member_ID')
        self.s_Nama          = self.findChild(QtWidgets.QLineEdit,   's_Nama')
        self.s_Alamat        = self.findChild(QtWidgets.QLineEdit,   's_Alamat')
        self.s_Level         = self.findChild(QtWidgets.QSpinBox,    's_Level')
        self.s_Username_ID   = self.findChild(QtWidgets.QLineEdit,   's_Username')
        self.s_Password_ID   = self.findChild(QtWidgets.QLineEdit,   's_Password')
        
        self.s_Member_ID_2   = self.findChild(QtWidgets.QLineEdit,   's_Member_ID_2')
        self.s_Nama_2        = self.findChild(QtWidgets.QLineEdit,   's_Nama_2')
        self.s_Alamat_2      = self.findChild(QtWidgets.QLineEdit,   's_Alamat_2')
        self.s_Level_2       = self.findChild(QtWidgets.QSpinBox,    's_Level_2')
        self.s_Username_ID_2 = self.findChild(QtWidgets.QLineEdit,   's_Username_2')
        self.s_Password_ID_2 = self.findChild(QtWidgets.QLineEdit,   's_Password_2')
        
        self.Member_ID       = self.findChild(QtWidgets.QLineEdit,   'Member_ID')
        
        #make event handler
        self.b_Update.clicked.connect(self.Update)
        self.b_Tambah.clicked.connect(self.Tambah)
        self.b_Hapus.clicked.connect(self.Hapus)
        self.b_Cari.clicked.connect(self.Cari)
        self.b_Back.clicked.connect(self.Back)
        
        #load gui
        self.show()
    def Back(self):
        global Logger,session
        if Logger: Out(f"Back")
        Level(session)
        self.close()
    def Cari(self):
        try:
            Query=f"SELECT * FROM Member Natural JOIN UserID WHERE Member_ID='{self.s_Member_ID_2.text()}'"
            data=connect(Query)[0][0]
            self.s_Nama_2.setText(data[1])
            self.s_Alamat_2.setText(data[2])
            self.s_Level_2.setValue(data[3])
            self.s_Username_ID_2.setText(data[4])
            self.s_Password_ID_2.setText(data[5])
        except:
            self.status.showMessage("Login Failed : Member Not Found")
    def Update(self):
        update(f"UPDATE Member SET Member_Name='{self.s_Nama_2.text()}', Member_Alamat='{self.s_Alamat_2.text()}', Member_Level={self.s_Level_2.value()} WHERE Member_ID={self.s_Member_ID_2.text()}")
        update(f"UPDATE UserID SET UserID_Usr='{self.s_Username_ID_2.text()}', UserID_Pwd='{self.s_Password_ID_2.text()}' WHERE Member_ID='{self.s_Member_ID_2.text()}'")
    def Tambah(self):
        update(f"INSERT INTO Member (Member_ID, Member_Name, Member_Alamat, Member_Level) VALUES ('{self.s_Member_ID.text()}','{self.s_Nama.text()}','{self.s_Alamat.text()}','{self.s_Level.text()}') ")
        update(f"INSERT INTO UserID (UserID_Usr,UserID_Pwd,Member_ID) VALUES ('{self.s_Username_ID.text()}','{self.s_Password_ID.text()}','{self.s_Member_ID.text()}') ")
    def Hapus(self):
        update(f"DELETE FROM Member WHERE Member_ID='{self.Member_ID.text()}'")
        update(f"DELETE FROM UserID WHERE Member_ID='{self.Member_ID.text()}'")
class Peminjaman(QtWidgets.QMainWindow):
    def __init__(self):
        super(Peminjaman, self).__init__()
        uic.loadUi('gui/Peminjaman.ui', self)
        self.setWindowTitle("Menu Peminjaman")

        self.status          = self.findChild(QtWidgets.QStatusBar, 'statusbar')
        self.b_Back          = self.findChild(QtWidgets.QPushButton ,'b_Back')
        
        self.b1_Buku_ID      = self.findChild( QtWidgets.QPushButton ,'b1_Buku_ID')
        self.b2_Confirm      = self.findChild( QtWidgets.QPushButton ,'b2_Confirm')
        self.b2_Member_ID    = self.findChild( QtWidgets.QPushButton ,'b2_Member_ID')
        self.b3_Delete       = self.findChild( QtWidgets.QPushButton ,'b3_Delete')
        self.b3_Transaksi_ID = self.findChild( QtWidgets.QPushButton ,'b3_Transaksi_ID')
        self.b3_Update       = self.findChild( QtWidgets.QPushButton ,'b3_Update')
        self.s1_Buku_ID      = self.findChild( QtWidgets.QLineEdit   ,'s1_Buku_ID')
        self.s2_Member_ID    = self.findChild( QtWidgets.QLineEdit   ,'s2_Member_ID')
        self.s3_Transaksi_ID = self.findChild( QtWidgets.QLineEdit   ,'s3_Transaksi_ID')
        self.w1Eksemplar     = self.findChild( QtWidgets.QLabel      ,'w1Eksemplar')
        self.w1Judul         = self.findChild( QtWidgets.QLabel      ,'w1Judul')
        self.w1Penerbit      = self.findChild( QtWidgets.QLabel      ,'w1Penerbit')
        self.w1Pengarang     = self.findChild( QtWidgets.QLabel      ,'w1Pengarang')
        self.w1Terpinjam     = self.findChild( QtWidgets.QLabel      ,'w1Terpinjam')
        self.w2Max_Pinjam    = self.findChild( QtWidgets.QLabel      ,'w2Max_Pinjam')
        self.w2Nama          = self.findChild( QtWidgets.QLabel      ,'w2Nama')
        self.w2Total_Pinjam  = self.findChild( QtWidgets.QLabel      ,'w2Total_Pinjam')
        self.w3Judul         = self.findChild( QtWidgets.QLabel      ,'w3Judul')
        self.w3Kembali       = self.findChild( QtWidgets.QLabel      ,'w3Kembali')
        self.w3Peminjam      = self.findChild( QtWidgets.QLabel      ,'w3Peminjam')
        self.w3Tgl_Pinjam    = self.findChild( QtWidgets.QLabel      ,'w3Tgl_Pinjam')
        self.w3Status        = self.findChild( QtWidgets.QComboBox   ,'w3Status')

        self.b_Back.clicked.connect(self.Back)
        self.b1_Buku_ID.clicked.connect(self.Buku_ID)
        self.b2_Confirm.clicked.connect(self.Confirm)
        self.b2_Member_ID.clicked.connect(self.Member_ID)
        self.b3_Delete.clicked.connect(self.Delete)
        self.b3_Transaksi_ID.clicked.connect(self.Transaksi_ID)
        self.b3_Update.clicked.connect(self.Update)
        self.show()
    def Back(self):
        global Logger,session
        if Logger: Out(f"Back")
        Level(session)
        self.close()
    def Buku_ID(self):
        data=connect(
            f"""SELECT * FROM (
                    SELECT Buku_Judul, Buku_Pengarang, Buku_Penerbitan,Buku_Copy,Buku_ID FROM Buku) 
                AS A Left JOIN (
                    SELECT Buku_ID,COUNT(Transaksi.Transaksi_ID) From Transaksi GROUP By Buku_ID ) 
                AS B ON A.Buku_ID=B.Buku_ID WHERE A.Buku_ID={self.s1_Buku_ID.text()}""")[0][0]
        self.w1Judul.setText    (data[0])
        self.w1Pengarang.setText(data[1])
        self.w1Penerbit.setText (data[2])
        self.w1Eksemplar.setText( str(data[3]))
        self.w1Terpinjam.setText( str(data[6]) if data[6] is not None else '0' )
    def Member_ID(self): 
        data=connect(f"SELECT Member_Name,Meminjam FROM Member LEFT JOIN (SELECT Member_ID, COUNT(*) AS Meminjam FROM Transaksi GROUP BY Member_ID) AS A ON Member.Member_ID=A.Member_ID Where Member.Member_ID='{self.s2_Member_ID.text()}'")[0][0]
        self.w2Nama.setText(data[0])
        self.w2Total_Pinjam.setText(str(data[1]))
    def Confirm(self):
        update(f'Insert INTO Transaksi (Buku_ID, Member_ID, Transaksi_F_Time, Transaksi_R_Time ) VALUES ("{self.s1_Buku_ID.text()}", "{self.s2_Member_ID.text()}", "{date.today()}", "{date.today() + timedelta(days=14)}" )')
    def Delete(self):
        update(f"DELETE FROM Transaksi WHERE Transaksi_ID='{self.s3_Transaksi_ID.text()}'")
    def Transaksi_ID(self):
        data=connect(f'SELECT Buku_Judul,Member_ID,Transaksi_F_Time,Transaksi_R_Time,Status FROM Transaksi JOIN Buku ON Buku.Buku_ID=Transaksi.Buku_ID WHERE Transaksi.Transaksi_ID={self.s3_Transaksi_ID.text()}')[0][0]
        self.w3Judul.setText(data[0])
        self.w3Kembali.setText(data[3].strftime("%d-%m-%Y") if data[3] is not None else '-')
        self.w3Peminjam.setText(data[1])
        self.w3Tgl_Pinjam.setText(data[2].strftime("%d-%m-%Y"))
        if data[4]=="Dipinjam":
            self.w3Status.setCurrentIndex(0)
        else:
            self.w3Status.setCurrentIndex(1)
    def Update(self):
        update(f"UPDATE Transaksi SET Status='{self.w3Status.currentText()}' WHERE Transaksi_ID={self.s3_Transaksi_ID.text()}")
class Inv(QtWidgets.QMainWindow):
    def __init__(self):
        super(Inv, self).__init__()
        uic.loadUi('gui/Penambahan Buku.ui', self)
        self.setWindowTitle("Menu Peminjaman")
        self.status     = self.findChild(QtWidgets.QStatusBar, 'statusbar')
        self.b_Back     = self.findChild(QtWidgets.QPushButton ,'b_Back')
        self.tabel      = self.findChild(QtWidgets.QTableWidget, "tabel")
        self.isian1     = self.findChild(QtWidgets.QLineEdit, "lineEdit_1")
        self.isian2     = self.findChild(QtWidgets.QLineEdit, "lineEdit_2")
        self.isian3     = self.findChild(QtWidgets.QLineEdit, "lineEdit_3")
        self.isian4     = self.findChild(QtWidgets.QLineEdit, "lineEdit_4")
        self.isian5     = self.findChild(QtWidgets.QLineEdit, "lineEdit_5")
        self.isian7     = self.findChild(QtWidgets.QLineEdit, "lineEdit_7")
        self.isian8     = self.findChild(QtWidgets.QLineEdit, "lineEdit_8")
        self.isian9     = self.findChild(QtWidgets.QLineEdit, "lineEdit_9")
        self.isian10    = self.findChild(QtWidgets.QLineEdit, "lineEdit_10")
        self.isian11    = self.findChild(QtWidgets.QSpinBox, "spinBox")
        self.tombol1    = self.findChild(QtWidgets.QPushButton, "pushButton_1" )
        self.tombol2    = self.findChild(QtWidgets.QPushButton, "pushButton_2" )
        self.tombol3    = self.findChild(QtWidgets.QPushButton, "pushButton_3" )
        self.tombol4    = self.findChild(QtWidgets.QPushButton, "pushButton_4" )
        self.tombol1.clicked.connect(self.Back)
        self.tombol2.clicked.connect(self.Add)
        self.tombol3.clicked.connect(self.Update)
        self.tombol4.clicked.connect(self.Delete)
        self.tabel.itemClicked.connect(self.getData)
        self.table()
        self.show()
    def getData(self):
        a=self.tabel.item(self.tabel.currentRow(), 0).text()
        data= connect(f"Select * from Buku WHERE Buku_ID='{a}'")[0][0]
        data=list(data)
        for i in range (len(data)): 
            data[i]=data[i] if data[i] is not None else 'None'
        self.isian1.setText(str(data[0]))
        self.isian2.setText(data[1])
        self.isian3.setText(data[2])
        self.isian4.setText(data[3])
        self.isian5.setText(data[4])
        self.isian7.setText(data[5])
        self.isian8.setText(data[6])
        self.isian9.setText(data[7])
        self.isian10.setText(data[8])
        self.isian11.setValue(data[9])
    def Back(self):
        global Logger,session
        if Logger: Out(f"Back")
        Level(session)
        self.close()
    def Add   (self):
        update(
            f"""INSERT INTO Buku (Buku_ID, Buku_Judul, Buku_Pengarang, Buku_Penerbitan, Buku_Fisik, Buku_Media, Buku_Subjek, Buku_Catatan, Buku_Rak, Buku_Copy ) VALUES ({self.isian1.text()},'{self.isian2.text()}','{self.isian3.text()}','{self.isian4.text()}','{self.isian5.text()}','{self.isian7.text()}','{self.isian8.text()}','{self.isian9.text()}','{self.isian10.text()}',{self.isian11.text()})""")
        self.table()
    def Update(self):
        update(
            f"""UPDATE Buku SET
                 Buku_Judul = "{self.isian2.text()}", 
                 Buku_Pengarang = "{self.isian3.text()}", 
                 Buku_Penerbitan = "{self.isian4.text()}", 
                 Buku_Fisik = "{self.isian5.text()}", 
                 Buku_Media = "{self.isian7.text()}", 
                 Buku_Subjek = "{self.isian8.text()}", 
                 Buku_Catatan = "{self.isian9.text()}", 
                 Buku_Rak = "{self.isian10.text()}", 
                 Buku_Copy = "{self.isian11.text()}"
                  WHERE Buku_ID = "{self.isian1.text()}"
            """)
        self.table()
    def Delete(self):
        update(f"DELETE FROM Buku WHERE Buku_ID={self.isian1.text()}")
        self.table()
    def table(self):
        selectdb(self.tabel, "SELECT Buku_ID AS ID, Buku_Judul As 'Judul Buku' FROM Buku")
#driver app
if Load:
    app      = QtWidgets.QApplication([]) 
    window   = Login()
    app.exec_()