
SELECT
    e.nombre,
    e.apellido,
    COUNT(o.id_oportunidad) AS oportunidades,
    COALESCE(SUM(o.valor), 0) AS valor_total

FROM empleados e

LEFT JOIN oportunidades o
ON e.id_empleado = o.id_empleado

GROUP BY e.id_empleado, e.nombre, e.apellido

ORDER BY valor_total DESC;
