-- CREATE OR REPLACE PROCEDURE export_data (in_file_name varchar, in_table_name varchar, in_delim varchar)
-- AS $export$
--     DECLARE
--     destination varchar;
--     BEGIN
--         destination:= (SELECT CONCAT((SELECT setting FROM pg_settings WHERE name = 'data_directory'),
--             '/export_data/', in_file_name));
--         IF in_file_name LIKE '_.csv' THEN
--         EXECUTE('COPY ' || in_table_name || ' TO ''' || destination || ''' DELIMITER '''
--                            || in_delim || ''' ');
--         ELSE
--              EXECUTE('COPY ' || in_table_name || ' TO ''' || destination || '''  ' );
--         END IF;
--     END;
-- $export$ LANGUAGE plpgsql;

CREATE OR REPLACE PROCEDURE import_data (in_file_name varchar, in_table_name varchar, in_delim varchar)
AS $import$
    DECLARE
    destination varchar;
    BEGIN
        destination := (SELECT CONCAT('/datasets/', in_file_name));
        IF in_file_name LIKE '_.csv' THEN
        EXECUTE('COPY ' || in_table_name || ' FROM ''' || destination || ''' DELIMITER '''
                           || in_delim || ''' ' );
        ELSE
             EXECUTE('COPY ' || in_table_name || ' FROM ''' || destination || '''  ' );
        END IF;
    END;
$import$ LANGUAGE plpgsql;

CREATE TABLE IF NOT EXISTS personal_data(
    customer_id bigint primary key,
    customer_name varchar,
    customer_surname varchar,
    customer_primary_email varchar,
    customer_primary_phone varchar,
    CONSTRAINT un_persons UNIQUE (customer_name, customer_surname, customer_primary_email, customer_primary_phone),
    CONSTRAINT ch_name_surname CHECK (customer_name ~ '^[А-Я]([а-я]|-| )+'  AND customer_surname ~ '^[А-Я]([а-я]|-| )+' ),
    CONSTRAINT ch_email CHECK (customer_primary_email ~ '([a-z]|[0-9])+@([a-z]|[0-9])+\.[a-z]+'),
    CONSTRAINT ch_phone CHECK (customer_primary_phone ~ '^(\+7)[0-9]{10}')
);

CREATE TABlE IF NOT EXISTS cards(
    customer_card_id bigint primary key,
    customer_id bigint,
    CONSTRAINT fk_cards_customer_id FOREIGN KEY (customer_id) REFERENCES personal_data(customer_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS groups_of_goods(
    group_id bigint primary key,
    group_name varchar
);

CREATE TABLE IF NOT EXISTS goods(
    sku_id bigint primary key,
    sku_name varchar,
    group_id bigint,
    CONSTRAINT fk_goods_group_id FOREIGN KEY (group_id) REFERENCES groups_of_goods(group_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS stores(
    transaction_store_id bigint,
    sku_id bigint,
    sku_purchase_price numeric,
    sku_retail_price numeric,
    CONSTRAINT fk_shops_sku_id FOREIGN KEY (sku_id) REFERENCES goods(sku_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS transactions(
    transaction_id bigint primary key,
    customer_card_id bigint,
    transaction_summ numeric,
    transaction_date_time timestamp,
    transaction_store_id bigint,
    CONSTRAINT fk_transactions_customer_card_id FOREIGN KEY (customer_card_id) REFERENCES cards(customer_card_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS checks(
    transaction_id bigint,
    sku_id bigint,
    sku_amount numeric,
    sku_summ numeric,
    sku_summ_paid numeric,
    sku_discount numeric,
    CONSTRAINT fk_cheques_transaction_id FOREIGN KEY (transaction_id) REFERENCES transactions(transaction_id) ON DELETE CASCADE,
    CONSTRAINT fk_cheques_sku_id FOREIGN KEY (sku_id) REFERENCES goods(sku_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS date_reports(
    analysis_formation date
);

 SET datestyle = dmy;

-- -- заполнить базу данными из dataset MINI tsv формат
CALL import_data('Personal_Data_Mini.tsv', 'personal_data', null);
CALL import_data('Cards_Mini.tsv', 'cards', null);
CALL import_data('Groups_SKU_Mini.tsv', 'groups_of_goods', null);
CALL import_data('SKU_Mini.tsv', 'goods', null);
CALL import_data('Stores_Mini.tsv', 'stores', null);
CALL import_data('Transactions_Mini.tsv', 'transactions',null);
CALL import_data('Checks_Mini.tsv', 'checks',null);
CALL import_data('Date_Of_Analysis_Formation.tsv', 'date_reports',null);

-- TRUNCATE date_reports;
-- TRUNCATE checks;
-- TRUNCATE transactions CASCADE;
-- TRUNCATE stores CASCADE;
-- TRUNCATE goods CASCADE;
-- TRUNCATE groups_of_goods CASCADE;
-- TRUNCATE cards CASCADE;
-- TRUNCATE personal_data CASCADE;

-- заполнить базу данными из dataset tsv формат
-- CALL import_data('Personal_Data.tsv', 'personal_data', null);
-- CALL import_data('Cards.tsv', 'cards', null);
-- CALL import_data('Groups_SKU.tsv', 'groups_of_goods', null);
-- CALL import_data('SKU.tsv', 'goods', null);
-- CALL import_data('Stores.tsv', 'stores', null);
-- CALL import_data('Transactions.tsv', 'transactions',null);
-- CALL import_data('Checks.tsv', 'checks',null);
-- CALL import_data('Date_Of_Analysis_Formation.tsv', 'date_reports',null);


-- part_2_task_1 view customers (Представление Клиенты)
CREATE OR REPLACE VIEW v_customers AS
    WITH card_list AS (
        SELECT customer_id, customer_card_id FROM cards
    ),
    average_check AS (
        SELECT card_list.customer_id, round(sum(transaction_summ) / count(*)::decimal, 10) AS avg_check
        FROM card_list
            INNER JOIN transactions ON card_list.customer_card_id = transactions.customer_card_id
        GROUP BY 1
        ORDER BY 2 DESC -- Сортировка по заданию
    ),
    check_segment AS (
        SELECT customer_id,
            CASE
                WHEN sub_query.row >= 0
                    AND sub_query.row <= round((SELECT count(*) FROM average_check) * 10 / 100::decimal) THEN 'High'
                WHEN sub_query.row > round((SELECT count(*) FROM average_check) * 10 / 100::decimal)
                    AND sub_query.row <= round((SELECT count(*) FROM average_check) * 35 / 100::decimal) THEN 'Medium'
                ELSE 'Low'
            END AS "Customer_Average_Check_Segment"
        FROM (SELECT customer_id, avg_check,
            row_number() OVER (ORDER BY 2 DESC) AS row
            FROM average_check) AS sub_query
    ),
    transaction_total AS (
        SELECT card_list.customer_id, count(*) AS transaction_total
        FROM card_list
            INNER JOIN transactions ON card_list.customer_card_id = transactions.customer_card_id
        GROUP BY 1
    ),
    transaction_last AS (
        SELECT DISTINCT ON(1) customer_id, transaction_date_time AS day
        FROM card_list
            INNER JOIN transactions ON card_list.customer_card_id = transactions.customer_card_id
        GROUP BY 1, 2
        ORDER BY 1, 2 DESC
    ),
    transaction_first AS (
        SELECT DISTINCT ON(1) customer_id, transaction_date_time AS day
        FROM card_list
            INNER JOIN transactions ON card_list.customer_card_id = transactions.customer_card_id
        GROUP BY 1, 2
        ORDER BY 1, 2
    ),
    transaction_intensity AS (
        SELECT transaction_last.customer_id,
        round(((date_part('day', transaction_last.day - transaction_first.day) + 1) / transaction_total::decimal)::decimal, 10)
            AS "Customer_Frequency"
        FROM transaction_last
            INNER JOIN transaction_first ON transaction_last.customer_id = transaction_first.customer_id
            INNER JOIN transaction_total ON transaction_last.customer_id = transaction_total.customer_id
        ORDER BY 2 -- Сортировка по заданию
    ),
    transaction_segment AS (
        SELECT sub_query.customer_id,
            CASE
                WHEN sub_query.row >= 0
                    AND sub_query.row <= round((SELECT count(*) FROM average_check) * 10 / 100::decimal) THEN 'Often'
                WHEN sub_query.row > round((SELECT count(*) FROM average_check) * 10 / 100::decimal)
                    AND sub_query.row <= round((SELECT count(*) FROM average_check) * 35 / 100::decimal) THEN 'Occasionally'
                ELSE 'Rarely'
            END AS "Customer_Frequency_Segment"
        FROM (SELECT customer_id, "Customer_Frequency",
            row_number() OVER (ORDER BY 2) AS row
            FROM transaction_intensity) AS sub_query
    ),
    period_after_last_transaction AS (
        SELECT transaction_last.customer_id,
        date_part('day', (SELECT * FROM date_reports ORDER BY 1 DESC LIMIT 1) - transaction_last.day) + 1
            AS "Customer_Inactive_Period"
        FROM transaction_last
            INNER JOIN transaction_first ON transaction_last.customer_id = transaction_first.customer_id
    ),
    churn_rate AS (
        SELECT card_list.customer_id,
        round("Customer_Inactive_Period"::decimal / "Customer_Frequency"::decimal, 10) AS "Customer_Churn_Rate"
        FROM card_list
            INNER JOIN period_after_last_transaction ON card_list.customer_id = period_after_last_transaction.customer_id
            INNER JOIN transaction_intensity ON card_list.customer_id = transaction_intensity.customer_id
    ),
    churn_probability AS (
        SELECT card_list.customer_id,
            CASE
                WHEN "Customer_Churn_Rate" >= 0 AND "Customer_Churn_Rate" <= 2 THEN 'Low'
                WHEN "Customer_Churn_Rate" > 2 AND "Customer_Churn_Rate" <= 5 THEN 'Medium'
                ELSE 'High'
            END AS "Customer_Churn_Segment"
        FROM card_list
            INNER JOIN churn_rate ON card_list.customer_id = churn_rate.customer_id
    ),
    customer_segment AS (
        SELECT sub_query.customer_id,
            CASE
                WHEN sub_query.avg_check = 'Low' THEN
                    CASE
                        WHEN sub_query.frequency = 'Rarely' AND sub_query.churn = 'Low' THEN 1
                        WHEN sub_query.frequency = 'Rarely' AND sub_query.churn = 'Medium' THEN 2
                        WHEN sub_query.frequency = 'Rarely' AND sub_query.churn = 'High' THEN 3
                        WHEN sub_query.frequency = 'Occasionally' AND sub_query.churn = 'Low' THEN 4
                        WHEN sub_query.frequency = 'Occasionally' AND sub_query.churn = 'Medium' THEN 5
                        WHEN sub_query.frequency = 'Occasionally' AND sub_query.churn = 'High' THEN 6
                        WHEN sub_query.frequency = 'Often' AND sub_query.churn = 'Low' THEN 7
                        WHEN sub_query.frequency = 'Often' AND sub_query.churn = 'Medium' THEN 8
                        WHEN sub_query.frequency = 'Often' AND sub_query.churn = 'High' THEN 9
                    END
                WHEN sub_query.avg_check = 'Medium' THEN
                    CASE
                        WHEN sub_query.frequency = 'Rarely' AND sub_query.churn = 'Low' THEN 10
                        WHEN sub_query.frequency = 'Rarely' AND sub_query.churn = 'Medium' THEN 11
                        WHEN sub_query.frequency = 'Rarely' AND sub_query.churn = 'High' THEN 12
                        WHEN sub_query.frequency = 'Occasionally' AND sub_query.churn = 'Low' THEN 13
                        WHEN sub_query.frequency = 'Occasionally' AND sub_query.churn = 'Medium' THEN 14
                        WHEN sub_query.frequency = 'Occasionally' AND sub_query.churn = 'High' THEN 15
                        WHEN sub_query.frequency = 'Often' AND sub_query.churn = 'Low' THEN 16
                        WHEN sub_query.frequency = 'Often' AND sub_query.churn = 'Medium' THEN 17
                        WHEN sub_query.frequency = 'Often' AND sub_query.churn = 'High' THEN 18
                    END
                WHEN sub_query.avg_check = 'High' THEN
                    CASE
                        WHEN sub_query.frequency = 'Rarely' AND sub_query.churn = 'Low' THEN 19
                        WHEN sub_query.frequency = 'Rarely' AND sub_query.churn = 'Medium' THEN 20
                        WHEN sub_query.frequency = 'Rarely' AND sub_query.churn = 'High' THEN 21
                        WHEN sub_query.frequency = 'Occasionally' AND sub_query.churn = 'Low' THEN 22
                        WHEN sub_query.frequency = 'Occasionally' AND sub_query.churn = 'Medium' THEN 23
                        WHEN sub_query.frequency = 'Occasionally' AND sub_query.churn = 'High' THEN 24
                        WHEN sub_query.frequency = 'Often' AND sub_query.churn = 'Low' THEN 25
                        WHEN sub_query.frequency = 'Often' AND sub_query.churn = 'Medium' THEN 26
                        WHEN sub_query.frequency = 'Often' AND sub_query.churn = 'High' THEN 27
                    END
            END AS "Customer_Segment"
        FROM (SELECT check_segment.customer_id, "Customer_Average_Check_Segment" AS avg_check,
            "Customer_Frequency_Segment" AS frequency, "Customer_Churn_Segment" AS churn
            FROM check_segment
                INNER JOIN transaction_segment ON check_segment.customer_id = transaction_segment.customer_id
                INNER JOIN churn_probability ON check_segment.customer_id = churn_probability.customer_id) AS sub_query
    ),
    transaction_every_store_number AS (
        SELECT customer_id, transaction_store_id, count(*) AS transaction_number
        FROM card_list
            INNER JOIN transactions ON card_list.customer_card_id = transactions.customer_card_id
        GROUP BY 1, 2
    ),
    transaction_every_store_share AS (
        SELECT transaction_total.customer_id, transaction_store_id,
        round(transaction_every_store_number.transaction_number / transaction_total.transaction_total::decimal, 10)
            AS transaction_share
        FROM transaction_every_store_number
            INNER JOIN transaction_total ON transaction_every_store_number.customer_id = transaction_total.customer_id
        GROUP BY 1, 2, 3
    ),
    last_three_transaction AS (
        SELECT sub_query.customer_id, sub_query.transaction_store_id
        FROM (SELECT customer_id, transaction_store_id,
            row_number() OVER (PARTITION BY customer_id ORDER BY customer_id, transaction_date_time DESC) AS row
            FROM card_list
                INNER JOIN transactions ON card_list.customer_card_id = transactions.customer_card_id) AS sub_query
        WHERE sub_query.row < 4
    ),
    store_number AS (
        SELECT sub_query.customer_id, sub_query.transaction_store_id AS transaction_store_id_three, sub_query.store_number
        FROM (SELECT customer_id, transaction_store_id, count(transaction_store_id) AS store_number
            FROM last_three_transaction
            GROUP BY 1, 2) AS sub_query
    ),
    select_rank AS ( -- В каждом магазине для каждой доли транзакций клиента проставляется ранг и выбираются
                        -- самые большие доли (для каждого клиента доли ранжируются от наибольших к наименьшим)
        SELECT sub_query.customer_id, sub_query.transaction_store_id
        FROM (SELECT customer_id, transaction_store_id,
        dense_rank() OVER (PARTITION BY customer_id ORDER BY customer_id, transaction_share DESC) AS rank
            FROM transaction_every_store_share) AS sub_query
        WHERE sub_query.rank = 1
    ),
    select_row AS ( -- Для отобранных долей проставляется номер в зависимости от времени совершения транзакции
                       -- (транзакции ранжируются от поздних к ранним) и выбирается магазин с самой поздней транзакцией
        SELECT sub_query.customer_id, sub_query.transaction_store_id AS transaction_store_id_last
        FROM (SELECT select_rank.customer_id, select_rank.transaction_store_id,
        row_number() OVER (PARTITION BY select_rank.customer_id ORDER BY transaction_date_time DESC) AS row
            FROM select_rank
                INNER JOIN card_list ON select_rank.customer_id = card_list.customer_id
                INNER JOIN transactions ON card_list.customer_card_id = transactions.customer_card_id
            WHERE select_rank.transaction_store_id = transactions.transaction_store_id) AS sub_query
        WHERE sub_query.row = 1
    ),
    customer_main_store AS (
        SELECT store_number.customer_id,
            CASE
                WHEN store_number >= 3 THEN transaction_store_id_three
                ELSE transaction_store_id_last
            END AS "Customer_Primary_Store"
        FROM store_number
            INNER JOIN select_row ON store_number.customer_id = select_row.customer_id
    )
    SELECT DISTINCT card_list.customer_id AS "Customer_ID", avg_check AS "Customer_Average_Check",
        "Customer_Average_Check_Segment", "Customer_Frequency", "Customer_Frequency_Segment", "Customer_Inactive_Period",
        "Customer_Churn_Rate", "Customer_Churn_Segment", "Customer_Segment", "Customer_Primary_Store"
    FROM card_list
        INNER JOIN average_check ON card_list.customer_id = average_check.customer_id
        INNER JOIN check_segment ON card_list.customer_id = check_segment.customer_id
        INNER JOIN transaction_intensity ON card_list.customer_id = transaction_intensity.customer_id
        INNER JOIN transaction_segment ON card_list.customer_id = transaction_segment.customer_id
        INNER JOIN period_after_last_transaction ON card_list.customer_id = period_after_last_transaction.customer_id
        INNER JOIN churn_rate ON card_list.customer_id = churn_rate.customer_id
        INNER JOIN churn_probability ON card_list.customer_id = churn_probability.customer_id
        INNER JOIN customer_segment ON card_list.customer_id = customer_segment.customer_id
        INNER JOIN customer_main_store ON card_list.customer_id = customer_main_store.customer_id
    ORDER BY 1;

CREATE MATERIALIZED VIEW v_purchase_history AS
    WITH cte_group_cost AS (
        SELECT cards.customer_id, group_id, transaction_date_time, SUM(sku_purchase_price * sku_amount) AS group_cost
        FROM checks
             INNER JOIN goods ON checks.sku_id = goods.sku_id
             INNER JOIN transactions ON checks.transaction_id = transactions.transaction_id
             INNER JOIN cards ON transactions.customer_card_id = cards.customer_card_id
             INNER JOIN stores ON checks.sku_id = stores.sku_id AND transactions.transaction_store_id = stores.transaction_store_id
        GROUP BY cards.customer_id, group_id, transaction_date_time
    ),
    cte_group_summ AS (
        SELECT cards.customer_id, group_id, transaction_date_time, SUM(sku_summ) AS group_summ
        FROM cards
             INNER JOIN transactions ON cards.customer_card_id = transactions.customer_card_id
             INNER JOIN checks ON transactions.transaction_id = checks.transaction_id
             INNER JOIN goods ON checks.sku_id = goods.sku_id
        GROUP BY cards.customer_id, group_id, transaction_date_time
    ),
    cte_group_summ_paid AS (
        SELECT cards.customer_id, group_id, transaction_date_time, SUM(sku_summ_paid) AS group_summ_paid
        FROM cards
             INNER JOIN transactions ON cards.customer_card_id = transactions.customer_card_id
             INNER JOIN checks ON transactions.transaction_id = checks.transaction_id
             INNER JOIN goods ON checks.sku_id = goods.sku_id
        GROUP BY cards.customer_id, group_id, transaction_date_time
    )
    SELECT DISTINCT cards.customer_id,
       transactions.transaction_id,
       transaction_date_time AS transaction_datetime,
       group_id,
       cte_group_cost.group_cost,
       cte_group_summ.group_summ,
       cte_group_summ_paid.group_summ_paid
    FROM cards
     INNER JOIN transactions ON cards.customer_card_id = transactions.customer_card_id
     INNER JOIN checks ON transactions.transaction_id = checks.transaction_id
     INNER JOIN goods ON checks.sku_id = goods.sku_id
     INNER JOIN cte_group_cost USING (customer_id, group_id, transaction_date_time)
     INNER JOIN cte_group_summ USING (customer_id, group_id, transaction_date_time)
     INNER JOIN cte_group_summ_paid USING (customer_id, group_id, transaction_date_time);

CREATE MATERIALIZED VIEW v_periods AS
    WITH cte_first_transaction_datetime AS (
        SELECT v_purchase_history.customer_id AS customer_id,
           v_purchase_history.group_id AS group_id,
           v_purchase_history.transaction_datetime AS first_group_purchase_date,
           ROW_NUMBER() OVER (PARTITION BY customer_id, group_id ORDER BY transaction_datetime) AS rating_first
        FROM v_purchase_history
    ),
    cte_last_transaction_datetime AS (
        SELECT v_purchase_history.customer_id AS customer_id,
           v_purchase_history.group_id AS group_id,
           v_purchase_history.transaction_datetime AS last_group_purchase_date,
           ROW_NUMBER() OVER (PARTITION BY customer_id, group_id ORDER BY transaction_datetime DESC ) AS rating_last
        FROM v_purchase_history
    ),
    cte_group_min_discount AS (
        WITH cte_tmp AS (
            SELECT customer_id, group_id,
                   SUM(sku_discount / sku_summ::numeric) AS group_min_discount
            FROM checks
                 INNER JOIN v_purchase_history ON v_purchase_history.transaction_id = checks.transaction_id
            GROUP BY customer_id, group_id
        )
        SELECT DISTINCT customer_id, group_id, group_min_discount
        FROM cte_tmp
        WHERE cte_tmp.group_min_discount = 0
        UNION
        SELECT DISTINCT customer_id, group_id,
               MIN(sku_discount / sku_summ::numeric) AS group_min_discount
        FROM checks
             INNER JOIN v_purchase_history ON v_purchase_history.transaction_id = checks.transaction_id
        WHERE sku_discount / sku_summ::numeric != 0
        GROUP BY customer_id, group_id
    )
    SELECT cards.customer_id, group_id, first_group_purchase_date, last_group_purchase_date,
       COUNT(transactions.transaction_id) AS group_purchase,
       ((SELECT EXTRACT(EPOCH FROM(last_group_purchase_date - first_group_purchase_date)+ interval '1 day')))/
       60000 / COUNT(transactions.transaction_id) AS group_frequency,
       cte_group_min_discount.group_min_discount
    FROM cards
     INNER JOIN transactions ON cards.customer_card_id = transactions.customer_card_id
     INNER JOIN checks ON transactions.transaction_id = checks.transaction_id
     INNER JOIN goods ON checks.sku_id = goods.sku_id
     INNER JOIN cte_first_transaction_datetime USING (customer_id, group_id)
     INNER JOIN cte_last_transaction_datetime USING (customer_id, group_id)
     INNER JOIN cte_group_min_discount USING (customer_id, group_id)
    WHERE rating_first = 1 AND rating_last = 1
    GROUP BY cards.customer_id, group_id, first_group_purchase_date, last_group_purchase_date, group_min_discount;

CREATE INDEX IF NOT EXISTS idx1_purchase_history ON v_purchase_history(customer_id);
CREATE INDEX IF NOT EXISTS idx2_purchase_history ON v_purchase_history(group_id);
CREATE INDEX IF NOT EXISTS idx3_purchase_history ON v_purchase_history(transaction_datetime);
CREATE INDEX IF NOT EXISTS idx1_periods ON v_periods(customer_id,group_id);
CREATE INDEX IF NOT EXISTS idx2_periods ON v_periods(group_min_discount);

CREATE OR REPLACE VIEW v_groups AS
    WITH count_all_transaction AS (
        SELECT cards.customer_id AS customer_id,
                COUNT(transactions.transaction_id) AS count_all_trans,
                groups_of_goods.group_id AS group_id
        FROM transactions JOIN cards ON cards.customer_card_id = transactions.customer_card_id
        CROSS JOIN groups_of_goods
        WHERE transactions.transaction_date_time >= (SELECT v_periods.first_group_purchase_date
                                                        FROM v_periods
                                                        WHERE cards.customer_id = v_periods.customer_id  AND
                                                        groups_of_goods.group_id = v_periods.group_id)
                                                                                AND
                transactions.transaction_date_time <= (SELECT vp.last_group_purchase_date
                                                         FROM v_periods vp
                                                         WHERE cards.customer_id = vp.customer_id  AND
                                                         groups_of_goods.group_id = vp.group_id)
        GROUP BY cards.customer_id, groups_of_goods.group_id
        ORDER BY 1
    ),
    cte_group_affinity_index_final AS (
        SELECT v_periods.customer_id, v_periods.group_id,
                group_purchase / count_all_trans::NUMERIC AS group_affinity_index
        FROM v_periods JOIN count_all_transaction USING(group_id, customer_id)
    ),
    cte_analysis_formation AS (
        SELECT analysis_formation, 'check_id' AS check_id
        FROM date_reports
    ),
    cte_avg_frequency AS (
        SELECT customer_id, group_id, AVG(group_frequency) AS avg_group_frequency
        FROM v_periods
        GROUP BY customer_id, group_id
    ),
    cte_group_churn_rate AS (
        SELECT DISTINCT cte_avg_frequency.customer_id,
               v_periods.group_id AS group_id,
               DATE_PART('day', cte_analysis_formation.analysis_formation - last_group_purchase_date) AS delta_day,
              (SELECT EXTRACT(EPOCH FROM (cte_analysis_formation.analysis_formation - last_group_purchase_date)))
                  / 60000 / cte_avg_frequency.avg_group_frequency::numeric AS group_churn_rate
        FROM v_periods
             INNER JOIN cte_analysis_formation ON cte_analysis_formation.check_id = 'check_id'
             INNER JOIN cte_avg_frequency ON v_periods.group_id = cte_avg_frequency.group_id
                                                 AND v_periods.customer_id = cte_avg_frequency.customer_id
    ),
    cte_lag_transaction AS (
        WITH  find_prev_lag AS (
            SELECT customer_id, group_id, transaction_datetime,
                   ROW_NUMBER() OVER (PARTITION BY customer_id, group_id ORDER BY transaction_datetime) AS rating,
                   LAG(transaction_datetime) OVER (PARTITION BY customer_id, group_id) AS prev_transaction_datetime
            FROM v_purchase_history
            )
        SELECT customer_id, group_id, rating,
               (SELECT EXTRACT(EPOCH FROM (transaction_datetime - prev_transaction_datetime))) / 60000::numeric AS delta_transaction
        FROM find_prev_lag
    ),
    cte_group_stability_index AS (
        SELECT customer_id, group_id,
            CASE
                WHEN ((delta_transaction - v_periods.group_frequency) / v_periods.group_frequency::NUMERIC) < 0
                THEN ((delta_transaction - v_periods.group_frequency) / v_periods.group_frequency::NUMERIC) * -1
                ELSE (delta_transaction - v_periods.group_frequency) / v_periods.group_frequency::NUMERIC
            END AS regarding_delta_transaction
        FROM cte_lag_transaction
            LEFT JOIN v_periods USING (customer_id, group_id)
        WHERE rating != 1
    ),
    cte_group_stability_index_final AS (
        SELECT customer_id, group_id, AVG(regarding_delta_transaction) AS group_stability_index
        FROM cte_group_stability_index
        GROUP BY customer_id, group_id
    ),
    cte_group_margin AS (
        SELECT customer_id, group_id,
               SUM(group_summ_paid - group_cost) AS group_margin
        FROM v_purchase_history
        GROUP BY customer_id, group_id
    ),
    cte_transaction_count AS (
        SELECT DISTINCT cards.customer_id AS customer_id, group_id,
               COUNT(checks.transaction_id) AS count_transaction
        FROM cards
            INNER JOIN transactions ON cards.customer_card_id = transactions.customer_card_id
            INNER JOIN checks ON transactions.transaction_id = checks.transaction_id
            INNER JOIN goods ON checks.sku_id = goods.sku_id
        WHERE sku_discount > 0
        GROUP BY cards.customer_id, group_id
    ),
    cte_transaction_count_final AS (
        SELECT v_periods.customer_id, v_periods.group_id,
               cte_transaction_count.count_transaction / v_periods.group_purchase::NUMERIC AS group_discount_share
        FROM v_periods
             INNER JOIN cte_transaction_count USING (customer_id, group_id)
    ),
    cte_min_group_discount AS (
        SELECT customer_id, group_id, group_min_discount,
               ROW_NUMBER() OVER (PARTITION BY customer_id, group_id ORDER BY group_min_discount) AS rating_discount
        FROM v_periods
    ),
    cte_min_group_discount_final AS (
        SELECT customer_id, group_id,
               group_min_discount AS group_minimum_discount
        FROM cte_min_group_discount
        WHERE rating_discount = 1
    ),
    cte_group_average_discount AS (
        SELECT customer_id, group_id,
               AVG(group_summ_paid/group_summ) AS group_average_discount
        FROM v_purchase_history
        WHERE (group_summ_paid/group_summ::numeric) != 1
        GROUP BY customer_id, group_id
    )
    SELECT DISTINCT cte_group_average_discount.customer_id, cte_group_average_discount.group_id,
       group_affinity_index, group_churn_rate, group_stability_index, group_margin,
       group_discount_share, group_minimum_discount, group_average_discount
    FROM cte_group_average_discount
     INNER JOIN cte_min_group_discount_final USING (customer_id, group_id)
     INNER JOIN cte_group_affinity_index_final USING (customer_id, group_id)
     INNER JOIN cte_group_churn_rate USING (customer_id, group_id)
     INNER JOIN cte_transaction_count_final USING (customer_id, group_id)
     INNER JOIN cte_group_stability_index_final USING (customer_id, group_id)
     LEFT JOIN cte_group_margin USING (customer_id, group_id);

CREATE OR REPLACE FUNCTION fnc_personal_offers_average_check(pmethod integer DEFAULT 1, pfirst_day date DEFAULT '2018-04-01',
    plast_day date DEFAULT '2022-03-01', ptransaction_number integer DEFAULT 5, pcoeff_avg_check decimal DEFAULT 1.5,
    pmax_churn_index integer DEFAULT 10, pmax_share_transactions integer DEFAULT 70, pshare_margin integer DEFAULT 50)
RETURNS TABLE("Customer_ID" bigint, "Required_Check_Measure" decimal, "Group_Name" varchar,
    "Offer_Discount_Depth" decimal)
AS $fnc_part4$
    BEGIN
        IF (pmethod <> 1 AND pmethod <> 2) THEN RAISE EXCEPTION 'Choose a method of calculating an average check';
        ELSIF (pfirst_day >= plast_day) THEN RAISE EXCEPTION 'Choose the first and last dates of the period';
        ELSIF (ptransaction_number <= 0) THEN RAISE EXCEPTION 'Choose the number of recent transactions';
        ELSIF (pcoeff_avg_check <= 0) THEN RAISE EXCEPTION 'Choose the number of recent transactions';
        ELSIF (pmax_churn_index <= 0 OR pmax_churn_index > 100) THEN RAISE EXCEPTION 'Choose the maximum churn index';
        ELSIF (pmax_share_transactions <= 0 OR pmax_share_transactions > 100) THEN RAISE EXCEPTION 'Choose the maximum share of transactions with a discount';
        ELSIF (pshare_margin <= 0 OR pshare_margin > 100) THEN RAISE EXCEPTION 'Choose the allowable share of margin';
        END IF;
        RETURN QUERY
        WITH avg_check_first_method AS (
            SELECT sub_query.customer_id, round(sum(sub_query.transaction_summ) / count(*) * pcoeff_avg_check, 10)
                AS avg_check_first_method
            FROM (SELECT customer_id, transaction_summ, transaction_date_time
                FROM cards
                    INNER JOIN transactions ON cards.customer_card_id = transactions.customer_card_id) AS sub_query
            WHERE sub_query.transaction_date_time BETWEEN pfirst_day AND plast_day
            GROUP BY 1, pcoeff_avg_check
            ORDER BY 1
        ),
        avg_check_second_method AS (
            SELECT sub_query.customer_id, round(sum(sub_query.transaction_summ) / ptransaction_number * pcoeff_avg_check, 10)
                AS avg_check_second_method
            FROM (SELECT customer_id, transaction_summ,
            row_number() OVER (PARTITION BY customer_id ORDER BY customer_id, transaction_date_time DESC) AS row
                FROM cards
                    INNER JOIN transactions ON cards.customer_card_id = transactions.customer_card_id) AS sub_query
            WHERE sub_query.row <= ptransaction_number
            GROUP BY 1, ptransaction_number, pcoeff_avg_check
        ),
        find_group AS (
            SELECT customer_id , group_id,
            dense_rank() OVER (PARTITION BY customer_id ORDER BY group_affinity_index DESC) AS rank
            FROM v_groups
            WHERE group_churn_rate <= pmax_churn_index AND group_discount_share * 100 < pmax_share_transactions
        ),
        select_group AS (
            SELECT find_group.customer_id, find_group.group_id, rank,
            group_margin * pshare_margin / 100::decimal AS limit_discount,
            CASE
                WHEN floor(v_groups.group_minimum_discount * 100) % 5 = 0
                    THEN floor(v_groups.group_minimum_discount * 100)
                ELSE (floor(v_groups.group_minimum_discount * 100 + 5) - floor(v_groups.group_minimum_discount * 100 + 5) % 5)
            END AS max_discount
            FROM find_group
                INNER JOIN v_groups ON find_group.customer_id = v_groups.customer_id
                    AND find_group.group_id = v_groups.group_id
        )
        SELECT avg_check_second_method.customer_id,
            CASE
                WHEN pmethod = 1 THEN avg_check_first_method
                ELSE avg_check_second_method
            END,
            group_name, max_discount
        FROM avg_check_first_method
            INNER JOIN avg_check_second_method ON avg_check_first_method.customer_id = avg_check_second_method.customer_id
            INNER JOIN select_group ON avg_check_first_method.customer_id = select_group.customer_id
            INNER JOIN groups_of_goods ON select_group.group_id = groups_of_goods.group_id
        WHERE max_discount < limit_discount AND max_discount != 0
            AND select_group.rank = (SELECT min(s_g.rank) FROM select_group s_g WHERE s_g.customer_id = select_group.customer_id);
    END;
$fnc_part4$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION fnc_offer_customer_frequency (first_date timestamp, last_date timestamp,
    add_count_transaction bigint, input_churn_rate numeric, input_discount_share numeric, input_group_margin numeric)
RETURNS TABLE (customer_id bigint, start_date timestamp, end_date timestamp,
                  required_transactions_count numeric, group_name varchar, offer_discount_depth numeric)
AS $fnc_part5$
    BEGIN
    RETURN QUERY
    WITH cte_base_intensity_transactions AS (
        SELECT v_customers."Customer_ID" AS customer_id,
               (SELECT EXTRACT(EPOCH FROM (last_date - first_date)) / 60000 / v_customers."Customer_Frequency"::numeric)
                   AS base_intensity_customer_transactions
        FROM v_customers
    ),
    cte_required_transactions_count AS (
        SELECT  cte_base_intensity_transactions.customer_id,
            ROUND(base_intensity_customer_transactions, 0) + add_count_transaction AS required_transactions_count
        FROM cte_base_intensity_transactions
    ),
    cte_find_group AS (
        SELECT v_groups.customer_id , v_groups.group_id, v_groups.group_affinity_index,
                v_groups.group_churn_rate, v_groups.group_discount_share,
                DENSE_RANK() OVER (PARTITION BY v_groups.customer_id ORDER BY v_groups.group_affinity_index DESC)  AS rank
        FROM v_groups
        WHERE group_churn_rate <= input_churn_rate AND (v_groups.group_discount_share * 100) < input_discount_share
    ),
    cte_select_group AS (
        SELECT fg.customer_id, fg.group_id,  group_margin * input_group_margin / 100::numeric AS limit_discount,
            CASE
                WHEN FLOOR(v.group_minimum_discount * 100) % 5 = 0 THEN FLOOR(v.group_minimum_discount*100)
                ELSE FLOOR(v.group_minimum_discount * 20) * 5 + 5
            END AS min_discount, fg.rank
        FROM cte_find_group fg JOIN v_groups v ON fg.customer_id = v.customer_id AND fg.group_id = v.group_id
    )
    SELECT  sg.customer_id, first_date, last_date, rtc.required_transactions_count,
           gg.group_name, sg.min_discount
    FROM cte_select_group sg JOIN groups_of_goods gg USING(group_id)
        JOIN cte_required_transactions_count rtc USING(customer_id)
    WHERE sg.min_discount < sg.limit_discount AND sg.min_discount != 0
      AND sg.rank = (SELECT MIN(sg1.rank) FROM cte_select_group sg1 WHERE sg1.customer_id = sg.customer_id);
    END;
$fnc_part5$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION fnc_offer_cross_selling(group_amount bigint, max_group_churn_rate numeric,
    max_group_stability_index numeric, max_sku_share numeric, limit_margin_share numeric)
RETURNS TABLE(customer_id bigint, sku_name varchar, offer_discount_depth numeric)
AS $fnc_part6$
    BEGIN
    RETURN QUERY
    WITH find_group AS (
        SELECT v_groups.customer_id , v_groups.group_id, v_groups.group_affinity_index,
                DENSE_RANK() OVER (PARTITION BY v_groups.customer_id ORDER BY v_groups.group_affinity_index DESC)  AS rank
        FROM v_groups
        WHERE group_churn_rate <= max_group_churn_rate AND group_stability_index < max_group_stability_index
    ),
    select_group AS (
        SELECT find_group.customer_id, find_group.group_id AS selected_group
        FROM find_group
        WHERE rank <= group_amount
    ),
    sku_every_group AS (
        SELECT s.customer_id, s.selected_group, g.sku_id, g.sku_name
        FROM select_group s JOIN goods g ON s.selected_group = g.group_id
        ORDER BY 1,2,3
    ),
    margin_sku_every_group AS (
        SELECT seg.customer_id, seg.selected_group, seg.sku_id, seg.sku_name, c."Customer_Primary_Store" AS main_store,
                s.sku_retail_price, s.sku_purchase_price, (s.sku_retail_price - s.sku_purchase_price) AS sku_margin
        FROM sku_every_group seg JOIN v_customers c ON c."Customer_ID" = seg.customer_id
            JOIN stores s ON s.transaction_store_id = c."Customer_Primary_Store" AND s.sku_id = seg.sku_id
    ),
    max_margin_sku_every_group AS (
        SELECT msg.customer_id, msg.selected_group, msg.sku_id, msg.sku_name, msg.main_store,
                msg.sku_retail_price, msg.sku_purchase_price, MAX(msg.sku_margin) AS max_margin
        FROM margin_sku_every_group msg
        GROUP BY msg.customer_id, msg.selected_group, msg.sku_id, msg.sku_name, msg.main_store,
                msg.sku_retail_price, msg.sku_purchase_price
        ORDER BY 1, 2, 3
    ),
    sku_trans_count AS (
        SELECT DISTINCT checks.sku_id, g2.sku_name, g2.group_id, COUNT(*) OVER (PARTITION BY checks.sku_id) AS sku_count,
                COUNT(*) OVER (PARTITION BY g2.group_id) AS group_count
        FROM checks JOIN goods g2 on g2.sku_id = checks.sku_id
        ORDER BY 3, 1
    ),
    sku_share_every_group AS (
        SELECT skt.sku_id, skt.sku_name, (skt.sku_count / skt.group_count::numeric * 100) AS sku_share
        FROM sku_trans_count skt
        WHERE (skt.sku_count / skt.group_count::numeric * 100) <= max_sku_share
    ),
    count_discount AS (
        SELECT mmsg.customer_id, mmsg.selected_group, mmsg.sku_id, mmsg.sku_name, mmsg.sku_retail_price, mmsg.max_margin,
                CASE
                    WHEN FLOOR(v.group_minimum_discount * 100) % 5 = 0 THEN FLOOR(v.group_minimum_discount*100)
                    ELSE FLOOR(v.group_minimum_discount * 20) * 5 + 5
                END AS min_discount,
                (limit_margin_share * mmsg.max_margin / mmsg.sku_retail_price ) AS compare_field
        FROM max_margin_sku_every_group mmsg JOIN v_groups v ON v.customer_id = mmsg.customer_id AND v.group_id = mmsg.selected_group
        WHERE mmsg.sku_id IN (SELECT sku_id FROM sku_share_every_group)
        ORDER BY 1, 2, 3
    )
    SELECT cd.customer_id,  cd.sku_name, cd.min_discount AS offer_discount_depth
    FROM count_discount cd
    WHERE cd.compare_field >= cd.min_discount;
   END;
$fnc_part6$ LANGUAGE plpgsql;
