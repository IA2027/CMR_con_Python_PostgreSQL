
SELECT
    c.nombre,
    c.apellido,
    c.email,
    e.nombre AS empresa
FROM clientes c
INNER JOIN empresas e
ON c.id_empresa = e.id_empresa
WHERE e.nombre = 'Tech Solutions';
