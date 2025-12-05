import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from maxheap import MaxHeap
import csv
import os


class NilaiEditorPopup(tk.Toplevel):
    """Popup editor nilai (Treeview) — tambah / edit / hapus nilai per siswa."""
    def __init__(self, parent, nilai_list):
        super().__init__(parent)
        self.title("Editor Nilai")
        self.geometry("320x360")
        self.resizable(False, False)
        self.parent = parent

        self.nilai_list = list(nilai_list)  

        # Treeview untuk menampilkan nilai
        cols = ("index", "nilai")
        self.tree = ttk.Treeview(self, columns=cols, show="headings", height=10)
        self.tree.heading("index", text="#")
        self.tree.heading("nilai", text="Nilai")
        self.tree.column("index", width=40, anchor="center")
        self.tree.column("nilai", width=200, anchor="center")
        self.tree.pack(padx=10, pady=(10,5), fill="x")

        # tombol small row actions
        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=6)

        ttk.Button(btn_frame, text="Tambah", command=self.tambah_nilai).grid(row=0, column=0, padx=4)
        ttk.Button(btn_frame, text="Edit", command=self.edit_nilai).grid(row=0, column=1, padx=4)
        ttk.Button(btn_frame, text="Hapus", command=self.hapus_nilai).grid(row=0, column=2, padx=4)

        # Save / Cancel
        action_frame = tk.Frame(self)
        action_frame.pack(fill="x", pady=10)
        ttk.Button(action_frame, text="Simpan & Tutup", command=self.simpan).pack(side="left", padx=10)
        ttk.Button(action_frame, text="Batal", command=self.batal).pack(side="right", padx=10)

        self.populate_tree()

    def populate_tree(self):
        for r in self.tree.get_children():
            self.tree.delete(r)
        for i, val in enumerate(self.nilai_list, start=1):
            self.tree.insert("", "end", values=(i, f"{val:.2f}" if isinstance(val, float) else val))

    def tambah_nilai(self):
        v = simpledialog.askstring("Tambah Nilai", "Masukkan nilai (0-100):", parent=self)
        if v is None: return
        try:
            n = float(v)
            if not (0 <= n <= 100):
                raise ValueError
        except:
            messagebox.showerror("Error", "Nilai harus angka 0–100!", parent=self)
            return
        self.nilai_list.append(n)
        self.populate_tree()

    def edit_nilai(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Pilih baris", "Pilih nilai yang ingin diedit.", parent=self)
            return
        idx = int(self.tree.item(sel[0])["values"][0]) - 1
        v = simpledialog.askstring("Edit Nilai", "Masukkan nilai (0-100):", initialvalue=str(self.nilai_list[idx]), parent=self)
        if v is None: return
        try:
            n = float(v)
            if not (0 <= n <= 100):
                raise ValueError
        except:
            messagebox.showerror("Error", "Nilai harus angka 0–100!", parent=self)
            return
        self.nilai_list[idx] = n
        self.populate_tree()

    def hapus_nilai(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Pilih baris", "Pilih nilai yang ingin dihapus.", parent=self)
            return
        idx = int(self.tree.item(sel[0])["values"][0]) - 1
        confirm = messagebox.askyesno("Konfirmasi", f"Hapus nilai ke-{idx+1} ?", parent=self)
        if not confirm: return
        self.nilai_list.pop(idx)
        self.populate_tree()

    def simpan(self):
        self.result = self.nilai_list
        self.destroy()

    def batal(self):
        self.result = None
        self.destroy()

class KategoriEditorPopup(tk.Toplevel):
    """Popup edit kategori: nama kategori tidak diubah, nilai + bobot (%) bisa diedit."""
    def __init__(self, parent, nilai_list, bobot_list):
        super().__init__(parent)
        self.title("Editor Nilai & Bobot")
        self.geometry("350x380")
        self.resizable(False, False)

        self.nilai_list = list(nilai_list)
        self.bobot_list = list(bobot_list)

        cols = ("idx", "nilai", "bobot")
        self.tree = ttk.Treeview(self, columns=cols, show="headings", height=10)
        self.tree.heading("idx", text="#")
        self.tree.heading("nilai", text="Nilai")
        self.tree.heading("bobot", text="Bobot (%)")
        self.tree.column("idx", width=40, anchor="center")
        self.tree.column("nilai", width=100, anchor="center")
        self.tree.column("bobot", width=100, anchor="center")
        self.tree.pack(padx=10, pady=10)

        self.populate()

        btn = tk.Frame(self)
        btn.pack(pady=6)
        ttk.Button(btn, text="Edit", command=self.edit).grid(row=0, column=0, padx=4)

        action = tk.Frame(self)
        action.pack(pady=10)
        ttk.Button(action, text="Simpan", command=self.simpan).pack(side="left", padx=10)
        ttk.Button(action, text="Batal", command=self.batal).pack(side="right", padx=10)

    def populate(self):
        for r in self.tree.get_children():
            self.tree.delete(r)
        for i,(n,b) in enumerate(zip(self.nilai_list, self.bobot_list), start=1):
            self.tree.insert("", "end", values=(i, n, b))

    def edit(self):
        sel = self.tree.selection()
        if not sel:
            return
        idx = int(self.tree.item(sel[0])['values'][0]) - 1

        v = simpledialog.askstring("Edit nilai", "Nilai:", initialvalue=str(self.nilai_list[idx]))
        b = simpledialog.askstring("Edit bobot (%)", "Bobot:", initialvalue=str(self.bobot_list[idx]))

        if v is None or b is None: return

        try:
            v = float(v)
            b = float(b)
        except:
            messagebox.showerror("Error", "Nilai & bobot harus angka.")
            return

        self.nilai_list[idx] = v
        self.bobot_list[idx] = b
        self.populate()

    def simpan(self):
        self.result = (self.nilai_list, self.bobot_list)
        self.destroy()

    def batal(self):
        self.result = None
        self.destroy()

class AplikasiRataMapel:
    def __init__(self, root):
        self.root = root
        self.root.title("Hitung Rata-Rata Mapel - MaxHeap (Dilengkapi Editor)")
        self.root.geometry("980x650")
        self.root.configure(bg="#f0f2f5")

        self.records_rata = {}          
        self.records_kategori = {}      
        self.kategori_kkm = {}         

        self.heap_rata = MaxHeap()
        self.heap_per_kelas = {}
        self.heap_kategori_global = {}
        self.heap_kategori_per_kelas = {}

        self.current_selected = None

        self.load_rata_from_csv()
        self.load_kategori_from_csv()
        self.rebuild_heaps_rata()
        self.rebuild_heaps_kategori()
        style = ttk.Style()
        style.theme_use("default")

        style.configure("Treeview",
                        rowheight=25,
                        bordercolor="#d9d9d9",
                        borderwidth=1,
                        relief="solid")

        style.configure("Treeview.Heading",
                        bordercolor="#d9d9d9",
                        borderwidth=1,
                        relief="solid")

        style.map("Treeview", background=[("selected", "#cce6ff")])
        style.layout("Treeview", [("Treeview.treearea", {"sticky": "nswe"})])

        self.frame_menu = tk.Frame(root, bg="#f0f2f5")
        self.frame_rata = tk.Frame(root, bg="#f0f2f5")
        self.frame_kategori = tk.Frame(root, bg="#f0f2f5")
        self.frame_lihat = tk.Frame(root, bg="#f0f2f5")

        self.show_menu()

    # Menu 
    def open_kategori(self):
        self.frame_menu.pack_forget()
        self.frame_kategori.pack(fill="both", expand=True)
        self.setup_ui_kategori_mapel()

    def open_rata_mapel(self):
        self.frame_menu.pack_forget()
        self.frame_rata.pack(fill="both", expand=True)
        self.setup_ui_rata_mapel()

    def open_lihat_peringkat(self):
        self.frame_menu.pack_forget()
        self.frame_rata.pack_forget()
        self.frame_kategori.pack_forget()

        self.frame_lihat.pack(fill="both", expand=True)
        self.setup_ui_lihat()

    def show_menu(self):
        for f in (self.frame_rata, self.frame_kategori):
            f.pack_forget()

        self.frame_menu.pack(fill="both", expand=True)
        tk.Label(self.frame_menu,
                text="Selamat Datang di Sistem Pemeringkatan Nilai Siswa",
                font=("Segoe UI", 20, "bold"),
                bg="#f0f2f5").pack(pady=40)

        tk.Label(self.frame_menu,
                text="Silakan pilih mode pemeringkatan yang ingin digunakan:",
                font=("Segoe UI", 12),
                bg="#f0f2f5").pack(pady=10)

        tk.Button(self.frame_menu, text="Peringkat Setiap Pelajaran",
                font=("Segoe UI", 12), width=30,
                command=self.open_kategori).pack(pady=10)
        tk.Button(self.frame_menu, text="Peringkat Seluruh Pelajaran",
                font=("Segoe UI", 12), width=30,
                command=self.open_rata_mapel).pack(pady=20)
        tk.Button(self.frame_menu, text="Lihat Peringkat",
                font=("Segoe UI", 12), width=30,
                command=self.open_lihat_peringkat).pack(pady=10)


    # UI Rata-mapel 
    def setup_ui_rata_mapel(self):
        for w in self.frame_rata.winfo_children():
            w.destroy()

        header = tk.Frame(self.frame_rata, bg="#343a40", pady=15)
        header.pack(fill="x")
        tk.Label(header, text="Pemeringkatan Berdasarkan Nilai Seluruh Mapel",
                 font=("Segoe UI", 16, "bold"), bg="#343a40", fg="white").pack()

        main_frame = tk.Frame(self.frame_rata, bg="#f0f2f5")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        left_panel = tk.LabelFrame(main_frame, text="Input Nilai Semua Mapel", padx=15, pady=15,
                                   bg="white", font=("Segoe UI", 11, "bold"))
        left_panel.pack(side="left", fill="y")

        tk.Label(left_panel, text="Nama:", bg="white").pack(anchor="w")
        self.entry_nama = ttk.Entry(left_panel, width=25)
        self.entry_nama.pack()

        tk.Label(left_panel, text="Kelas:", bg="white").pack(anchor="w")
        self.entry_kelas = ttk.Entry(left_panel, width=25)
        self.entry_kelas.pack()

        tk.Label(left_panel, text="Jumlah Mapel:", bg="white").pack(anchor="w")
        self.entry_jumlah_mapel = ttk.Entry(left_panel, width=25)
        self.entry_jumlah_mapel.pack()

        ttk.Button(left_panel, text="Buat Input Mapel", command=self.generate_mapel_input).pack(pady=5)

        self.mapel_frame = tk.Frame(left_panel, bg="white")
        self.mapel_frame.pack(fill="x", pady=10)
        self.mapel_entries = []

        ttk.Button(left_panel, text="Edit Nilai", command=self.open_popup_nilai_from_form).pack(pady=5)

        btn_frame = tk.Frame(left_panel, bg="white")
        btn_frame.pack(pady=6)
        ttk.Button(btn_frame, text="Input", command=self.hitung_dan_tambah).grid(row=0, column=0, padx=4)
        ttk.Button(btn_frame, text="Update", command=self.handle_update_rata).grid(row=0, column=1, padx=4)
        ttk.Button(btn_frame, text="Hapus", command=self.handle_delete_rata).grid(row=0, column=2, padx=4)

        ttk.Separator(left_panel).pack(fill="x", pady=8)

        tk.Label(left_panel, text="Mode Peringkat:", bg="white").pack(anchor="w")
        self.mode_var = tk.StringVar(value="Global")

        tk.Radiobutton(left_panel, text="Global", variable=self.mode_var,
                    value="Global", bg="white",
                    command=self.on_mode_change).pack(anchor="w")

        tk.Radiobutton(left_panel, text="Per Kelas", variable=self.mode_var,
                    value="PerKelas", bg="white",
                    command=self.on_mode_change).pack(anchor="w")

        self.kelas_var = tk.StringVar()
        self.dropdown_kelas = ttk.Combobox(left_panel, textvariable=self.kelas_var,
                                   state="disabled", width=22)
        self.dropdown_kelas.pack(pady=5)
        self.dropdown_kelas.bind("<<ComboboxSelected>>", lambda e: self.refresh_table())

        right_panel = tk.LabelFrame(main_frame, text="Peringkat Nilai", bg="white",
                                    font=("Segoe UI", 11, "bold"))
        right_panel.pack(side="right", fill="both", expand=True)

        cols = ("nama", "kelas", "nilai", "rank")
        self.tree = ttk.Treeview(right_panel, columns=cols, show="headings")

        self.tree.heading("nama", text="Nama")
        self.tree.heading("kelas", text="Kelas")
        self.tree.heading("nilai", text="Nilai")
        self.tree.heading("rank", text="Ranking")

        self.tree.column("nama", width=150)
        self.tree.column("kelas", width=80, anchor="center")
        self.tree.column("nilai", width=80, anchor="center")
        self.tree.column("rank", width=80, anchor="center")

        self.tree.pack(fill="both", expand=True, padx=5, pady=5)

        self.tree.bind("<<TreeviewSelect>>", self.on_select_rata)
        self.update_dropdown()
        self.on_mode_change()
        self.refresh_table()

    # UI per mapel
    def setup_ui_kategori_mapel(self):
        for w in self.frame_kategori.winfo_children():
            w.destroy()

        header = tk.Frame(self.frame_kategori, bg="#343a40", pady=15)
        header.pack(fill="x")
        tk.Label(header, text="Pemeringkatan Berdasarkan Kategori per Mapel",
                font=("Segoe UI", 16, "bold"), bg="#343a40", fg="white").pack()

        main = tk.Frame(self.frame_kategori, bg="#f0f2f5")
        main.pack(fill="both", expand=True, padx=20, pady=20)

        left = tk.LabelFrame(main, text="Input Nilai per Mapel", bg="white",
                            font=("Segoe UI", 11, "bold"), padx=15, pady=15)
        left.pack(side="left", fill="y")

        tk.Label(left, text="Nama:", bg="white").pack(anchor="w")
        self.kat_nama = ttk.Entry(left, width=25)
        self.kat_nama.pack()

        tk.Label(left, text="Kelas:", bg="white").pack(anchor="w")
        self.kat_kelas = ttk.Entry(left, width=25)
        self.kat_kelas.pack()

        tk.Label(left, text="Mapel:", bg="white").pack(anchor="w")
        self.kat_mapel = ttk.Entry(left, width=25)
        self.kat_mapel.pack()

        tk.Label(left, text="Jumlah Kategori:", bg="white").pack(anchor="w")
        self.entry_jumlah_kategori = ttk.Entry(left, width=25)
        self.entry_jumlah_kategori.pack()

        ttk.Button(left, text="Buat Input Kategori", command=self.generate_kategori_input).pack(pady=5)

        tk.Label(left, text="KKM:", bg="white").pack(anchor="w")
        self.entry_kkm_kat = ttk.Entry(left, width=10)
        self.entry_kkm_kat.pack(pady=5)

        self.kategori_frame = tk.Frame(left, bg="white")
        self.kategori_frame.pack(fill="x", pady=10)
        self.kategori_entries = []

        ttk.Button(left, text="Edit Nilai", command=self.open_popup_kategori_from_form).pack(pady=5)

        btn_frame = tk.Frame(left, bg="white")
        btn_frame.pack(pady=6)
        ttk.Button(btn_frame, text="Input", command=self.hitung_kategori).grid(row=0, column=0, padx=4)
        ttk.Button(btn_frame, text="Update", command=self.handle_update_kategori).grid(row=0, column=1, padx=4)
        ttk.Button(btn_frame, text="Hapus", command=self.handle_delete_kategori).grid(row=0, column=2, padx=4)

        ttk.Separator(left).pack(fill="x", pady=10)

        tk.Label(left, text="Mode Peringkat:", bg="white").pack(anchor="w")
        self.mode_kat_var = tk.StringVar(value="Global")

        tk.Radiobutton(left, text="Global", variable=self.mode_kat_var,
                    value="Global", bg="white",
                    command=self.on_mode_change_kategori).pack(anchor="w")

        tk.Radiobutton(
            left,
            text="Per Kelas",
            variable=self.mode_kat_var,
            value="PerKelas",
            bg="white",
            command=self.on_mode_change_kategori
        ).pack(anchor="w")


        self.kat_kelas_var = tk.StringVar()
        self.dropdown_kelas_kat = ttk.Combobox(left, textvariable=self.kat_kelas_var,
                                            width=20, state="disabled")
        self.dropdown_kelas_kat.pack(pady=5)
        self.dropdown_kelas_kat.bind("<<ComboboxSelected>>", lambda e: self.refresh_tabel_kategori())

        right = tk.LabelFrame(main, text="Peringkat Nilai Setiap Mapel", bg="white",
                            font=("Segoe UI", 11, "bold"))
        right.pack(side="right", fill="both", expand=True)

        cols = ("mapel", "rank", "nama", "kelas", "nilai", "status")
        self.tree_kategori = ttk.Treeview(right, columns=cols, show="headings")

        self.tree_kategori.heading("mapel", text="Mapel")
        self.tree_kategori.heading("rank", text="Peringkat")
        self.tree_kategori.heading("nama", text="Nama")
        self.tree_kategori.heading("kelas", text="Kelas")
        self.tree_kategori.heading("nilai", text="Nilai")
        self.tree_kategori.heading("status", text="Status")

        self.tree_kategori.column("mapel", width=120)
        self.tree_kategori.column("rank", width=60, anchor="center")
        self.tree_kategori.column("nama", width=150)
        self.tree_kategori.column("kelas", width=80, anchor="center")
        self.tree_kategori.column("nilai", width=80, anchor="center")
        self.tree_kategori.column("status", width=90, anchor="center")

        self.tree_kategori.pack(fill="both", expand=True, padx=5, pady=5)

        self.tree_kategori.bind("<<TreeviewSelect>>", self.on_select_kategori)
        self.update_dropdown_kategori()
        self.on_mode_change_kategori()
        self.refresh_tabel_kategori()

    def setup_ui_lihat(self):
        for w in self.frame_lihat.winfo_children():
            w.destroy()

        header = tk.Frame(self.frame_lihat, bg="#343a40", pady=15)
        header.pack(fill="x")
        tk.Label(header, text="Lihat Peringkat Nilai",
                font=("Segoe UI", 16, "bold"), bg="#343a40", fg="white").pack()

        main = tk.Frame(self.frame_lihat, bg="#f0f2f5")
        main.pack(fill="both", expand=True, padx=20, pady=20)

        left = tk.LabelFrame(main, text="Mode Lihat Data", bg="white",
                            font=("Segoe UI", 11, "bold"), padx=15, pady=15)
        left.pack(side="left", fill="y")

        tk.Label(left, text="Mode:", bg="white").pack(anchor="w")

        self.lihat_mode = tk.StringVar(value="Global")

        tk.Radiobutton(left, text="Global", bg="white",
                    variable=self.lihat_mode, value="Global",
                    command=self.refresh_tabel_lihat).pack(anchor="w")

        tk.Radiobutton(left, text="Per Kelas", bg="white",
                    variable=self.lihat_mode, value="PerKelas",
                    command=self.refresh_tabel_lihat).pack(anchor="w")

        self.lihat_kelas_var = tk.StringVar()
        self.dropdown_lihat_kelas = ttk.Combobox(left, width=20,
                                                textvariable=self.lihat_kelas_var,
                                                state="disabled")
        self.dropdown_lihat_kelas.pack(pady=5)

        self.dropdown_lihat_kelas.bind("<<ComboboxSelected>>",
                                    lambda e: self.refresh_tabel_lihat())

        right = tk.LabelFrame(main, text="Peringkat Nilai", bg="white",
                            font=("Segoe UI", 11, "bold"))
        right.pack(side="right", fill="both", expand=True)

        cols = ("nama", "kelas", "nilai", "rank")
        self.tree_lihat = ttk.Treeview(right, columns=cols, show="headings")

        self.tree_lihat.heading("nama", text="Nama")
        self.tree_lihat.heading("kelas", text="Kelas")
        self.tree_lihat.heading("nilai", text="Nilai")
        self.tree_lihat.heading("rank", text="Rank")

        self.tree_lihat.column("nama", width=150)
        self.tree_lihat.column("kelas", width=80, anchor="center")
        self.tree_lihat.column("nilai", width=80, anchor="center")
        self.tree_lihat.column("rank", width=80, anchor="center")

        self.tree_lihat.pack(fill="both", expand=True, padx=5, pady=5)

        kelas_list = sorted(self.heap_per_kelas.keys())
        self.dropdown_lihat_kelas["values"] = kelas_list
        if kelas_list:
            self.lihat_kelas_var.set(kelas_list[0])

        self.refresh_tabel_lihat()

    # Generate inputs 
    def generate_mapel_input(self):
        for widget in self.mapel_frame.winfo_children():
            widget.destroy()

        try:
            jumlah = int(self.entry_jumlah_mapel.get())
        except:
            messagebox.showwarning("Perhatian", "Jumlah mapel harus angka, kosongkan apabila ingin pakai popup.")
            return

        self.mapel_entries = []
        for i in range(jumlah):
            row = tk.Frame(self.mapel_frame, bg="white")
            row.pack(fill="x", pady=3)
            tk.Label(row, text=f"Mapel {i+1}:", bg="white", width=10).pack(side="left")
            entry_nama = ttk.Entry(row, width=18)
            entry_nama.pack(side="left", padx=5)
            entry_nama.insert(0, f"Mapel{i+1}")
            entry_nilai = ttk.Entry(row, width=10)
            entry_nilai.pack(side="left", padx=5)
            self.mapel_entries.append((entry_nama, entry_nilai))

    def generate_kategori_input(self):
        for w in self.kategori_frame.winfo_children():
            w.destroy()

        try:
            jumlah = int(self.entry_jumlah_kategori.get())
        except:
            messagebox.showwarning("Perhatian", "Jumlah input harus angka.")
            return

        self.kategori_entries = []
        for i in range(jumlah):
            baris = tk.Frame(self.kategori_frame, bg="white")
            baris.pack(fill="x", pady=3)

            tk.Label(baris, text=f"Kategori {i+1}:", bg="white").pack(side="left")

            entry_nama = ttk.Entry(baris, width=15)
            entry_nama.pack(side="left", padx=5)
            entry_nama.insert(0, f"Kategori{i+1}")

            entry_nilai = ttk.Entry(baris, width=8)
            entry_nilai.pack(side="left", padx=5)

            entry_bobot = ttk.Entry(baris, width=8)
            entry_bobot.pack(side="left", padx=5)
            entry_bobot.insert(0, "0")   

            self.kategori_entries.append((entry_nama, entry_nilai, entry_bobot))
            
    # Popup openers 
    def open_popup_nilai_from_form(self):
        """Buka popup editor dan simpan hasil di self._popup_nilai_list (for rata mode)."""
        nilai_list = []
        if getattr(self, "mapel_entries", None):
            for en_name, en_nilai in self.mapel_entries:
                txt = en_nilai.get().strip()
                if txt != "":
                    try:
                        n = float(txt)
                        nilai_list.append(n)
                    except:
                        messagebox.showerror("Error", "Nilai mapel harus angka 0-100!")
                        return
        if self.current_selected and self.current_selected[0] == "rata":
            key = self.current_selected[1]
            if key in self.records_rata:
                nilai_list = list(self.records_rata[key]["nilai"])

        popup = NilaiEditorPopup(self.root, nilai_list)
        self.root.wait_window(popup)
        if hasattr(popup, "result") and popup.result is not None:
            self._popup_nilai_list = popup.result
            messagebox.showinfo("Sukses", f"Nilai tersimpan ({len(self._popup_nilai_list)} item).")
        else:
            pass

    def open_popup_kategori_from_form(self):
        nilai_list = []
        bobot_list = []

        if getattr(self, "kategori_entries", None):
            for en_nama, en_nilai, en_bobot in self.kategori_entries:
                val = en_nilai.get().strip()
                bob = en_bobot.get().strip()

                if val != "":
                    try:
                        nilai_list.append(float(val))
                        bobot_list.append(float(bob))
                    except:
                        messagebox.showerror("Error", "Nilai & bobot harus angka!")
                        return

        if self.current_selected and self.current_selected[0] == "kategori":
            key = self.current_selected[1]
            if key in self.records_kategori:
                nilai_list = list(self.records_kategori[key]["nilai"])
                bobot_list = list(self.records_kategori[key]["bobot"])

        popup = KategoriEditorPopup(self.root, nilai_list, bobot_list)
        self.root.wait_window(popup)

        if hasattr(popup, "result") and popup.result is not None:
            self._popup_kategori_list = popup.result[0]
            self._popup_bobot_list = popup.result[1]
            messagebox.showinfo("Sukses", "Nilai & bobot berhasil disimpan.")


    # Add / Update / Delete Rata 
    def hitung_dan_tambah(self):
        nama = self.entry_nama.get().strip()
        kelas = self.entry_kelas.get().strip().lower()
        if not nama or not kelas:
            messagebox.showerror("Error", "Nama dan Kelas wajib diisi!")
            return

        nilai_mapel = []
        if hasattr(self, "_popup_nilai_list"):
            nilai_mapel = list(self._popup_nilai_list)
        else:
            for entry_nama, entry_nilai in getattr(self, "mapel_entries", []):
                txt = entry_nilai.get().strip()
                if txt == "":
                    continue
                try:
                    n = float(txt)
                    nilai_mapel.append(n)
                except:
                    messagebox.showerror("Error", "Nilai mapel harus angka 0–100!")
                    return

        if not nilai_mapel:
            messagebox.showerror("Error", "Tidak ada nilai mapel! (pakai popup atau input mapel)")
            return

        rata = sum(nilai_mapel) / len(nilai_mapel)
        key = (nama.lower(), kelas.lower())

        self.records_rata[key] = {
            "nama": nama,
            "kelas": kelas,
            "nilai": list(nilai_mapel),
            "rata": rata
        }

        self.rebuild_heaps_rata()

        self.update_dropdown()
        self.refresh_table()
        self.save_rata_to_csv()
        messagebox.showinfo("Berhasil", f"Rata-rata {nama} = {rata:.2f} berhasil ditambahkan.")


    def handle_update_rata(self):
        if not self.current_selected or self.current_selected[0] != "rata":
            messagebox.showwarning("Pilih siswa", "Klik baris di tabel ranking untuk memilih siswa yang ingin diupdate.")
            return
        key = self.current_selected[1]
        if key not in self.records_rata:
            messagebox.showerror("Error", "Data tidak ditemukan.")
            return

        nama_baru = self.entry_nama.get().strip()
        kelas_baru = self.entry_kelas.get().strip()
        if not nama_baru or not kelas_baru:
            messagebox.showerror("Error", "Nama dan Kelas wajib diisi!")
            return

        if hasattr(self, "_popup_nilai_list"):
            nilai_baru = list(self._popup_nilai_list)
        else:
            nilai_baru = []
            for entry_nama, entry_nilai in getattr(self, "mapel_entries", []):
                txt = entry_nilai.get().strip()
                if txt == "":
                    continue
                try:
                    n = float(txt)
                    nilai_baru.append(n)
                except:
                    messagebox.showerror("Error", "Nilai mapel harus angka 0–100!")
                    return
            if not nilai_baru:
                messagebox.showerror("Error", "Tidak ada nilai mapel! (pakai popup atau input mapel)")
                return

        rata_baru = sum(nilai_baru) / len(nilai_baru)

        try:
            del self.records_rata[key]
        except KeyError:
            pass

        new_key = (nama_baru.lower(), kelas_baru.lower())
        self.records_rata[new_key] = {
            "nama": nama_baru,
            "kelas": kelas_baru.lower(),
            "nilai": list(nilai_baru),
            "rata": rata_baru
        }

        if hasattr(self, "_popup_nilai_list"):
            del self._popup_nilai_list

        self.rebuild_heaps_rata()
        self.update_dropdown()
        self.refresh_table()
        self.save_rata_to_csv()
        messagebox.showinfo("Berhasil", f"Data {nama_baru} berhasil diupdate.")

    def handle_delete_rata(self):
        if not self.current_selected or self.current_selected[0] != "rata":
            messagebox.showwarning("Pilih siswa", "Klik baris di tabel ranking untuk memilih siswa yang ingin dihapus.")
            return
        key = self.current_selected[1]
        if key not in self.records_rata:
            messagebox.showerror("Error", "Data tidak ditemukan.")
            return
        nama = self.records_rata[key]["nama"]
        confirm = messagebox.askyesno("Konfirmasi", f"Hapus data {nama} ?")
        if not confirm:
            return
        del self.records_rata[key]
        if hasattr(self, "_popup_nilai_list"):
            del self._popup_nilai_list
        self.rebuild_heaps_rata()
        self.update_dropdown()
        self.refresh_table()
        self.save_rata_to_csv()
        messagebox.showinfo("Berhasil", f"Data {nama} berhasil dihapus.")

    # Add / Update / Delete Kategori 
    def hitung_kategori(self):
        try:
            kkm = float(self.entry_kkm_kat.get())
        except:
            messagebox.showerror("Error", "KKM harus berupa angka!")
            return

        nama = self.kat_nama.get().strip()
        kelas = self.kat_kelas.get().strip().lower()
        mapel = self.kat_mapel.get().strip()

        if not nama or not kelas or not mapel:
            messagebox.showerror("Error", "Nama, Kelas, dan Mapel wajib diisi!")
            return

        self.kategori_kkm[mapel] = kkm

        nilai_list = []
        bobot_list = []

        if hasattr(self, "_popup_kategori_list"):
            nilai_list = list(self._popup_kategori_list)
            bobot_list = list(self._popup_bobot_list)
        else:
            for en_nama, en_nilai, en_bobot in getattr(self, "kategori_entries", []):
                v = en_nilai.get().strip()
                b = en_bobot.get().strip()
                if v:
                    try:
                        nilai_list.append(float(v))
                        bobot_list.append(float(b))
                    except:
                        messagebox.showerror("Error", "Nilai & Bobot harus berupa angka!")
                        return

        if not nilai_list:
            messagebox.showerror("Error", "Tidak ada input kategori.")
            return

        if sum(bobot_list) != 100:
            messagebox.showerror("Error", "Total bobot harus = 100%.")
            return

        nilai_akhir = sum(n*(b/100) for n,b in zip(nilai_list, bobot_list))

        key = (mapel.lower(), nama.lower(), kelas)
        self.records_kategori[key] = {
            "mapel": mapel,
            "nama": nama,
            "kelas": kelas,
            "nilai": list(nilai_list),
            "bobot": list(bobot_list),
            "rata": nilai_akhir
        }

        self.rebuild_heaps_kategori()
        self.update_dropdown_kategori()
        self.save_kategori_to_csv()
        self.refresh_tabel_kategori()


    def handle_update_kategori(self):
        if not self.current_selected or self.current_selected[0] != "kategori":
            messagebox.showwarning("Pilih siswa", "Klik baris di tabel kategori untuk memilih data yang ingin diupdate.")
            return

        key = self.current_selected[1]
        if key not in self.records_kategori:
            messagebox.showerror("Error", "Data tidak ditemukan.")
            return

        nama_baru = self.kat_nama.get().strip()
        kelas_baru = self.kat_kelas.get().strip().lower()
        mapel_baru = self.kat_mapel.get().strip()

        if not nama_baru or not kelas_baru or not mapel_baru:
            messagebox.showerror("Error", "Nama, Kelas, dan Mapel wajib diisi!")
            return

        if hasattr(self, "_popup_kategori_list"):
            nilai_baru = list(self._popup_kategori_list)
            bobot_baru = list(self._popup_bobot_list)
        else:
            nilai_baru = []
            bobot_baru = []
            for _, en_nilai, en_bobot in getattr(self, "kategori_entries", []):
                v = en_nilai.get().strip()
                b = en_bobot.get().strip()
                if v:
                    try:
                        nilai_baru.append(float(v))
                        bobot_baru.append(float(b))
                    except:
                        messagebox.showerror("Error", "Nilai & bobot harus angka!")
                        return

        if not nilai_baru:
            messagebox.showerror("Error", "Tidak ada input kategori!")
            return

        if sum(bobot_baru) != 100:
            messagebox.showerror("Error", "Total bobot harus 100%.")
            return

        nilai_akhir_baru = sum(n*(b/100) for n,b in zip(nilai_baru, bobot_baru))

        del self.records_kategori[key]

        new_key = (mapel_baru.lower(), nama_baru.lower(), kelas_baru)

        self.records_kategori[new_key] = {
            "mapel": mapel_baru,
            "nama": nama_baru,
            "kelas": kelas_baru,
            "nilai": nilai_baru,
            "bobot": bobot_baru,
            "rata": nilai_akhir_baru
        }

        if hasattr(self, "_popup_kategori_list"):
            del self._popup_kategori_list
            del self._popup_bobot_list

        self.rebuild_heaps_kategori()
        self.update_dropdown_kategori()
        self.save_kategori_to_csv()
        self.refresh_tabel_kategori()

        messagebox.showinfo("Berhasil", f"Data {nama_baru} pada mapel {mapel_baru} berhasil diupdate.")

    def handle_delete_kategori(self):
        if not self.current_selected or self.current_selected[0] != "kategori":
            messagebox.showwarning("Pilih data", "Klik baris di tabel kategori untuk memilih data yang ingin dihapus.")
            return
        key = self.current_selected[1]
        if key not in self.records_kategori:
            messagebox.showerror("Error", "Data tidak ditemukan.")
            return
        nama = self.records_kategori[key]["nama"]
        mapel = self.records_kategori[key]["mapel"]
        confirm = messagebox.askyesno("Konfirmasi", f"Hapus data {nama} pada mapel {mapel} ?")
        if not confirm:
            return
        del self.records_kategori[key]
        if hasattr(self, "_popup_kategori_list"):
            del self._popup_kategori_list
        self.rebuild_heaps_kategori()
        self.update_dropdown_kategori()
        self.refresh_tabel_kategori()
        messagebox.showinfo("Berhasil", f"Data {nama} pada mapel {mapel} berhasil dihapus.")

    # Helpers: rebuild heaps from records 
    def rebuild_heaps_rata(self):
        # reset
        self.heap_rata = MaxHeap()
        self.heap_per_kelas = {}

        for key, rec in self.records_rata.items():
            nama = rec["nama"]
            kelas = rec["kelas"]
            rata = rec["rata"]
            self.heap_rata.insert(nama, rata, kelas)
            if kelas not in self.heap_per_kelas:
                self.heap_per_kelas[kelas] = MaxHeap()
            self.heap_per_kelas[kelas].insert(nama, rata, kelas)

    def rebuild_heaps_kategori(self):
        self.heap_kategori_global = {}
        self.heap_kategori_per_kelas = {}

        for key, rec in self.records_kategori.items():
            mapel = rec["mapel"]
            nama = rec["nama"]
            kelas = rec["kelas"]
            rata = rec["rata"]

            if mapel not in self.heap_kategori_global:
                self.heap_kategori_global[mapel] = MaxHeap()
            self.heap_kategori_global[mapel].insert(nama, rata, kelas)

            if mapel not in self.heap_kategori_per_kelas:
                self.heap_kategori_per_kelas[mapel] = {}
            if kelas not in self.heap_kategori_per_kelas[mapel]:
                self.heap_kategori_per_kelas[mapel][kelas] = MaxHeap()
            self.heap_kategori_per_kelas[mapel][kelas].insert(nama, rata, kelas)

    def update_dropdown(self):
        kelas_list = sorted(self.heap_per_kelas.keys())
        self.dropdown_kelas['values'] = kelas_list
        if kelas_list:
            if self.kelas_var.get() == "":
                self.kelas_var.set(kelas_list[0])

    def update_dropdown_kategori(self):
        kelas_set = set()
        for mapel in self.heap_kategori_per_kelas:
            for k in self.heap_kategori_per_kelas[mapel].keys():
                kelas_set.add(k.lower())

        kelas_list = sorted(kelas_set)
        self.dropdown_kelas_kat["values"] = kelas_list

        if kelas_list and (self.kat_kelas_var.get() == "" or self.kat_kelas_var.get() not in kelas_list):
            self.kat_kelas_var.set(kelas_list[0])


    def refresh_table(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        mode = self.mode_var.get()
        if mode == "Global":
            data = self.heap_rata.get_sorted_data()
        else:
            kelas = self.kelas_var.get()
            if kelas not in self.heap_per_kelas:
                return
            data = self.heap_per_kelas[kelas].get_sorted_data()

        for i, s in enumerate(data, start=1):
            self.tree.insert(
                "",
                "end",
                values=(
                    s['nama'],            
                    s['kelas'],           
                    f"{s['nilai']:.2f}",  
                    i                     
                )
            )

    def refresh_tabel_lihat(self):
        for i in self.tree_lihat.get_children():
            self.tree_lihat.delete(i)

        mode = self.lihat_mode.get()

        if mode == "Global":
            self.dropdown_lihat_kelas.configure(state="disabled")
            data = self.heap_rata.get_sorted_data()

        else:  
            self.dropdown_lihat_kelas.configure(state="readonly")
            kelas = self.lihat_kelas_var.get()
            if kelas not in self.heap_per_kelas:
                return
            data = self.heap_per_kelas[kelas].get_sorted_data()

        for i, s in enumerate(data, start=1):
            self.tree_lihat.insert(
                "",
                "end",
                values=(s["nama"], s["kelas"], f"{s['nilai']:.2f}", i)
            )


    def refresh_tabel_kategori(self):
        for i in self.tree_kategori.get_children():
            self.tree_kategori.delete(i)

        mode = self.mode_kat_var.get()

        if mode == "Global":
            for mapel, heap in self.heap_kategori_global.items():
                rank = 1
                data = heap.get_sorted_data()

                for s in data:
                    nilai_akhir = s.get("rata", s.get("nilai", 0))
                    kkm = self.kategori_kkm.get(mapel, 0)

                    status = "Lulus" if nilai_akhir >= kkm else "Remedial"

                    self.tree_kategori.insert(
                        "",
                        "end",
                        values=(mapel, rank, s["nama"], s["kelas"], f"{nilai_akhir:.2f}", status)
                    )
                    rank += 1

        else:
            kelas = self.kat_kelas_var.get()

            for mapel in self.heap_kategori_per_kelas:
                if kelas not in self.heap_kategori_per_kelas[mapel]:
                    continue

                rank = 1
                data = self.heap_kategori_per_kelas[mapel][kelas].get_sorted_data()

                for s in data:
                    nilai_akhir = s.get("rata", s.get("nilai", 0))
                    kkm = self.kategori_kkm.get(mapel, 0)

                    status = "Lulus" if nilai_akhir >= kkm else "Remedial"

                    self.tree_kategori.insert(
                        "",
                        "end",
                        values=(mapel, rank, s["nama"], s["kelas"], f"{nilai_akhir:.2f}", status)
                    )
                    rank += 1

    def on_select_kategori(self, event):
        sel = self.tree_kategori.selection()
        if not sel:
            return

        vals = self.tree_kategori.item(sel[0])["values"]

        mapel = vals[0]
        nama = vals[2]
        kelas = vals[3]

        key = (mapel.lower(), nama.lower(), kelas.lower())

        print("TRY KAT KEY:", key)

        if key not in self.records_kategori:
            print("KEY KATEGORI TIDAK COCOK:", key)
            return

        rec = self.records_kategori[key]

        self.kat_nama.delete(0, tk.END)
        self.kat_nama.insert(0, rec["nama"])

        self.kat_kelas.delete(0, tk.END)
        self.kat_kelas.insert(0, rec["kelas"])

        self.kat_mapel.delete(0, tk.END)
        self.kat_mapel.insert(0, rec["mapel"])

        for w in self.kategori_frame.winfo_children():
            w.destroy()
        self.kategori_entries = []

        self.current_selected = ("kategori", key)

        self._popup_kategori_list = list(rec["nilai"])
        self._popup_bobot_list = list(rec["bobot"])

    def on_select_rata(self, event):
        sel = self.tree.selection()
        if not sel:
            return

        vals = self.tree.item(sel[0])["values"]

        nama = vals[0]
        kelas = vals[1]

        key = (nama.lower(), kelas.lower())       
        print("TRY RATA KEY:", key)

        if key not in self.records_rata:
            print("KEY RATA TIDAK COCOK:", key)
            return

        rec = self.records_rata[key]

        self.entry_nama.delete(0, tk.END)
        self.entry_nama.insert(0, rec["nama"])

        self.entry_kelas.delete(0, tk.END)
        self.entry_kelas.insert(0, rec["kelas"])

        for w in self.mapel_frame.winfo_children():
            w.destroy()

        self.mapel_entries = []
        self.current_selected = ("rata", key)

        self._popup_nilai_list = list(rec["nilai"])

    def on_mode_change(self):
        mode = self.mode_var.get()
        if mode == "Global":
            self.dropdown_kelas.configure(state="disabled")
        else:
            self.dropdown_kelas.configure(state="readonly")
        self.refresh_table()
    
    def on_mode_change_kategori(self):
        mode = self.mode_kat_var.get()
        if mode == "Global":
            self.dropdown_kelas_kat.configure(state="disabled")
        else:
            # isi ulang dropdown kelas
            self.update_dropdown_kategori()
            kelas_list = list(self.dropdown_kelas_kat["values"])
            if kelas_list:
                if self.kat_kelas_var.get() == "" or self.kat_kelas_var.get() not in kelas_list:
                    self.kat_kelas_var.set(kelas_list[0])
            self.dropdown_kelas_kat.configure(state="readonly")

        self.refresh_tabel_kategori()


    def save_rata_to_csv(self):
        with open("keseluruhan_mapel.csv", "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["nama", "kelas", "nilai_list", "rata"])
            for rec in self.records_rata.values():
                writer.writerow([
                    rec["nama"],
                    rec["kelas"],
                    ";".join(str(n) for n in rec["nilai"]),
                    rec["rata"]
                ])

    def save_kategori_to_csv(self):
        with open("per_mapel.csv", "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["mapel", "nama", "kelas", "nilai_list", "bobot_list", "rata", "kkm"])
            for key, rec in self.records_kategori.items():
                mapel = rec["mapel"]
                kkm = self.kategori_kkm.get(mapel, 75)
                writer.writerow([
                    rec["mapel"],
                    rec["nama"],
                    rec["kelas"],
                    ";".join(str(n) for n in rec["nilai"]),
                    ";".join(str(b) for b in rec["bobot"]),
                    rec["rata"],
                    kkm
                ])

    def load_rata_from_csv(self):
        if not os.path.exists("keseluruhan_mapel.csv"):
            return
        with open("keseluruhan_mapel.csv", "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                nilai_list = [float(x) for x in row["nilai_list"].split(";")] if row["nilai_list"] else []
                rata = float(row["rata"])
                key = (row["nama"].lower(), row["kelas"].lower())
                self.records_rata[key] = {
                    "nama": row["nama"],
                    "kelas": row["kelas"].lower(),
                    "nilai": nilai_list,
                    "rata": rata
                }

    def load_kategori_from_csv(self):
        if not os.path.exists("per_mapel.csv"):
            return

        with open("per_mapel.csv", "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                
                nilai_list = []
                if row["nilai_list"]:
                    nilai_list = [float(x) for x in row["nilai_list"].split(";")]

                bobot_list = []
                if row["bobot_list"]:
                    bobot_list = [float(x) for x in row["bobot_list"].split(";")]

                rata = float(row["rata"])
                mapel = row["mapel"]

                nama_lc = row["nama"].lower()
                kelas_lc = row["kelas"].lower()
                mapel_lc = mapel.lower()

                key = (mapel_lc, nama_lc, kelas_lc)

                self.records_kategori[key] = {
                    "mapel": row["mapel"],
                    "nama": row["nama"],
                    "kelas": row["kelas"].lower(),
                    "nilai": nilai_list,
                    "bobot": bobot_list,
                    "rata": rata
                }

                self.kategori_kkm[mapel] = float(row["kkm"])

        self.rebuild_heaps_kategori()

# main
if __name__ == "__main__":
    root = tk.Tk()
    app = AplikasiRataMapel(root)
    root.mainloop()
