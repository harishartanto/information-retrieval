import tkinter
from tkinter import messagebox
from tkinter import scrolledtext
import customtkinter
from DatabaseSystem import *

class App(customtkinter.CTk):
    def __init__(self):
        global icon_path
        super().__init__()

        self.title("Document Search")
        icon_path = os.path.join(os.path.dirname(__file__))+"/icon.ico"
        self.iconbitmap(icon_path)
        
        # ============ create two frames ============
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.frame_top = customtkinter.CTkFrame(master=self, height=80)
        self.frame_top.grid(row=0, column=0, sticky="nswe", padx=20, pady=(20, 10))

        self.frame_bottom = customtkinter.CTkFrame(master=self)
        self.frame_bottom.grid(row=1, column=0, sticky="nswe", padx=20, pady=(10, 20))

        # ============ create widgets ============
        self.frame_top.columnconfigure(0, weight=1)
        self.frame_bottom.columnconfigure(0, weight=1)
        self.frame_bottom.rowconfigure(0, weight=1)

        # entry box
        self.entry_search = customtkinter.CTkEntry(master=self.frame_top, placeholder_text="Kata Kunci")
        self.entry_search.grid(row=0, column=0, columnspan=2, pady=20, padx=20, sticky="we")

        # button search
        self.button_search = customtkinter.CTkButton(master=self.frame_top, text="Cari", width=100, height=30, command=self.search)
        self.button_search.grid(row=0, column=2, columnspan=1, pady=20, padx=20, sticky="we")

        # button reset
        self.button_reset = customtkinter.CTkButton(master=self.frame_top, text="Reset", width=100, height=30, command=self.reset_search)
        self.button_reset.grid(row=0, column=3, columnspan=1, pady=20, padx=20, sticky="we")
        
        # scrollbar
        self.scrollbar = tkinter.Scrollbar(master=self.frame_bottom)
        self.scrollbar.grid(row=0, column=1, sticky="ns", padx=(0, 20), pady=(20, 20))
        
        # treeview
        style = tkinter.ttk.Style()
        style.configure("mystyle.Treeview", highlightthickness=0, bd=0, font=('Helectiva', 10)) # Modify the font of the body
        style.configure("mystyle.Treeview.Heading", font=('Helectiva', 11, 'bold')) # Modify the font of the headings
        style.layout("mystyle.Treeview", [('mystyle.Treeview.treearea', {'sticky': 'nswe'})]) # Remove the borders

        self.cols = ('JUDUL BERITA',)
        self.listBox = tkinter.ttk.Treeview(self.frame_bottom, columns = self.cols, show='headings', style="mystyle.Treeview", yscrollcommand=self.scrollbar.set)
        self.listBox.column(self.cols[0], width = 500, anchor='center')
        self.scrollbar.config(command=self.listBox.yview)
        
        for col in self.cols:
            self.listBox.heading(col, text=col)
            self.listBox.grid(row=0, column=0, sticky="nswe", padx=(20, 0), pady=20)

        # button detail
        self.button_detail = customtkinter.CTkButton(master=self.frame_bottom, text="Lihat Isi Berita Terpilih", height=30, command=self.detail)
        self.button_detail.grid(row=1, column=0, columnspan=2, padx=20, sticky="we")

        # switch theme
        self.switch_theme = customtkinter.CTkSwitch(master=self.frame_bottom,
                                                text="Dark Mode",
                                                command=self.change_mode)
        self.switch_theme.grid(row=2, column=0, pady=10, padx=20, sticky="w")

    def change_mode(self):
        if self.switch_theme.get() == 1:
            customtkinter.set_appearance_mode("Dark")
        else:
            customtkinter.set_appearance_mode("Light")

    def start(self):
        self.mainloop()

    def show_all(self):
        doc = ts.show_title()

        for i, (judul) in enumerate(doc, start=1):
            self.listBox.insert('', 'end', values=(judul))

    def search(self):
        if self.entry_search.get() == "":
            self.listBox.delete(*self.listBox.get_children())
            App.show_all(self)
        else:
            self.listBox.delete(*self.listBox.get_children())
            query = self.entry_search.get()

            idteks = ts.show_id()
            list_idteks = ts.sql_to_list(idteks)

            content = ts.show_content()
            list_content = ts.sql_to_list(content)

            list_querycontent = ts.combine_query_content(query, list_content)

            tokenizing_list_querycontent = ts.tokenizing(list_querycontent)
            stopword_list_querycontent = ts.stopword_removal(tokenizing_list_querycontent)
            casefolding_list_querycontent = ts.case_folding(stopword_list_querycontent)
            stemming_list_querycontent = ts.stemming(casefolding_list_querycontent)
            clean_list_querycontent = ts.clean_doc(stemming_list_querycontent)

            clean_list_content = ts.get_content(clean_list_querycontent)

            list_word_content = ts.get_list_word(clean_list_content)

            tf = ts.get_tf(clean_list_querycontent, list_word_content)
            idf = ts.get_idf(tf, list_word_content)
            wqt = ts.get_wqt(tf, idf)

            cos_sim = ts.get_vsm(tf, wqt)

            if cos_sim == []:
                messagebox.showwarning(title='Pencarian', message=(f'Pencarian "{query}" tidak ditemukan!'))
                self.listBox.delete(*self.listBox.get_children())
                App.show_all(self)
            else:
                result_list, result_string = ts.get_result_order(cos_sim, list_idteks)
                final_result = ts.show_result(result_list, result_string)

                for i, (judul) in enumerate(final_result, start=1):
                    self.listBox.insert("", "end", values=(judul))
    
    def reset_search(self):
        self.listBox.delete(*self.listBox.get_children())
        self.entry_search.delete(0, 'end')
        App.show_all(self)

    def detail(self):
        curItems = self.listBox.selection()  
        if self.listBox.selection() == ():
            messagebox.showinfo(title='Isi Dokumen', message='Pilih satu dokumen yang ingin dilihat terlebih dahulu!')
        elif len(curItems) > 1:
            messagebox.showinfo(title='Isi Dokumen', message='Pilih satu dokumen saja!')
        else:
            top = customtkinter.CTkToplevel()
            top.geometry("780x520")
            top.title("Isi Dokumen")
            top.iconbitmap(icon_path)
            pilihan = self.listBox.selection()[0]
            judul = self.listBox.item(pilihan, "values")[0]
            isi = ts.show_single_content(judul)
            list_isi = ts.sql_to_list(isi)
            clean_isi = list_isi[0]

            self.frame_top_detail = customtkinter.CTkFrame(master=top, height=50)
            self.frame_bottom_detail = customtkinter.CTkFrame(master=top, height=1000)
            self.frame_top_detail.pack(padx=20, pady=(20, 10), expand=True, fill='x')
            self.frame_bottom_detail.pack(padx=20, pady=(10, 20), expand=True, fill='x')
            
            # label
            self.label_title = customtkinter.CTkLabel(self.frame_top_detail, text=judul)
            self.label_title.pack(padx=20, pady=20, expand=True, fill='x')
            self.label_title.config(font=("Helectiva", 20, "bold"))

            # text box
            self.text_box = scrolledtext.ScrolledText(self.frame_bottom_detail, height=900, wrap='word')
            self.text_box.pack(padx=20, pady=20, expand=True, fill='x')
            self.text_box.insert('insert', clean_isi)
            self.text_box.config(state='disabled', font=('Helectiva', 12))

if __name__ == "__main__":
    db = Database()
    ts = Text_Search()
    app = App()
    app.show_all()
    app.start()