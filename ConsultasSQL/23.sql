
SELECT
    COUNT(*) AS oportunidades_ganadas,
    SUM(valor) AS facturacion_potencial_ganada
FROM oportunidades
WHERE estado = 'Ganada';
