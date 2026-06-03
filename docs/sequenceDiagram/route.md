```mermaid
sequenceDiagram
actor User

User ->> UserForm: submit

UserForm ->> UserService: create(data)
UserService ->> API: POST /users

API -->> UserService: success
UserService -->> UserForm: success

UserForm ->> Router: navigate(USER_LIST)
```