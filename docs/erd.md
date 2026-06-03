```mermaid
erDiagram
    User {
        uuid id PK
        string email UK
        string nama
    }

    Profile {
        uuid id PK
        string nama
        string nik FK
    }

    Cart {
        uuid id PK
        string nama
    }
    
    User ||--|{ Profile : ""
    User ||--|| Cart : ""
```