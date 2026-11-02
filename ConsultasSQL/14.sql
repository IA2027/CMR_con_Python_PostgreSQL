
SELECT 'empresas' AS tabla, COUNT(*) AS registros
FROM empresas

UNION ALL

SELECT 'empleados', COUNT(*)
FROM empleados

UNION ALL

SELECT 'clientes', COUNT(*)
FROM clientes

UNION ALL

SELECT 'interacciones', COUNT(*)
FROM interacciones

UNION ALL

SELECT 'oportunidades', COUNT(*)
FROM oportunidades;
