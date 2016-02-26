        
select 
  (select count(*) from patient p
    join person_attribute pa on p.patient_id=pa.person_id and pa.person_attribute_type_id=27 AND pa.value=1
    join visit v on p.patient_id = v.patient_id
    join encounter e on e.visit_id=v.visit_id
    join obs o on o.encounter_id=e.encounter_id and o.value_numeric is NOT NULL or o.value_coded is not null or o.value_text is not null
    join orders od on o.order_id=od.order_id and order_type_id=3
    JOIN concept c on c.concept_id = o.concept_id
    join concept_class cc on cc.concept_class_id = c.class_id and cc.concept_class_id=26 where o.date_created between '#startDate#' and '#endDate#') as CountofTribal,
  (select count(*) from patient p
        join person_attribute pa on p.patient_id=pa.person_id and pa.person_attribute_type_id=27 AND pa.value=2
        join visit v on p.patient_id = v.patient_id
        join encounter e on e.visit_id=v.visit_id
        join obs o on o.encounter_id=e.encounter_id and o.value_numeric is NOT NULL or o.value_coded is not null or o.value_text is not null
        join orders od on o.order_id=od.order_id and order_type_id=3
        JOIN concept c on c.concept_id = o.concept_id
        join concept_class cc on cc.concept_class_id = c.class_id and cc.concept_class_id=26 where o.date_created between '#startDate#' and '#endDate#') as CountofNontribal;