SELECT
    o.titulo,
    c.nombre || ' ' || c.apellido AS cliente,
    em.nombre || ' ' || em.apellido AS responsable,
    e.nombre AS empresa,
    o.valor,
    o.estado

FROM oportunidades o

INNER JOIN clientes c
ON o.id_cliente = c.id_cliente

INNER JOIN empleados em
ON o.id_empleado = em.id_empleado

LEFT JOIN empresas e
ON c.id_empresa = e.id_empresa

ORDER BY o.valor DESC;