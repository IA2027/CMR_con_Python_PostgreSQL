
SELECT
    estado,
    COUNT(*) AS cantidad,
    SUM(valor) AS valor_total
FROM oportunidades
GROUP BY estado
ORDER BY valor_total DESC;
