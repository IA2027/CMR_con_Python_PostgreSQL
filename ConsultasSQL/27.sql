
CREATE OR REPLACE VIEW vista_historial_crm AS

SELECT
    i.id_interaccion,
    c.nombre || ' ' || c.apellido AS cliente,
    em.nombre || ' ' || em.apellido AS empleado,
    i.tipo,
    i.descripcion,
    i.fecha_interaccion

FROM interacciones i

INNER JOIN clientes c
ON i.id_cliente = c.id_cliente

INNER JOIN empleados em
ON i.id_empleado = em.id_empleado;
