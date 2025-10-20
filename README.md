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

| Column      | Type          | Constraints                                                                                   | Description               |
| ----------- | ------------- | --------------------------------------------------------------------------------------------- | ------------------------- |
| id          | SERIAL        | PRIMARY KEY                                                                                   | Order ID                  |
| user_id     | INT           | REFERENCES users(id) ON DELETE CASCADE                                                        | Buyurtma egasi            |
| ticket_id   | INT           | REFERENCES tickets(id) ON DELETE CASCADE                                                      | Qaysi ticket              |
| quantity    | INT           | CHECK (quantity > 0)                                                                          | Nechta chipta             |
| status      | VARCHAR(20)   | DEFAULT 'pending' CHECK (status IN ('pending', 'paid', 'cancelled', 'refunded', 'completed')) | Buyurtma holati           |
| total_price | DECIMAL(10,2) | CHECK (total_price >= 0)                                                                      | Umumiy summa              |
| created_at  | TIMESTAMP     | DEFAULT now()                                                                                 | Yaratilgan vaqt           |
| updated_at  | TIMESTAMP     | DEFAULT now()                                                                                 | Oxirgi o‘zgartirish vaqti |

---

## ⚙️ API Overview

### Base URL

```
/api/v1
```

### Authentication

* JWT (Bearer token)
* `role`: `"admin"` yoki `"user"`

---

## 🧍‍♂️ USER AUTH MODULE

### **POST /users/register**

> Yangi foydalanuvchi yaratish

**Request**

```json
{
  "username": "diyor",
  "email": "diyor@example.com",
  "phone": "+998901234567",
  "password": "12345",
  "age": 20
}
```

**Response**

```json
{
  "id": 1,
  "username": "diyor",
  "email": "diyor@example.com",
  "role": "user"
}
```

---

### **POST /users/login**

> Login va JWT olish

**Request**

```json
{
  "username": "diyor",
  "password": "12345"
}
```

**Response**

```json
{
  "access_token": "jwt.token.value",
  "token_type": "bearer"
}
```

---

### **GET /users/me**

> Hozirgi foydalanuvchini qaytaradi

**Auth:** Bearer Token
**Response:**

```json
{
  "id": 1,
  "username": "diyor",
  "email": "diyor@example.com",
  "role": "user"
}
```

---

## 📍 VENUE MODULE

### **GET /venues/**

> Barcha joylarni olish

**Response**

```json
[
  { "id": 1, "name": "Humo Arena", "lon": 69.275, "lat": 41.312 },
  { "id": 2, "name": "Milliy Stadium", "lon": 69.287, "lat": 41.339 }
]
```

---

### **POST /venues/** *(admin only)*

> Yangi joy qo‘shish

**Request**

```json
{
  "name": "Humo Arena",
  "lon": 69.275,
  "lat": 41.312
}
```

---

### **PATCH /venues/{id}** *(admin only)*

> Venue ma’lumotini yangilash

---

### **DELETE /venues/{id}** *(admin only)*

> Venue ni o‘chirish

---

## 🎤 EVENT MODULE

### **GET /events/**

> Barcha eventlarni olish

**Response**

```json
[
  {
    "id": 1,
    "name": "Concert",
    "description": "Live music night",
    "limit_age": 18,
    "venue": { "id": 1, "name": "Humo Arena" },
    "start_time": "2025-11-02T19:00:00",
    "end_time": "2025-11-02T22:00:00"
  }
]
```

---

### **GET /events/{id}**

> Bitta event tafsilotlari (barcha ticketlar bilan)

**Response**

```json
{
  "id": 1,
  "name": "Concert",
  "description": "Live music night",
  "limit_age": 18,
  "venue": { "id": 1, "name": "Humo Arena" },
  "tickets": [
    { "id": 1, "name": "VIP", "price": 300.00, "quantity": 50 },
    { "id": 2, "name": "Standard", "price": 100.00, "quantity": 200 }
  ]
}
```

---

### **POST /events/** *(admin only)*

> Yangi event qo‘shish

**Request**

```json
{
  "name": "Concert",
  "description": "Live music night",
  "limit_age": 18,
  "venue_id": 1,
  "start_time": "2025-11-02T19:00:00",
  "end_time": "2025-11-02T22:00:00"
}
```

---

### **PATCH /events/{id}** *(admin only)*

### **DELETE /events/{id}** *(admin only)*

---

## 🎟️ TICKET MODULE

### **GET /tickets/**

> Barcha ticketlar ro‘yxati (admin only)

---

### **POST /tickets/** *(admin only)*

> Event uchun yangi ticket yaratish

**Request**

```json
{
  "name": "VIP",
  "event_id": 1,
  "price": 300.00,
  "quantity": 100
}
```

---

### **PATCH /tickets/{id}** *(admin only)*

> Narx yoki miqdorni o‘zgartirish

---

### **DELETE /tickets/{id}** *(admin only)*

---

## 🧾 ORDER MODULE

### **GET /orders/** *(admin only)*

> Barcha buyurtmalar

**Response**

```json
[
  {
    "id": 1,
    "user": "diyor",
    "ticket": "VIP",
    "quantity": 2,
    "status": "paid",
    "total_price": 600.00
  }
]
```

---

### **GET /orders/my** *(user only)*

> Foydalanuvchining o‘z buyurtmalari

---

### **POST /orders/** *(user only)*

> Yangi order yaratish

**Request**

```json
{
  "ticket_id": 1,
  "quantity": 2
}
```

**Response**

```json
{
  "id": 1,
  "status": "pending",
  "total_price": 600.00
}
```

---

### **PATCH /orders/{id}/status** *(admin only)*

> Admin buyurtma statusini o‘zgartiradi

**Request**

```json
{ "status": "paid" }
```

**Response**

```json
{
  "id": 1,
  "status": "paid"
}
```

---

### **DELETE /orders/{id}** *(user yoki admin)*

> Orderni bekor qilish

---

## 🔐 Access Summary

| Role  | Endpoint prefix                                     | Permissions  |
| ----- | --------------------------------------------------- | ------------ |
| user  | `/users/*`, `/orders/my`, `/orders/`                | view, create |
| admin | `/venues/*`, `/events/*`, `/tickets/*`, `/orders/*` | full access  |

---
