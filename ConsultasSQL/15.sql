
SELECT
    c.id_cliente,
    c.nombre,
    c.apellido,
    c.email,
    c.estado,
    e.nombre AS empresa,
    e.sector

FROM clientes c

INNER JOIN empresas e
ON c.id_empresa = e.id_empresa

ORDER BY c.id_cliente;
