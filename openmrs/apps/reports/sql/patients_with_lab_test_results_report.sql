SELECT so.care_setting,rp.ref as Patient_id,rp.name as "Patient Name",sol.name as "Test Name",
sol.product_uom_qty,sol.price_unit,cast(sum(price_unit * sol.product_uom_qty) as DECIMAL (10,2)) as "TotalAmount",
cast(sol.create_date as Date)
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
     GROUP BY order_id,sol.name,sol.product_uom_qty,so.care_setting,rp.ref,sol.price_unit,rp.name,sol.create_date 
     order by rp.name asc;

