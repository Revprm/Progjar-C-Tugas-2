# Tugas 2 Pemrograman Jaringan C

| Nama             | NRP            |
|:----------------:|:--------------:|
| Revy Pramana     | 5025221252     |

## TimeServer

Server TCP multi-threaded yang merespons permintaan waktu saat ini.

### Fitur

- Menangani banyak koneksi klien secara bersamaan (threading).
- Perintah:
  - `TIME` — mengirim waktu server dalam format `HH:MM:SS`.
  - `QUIT` — memutus koneksi.
- Logging koneksi dan error.

### Cara Menjalankan


1. Jalankan server di mesin1:
   ```bash
   python3 TimeServer.py
    ```
    Secara default mendengarkan di `0.0.0.0:45000`.

2. Hubungkan ke server dengan netcat:

   ```bash
   nc 172.16.16.101 45000
   ```

3. Contoh interaksi:

   ```bash
   TIME
   JAM 14:32:10
   QUIT
   ```

### Logging

Log akan muncul di terminal, misalnya:

```
14:30:12 INFO: [CONNECTED] ('127.0.0.1', 56789)
14:30:12 INFO: Client ('127.0.0.1', 56789) disconnected.
```

### Catatan

* Perintah harus berbaris sendiri dan diakhiri Enter.
* Selain `TIME` dan `QUIT`, server membalas `Invalid request`.