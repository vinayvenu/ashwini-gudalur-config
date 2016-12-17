SELECT so.care_setting,(case when rpa."x_Is_Tribal" = 'False' then 'Non Tribe'
else 'Tribe' END) as Caste,sum(vop.amount_original)as "Amount Original",sum(vop.amount_total) as "Total Billed",
sum(vop.amount_tax) as "Amount_Tax",
sum(vop.amount_untaxed) as "Amount Untaxed",sum(vop.discount_amount) as Discount,
sum(vop.paid) as Paid FROM so_payment_rln vop 
INNER JOIN sale_order so on so.id = vop.order_id 
INNER join res_partner rp on rp.id = so.partner_id
INNER JOIN res_partner_attributes rpa on rp.id = rpa.partner_id
where order_id in (SELECT distinct(sol.order_id) FROM sale_order_line sol
WHERE product_id IN(SELECT pp.id FROM product_product pp INNER JOIN product_template pt ON pp.product_tmpl_id = pt.id
WHERE pt.categ_id IN (select category_id from syncjob_chargetype_category_mapping WHERE chargetype_name = 'Investigations'))
AND sol.create_date between '#startDate#' and '#endDate#')
GROUP by so.care_setting,rpa."x_Is_Tribal"
order by so.care_setting;
