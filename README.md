# Bike-Sharing-Data-Analysis-DBS
## 🔧 Persiapan Lingkungan

Pilih salah satu metode berikut untuk menyiapkan lingkungan Anda:

### Anaconda (Windows, macOS, Linux)
```bash
conda create --name bike-sharing-env python=3.9
conda activate bike-sharing-env
pip install -r requirements.txt
```

### Shell/Terminal (Windows, macOS, Linux)
```bash
mkdir Bike_Sharing_Dataset__proyek_Data_Analysis
cd Bike_Sharing_Dataset__proyek_Data_Analysis
python -m venv venv  # Membuat virtual environment
source venv/bin/activate  # Untuk macOS/Linux
venv\Scripts\activate  # Untuk Windows
pip install -r requirements.txt
```

### Pipenv (Windows, macOS, Linux)
```bash
mkdir Bike_Sharing_Dataset__proyek_Data_Analysis
cd Bike_Sharing_Dataset__proyek_Data_Analysis
pipenv install
pipenv shell
pip install -r requirements.txt
```

## 🚀 Menjalankan Aplikasi Streamlit

Cukup jalankan perintah berikut:

```bash
streamlit run dashboard/dashboard.py
```

