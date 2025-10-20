## 🎯 Maqsad

Foydalanuvchilar (user) turli **event**lar uchun **ticket** sotib oladigan tizim yaratish.
Admin yangi event va ticket qo‘shadi, user esa buyurtma beradi.

---

## 🧩 1. Entity Relationship Diagram (ERD) — tavsifiy ko‘rinish

```
User (1)───(M) Order (M)───(1) Ticket (M)───(1) Event (M)───(1) Venue
```

Bu degani:

* Har bir **User** ko‘p **Order** qilishi mumkin.
* Har bir **Order** faqat bitta **Ticket**ga tegishli.
* Har bir **Ticket** bitta **Event**ga tegishli, lekin har bir **Event**da bir nechta **Ticket** bo‘lishi mumkin.
* Har bir **Event** bitta **Venue**da bo‘ladi, lekin har bir **Venue**da bir nechta **Event** bo‘lishi mumkin.

---

## 🧱 2. Jadval dizayni (relational schema)

### **1️⃣ users**

| Column     | Type         | Constraints      | Description         |
| ---------- | ------------ | ---------------- | ------------------- |
| id         | SERIAL       | PRIMARY KEY      | Foydalanuvchi ID    |
| username   | VARCHAR(100) | UNIQUE NOT NULL  | Login uchun nom     |
| email      | VARCHAR(150) | UNIQUE NOT NULL  | Elektron pochta     |
| phone      | VARCHAR(20)  | UNIQUE           | Telefon raqam       |
| password   | VARCHAR(255) | NOT NULL         | Hashlangan parol    |
| age        | INT          | CHECK (age >= 0) | Yoshi               |
| role       | VARCHAR(10)  | DEFAULT 'user'   | 'admin' yoki 'user' |
| created_at | TIMESTAMP    | DEFAULT now()    | Qo‘shilgan sana     |

---

### **2️⃣ venues**

| Column | Type         | Constraints | Description |
| ------ | ------------ | ----------- | ----------- |
| id     | SERIAL       | PRIMARY KEY | Venue ID    |
| name   | VARCHAR(150) | NOT NULL    | Joy nomi    |
| lon    | DECIMAL(9,6) | NOT NULL    | Longitude   |
| lat    | DECIMAL(9,6) | NOT NULL    | Latitude    |

---

### **3️⃣ events**

| Column      | Type         | Constraints                             | Description      |
| ----------- | ------------ | --------------------------------------- | ---------------- |
| id          | SERIAL       | PRIMARY KEY                             | Event ID         |
| name        | VARCHAR(150) | NOT NULL                                | Tadbir nomi      |
| description | TEXT         |                                         | Izoh             |
| limit_age   | INT          | CHECK (limit_age >= 0)                  | Yosh cheklovi    |
| venue_id    | INT          | REFERENCES venues(id) ON DELETE CASCADE | Joy manzili      |
| start_time  | TIMESTAMP    | NOT NULL                                | Boshlanish vaqti |
| end_time    | TIMESTAMP    |                                         | Tugash vaqti     |

---

### **4️⃣ tickets**

| Column   | Type          | Constraints                             | Description                    |
| -------- | ------------- | --------------------------------------- | ------------------------------ |
| id       | SERIAL        | PRIMARY KEY                             | Ticket ID                      |
| name     | VARCHAR(100)  | NOT NULL                                | Chipta nomi (VIP, Standard...) |
| event_id | INT           | REFERENCES events(id) ON DELETE CASCADE | Qaysi event uchun              |
| price    | DECIMAL(10,2) | CHECK (price >= 0)                      | Narxi                          |
| quantity | INT           | CHECK (quantity >= 0)                   | Umumiy miqdor                  |

---

### **5️⃣ orders**

| Column      | Type          | Constraints                                                                                      | Description    |
| ----------- | ------------- | ------------------------------------------------------------------------------------------------ | -------------- |
| id          | SERIAL        | PRIMARY KEY                                                                                      | Order ID       |
| user_id     | INT           | REFERENCES users(id) ON DELETE CASCADE                                                           | Kim sotib oldi |
| ticket_id   | INT           | REFERENCES tickets(id) ON DELETE CASCADE                                                         | Qaysi ticket   |
| quantity    | INT           | CHECK (quantity > 0)                                                                             | Nechta chipta  |
| total_price | DECIMAL(10,2) | GENERATED ALWAYS AS (quantity * (SELECT price FROM tickets WHERE tickets.id = ticket_id)) STORED | Umumiy summa   |
| created_at  | TIMESTAMP     | DEFAULT now()                                                                                    | Buyurtma vaqti |

---
