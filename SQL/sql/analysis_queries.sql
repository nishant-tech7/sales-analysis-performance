-- 1. Total business KPIs
SELECT
    ROUND(SUM(Sales), 2) AS TotalSales,
    ROUND(SUM(Profit), 2) AS TotalProfit,
    COUNT(DISTINCT OrderID) AS TotalOrders,
    COUNT(DISTINCT CustomerID) AS TotalCustomers,
    ROUND(SUM(Profit) * 100.0 / SUM(Sales), 2) AS ProfitMarginPercentage
FROM retail_orders;


-- 2. Monthly sales and profit trend
SELECT
    strftime('%Y-%m', OrderDate) AS Month,
    ROUND(SUM(Sales), 2) AS TotalSales,
    ROUND(SUM(Profit), 2) AS TotalProfit
FROM retail_orders
GROUP BY Month
ORDER BY Month;


-- 3. Sales and profit by category
SELECT
    Category,
    ROUND(SUM(Sales), 2) AS TotalSales,
    ROUND(SUM(Profit), 2) AS TotalProfit,
    ROUND(SUM(Profit) * 100.0 / SUM(Sales), 2) AS ProfitMarginPercentage
FROM retail_orders
GROUP BY Category
ORDER BY TotalSales DESC;


-- 4. Sales and profit by region
SELECT
    Region,
    ROUND(SUM(Sales), 2) AS TotalSales,
    ROUND(SUM(Profit), 2) AS TotalProfit
FROM retail_orders
GROUP BY Region
ORDER BY TotalSales DESC;


-- 5. Top 10 products by sales
SELECT
    Product,
    Category,
    ROUND(SUM(Sales), 2) AS TotalSales,
    ROUND(SUM(Profit), 2) AS TotalProfit
FROM retail_orders
GROUP BY Product, Category
ORDER BY TotalSales DESC
LIMIT 10;


-- 6. Top 10 customers by sales
SELECT
    CustomerID,
    CustomerName,
    ROUND(SUM(Sales), 2) AS TotalSales,
    ROUND(SUM(Profit), 2) AS TotalProfit,
    COUNT(DISTINCT OrderID) AS NumberOfOrders
FROM retail_orders
GROUP BY CustomerID, CustomerName
ORDER BY TotalSales DESC
LIMIT 10;


-- 7. Discount impact on profit
SELECT
    Discount,
    COUNT(OrderID) AS NumberOfOrders,
    ROUND(SUM(Sales), 2) AS TotalSales,
    ROUND(SUM(Profit), 2) AS TotalProfit,
    ROUND(
        SUM(Profit) * 100.0 / NULLIF(SUM(Sales), 0),
        2
    ) AS AverageProfitMargin
FROM retail_orders
GROUP BY Discount
ORDER BY Discount;


-- 8. Loss-making orders
SELECT
    OrderID,
    OrderDate,
    CustomerName,
    Product,
    Category,
    Discount,
    Sales,
    Profit
FROM retail_orders
WHERE Profit < 0
ORDER BY Profit ASC;

--9. Total rows in the retail_orders table

SELECT COUNT(*) AS total_rows
FROM retail_orders;

--10. Sample data from the retail_orders table

SELECT *
FROM retail_orders
LIMIT 10;

SELECT category, SUM(sales) AS total_sales
FROM retail_orders
GROUP BY category
ORDER BY total_sales DESC;