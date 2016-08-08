SELECT rp.name as "Patient name",rp.village, (case when rpa."x_Is_Tribal" = 'False' then 'Non Tribe'
                           else 'Tribe' END) as Caste,
pt.name as Medicine,spl.name as Batch,cast(spl.life_date as Date) as Expiry,pp.manufacturer as Mfg,sol.product_uom_qty as Qty,(sol.price_unit*sol.product_uom_qty) as "Bill Amount",
so.provider_name from sale_order_line sol inner JOIN
product_product pp on pp.id = sol.product_id and pp.product_scheduleh=TRUE
  INNER JOIN
  product_template pt on pt.id=pp.product_tmpl_id
and pt.categ_id in(SELECT id from product_category where parent_id= (select id from product_category where name='Drug')
)
INNER JOIN sale_order so on so.id = sol.order_id and cast(so.date_confirm as DATE) between '#startDate#' and '#endDate#'
INNER JOIN res_partner rp on rp.id = so.partner_id
INNER JOIN res_partner_attributes rpa on rp.id = rpa.partner_id
inner JOIN stock_production_lot spl on spl.id = sol.batch_id
GROUP BY rp.id,pt.name,sol.product_uom_qty,sol.price_unit,so.provider_name,rpa."x_Is_Tribal",spl.name,spl.life_date
,pp.manufacturer
ORDER BY rp.name;
