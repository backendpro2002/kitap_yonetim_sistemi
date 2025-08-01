
```markdown
# Kütüphane Yönetim Sistemi - Teknoloji Raporu

## 📋 Proje Özeti

Bu proje, FastAPI (Python) backend ve Next.js (React) frontend kullanarak geliştirilmiş modern bir kütüphane yönetim sistemidir. PostgreSQL veritabanı ile veri yönetimi yapılmaktadır.

## 🛠️ Kullanılan Teknolojiler

### Backend Teknolojileri

#### 1. **FastAPI** (Python Web Framework)
- **Versiyon**: 0.104.1
- **Neden Seçildi**: 
  - Otomatik API dokümantasyonu (Swagger/OpenAPI)
  - Yüksek performans (Starlette tabanlı)
  - Type hints desteği
  - Async/await desteği
- **Öğrenme Kaynakları**:
  - [FastAPI Resmi Dokümantasyon](https://fastapi.tiangolo.com/)
  - [FastAPI Tutorial](https://fastapi.tiangolo.com/tutorial/)

#### 2. **SQLAlchemy** (ORM - Object Relational Mapping)
- **Versiyon**: 2.0.23
- **Kullanım Amacı**: Veritabanı işlemleri ve model tanımlamaları
- **Özellikler**:
  - Declarative Base ile model tanımlama
  - Session yönetimi
  - Relationship tanımlamaları
- **Öğrenme Kaynakları**:
  - [SQLAlchemy Dokümantasyon](https://docs.sqlalchemy.org/)

#### 3. **Pydantic** (Veri Validasyonu)
- **Versiyon**: 2.5.0
- **Kullanım Amacı**: API request/response validasyonu
- **Özellikler**:
  - BaseModel sınıfları
  - Otomatik tip kontrolü
  - JSON serialization
- **Öğrenme Kaynakları**:
  - [Pydantic Dokümantasyon](https://docs.pydantic.dev/)

#### 4. **PostgreSQL** (Veritabanı)
- **Kullanım Amacı**: Ana veri depolama
- **Bağlantı**: psycopg2-binary driver
- **Özellikler**:
  - ACID uyumluluğu
  - İlişkisel veritabanı
  - JSON desteği

#### 5. **Uvicorn** (ASGI Server)
- **Versiyon**: 0.24.0
- **Kullanım Amacı**: FastAPI uygulamasını çalıştırma
- **Özellikler**:
  - Async desteği
  - Hot reload
  - Yüksek performans

### Frontend Teknolojileri

#### 1. **Next.js** (React Framework)
- **Versiyon**: 14.0.0
- **Özellikler**:
  - App Router (yeni routing sistemi)
  - Server Components
  - TypeScript desteği
  - Otomatik optimizasyon
- **Öğrenme Kaynakları**:
  - [Next.js Dokümantasyon](https://nextjs.org/docs)
  - [Next.js Learn](https://nextjs.org/learn)

#### 2. **React** (UI Kütüphanesi)
- **Versiyon**: 18
- **Kullanılan Hook'lar**:
  - `useState` - State yönetimi
  - `useEffect` - Side effects
  - `React.FormEvent` - Form handling
- **Öğrenme Kaynakları**:
  - [React Dokümantasyon](https://react.dev/)

#### 3. **TypeScript** (Tip Güvenliği)
- **Versiyon**: 5
- **Kullanım Amacı**: Tip güvenliği ve geliştirici deneyimi
- **Özellikler**:
  - Interface tanımlamaları
  - Type checking
  - IntelliSense desteği

#### 4. **Tailwind CSS** (Styling Framework)
- **Versiyon**: 3.4.17
- **Kullanım Amacı**: Hızlı ve tutarlı styling
- **Özellikler**:
  - Utility-first approach
  - Responsive design
  - Dark mode desteği

#### 5. **shadcn/ui** (UI Component Library)
- **Bileşenler**:
  - Card, Button, Input, Label
  - Dialog, Tabs, Table
  - Badge, Textarea
  - Sonner (Toast notifications)
- **Özellikler**:
  - Radix UI tabanlı
  - Accessible components
  - Customizable

#### 6. **Lucide React** (Icon Library)
- **Kullanım Amacı**: Modern ve tutarlı ikonlar
- **Özellikler**:
  - Tree-shakable
  - SVG tabanlı
  - Geniş ikon koleksiyonu

## 🏗️ Proje Mimarisi

### Backend Mimarisi
```

