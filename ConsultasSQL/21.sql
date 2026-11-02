
SELECT
    estado,
    COUNT(*) AS cantidad_clientes
FROM clientes
GROUP BY estado
ORDER BY cantidad_clientes DESC;
