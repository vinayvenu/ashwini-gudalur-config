SELECT ROW_NUMBER() OVER (ORDER BY sm.create_date) as "Sl No",sm.name as Product,spl.name as Batch,sm.product_qty as Quantity,
spl.mrp as MRP,cast((spl.mrp*sm.product_qty)as DECIMAL (10,2)) as "MRP Value",
spl.cost_price as CP,cast((spl.cost_price*sm.product_qty)as DECIMAL (10,2)) as "CP Value",spl.sale_price as SP,
cast((spl.sale_price*sm.product_qty)as DECIMAL(10,2)) as "SP Value",
cast(sm.create_date as date),sl.name as Location
  FROM stock_move sm
   INNER JOIN stock_location sl on sl.id = sm.location_dest_id
    INNER JOIN stock_production_lot spl on spl.id = sm.prodlot_id 
      WHERE sl.name like '%Area%'
  	 AND state = 'done'
  	   AND sm.create_date BETWEEN '#startDate#' and '#endDate#'
           ORDER BY sm.create_date Asc;
