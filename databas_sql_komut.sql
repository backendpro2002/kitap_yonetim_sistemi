-- Kütüphane Yönetim Sistemi Veritabanı Kurulum Scripti
-- PostgreSQL için hazırlanmıştır

-- Veritabanı oluşturma (pgAdmin'de manuel olarak oluşturabilirsiniz)
-- CREATE DATABASE library_db;

-- Veritabanına bağlandıktan sonra aşağıdaki tabloları oluşturun

-- Books tablosu
CREATE TABLE books (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    author VARCHAR(255) NOT NULL,
    isbn VARCHAR(20) UNIQUE NOT NULL,
    category VARCHAR(100) NOT NULL,
    publication_year INTEGER,
    total_copies INTEGER DEFAULT 1,
    available_copies INTEGER DEFAULT 1,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Members tablosu
CREATE TABLE members (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    phone VARCHAR(20),
    address TEXT,
    membership_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE
);

-- Borrowings tablosu
CREATE TABLE borrowings (
    id SERIAL PRIMARY KEY,
    book_id INTEGER NOT NULL REFERENCES books(id) ON DELETE CASCADE,
    member_id INTEGER NOT NULL REFERENCES members(id) ON DELETE CASCADE,
    borrow_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    due_date TIMESTAMP NOT NULL,
    return_date TIMESTAMP,
    is_returned BOOLEAN DEFAULT FALSE
);

-- İndeksler oluşturma (performans için)
CREATE INDEX idx_books_title ON books(title);
CREATE INDEX idx_books_author ON books(author);
CREATE INDEX idx_books_category ON books(category);
CREATE INDEX idx_members_email ON members(email);
CREATE INDEX idx_borrowings_book_id ON borrowings(book_id);
CREATE INDEX idx_borrowings_member_id ON borrowings(member_id);
CREATE INDEX idx_borrowings_is_returned ON borrowings(is_returned);

-- Örnek veri ekleme
INSERT INTO books (title, author, isbn, category, publication_year, total_copies, available_copies, description) VALUES
('Suç ve Ceza', 'Fyodor Dostoyevski', '978-0-14-044913-6', 'Klasik Edebiyat', 1866, 3, 3, 'Rus edebiyatının başyapıtlarından biri'),
('1984', 'George Orwell', '978-0-452-28423-4', 'Distopya', 1949, 2, 2, 'Totaliter rejimi anlatan ünlü roman'),
('Simyacı', 'Paulo Coelho', '978-0-06-112241-5', 'Felsefe', 1988, 4, 4, 'Kişisel efsaneyi bulma yolculuğu'),
('Satranç', 'Stefan Zweig', '978-975-13-0123-4', 'Novella', 1942, 2, 2, 'Psikolojik gerilim dolu kısa roman'),
('Beyaz Diş', 'Jack London', '978-0-486-26968-1', 'Macera', 1906, 3, 3, 'Vahşi doğada yaşam mücadelesi');

INSERT INTO members (name, email, phone, address) VALUES
('Ahmet Yılmaz', 'ahmet.yilmaz@email.com', '0532-123-4567', 'İstanbul, Kadıköy'),
('Ayşe Demir', 'ayse.demir@email.com', '0533-234-5678', 'Ankara, Çankaya'),
('Mehmet Kaya', 'mehmet.kaya@email.com', '0534-345-6789', 'İzmir, Konak'),
('Fatma Şahin', 'fatma.sahin@email.com', '0535-456-7890', 'Bursa, Nilüfer'),
('Ali Özkan', 'ali.ozkan@email.com', '0536-567-8901', 'Antalya, Muratpaşa');

-- Örnek ödünç alma kayıtları
INSERT INTO borrowings (book_id, member_id, due_date, is_returned) VALUES
(1, 1, '2024-02-15 23:59:59', FALSE),
(2, 2, '2024-02-10 23:59:59', TRUE),
(3, 3, '2024-02-20 23:59:59', FALSE);

-- Ödünç verilen kitapların available_copies değerlerini güncelle
UPDATE books SET available_copies = available_copies - 1 WHERE id IN (1, 3);

-- Veritabanı kullanıcısı oluşturma (opsiyonel)
-- CREATE USER library_user WITH PASSWORD 'your_password';
-- GRANT ALL PRIVILEGES ON DATABASE library_db TO library_user;
-- GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO library_user;
-- GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO library_user;



