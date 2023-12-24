### Buat Virtual Environment (venv)

1. Buka terminal atau command prompt.
2. Buat virtual environment baru dengan menjalankan perintah:
    ```bash
    python -m venv nama_env
    ```
    Ganti `nama_env` dengan nama yang Anda inginkan untuk environment.

3. Aktifkan virtual environment:
    - **Windows**: 
        ```bash
        nama_env\Scripts\activate
        ```
    - **Mac/Linux**:
        ```bash
        source nama_env/bin/activate
        ```

### Install Dependencies

Setelah virtual environment aktif, instal dependensi dari `requirements.txt` dengan perintah:

```bash
pip install -r requirements.txt