FastAPI Application
├── Models (SQLAlchemy)
│   ├── Book
│   ├── Member
│   └── Borrowing
├── Schemas (Pydantic)
│   ├── BookCreate/Response
│   ├── MemberCreate/Response
│   └── BorrowingCreate/Response
├── Database
│   ├── Engine
│   ├── SessionLocal
│   └── Base
└── Endpoints
├── Books CRUD
├── Members CRUD
└── Borrowings CRUD

```plaintext

### Frontend Mimarisi
```

Next.js App Router
├── app/
│   ├── layout.tsx (Root Layout)
│   ├── page.tsx (Main Component)
│   └── globals.css
├── components/ui/ (shadcn/ui)
│   ├── card.tsx
│   ├── button.tsx
│   ├── dialog.tsx
│   └── ...
└── lib/
└── utils.ts

```plaintext

### Veritabanı Şeması
```sql
Books Table
├── id (Primary Key)
├── title, author, isbn
├── category, publication_year
├── total_copies, available_copies
└── description, created_at

Members Table
├── id (Primary Key)
├── name, email, phone
├── address, membership_date
└── is_active

Borrowings Table
├── id (Primary Key)
├── book_id (Foreign Key)
├── member_id (Foreign Key)
├── borrow_date, due_date
├── return_date
└── is_returned
```

## Sıfırdan Proje Geliştirme Rehberi

### Ön Gereksinimler

1. **Python** (3.8+)
2. **Node.js** (18+)
3. **PostgreSQL** (12+)
4. **Git** (versiyon kontrolü)


### Adım 1: Backend Geliştirme

#### 1.1 Python Ortamı Hazırlama

```shellscript
# Sanal ortam oluştur
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Gerekli paketleri yükle
pip install fastapi uvicorn sqlalchemy psycopg2-binary pydantic
```

#### 1.2 FastAPI Uygulaması Oluşturma

```python
# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Library Management System")

