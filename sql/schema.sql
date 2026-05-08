-- Products table
CREATE TABLE products (
    product_id      NVARCHAR(20)    NOT NULL PRIMARY KEY,
    product_name    NVARCHAR(255)   NOT NULL,
    category        NVARCHAR(100)   NOT NULL,
    created_at      DATETIME2       DEFAULT GETDATE()
);

-- Reviews table
CREATE TABLE reviews (
    review_id       INT             IDENTITY(1,1) PRIMARY KEY,
    product_id      NVARCHAR(20)    NOT NULL,
    reviewer_id     NVARCHAR(50)    NOT NULL,
    rating          TINYINT         NOT NULL CHECK (rating BETWEEN 1 AND 5),
    review_text     NVARCHAR(MAX),
    review_date     DATETIME2       NOT NULL,
    verified        BIT             DEFAULT 0,
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);

-- Sentiment scores table
CREATE TABLE sentiment_scores (
    score_id        INT             IDENTITY(1,1) PRIMARY KEY,
    review_id       INT             NOT NULL,
    sentiment_label NVARCHAR(20)    NOT NULL,
    sentiment_score FLOAT           NOT NULL,
    topic_cluster   NVARCHAR(100),
    processed_at    DATETIME2       DEFAULT GETDATE(),
    FOREIGN KEY (review_id) REFERENCES reviews(review_id)
);