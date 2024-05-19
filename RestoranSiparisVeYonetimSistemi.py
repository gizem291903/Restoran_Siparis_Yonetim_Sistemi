import sqlite3
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import random

class Ürün:
    def __init__(self, yemek_adı, fiyatı, stok_durumu):
        self.yemek_adı = yemek_adı
        self.fiyatı = fiyatı
        self.stok_durumu = stok_durumu

    def ürün_ekle(self, conn):
        cursor = conn.cursor()
        cursor.execute("INSERT INTO ürünler (yemek_adı, fiyatı, stok_durumu) VALUES (?, ?, ?)",
                       (self.yemek_adı, self.fiyatı, self.stok_durumu))
        conn.commit()
        cursor.close()

    @staticmethod
    def stok_güncelle(conn, yemek_adı, miktar):
        cursor = conn.cursor()
        cursor.execute("UPDATE ürünler SET stok_durumu = stok_durumu - ? WHERE yemek_adı = ?", (miktar, yemek_adı))
        conn.commit()
        cursor.close()

class Sipariş:
    def __init__(self, sipariş_numarası, içerik, müşteri_bilgileri):
        self.sipariş_numarası = sipariş_numarası
        self.içerik = içerik
        self.müşteri_bilgileri = müşteri_bilgileri

class Müşteri:
    def __init__(self, müşteri_adı, soyadı, adresi):
        self.müşteri_adı = müşteri_adı
        self.soyadı = soyadı
        self.adresi = adresi

    def sipariş_ver(self, conn, sipariş_tarihi, içerik):
        cursor = conn.cursor()
        cursor.execute("INSERT INTO müşteriler (müşteri_adı, soyadı, adresi, sipariş_geçmişi, sipariş_tarihi) VALUES (?, ?, ?, ?, ?)",
                       (self.müşteri_adı, self.soyadı, self.adresi, içerik, sipariş_tarihi))
        conn.commit()
        cursor.close()

