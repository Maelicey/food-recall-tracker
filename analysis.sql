-- Food Recall Tracker: SQL analysis in BigQuery
-- Data: FDA openFDA food enforcement reports

-- 1. Validate the row count (expected: 29,485)
SELECT COUNT(*) AS total_products
FROM `food-recall-tracker-511601.food_recalls.recalls`;

-- 2. Recalled products and recall events per year
SELECT
  EXTRACT(YEAR FROM report_date) AS year,
  COUNT(*) AS total_products,
  COUNT(DISTINCT event_id) AS total_events
FROM `food-recall-tracker-511601.food_recalls.recalls`
GROUP BY year
ORDER BY year;

-- 3. Class I recalls mentioning Listeria, Salmonella, or undeclared allergens
SELECT COUNT(*) AS total_products
FROM `food-recall-tracker-511601.food_recalls.recalls`
WHERE classification = 'Class I'
  AND LOWER(reason_for_recall) LIKE '%listeria%';

SELECT COUNT(*) AS total_products
FROM `food-recall-tracker-511601.food_recalls.recalls`
WHERE classification = 'Class I'
  AND LOWER(reason_for_recall) LIKE '%salmonella%';

SELECT COUNT(*) AS total_products
FROM `food-recall-tracker-511601.food_recalls.recalls`
WHERE classification = 'Class I'
  AND LOWER(reason_for_recall) LIKE '%undeclared%';

-- 4. Explore uncategorized Class II reasons to find new keywords
SELECT DISTINCT reason_for_recall
FROM `food-recall-tracker-511601.food_recalls.recalls`
WHERE classification = 'Class II'
  AND LOWER(reason_for_recall) NOT LIKE '%listeria%'
  AND LOWER(reason_for_recall) NOT LIKE '%salmonella%'
  AND LOWER(reason_for_recall) NOT LIKE '%undeclared%'
LIMIT 30;

-- 5. App data: all recalls with a keyword-based reason category
SELECT
  *,
  CASE
    WHEN LOWER(reason_for_recall) LIKE '%listeria%' THEN 'Listeria'
    WHEN LOWER(reason_for_recall) LIKE '%salmonella%' THEN 'Salmonella'
    WHEN LOWER(reason_for_recall) LIKE '%undeclared%'
      OR LOWER(reason_for_recall) LIKE '%allergen%' THEN 'Undeclared allergen'
    WHEN LOWER(reason_for_recall) LIKE '%metal%'
      OR LOWER(reason_for_recall) LIKE '%plastic%'
      OR LOWER(reason_for_recall) LIKE '%glass%' THEN 'Foreign material'
    WHEN LOWER(reason_for_recall) LIKE '%insanitary%' THEN 'Insanitary conditions'
    WHEN LOWER(reason_for_recall) LIKE '%clostridium%' THEN 'Other bacteria'
    ELSE 'other'
  END AS reason_category
FROM `food-recall-tracker-511601.food_recalls.recalls`;

-- 6. Companies with the most recall events
SELECT
  recalling_firm,
  COUNT(*) AS total_products,
  COUNT(DISTINCT event_id) AS total_events
FROM `food-recall-tracker-511601.food_recalls.recalls`
GROUP BY recalling_firm
ORDER BY total_events DESC
LIMIT 10;
