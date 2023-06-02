# Information Retrieval of Text Documents Using TF-IDF Weighting and Cosine Similarity Algorithm

This project is a prototype of text document retrieval system that utilizes the TF-IDF (Term Frequency-Inverse Document Frequency) weighting and Cosine Similarity algorithm. The text documents used in this project are news articles related to the activities of the Data Science Study Program at the Universitas Pembangunan Nasional "Veteran" Jawa Timur, which can be accessed through [https://sada.upnjatim.ac.id/category/berita/](https://sada.upnjatim.ac.id/category/berita/). This project is designed to search and display news articles related to the queries entered by the users.

Additionally, the project includes a graphical user interface (GUI) created using Tkinter and CustomTkinter. The GUI allows users to input search queries and obtain retrieval results in the form of a list of documents most relevant to the query.

## Prerequisites

Before running this project, make sure you have the following prerequisites:

- Python 3.9 or above.

## Installation

Follow these steps to install the project:

1. Clone this repository to your local directory:

   ```bash
   $ git clone https://github.com/harishartanto/information-retrieval.git
   ```

2. Navigate to the project directory:

   ```bash
   $ cd information-retrieval
   ```

3. Install the required dependencies:

   ```bash
   $ pip install -r requirements.txt
   ```

## Usage

To run this project, follow these steps:

1. Make sure you are in the project directory:

   ```bash
   $ cd information-retrieval
   ```

2. Run the `main.py` file:

   ```bash
   $ python main.py
   ```

   This will open the user interface (GUI) of the text document retrieval system.

3. Enter your search query in the provided text box and click the "Search" button.

4. The search results will be displayed as a list of documents, sorted based on their relevance to the query.

## Scientific Publication

A scientific paper related to this project has been published in the Seminar Nasional Teknologi dan Sistem Informasi (SITASI) 2022. You can access the paper through the following link:

- [TEMU KEMBALI INFORMASI BERITA KEGIATAN PROGRAM STUDI MENGGUNAKAN ALGORITMA PEMBOBOTAN TF-IDF DAN COSINE SIMILARITY](https://sitasi.upnjatim.ac.id/index.php/sitasi/article/view/309)

## License

This project is licensed under the [MIT License](LICENSE). Please read the [LICENSE](LICENSE) file for more details.