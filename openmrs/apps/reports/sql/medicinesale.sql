SELECT  pp.name_template ,sum(sol.product_uom_qty) as qty FROM sale_order_line sol
INNER JOIN sale_order so on sol.order_id=so.id and (so.state!='cancel' and so.state!='draft')
  and cast(so.date_confirm as DATE) between '#startDate#' and '#endDate#'
LEFT JOIN product_product pp on pp.id = sol.product_id
INNER JOIN product_template pt on pt.id = pp.product_tmpl_id and pt.categ_id
in (select category_id from syncjob_chargetype_category_mapping where chargetype_name='Medicines' )
GROUP BY sol.product_id,pp.name_template ORDER BY qty desc;
