SELECT rs.name as "Supplier Name",pol.name as "Product Name",spl.cost_price ,spl.mrp,spl.sale_price, Max(cast(sm.create_date as Date))
FROM  purchase_order_line pol
INNER JOIN purchase_order po on po.id = pol.order_id
INNER JOIN res_partner rs on rs.id = pol.partner_id
INNER JOIN stock_move sm on sm.purchase_line_id = pol.id
INNER JOIN stock_production_lot spl on spl.id = sm.prodlot_id
Where pol.state = 'confirmed' 
group by rs.name,pol.name,spl.cost_price ,spl.mrp,spl.sale_price
order by pol.name; 
