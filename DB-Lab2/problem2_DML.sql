USE library;

INSERT INTO AUTHOR (author_id, name, country, photo) VALUES 
(1, 'Agatha Christie', 'UK', 'agatha.jpg'),
(2, 'Dan Brown', 'USA', 'dan.jpg'),
(3, 'Naguib Mahfouz', 'Egypt', 'naguib.jpg');

INSERT INTO BOOK (book_id, title, price, author_id, cover_image) VALUES 
(1, 'And Then There Were None', 15.50, 1, 'and_then_there_were_none.jpg'),
(2, 'Murder on the Orient Express', 12.00, 1, 'orient_express.jpg'),
(3, 'The Da Vinci Code', 18.99, 2, 'davinci_code.jpg'),
(4, 'Angels & Demons', 14.50, 2, 'angels_demons.jpg'),
(5, 'Palace Walk', 20.00, 3, 'palace_walk.jpg'),
(6, 'Sugar Street', 22.00, 3, 'sugar_street.jpg');