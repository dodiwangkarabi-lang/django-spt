```mermaid
graph LR

    BaseLayout[base.html]

    BaseLayout --> Navbar
    BaseLayout --> Sidebar
    BaseLayout --> MainContent
    BaseLayout --> Footer

    MainContent --> DashboardPage
    MainContent --> ProfilePage

    DashboardPage --> StatsCard
    DashboardPage --> NotificationList
    DashboardPage --> ActivityChart

    NotificationList --> NotificationItem

    Sidebar --> Contoh
```