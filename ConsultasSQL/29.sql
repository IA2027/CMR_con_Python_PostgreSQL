
CREATE OR REPLACE VIEW vista_oportunidades_crm AS

SELECT
    o.id_oportunidad,
    o.titulo,
    c.nombre || ' ' || c.apellido AS cliente,
    em.nombre || ' ' || em.apellido AS responsable,
    o.valor,
    o.estado,
    o.fecha_creacion

FROM oportunidades o

INNER JOIN clientes c
ON o.id_cliente = c.id_cliente

INNER JOIN empleados em
ON o.id_empleado = em.id_empleado;
