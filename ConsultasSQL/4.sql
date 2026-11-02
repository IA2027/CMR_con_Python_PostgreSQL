SELECT
    c.nombre AS cliente,
    c.apellido,
    p.id_pedido,
    p.fecha_pedido,
    pr.nombre AS producto,
    cat.nombre AS categoria,
    dp.cantidad,
    dp.precio_unitario,
    dp.cantidad * dp.precio_unitario AS subtotal

FROM clientes c

INNER JOIN pedidos p
    ON c.id_cliente = p.id_cliente

INNER JOIN detalle_pedidos dp
    ON p.id_pedido = dp.id_pedido

INNER JOIN productos pr
    ON dp.id_producto = pr.id_producto

INNER JOIN categorias cat
    ON pr.id_categoria = cat.id_categoria;