# CORS ayarları
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Library Management API"}
```

#### 1.3 Veritabanı Modelleri

```python
# SQLAlchemy modelleri tanımla
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Book(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    # ... diğer alanlar
```

#### 1.4 Pydantic Şemaları

```python
# API request/response modelleri
from pydantic import BaseModel

class BookCreate(BaseModel):
    title: str
    author: str
    # ... diğer alanlar

class BookResponse(BaseModel):
    id: int
    title: str
    # ... diğer alanlar
    
    class Config:
        from_attributes = True
```

#### 1.5 CRUD Endpoints

```python
# API endpoint'leri
@app.get("/books", response_model=List[BookResponse])
def get_books(db: Session = Depends(get_db)):
    return db.query(Book).all()

@app.post("/books", response_model=BookResponse)
def create_book(book: BookCreate, db: Session = Depends(get_db)):
    # ... implementation
```

### Adım 2: Frontend Geliştirme

#### 2.1 Next.js Projesi Oluşturma

```shellscript
npx create-next-app@latest library-frontend --typescript --tailwind --eslint --app
cd library-frontend
```

#### 2.2 UI Kütüphanesi Kurulumu

```shellscript
# shadcn/ui kurulumu
npx shadcn@latest init
npx shadcn@latest add card button input dialog table tabs badge sonner

# İkon kütüphanesi
npm install lucide-react
```

#### 2.3 Ana Bileşen Geliştirme

```typescriptreact
// app/page.tsx
"use client"
import { useState, useEffect } from "react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"

export default function LibraryManagement() {
    const [books, setBooks] = useState([])
    
    // API çağrıları
    const fetchBooks = async () => {
        const response = await fetch("http://localhost:8000/books")
        const data = await response.json()
        setBooks(data)
    }
    
    useEffect(() => {
        fetchBooks()
    }, [])
    
    return (
        <div className="container mx-auto p-6">
            {/* UI bileşenleri */}
        </div>
    )
}
```

### Adım 3: Veritabanı Kurulumu

#### 3.1 PostgreSQL Kurulumu

- **Windows**: PostgreSQL installer
- **Mac**: `brew install postgresql`
- **Linux**: `sudo apt-get install postgresql`


#### 3.2 Veritabanı Oluşturma

```sql
-- pgAdmin veya psql ile
CREATE DATABASE library_db;

-- Tabloları oluştur
CREATE TABLE books (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    -- ... diğer alanlar
);
```

## Öğrenme Yol Haritası

### Başlangıç Seviyesi (1-2 ay)

1. **Python Temelleri**

1. Veri tipleri, fonksiyonlar, sınıflar
2. Paket yönetimi (pip)



2. **JavaScript/TypeScript**

1. ES6+ özellikleri
2. Async/await
3. Type annotations



3. **HTML/CSS**

1. Semantic HTML
2. CSS Grid/Flexbox
3. Responsive design





### Orta Seviye (2-3 ay)

1. **React**

1. Components, Props, State
2. Hooks (useState, useEffect)
3. Event handling



2. **FastAPI**

1. REST API konseptleri
2. Request/Response handling
3. Middleware



3. **SQL**

1. Temel sorgular (SELECT, INSERT, UPDATE, DELETE)
2. JOIN işlemleri
3. İndeksler





### İleri Seviye (3-4 ay)

1. **SQLAlchemy**

1. ORM konseptleri
2. Relationships
3. Migrations



2. **Next.js**

1. App Router
2. Server Components
3. API Routes



3. **Veritabanı Tasarımı**

1. Normalizasyon
2. İndeksleme stratejileri
3. Performance optimization





## Geliştirme Araçları

### Kod Editörü

- **VS Code** (önerilen)

- Python extension
- TypeScript extension
- Tailwind CSS IntelliSense





### Veritabanı Yönetimi

- **pgAdmin** (PostgreSQL GUI)
- **DBeaver** (Universal database tool)


### API Testi

- **Postman** veya **Insomnia**
- **FastAPI Swagger UI** (otomatik)


### Versiyon Kontrolü

- **Git** + **GitHub**


## Önerilen Kaynaklar

### Kitaplar

1. "FastAPI Modern Python Web Development" - Bill Lubanovic
2. "Learning React" - Alex Banks, Eve Porcello
3. "PostgreSQL: Up and Running" - Regina Obe


### Online Kurslar

1. **FastAPI**: FastAPI resmi tutorial
2. **React**: React.dev tutorial
3. **Next.js**: Next.js Learn
4. **PostgreSQL**: PostgreSQL Tutorial


### YouTube Kanalları

1. **Corey Schafer** (Python/FastAPI)
2. **Traversy Media** (Web Development)
3. **The Net Ninja** (React/Next.js)


## Proje Geliştirme İpuçları

### Best Practices

1. **Kod Organizasyonu**

1. Dosyaları mantıklı klasörlere ayır
2. Naming conventions'a uy
3. Comments ve docstrings kullan



2. **Error Handling**

1. Try-catch blokları kullan
2. Kullanıcı dostu hata mesajları
3. Logging implementasyonu



3. **Security**

1. Input validation
2. SQL injection koruması
3. CORS ayarları



4. **Performance**

1. Database indexing
2. API response caching
3. Image optimization





### Gelişim Önerileri

1. **Authentication** sistemi ekle
2. **Search ve filtering** özellikleri
3. **File upload** (kitap kapakları)
4. **Email notifications**
5. **Reporting dashboard**
6. **Mobile responsive** tasarım
7. **Dark mode** desteği
8. **Unit testing** implementasyonu


## Paket Listesi

### Backend (requirements.txt)

```plaintext
fastapi==0.104.1
uvicorn[standard]==0.24.0
sqlalchemy==2.0.23
psycopg2-binary==2.9.9
pydantic==2.5.0
python-multipart==0.0.6
```

### Frontend (package.json dependencies)

```json
{
  "next": "14.0.0",
  "react": "^18",
  "react-dom": "^18",
  "@radix-ui/react-dialog": "^1.0.5",
  "@radix-ui/react-tabs": "^1.0.4",
  "lucide-react": "^0.294.0",
  "sonner": "^1.0.0",
  "class-variance-authority": "^0.7.0",
  "clsx": "^2.0.0",
  "tailwind-merge": "^2.0.0"
}
```

## ️ Proje Dosya Yapısı

```plaintext
library-management/
├── backend/
│   ├── main.py
│   ├── requirements.txt
│   └── scripts/
│       └── database_setup.sql
├── frontend/
│   ├── app/
│   │   ├── layout.tsx
│   │   ├── page.tsx
│   │   └── globals.css
│   ├── components/
│   │   └── ui/
│   ├── lib/
│   │   └── utils.ts
│   ├── package.json
│   ├── tailwind.config.js
│   └── tsconfig.json
└── README.md
```

## Deployment Önerileri

### Backend Deployment

- **Vercel** (Serverless)
- **Railway** (Container)
- **DigitalOcean** (VPS)
- **AWS EC2** (Cloud)


### Frontend Deployment

- **Vercel** (önerilen)
- **Netlify**
- **GitHub Pages**


### Database Hosting

- **Supabase** (PostgreSQL as a Service)
- **Railway** (PostgreSQL)
- **AWS RDS**
- **Google Cloud SQL**


---

Bu rapor, kütüphane yönetim sistemi projesini sıfırdan geliştirmek için gereken tüm bilgileri içermektedir. Her teknoloji için ayrıntılı öğrenme kaynakları ve adım adım rehber sunulmuştur.

```plaintext


```