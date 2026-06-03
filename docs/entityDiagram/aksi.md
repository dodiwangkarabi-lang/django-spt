```mermaid
sequenceDiagram

actor User
participant UI
participant Aksi
participant Modal

User ->>+ UI: pilih aksi 
UI ->>+ Aksi: validasi aksi
Aksi ->>+ Modal: openModal
Modal ->> Modal: proses
Modal ->> Modal: closeModal
Modal -->>- Aksi: tampilkan detail
Aksi -->>- UI: selesai

UI -->>- User: selesai


```