class RestoranUygulaması:
    def __init__(self, pencere):
        self.pencere = pencere
        self.pencere.title("Restoran ve Sipariş Yönetim Sistemi")

        self.müşteriler_label = tk.Label(pencere, text="Müşteriler")
        self.müşteriler_label.pack()

        self.müşteri_listesi = tk.Listbox(pencere, width=50)
        self.müşteri_listesi.pack()

        self.ürünler_label = tk.Label(pencere, text="Ürünler")
        self.ürünler_label.pack()

        self.ürün_listesi = tk.Listbox(pencere, width=50, selectmode=tk.MULTIPLE)
        self.ürün_listesi.pack()

        self.sipariş_alan_frame = tk.Frame(pencere)
        self.sipariş_alan_frame.pack()

        self.müşteri_adı_label = tk.Label(self.sipariş_alan_frame, text="Müşteri Adı:")
        self.müşteri_adı_label.grid(row=0, column=0)
        self.müşteri_adı_entry = tk.Entry(self.sipariş_alan_frame)
        self.müşteri_adı_entry.grid(row=0, column=1)

        self.müşteri_soyadı_label = tk.Label(self.sipariş_alan_frame, text="Müşteri Soyadı:")
        self.müşteri_soyadı_label.grid(row=1, column=0)
        self.müşteri_soyadı_entry = tk.Entry(self.sipariş_alan_frame)
        self.müşteri_soyadı_entry.grid(row=1, column=1)

        self.müşteri_adresi_label = tk.Label(self.sipariş_alan_frame, text="Müşteri Adresi:")
        self.müşteri_adresi_label.grid(row=2, column=0)
        self.müşteri_adresi_entry = tk.Entry(self.sipariş_alan_frame)
        self.müşteri_adresi_entry.grid(row=2, column=1)

        self.sipariş_tarihi_label = tk.Label(self.sipariş_alan_frame, text="Sipariş Tarihi:")
        self.sipariş_tarihi_label.grid(row=3, column=0)
        self.sipariş_tarihi_entry = tk.Entry(self.sipariş_alan_frame)
        self.sipariş_tarihi_entry.grid(row=3, column=1)

        self.sipariş_al_button = tk.Button(self.sipariş_alan_frame, text="Sipariş Al", command=self.sipariş_al)
        self.sipariş_al_button.grid(row=4, columnspan=2)

        self.kaydet_button = tk.Button(pencere, text="Kaydet", command=self.kaydet)
        self.kaydet_button.pack()

        self.ürünleri_güncelle()
        self.müşterileri_güncelle()

    def ürünleri_güncelle(self):
        conn = sqlite3.connect('restoran.db')
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS ürünler
                          (yemek_adı TEXT, fiyatı REAL, stok_durumu INTEGER)''')

        # Örnek ürünler ekleyelim ve fiyatlarını %20 artıralım
        örnek_ürünler = [
            ("Pizza", round(random.uniform(15, 25), 2), random.randint(5, 20)),
            ("Hamburger", round(random.uniform(10, 20), 2), random.randint(10, 30)),
            ("Kebap", round(random.uniform(20, 35), 2), random.randint(5, 15)),
            ("Salata", round(random.uniform(8, 15), 2), random.randint(15, 25)),
            ("Pasta", round(random.uniform(10, 18), 2), random.randint(8, 20)),
            ("Kola", round(random.uniform(2, 5), 2), random.randint(30, 60)),
            ("Limonata", round(random.uniform(2, 4), 2), random.randint(20, 40)),
            ("Su", round(random.uniform(0.5, 2), 2), random.randint(50, 100)),
            ("Çay", round(random.uniform(1, 2), 2), random.randint(40, 80)),
            ("Kahve", round(random.uniform(3, 6), 2), random.randint(20, 40))
        ]
        for ürün in örnek_ürünler:
            cursor.execute("INSERT INTO ürünler (yemek_adı, fiyatı, stok_durumu) VALUES (?, ?, ?)", ürün)

        cursor.execute("SELECT yemek_adı, fiyatı, stok_durumu FROM ürünler")
        ürünler = cursor.fetchall()
        for ürün in ürünler:
            self.ürün_listesi.insert(tk.END, f"{ürün[0]} - Fiyat: {ürün[1]} TL - Stok: {ürün[2]} adet")
        conn.close()

    def müşterileri_güncelle(self):
        conn = sqlite3.connect('restoran.db')
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS müşteriler
                          (müşteri_adı TEXT, soyadı TEXT, adresi TEXT, sipariş_geçmişi TEXT, sipariş_tarihi TEXT)''')

        # Sipariş tarihi sütununu kontrol et
        cursor.execute("PRAGMA table_info(müşteriler)")
        columns = cursor.fetchall()
        column_names = [column[1] for column in columns]
        if 'sipariş_tarihi' not in column_names:
            cursor.execute("ALTER TABLE müşteriler ADD COLUMN sipariş_tarihi TEXT")

        conn.commit()  # Yapılan değişiklikleri kaydet

        # Yalnızca yeni sipariş alınan müşterileri ekle
        cursor.execute("SELECT müşteri_adı, soyadı FROM müşteriler")
        mevcut_müşteriler = [(müşteri[0], müşteri[1]) for müşteri in cursor.fetchall()]
        for müşteri in mevcut_müşteriler:
            if müşteri[0] + " " + müşteri[1] not in self.müşteri_listesi.get(0, tk.END):
                self.müşteri_listesi.insert(tk.END, müşteri[0] + " " + müşteri[1])

        # Tıklama olayını ekle
        self.müşteri_listesi.bind("<Double-Button-1>", self.müşteriye_tıklandı)

        conn.close()

    def müşteriye_tıklandı(self, event):
        seçili_müşteri = self.müşteri_listesi.curselection()
        if len(seçili_müşteri) == 0:
            return

        seçili_müşteri_index = seçili_müşteri[0]
        müşteri_adı_soyadı = self.müşteri_listesi.get(seçili_müşteri_index)
        müşteri_adı, müşteri_soyadı = müşteri_adı_soyadı.split()

        conn = sqlite3.connect('restoran.db')
        cursor = conn.cursor()
        cursor.execute("SELECT sipariş_geçmişi, sipariş_tarihi FROM müşteriler WHERE müşteri_adı = ? AND soyadı = ?",
                       (müşteri_adı, müşteri_soyadı))
        müşteri_bilgisi = cursor.fetchone()

        if müşteri_bilgisi:
            sipariş_geçmişi, sipariş_tarihi = müşteri_bilgisi
            sipariş_listesi = sipariş_geçmişi.split(', ')
            self.sipariş_geçmişi_popup(müşteri_adı_soyadı, sipariş_listesi, sipariş_tarihi)
        else:
            messagebox.showinfo("Müşteri Sipariş Geçmişi",
                                f"{müşteri_adı_soyadı} adlı müşterinin henüz siparişi bulunmamaktadır.")

        conn.close()

    def sipariş_geçmişi_popup(self, müşteri_adı_soyadı, sipariş_listesi, sipariş_tarihi):
        popup = tk.Toplevel()
        popup.title("Müşteri Sipariş Geçmişi")

        tree = ttk.Treeview(popup, columns=("Ürün", "Sipariş Tarihi"))
        tree.heading("#0", text="Sıra No.")
        tree.heading("#1", text="Ürün")
        tree.heading("#2", text="Sipariş Tarihi")

        for index, ürün in enumerate(sipariş_listesi, start=1):
            tree.insert("", tk.END, text=index, values=(ürün, sipariş_tarihi))

        tree.pack(expand=True, fill=tk.BOTH)

        info_label = tk.Label(popup, text=f"{müşteri_adı_soyadı} adlı müşterinin sipariş geçmişi:")
        info_label.pack()

        popup.mainloop()

    def sipariş_al(self):
        conn = sqlite3.connect('restoran.db')  # Bağlantıyı aç
        try:
            seçili_ürünler = self.ürün_listesi.curselection()
            if len(seçili_ürünler) == 0:
                messagebox.showerror("Hata", "Lütfen bir ürün seçin.")
                return

            müşteri_adı = self.müşteri_adı_entry.get().strip()
            müşteri_soyadı = self.müşteri_soyadı_entry.get().strip()
            müşteri_adresi = self.müşteri_adresi_entry.get().strip()
            sipariş_tarihi = self.sipariş_tarihi_entry.get().strip()

            if not müşteri_adı or not müşteri_soyadı or not müşteri_adresi or not sipariş_tarihi:
                messagebox.showerror("Hata", "Lütfen müşteri bilgilerini ve sipariş tarihini eksiksiz girin.")
                return

            seçili_ürünler_list = [self.ürün_listesi.get(index) for index in seçili_ürünler]

            # Sipariş alındığında stoktan düşme işlemi
            for ürün_str in seçili_ürünler_list:
                ürün_adı = ürün_str.split(' - ')[0]
                miktar = 1  # Her üründen bir tane sipariş edildiğini varsayalım
                Ürün.stok_güncelle(conn, ürün_adı, miktar)

            müşteri = Müşteri(müşteri_adı, müşteri_soyadı, müşteri_adresi)
            müşteri.sipariş_ver(conn, sipariş_tarihi, ", ".join(seçili_ürünler_list))
            messagebox.showinfo("Sipariş Alındı",
                                f"{seçili_ürünler_list} siparişi, {müşteri_adı} {müşteri_soyadı} adlı müşteriye {sipariş_tarihi} tarihinde alındı.")
            self.müşterileri_güncelle()
        finally:
            conn.close()  # Bağlantıyı kapatmayı unutmayın

    def kaydet(self):
        # Bu kısımda seçili ürünleri ve müşteri bilgilerini veritabanına kaydetme işlemleri yapılabilir
        pass

# Ana uygulama döngüsü
if __name__ == "__main__":
    pencere = tk.Tk()
    uygulama = RestoranUygulaması(pencere)
    pencere.mainloop()


