```mermaid
sequenceDiagram

    actor User

    participant View
    participant Service
    participant DB

    User->>+View: 1. Submit Form

    View->>+Service: 2. Validasi Data

    Service->>+DB: 3. Simpan Data

    DB-->>-Service: 4. Success

    Service-->>-View: 5. Response

    View-->>-User: 6. Tampilkan Notifikasi
```

```mermaid
sequenceDiagram

    User->>Service: 1. Submit

    Service->>Service: 1.1 Validasi Status

    Service->>Service: 1.2 Validasi Lampiran

    Service->>DB: 2. Simpan
```