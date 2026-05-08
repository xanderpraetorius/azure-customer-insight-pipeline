SELECT 
    p.category,
    AVG(r.rating)                           AS avg_rating,
    COUNT(r.review_id)                      AS total_reviews,
    SUM(CASE WHEN ss.sentiment_label = 'positive' THEN 1 ELSE 0 END) AS positive_count,
    SUM(CASE WHEN ss.sentiment_label = 'negative' THEN 1 ELSE 0 END) AS negative_count,
    AVG(ss.sentiment_score)                 AS avg_sentiment_score
FROM products p
JOIN reviews r       ON p.product_id    = r.product_id
JOIN sentiment_scores ss ON r.review_id = ss.review_id
GROUP BY p.category
ORDER BY avg_sentiment_score DESC;