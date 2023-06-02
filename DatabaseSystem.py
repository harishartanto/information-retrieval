import sqlite3
import os.path
from math import log10, sqrt
from nltk.tokenize import RegexpTokenizer
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory

class Database:
    my_db = my_cursor = None
    
    def __init__(self):
        global my_db, my_cursor
        file_path = os.path.join(os.path.dirname(__file__)
                                 )+"/db_dokumen/dokumen.db"
        my_db = sqlite3.connect(os.path.realpath(file_path))
        my_cursor = my_db.cursor()

class Text_Search(Database):

    def show_id(self, mode='ASC'):
        sql = 'SELECT id_teks FROM teks ORDER BY id_teks {}'.format(mode)
        
        try:
            my_cursor.execute(sql)
            result = my_cursor.fetchall()
        except Exception as e:
            return e
        
        return result

    def show_content(self, mode='ASC'):
        '''
        Method untuk menampilkan seluruh isi dokumen dari database, yang diurutkan secara ascending berdasarkan id_teks
        '''
        sql = 'SELECT isi FROM teks ORDER BY id_teks {}'.format(mode)
        
        try:
            my_cursor.execute(sql)
            result = my_cursor.fetchall()
        except Exception as e:
            return e
        
        return result

    def show_title(self, mode='ASC'):
        '''
        Method untuk menampilkan seluruh judul dokumen dari database, yang diurutkan secara ascending berdasarkan id_teks.
        '''
        sql = 'SELECT judul FROM teks ORDER BY id_teks {}'.format(mode)
        
        try:
            my_cursor.execute(sql)
            result_title = my_cursor.fetchall()
        except Exception as e:
            return e
        
        return result_title

    def show_single_content(self, judul):
        sql = 'SELECT isi FROM teks WHERE judul = "{}"'.format(str(judul))
        
        try:
            my_cursor.execute(sql)
            result = my_cursor.fetchall()
        except Exception as e:
            return e
        
        return result

    def sql_to_list(self, data):
        '''
        Method untuk mengubah list of tuple [(),(),()] menjadi list of string ['', '', '']
        '''
        
        # Pertama, bentuk list of tuple diubah menjadi list 2D [[], [], []]
        list_2d = [list(x) for x in data]
        # Kedua, setiap elemen list 2D diubah menjadi list 1D ['', '', '']
        list_1d = [s for S in list_2d for s in S]
        # Cara lain list_1d = list_1d = [_ for i in range(len(list_a)) for _ in list_a[i]]

        return list_1d

    def tokenizing(self, doc):
        '''
        Method untuk proses tokenisasi.
        '''
        tokenizer = RegexpTokenizer(r'\w+')
        tokenizing_doc = []
        # Untuk setiap dokumen di dalam list,
        # dikenakan str.lower() untuk mengubah semua huruf menjadi huruf kecil,
        # kemudian, menggunakan fungsi word_tokenize() untuk melakukan tokenisasi
        for x in doc:
            lowerdoc = x.lower()
            proses_token = tokenizer.tokenize(lowerdoc)
            tokenizing_doc.append(proses_token)
            # Setelah dilakukan tokenisasi, hasilnya akan dimasukkan ke dalam tokenizing_doc
            # Hasil akhir dari tokenisasi adalah list 2D, tokenizing_doc = [[], [], []]
        return tokenizing_doc

    def stopword_removal(self, doc):
        '''
        Method untuk menghapus kata umum yang sering muncul dan dianggap tidak bermakna.
        '''
        
        # Inisialisasi StopWordRemoverFactory dari SasTrawi
        stopwords_factory = StopWordRemoverFactory()
        # Mendapatkan daftar kata umum yang tidak bermakna, disimpan dalam variabel stopwords dalam bentuk list []
        stopwords = stopwords_factory.get_stop_words()
        sw_doc = []
        # mengubah bentuk list [] menjadi tuple () agar dapat diproses
        tuple_stopword = tuple(stopwords)
        i = 0
        # Untuk setiap a (list [], []) di dalam doc (list [[], []])
        for a in doc:
            # Dimasukkan [] ke dalam list sw_doc sebanyak panjang a
            sw_doc.append([])
            # Untuk setiap b (kata 'a','b') di dalam a (list ['a','b'])
            for b in a:
                # Jika b tidak ada di dalam list stopword, maka b dimasukkan ke dalam list sw_doc
                if b not in tuple_stopword:
                    sw_doc[i].append(b)
            i += 1 
        # Hasil akhir dari proses stopword removal adalah list 2D, sw_doc = [[], [], []]
        return sw_doc

    def case_folding(self, doc):
        '''
        Method untuk menghapus karaktek selain huruf A-Z dan a-z.
        '''

        case_folding_doc = []
        i = 0
        # Untuk setiap a (list [], []) di dalam doc (list [[], []])
        for a in doc:
            # Dimasukkan [] ke dalam list case_folding_doc sebanyak panjang a
            case_folding_doc.append([])
            # Untuk setiap b (kata 'a','b') di dalam a (list ['a','b'])
            for b in a:
                # Jika b (kata 'a','b') yang dikenakan str.isalpha() = True, maka b dimasukkan ke dalam list case_folding_doc
                if b.isalpha():
                    case_folding_doc[i].append(b)
            i += 1
        # Hasil akhir dari proses case folding adalah list 2D, case_folding_doc = [[], [], []]
        return case_folding_doc

    def stemming(self, doc):
        '''
        Method untuk proses stemming.
        '''
        
        # Inisialisasi StemmerFactory dari SasTrawi
        factory = StemmerFactory()
        stemmer = factory.create_stemmer()
        stemmed_doc = []

        i = 0
        # Untuk setiap a (list [], []) di dalam doc (list [[], []])
        for a in doc:
            # Dimasukkan [] ke dalam list stemmed_doc sebanyak panjang a
            stemmed_doc.append([])
            # Untuk setiap b (kata 'a','b') di dalam a (list ['a','b'])
            for b in a:
                # Dilakukan proses stemming terhadap b (kata), lalu dimasukkan ke dalam list stemmed_doc
                stemmed_doc[i].append(stemmer.stem(b))
            i += 1
        # Hasil akhir dari proses stemming adalah list 2D, stemmed_doc = [[], [], []]
        return stemmed_doc
    
    def clean_doc(self, doc):
        '''
        Method untuk menggabungkan list 2D [['',''], ['','']] menjadi list 1D ['', '']
        '''
        
        readydoc = []
        i = 0
        # Untuk setiap x (list [], []) di dalam doc (list [[], []])
        for x in doc:
            # Kata dalam list 1D akan digabungkan menjadi 1 kalimat denngan pemisah spasi menggunakan method ' '.join()
            # Setelah itu akan di masukkan ke dalam list readydoc
            readydoc.append((' '.join(map(str, doc[i]))))
            i += 1
        # Hasil akhir dari proses clean doc adalah list 1D, readydoc = ['', '']  
        return readydoc

    def get_list_word(self, readydoc):
        '''
        Method untuk mendapatkan semua kata yang muncul dalam dokumen.
        '''
        
        list_word = []
        # Untuk setiap kalimat ('', '') di dalam readydoc (list ['', ''])
        for sentence in readydoc:
            # Untuk setiap kata di dalam kalimat, akan dipisah menjadi list ['', '']
            for word in sentence.split(" "):
                # Jika kata belum/tidak ada di dalam list_word, maka kata akan dimasukkan ke dalam list_word
                if word not in list_word:
                    list_word.append(word)
        # Dilakukan pengurutan kata dari abjad terkecil ke terbesar (a-z)
        sorted_word = sorted(list_word)
        # Hasil akhir dari get_list_word adalah list 1D, list_word = ['', '']
        return sorted_word

    def get_content(self, doc):
        '''
        Method untuk mendapatkan kalimat dokumen dari list gabungan query dan dokumen.
        '''
        
        # Ekstrak indeks ke-1 sampai terakhir dari list karena dokumen berada pada indeks ke-1 sampai terkahir
        return doc[1:]

    def combine_query_content(self, query, content):
        '''
        Method untuk menggabungkan query dan dokumen menjadi list.
        Query diletakkan pada indeks ke-0
        '''
        
        # Membuat salinan dari list dokumen
        combined_list = content.copy()
        # Menambahkan query pada indeks ke-0 ke dalam salinan list dokumen
        combined_list.insert(0, query)
        # Hasil akhir dari combine_query_content adalah list 1D
        return combined_list

    def get_tf(self, clean_list_querycontent, list_word_content):
        '''
        Method untuk mendapatkan frekuensi kemunculan kata dalam query dan dokumen.
        '''

        # Mendapatkan panjang list querycontent
        length_list_querycontent = len(clean_list_querycontent)

        tf = []
        # tf =[{'kata1' : 0,
        #       'kata2' : 0},
        #      {'kata1' : 0
        #       'kata2' : 0}]

        # Membuat template tf dengan value awal = 0
        # Untuk setiap x dari panjang list querycontent
        for x in range(length_list_querycontent):
            # tf merupakan list of dictionary dengan key yang berupa kata dalam list_word_content
            tf.append(dict(zip(list_word_content, [0 for x in range(len(list_word_content))])))

        # tf =[{'kata1' : 1,
        #       'kata2' : 0},
        #      {'kata1' : 0
        #       'kata2' : 1}]

        # Perulangan untuk mengisi value tf dengan frekuensi kata yang muncul dalam query dan dokumen
        # Untuk setiap indeks dan kalimat dalam list clean_list_querycontent
        for index, sentence in enumerate(clean_list_querycontent):
            # Untuk setiap kata di dalam kalimat, akan dipisah menjadi list ['', '']
            for word in sentence.split(" "):
                # Jika kata ada dalam template tf, 
                # maka value pada template tf dari kata tersebut akan ditambah 1
                if word in tf[index]:
                    tf[index][word] += 1

        return tf
    
    def get_idf(self, tf, list_word_content):
        '''
        Method untuk menghitung nilai IDF
        '''

        # Mendapatkan panjang list content
        length_list_content = len(tf) - 1
        
        # Membuat template df dengan value awal = 0
        df = dict(zip(list_word_content, [0 for x in range(len(list_word_content))]))
        # df = {'kata1' : 0,
        #       'kata2' : 0}

        # Perulangan untuk mengisi value df dengan frekuensi kata dalam dokumen
        # Untuk setiap indeks [{}, {}] dan document (dict) {}, {} dalam tf
        for index, document in enumerate(tf):
            # Jika indeks > 0, (indeks = 0 adalah query)
            if index > 0 :
                # Untuk setiap key dan value dalam document (dict) {'kata1' : 0, 'kata2' : 0}
                for key, value in document.items():
                    # Jika value ada, maka value pada df dari key tersebut akan ditambah 1
                    if value:
                        df[key] += 1

        # d_df menampung nilai dari d/df
        d_df = {}
        # d_df = {'kata1' : d/df,
        #         'kata2' : d/df}

        # Perulangan untuk mengisi value d_df dengan nilai d/df
        # Untuk setiap key dan value dalam df {'kata1' : 1, 'kata2' : 1}
        for key, value in df.items():
            # Value dari d_df dari key dalam df adalah d (length_list_content)/df dari key df
            d_df[key] = length_list_content / value

        # idf menampung nilai dari idf
        idf = {}
        # idf = {'kata1' : log(d/df),
        #        'kata2' : log(d/df)}

        # Perulangan untuk mengisi value idf dengan nilai idf (log(d/df))
        # Untuk setiap key dan value dalam d_df {'kata1' : d/df, 'kata2' : d/df}
        for key, value in d_df.items():
            # Value dari idf dari key dalam d_df adalah log(d_df) dari key d_df
            # Dilakukan pembulatan 3 angka di belakang koma
            idf[key] = log10(value)

        # Hasil akhir dari get_idf adalah dictionary {'kata1' : idf, 'kata2' : idf}
        return idf

    def get_wqt(self, tf, idf):
        '''
        Method untuk menghitung nilai TF-IDF atau bobot kata (Wqt)
        '''
        
        wqt = []

        # Untuk setiap indeks [{}, {}] dan document (dict) {}, {} dalam tf
        for index, document in enumerate(tf):
            # Dimasukkan {} ke dalam list wqt sebanyak panjang tf
            wqt.append({})
            # Untuk setiap key dan value dalam document (dict) {'kata1' : 1, 'kata2' : 1}
            for key, value in document.items():
                # Value dari wqt dari indeks dan key dalam document adalah tf x idf dari key idf
                wqt[index][key] = value * idf[key]

        # Hasil akhir dari get_wqt adalah list of dictionary [{'kata1' : wqt, 'kata2' : wqt}, {'kata1' : wqt, 'kata2' : wqt}]
        return wqt

    # Method untuk menghitung nilai Cosine Similarity
    def get_vsm(self, tf, wqt):
        
        length_list_content = len(tf) - 1

        # ww = Wqt^2
        ww = []
        ## ww = [{'kata1' : wqt^2, 
        #         'kata2' : wqt^2}, 
        #        {'kata1' : wqt^2, 
        #         'kata2' : wqt^2}]
        
        wq = {}

        total_ww_doc = {}

        # tf_ww = TF x Wq^2
        wq_wd = []
        # tf_ww = [{'kata1' : value}, 
        #          {'kata2' : value}]

        # sum_tf_ww = Penjumlahan semua value dari tf_ww masing-masing dokumen
        sum_wq_wd = {}
        # sum_tf_ww = {'Bobot dokumen 1' : value, 'Bobot dokumen 2' : value}

        # result = Cosine Similarity = sum(Wq^2 x TF) dokumen(i) / (sum(sqrt(Wq^2)) x sum(sqrt(Wt^2 dokumen(i))))
        result = []
        
        #Coba
        try:
            # Untuk setiap indeks [{}, {}] dan document (dict) {}, {} dalam wqt
            for index, document in enumerate(wqt):
                # Dimasukkan {} ke dalam ww sebanyak panjang wqt
                ww.append({})
                # Membuat key-value baru 
                total = 0
                # Untuk setiap key dan value dalam document (dict) {'kata1': 1, 'kata2': 1}   
                for key, value in document.items():
                    # Value dari ww dari indeks dan key dalam document adalah value dari key dalam document yang dipangkat 2
                    # Dilakukan pembulatan 3 angka di belakang koma
                    ww[index][key] = value ** 2
                    # Value dari total adalah penjumlahan value dari key dalam document yang dipangkat 2
                    total += ww[index][key]
                # Value dari total diakarkan, dengan pembulatan 3 angka di belakang koma
                ww[index]['total'] = sqrt(total)

            a = wqt[0]
            for key, value in a.items():
                if value > 0:
                    wq[key] = value

            # Untuk setiap indeks [{}, {}] dan document (dict) {}, {} dalam ww
            for index, document in enumerate(ww):
                # Untuk setiap key dan value dalam document (dict) {'kata1' : wqt^2, 'kata2' : wqt^2}
                for key, value in document.items():
                    # jika key = 'total' 
                    if key == 'total':
                        # Jika indeks = 0
                        if index == 0:
                            # Value dari total_ww_doc dengan key=Bobot pencarian adalah value dari document dalam ww
                            total_ww_doc['Bobot pencarian'] = value
                        # Jika indeks bukan = 0
                        else:
                            # Value dari total_ww_doc dengan key=Bobot dokumen {index} adalah value dari document dalam ww
                            total_ww_doc[f'Bobot dokumen {index}'] = value            

            # Perulangan untuk mendapatkan nilai Wq^2 x TF
            # Untuk setiap indeks [{}, {}] dan document (dict) {}, {} dalam tf
            for index, document in enumerate(wqt):
                # Jika indeks > 0
                if index > 0:
                    # Dimasukkan {} ke dalam tf_ww sebanyak panjang tf (index > 0)
                    wq_wd.append({})
                    # Untuk setiap key dan value dalam document (dict) {'kata1' : value, 'kata2' : value}
                    for key, value in document.items():
                        # Jika key ada dalam ww_query
                        if key in wq:
                            # Value dari tf_ww dari indeks-1 dan key dalam document adalah 
                            # value dari key dalam document yang dikali dengan value dari ww_query dengan key yang sama
                            wq_wd[index-1][key] = value * wq[key]

            # Perulangan untuk mendapatkan nilai penjumalahan semua value dari tf_ww masing-masing dokumen
            # Untuk setiap indeks [{}, {}] dan document (dict) {}, {} dalam tf_ww
            for index, document in enumerate(wq_wd):
                # Inisialisasi total =  0
                total = 0
                # Untuk setiap value dalam document (dict) {'kata1' : value, 'kata2' : value}
                for _, value in document.items():
                    # total = total + value
                    total += value
                # Value dari sum_tf_ww dengan key=Bobot dokumen {index+1} adalah total
                sum_wq_wd[f'Bobot dokumen {index+1}'] = total

            # Perulangan untuk mendapatkan nilai Cosine Similarity
            # Untuk x dalam range length_list_content
            for x in range(length_list_content):
                # Cosine Similarity = sum_tf_ww(doc(i)) / (total_ww_query * total_ww_doc(i))
                cos = (sum_wq_wd['Bobot dokumen ' + str(x+1)] / 
                            (total_ww_doc['Bobot pencarian'] * 
                            total_ww_doc['Bobot dokumen ' + str(x+1)]))
                # Hasil perhitungan Cosine Similarity ditambahkan ke dalam list result
                result.append(cos)

        # Jika terjadi ZeroDivisionError, 
        # maka akan pass atau tidak ada perubahan pada result atau kosong []    
        except ZeroDivisionError:
            pass
        
        return result

    def get_result_order(self, vsm, idteks):
        '''Method untuk menampilkan hasil pencarian'''
        order = sorted(range(len(vsm)), key=lambda order: vsm[order], reverse = True)
        list_id_hasil = []
        if vsm == []:
            pass
        else:
            for d in order:
                if vsm[d] > 0:
                    list_id_hasil.append(idteks[d])
                    
        int_to_str_inlist = [str(integer) for integer in list_id_hasil]
        full_str = ','.join(int_to_str_inlist)
        
        return list_id_hasil, full_str

    def show_result(self, result_list, result_string):
        listsyntax_from_resultlist = []
        for x in result_list:
            listsyntax_from_resultlist.append(
                                             'id_teks = {} DESC'.format(x))

        stringsyntax = ','.join(listsyntax_from_resultlist) 
        
        sql = 'SELECT judul FROM teks WHERE id_teks in ({}) ORDER BY {}'.format(result_string, stringsyntax)
        
        try:
            my_cursor.execute(sql)
            result_final = my_cursor.fetchall()
        except Exception as e:
            return e
        
        return result_final