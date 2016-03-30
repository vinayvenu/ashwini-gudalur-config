select count(o.obs_id) as LabTest,visit_type.name as 'Visit Location',case when (pa.value=1 or pa.value= 2146) then 'Tribal'
when (pa.value=2 or pa.value= 2147) then 'Non Tribal' else '' end as 'Tribal or Non Tribal'from obs o join orders od on o.order_id=od.order_id and order_type_id=3
  JOIN concept c on c.concept_id = o.concept_id
  join concept_class cc on cc.concept_class_id = c.class_id and cc.concept_class_id=26
  join encounter e on e.encounter_id = o.encounter_id
  join visit v on v.visit_id = e.visit_id
  join visit_type on visit_type.visit_type_id = v.visit_type_id
  left join person p on p.person_id = o.person_id
  left join person_attribute pa on p.person_id = pa.person_id and pa.person_attribute_type_id=27
where (o.value_numeric is NOT NULL or o.value_coded is not null or o.value_text is not null ) and cast (o.date_created as DATE) between '#startDate#' and '#endDate#'
GROUP BY pa.value,visit_type.name;