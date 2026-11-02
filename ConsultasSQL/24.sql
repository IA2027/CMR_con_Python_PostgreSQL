
CREATE OR REPLACE VIEW vista_clientes_crm AS

SELECT
    c.id_cliente,
    c.nombre,
    c.apellido,
    c.email,
    c.telefono,
    c.estado,
    e.nombre AS empresa,
    e.sector,
    c.fecha_registro

FROM clientes c

LEFT JOIN empresas e
ON c.id_empresa = e.id_empresa;
