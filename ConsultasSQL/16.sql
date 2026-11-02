
SELECT
    c.nombre || ' ' || c.apellido AS cliente,
    em.nombre || ' ' || em.apellido AS empleado,
    e.nombre AS empresa,
    i.tipo,
    i.descripcion,
    i.fecha_interaccion

FROM interacciones i

INNER JOIN clientes c
ON i.id_cliente = c.id_cliente

INNER JOIN empleados em
ON i.id_empleado = em.id_empleado

LEFT JOIN empresas e
ON c.id_empresa = e.id_empresa

ORDER BY i.fecha_interaccion DESC;
