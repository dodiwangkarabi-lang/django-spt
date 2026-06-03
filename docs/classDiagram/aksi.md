```mermaid
classDiagram

class Modal {
    ModalOpen: bool
    openModal()
    closeModal() 
}

DisposisiDetailPage o-- Aksi
Modal o-- Form
DisposisiDetailPage o-- Modal

```