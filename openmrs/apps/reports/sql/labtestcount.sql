SELECT ROW_NUMBER() OVER (ORDER BY sol.name) as "Sl No",sol.name as "Test Name",sum(sol.product_uom_qty)as "Total Count",sol.price_unit as "Unit price",cast(sum(price_unit * sol.product_uom_qty) as DECIMAL (10,2)) as "TotalAmount"
FROM sale_order_line sol
LEFT JOIN res_partner rp on rp.id=sol.order_partner_id
inner join sale_order so on so.id=sol.order_id
WHERE product_id IN(
  SELECT pp.id
  FROM product_product pp
    INNER JOIN product_template pt ON pp.product_tmpl_id = pt.id
  WHERE pt.categ_id IN (select category_id from syncjob_chargetype_category_mapping
                          WHERE chargetype_name = 'Investigations'))
      AND (sol.create_date BETWEEN '#startDate#' and '#endDate#')
      AND (sol.state = 'confirmed')
     GROUP BY sol.name,sol.price_unit
     order by sol.name;
