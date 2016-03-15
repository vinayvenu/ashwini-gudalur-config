Select ((select count(*)  from patient p
  join visit v on p.patient_id = v.patient_id
  join encounter e on e.visit_id=v.visit_id
  join obs o on o.encounter_id=e.encounter_id
  join orders od on o.order_id=od.order_id and order_type_id=4
        AND o.value_text is not null
        and cast(o.date_created as DATE) between '#startDate#' AND '#endDate#')) as RadiologyOrder,
 	  (select count(*) from patient p
  join visit v on p.patient_id = v.patient_id
  join encounter e on e.visit_id=v.visit_id
  join obs o on o.encounter_id=e.encounter_id
  join orders od on o.order_id=od.order_id and order_type_id=5 AND o.value_text is not null
   where  cast(o.date_created as DATE) between '#startDate#' AND '#endDate#') as ProcedureOrder,
    (select count(*)  from patient p
  join visit v on p.patient_id = v.patient_id
  join encounter e on e.visit_id=v.visit_id
  join obs o on o.encounter_id=e.encounter_id
  join orders od on o.order_id=od.order_id and order_type_id=6
        AND o.value_text is not null
        and cast(o.date_created as DATE) between '#startDate#' AND '#endDate#') as DentalOrder,
    (select count(*)  from patient p
  join visit v on p.patient_id = v.patient_id
  join encounter e on e.visit_id=v.visit_id
  join obs o on o.encounter_id=e.encounter_id
  join orders od on o.order_id=od.order_id and order_type_id=7
        AND o.value_text is not null
        and cast(o.date_created as DATE) between '#startDate#' AND '#endDate#')as USGOrder ;