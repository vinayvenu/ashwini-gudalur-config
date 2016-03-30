Select(select count(ord.order_id)
from orders ord join obs o on ord.order_id = o.order_id and order_type_id=3
  JOIN concept c on c.concept_id = o.concept_id
  join concept_class cc on cc.concept_class_id = c.class_id and cc.concept_class_id=26
  join encounter en on en.encounter_id = o.encounter_id and o.value_numeric is NOT NULL or o.value_coded is not null or o.value_text is not null
  join visit v on v.visit_id=en.visit_id
  join person p on v.patient_id=p.person_id
  join person_attribute pa on p.person_id = pa.person_id and pa.person_attribute_type_id=27 AND (pa.value=2 or pa.value= 2147)  where cast(o.date_created as DATE) between '#startDate#' and '#endDate#') as 'Non Tribal',
  (select count(ord.order_id)
from orders ord join obs o on ord.order_id = o.order_id and order_type_id=3
  JOIN concept c on c.concept_id = o.concept_id
  join concept_class cc on cc.concept_class_id = c.class_id and cc.concept_class_id=26
  join encounter en on en.encounter_id = o.encounter_id and o.value_numeric is NOT NULL or o.value_coded is not null or o.value_text is not null
  join visit v on v.visit_id=en.visit_id
  join person p on v.patient_id=p.person_id
  join person_attribute pa on p.person_id = pa.person_id and pa.person_attribute_type_id=27 AND (pa.value=1 or pa.value= 2146) where cast(o.date_created as DATE) between '#startDate#' and '#endDate#') as 'Tribal';
