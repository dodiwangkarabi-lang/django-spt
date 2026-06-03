```mermaid

sequenceDiagram
actor User

User ->> UI: klik tombol

UI ->> Modal: open(contentType, contentKey)

Modal ->> Modal: resolveContent(contentType, contentKey)

Modal ->> Content: render()

```
