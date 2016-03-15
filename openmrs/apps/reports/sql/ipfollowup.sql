select CONCAT(pn.given_name,pn.family_name) as Name,p.gender as Gender,padd.city_village as Area,padd.address2 as Village ,
  GROUP_CONCAT(DISTINCT(cdvn.name))as Diagnosis,GROUP_CONCAT(DISTINCT(obs.value_text)) as 'ADT Notes' from  confirmed_diagnosis_view_new cdvn
  left join visit v on cdvn.visit_id=v.visit_id
  left join encounter e on v.visit_id = e.visit_id
  join obs on e.encounter_id = obs.encounter_id and obs.concept_id in (Select concept_id from concept_name cn where name='Adt Notes')
  left join person p on cdvn.person_id=p.person_id
  left join person_name pn on p.person_id = pn.person_id
  left join person_address padd on p.person_id = padd.person_id
  where cast(v.date_created as DATE)  between '#startDate#' and '#endDate#'
group by cdvn.visit_id;