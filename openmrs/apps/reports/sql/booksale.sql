select 'Book Fee' as product,count(sol.id),sum(sol.product_uom_qty*sol.price_unit) from sale_order_line sol
INNER JOIN sale_order so on sol.order_id=so.id and (so.state!='cancel' or so.state!='draft')
  and cast(so.date_confirm as DATE) between '#startDate#' and '#endDate#'
where product_id=2420;