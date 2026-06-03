```mermaid
sequenceDiagram

    actor User
    participant UI
    participant PermohonanService
    participant DisposisiService
    participant SPTService
    participant DB

    User ->> UI: Ajukan Permohonan SPT
    activate UI
        UI ->> PermohonanService : SubmitPermohonan(data)
        activate PermohonanService
            PermohonanService ->> DB: Simpan Permohonan
            DB -->> PermohonanService: success
            PermohonanService -->> UI: success
        deactivate PermohonanService
        UI -->> User: Berhasil Simpan
    deactivate UI

    User ->> UI: Buat Disposisi
    activate UI
        UI ->> DisposisiService: SubmitDisposisi(data)
    deactivate UI

    activate DisposisiService
        DisposisiService ->> DB: Simpan Disposisi
        DB -->> DisposisiService: Success
        DisposisiService ->> SPTService: Buat SPT
            
            activate SPTService
                SPTService ->> SPTService: Validasi SPT
                SPTService ->> DB: mantap
            deactivate SPTService
    deactivate DisposisiService

```