SELECT so.care_setting,(case when rpa."x_Is_Tribal" = 'False' then 'Non Tribe'
else 'Tribe' END) as Caste,pc.name,sol.name as "Product name",count(sol.id),sol.price_unit,
round(sum(sol.product_uom_qty*sol.price_unit),2) as Total from sale_order_line sol
INNER JOIN sale_order so on sol.order_id=so.id and (so.state!='cancel' or so.state!='draft')
INNER join res_partner rp on rp.id = so.partner_id
INNER JOIN res_partner_attributes rpa on rp.id = rpa.partner_id
INNER JOIN product_template pt ON pt.id = sol.product_id
INNER JOIN product_category pc on pc.id = pt.categ_id
WHERE product_id IN(SELECT pp.id FROM product_product pp INNER JOIN product_template pt ON pp.product_tmpl_id = pt.id
WHERE pt.categ_id IN (select id from product_category WHERE  parent_id in (551,534)))
and cast(so.date_confirm as DATE) between '#startDate#' and '#endDate#'
group by sol.name,sol.price_unit,so.care_setting,rpa."x_Is_Tribal",pc.name
order by pc.name;

