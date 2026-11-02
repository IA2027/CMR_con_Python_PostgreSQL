
SELECT
    titulo,
    valor,
    estado
FROM oportunidades
WHERE valor > 1000000
ORDER BY valor DESC;
