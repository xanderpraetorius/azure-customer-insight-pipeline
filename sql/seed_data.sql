-- Insert sample products
INSERT INTO products (product_id, product_name, category) VALUES
('B001', 'Wireless Noise-Cancelling Headphones', 'Electronics'),
('B002', 'Portable Bluetooth Speaker', 'Electronics'),
('B003', 'Ergonomic Office Chair', 'Furniture'),
('B004', 'Stainless Steel Water Bottle', 'Kitchen'),
('B005', 'Running Shoes', 'Sports');

-- Insert sample reviews
INSERT INTO reviews (product_id, reviewer_id, rating, review_text, review_date, verified) VALUES
('B001', 'U001', 5, 'Exceptional sound quality and battery life. Best headphones I have owned.', '2024-01-15', 1),
('B001', 'U002', 4, 'Great noise cancellation but slightly uncomfortable after long use.', '2024-01-18', 1),
('B001', 'U003', 2, 'Stopped working after two months. Very disappointing build quality.', '2024-02-01', 1),
('B002', 'U004', 5, 'Incredible bass and very loud for its size. Highly recommend.', '2024-01-20', 1),
('B002', 'U005', 3, 'Decent speaker but battery drains faster than advertised.', '2024-02-05', 0),
('B003', 'U006', 5, 'My back pain disappeared after switching to this chair. Worth every cent.', '2024-01-25', 1),
('B003', 'U007', 4, 'Very comfortable but assembly instructions were confusing.', '2024-02-10', 1),
('B004', 'U008', 5, 'Keeps water cold for 24 hours as promised. Excellent product.', '2024-01-30', 1),
('B004', 'U009', 1, 'Lid started leaking after first wash. Complete waste of money.', '2024-02-15', 1),
('B005', 'U010', 4, 'Very comfortable for long runs. True to size.', '2024-02-20', 1);

-- Insert sample sentiment scores
INSERT INTO sentiment_scores (review_id, sentiment_label, sentiment_score, topic_cluster) VALUES
(1, 'positive', 0.97, 'sound_quality'),
(2, 'positive', 0.72, 'comfort'),
(3, 'negative', 0.89, 'durability'),
(4, 'positive', 0.95, 'sound_quality'),
(5, 'neutral',  0.54, 'battery_life'),
(6, 'positive', 0.98, 'ergonomics'),
(7, 'positive', 0.68, 'assembly'),
(8, 'positive', 0.96, 'performance'),
(9, 'negative', 0.92, 'quality_control'),
(10,'positive', 0.81, 'comfort');