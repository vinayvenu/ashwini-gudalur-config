select p.person_id,CONCAT(pn.given_name, " ", pn.family_name) as Name,padd.city_village,v.visit_id,e.encounter_id,GROUP_CONCAT(DISTINCT(cdvn.name)) from  confirmed_diagnosis_view_new cdvn
  left join visit v on cdvn.visit_id=v.visit_id
  left join encounter e on v.visit_id = e.visit_id
  left join person p on cdvn.person_id=p.person_id
  left join person_name pn on p.person_id = pn.person_id
  left join person_address padd on p.person_id = padd.person_id
  where v.date_created is between '#startDate#' and '#endDate#'
group by cdvn.visit_id;