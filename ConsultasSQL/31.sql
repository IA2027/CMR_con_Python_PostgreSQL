
SELECT

    (SELECT COUNT(*)
     FROM clientes) AS total_clientes,

    (SELECT COUNT(*)
     FROM clientes
     WHERE estado = 'Activo') AS clientes_activos,

    (SELECT COUNT(*)
     FROM oportunidades) AS total_oportunidades,

    (SELECT COUNT(*)
     FROM oportunidades
     WHERE estado = 'Ganada') AS oportunidades_ganadas,

    (SELECT COALESCE(SUM(valor), 0)
     FROM oportunidades
     WHERE estado = 'Ganada') AS valor_ganado,

    (SELECT COALESCE(SUM(valor), 0)
     FROM oportunidades
     WHERE estado IN ('Nueva', 'En proceso')) AS pipeline_comercial;
