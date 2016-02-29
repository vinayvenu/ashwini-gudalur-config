select pad.address2 as Area,sum((if(pat.name='Is_Tribal' and cv.concept_full_name='True',1,0))) as Tribe,
                   sum((if(pat.name='Is_Tribal' and cv.concept_full_name='False',1,0))) as 'Non Tribe',
  count(v.visit_id) as 'OPD Visit Count' from visit v inner join person_address pad
on v.patient_id=pad.person_id
  INNER JOIN person_attribute pa on pa.person_id = v.patient_id
  INNER JOIN person_attribute_type pat on pat.person_attribute_type_id = pa.person_attribute_type_id
  INNER JOIN concept_view cv on cv.concept_id = pa.value
where visit_type_id in (select visit_type_id from visit_type where name='OPD') and cast(date_started as DATE) between '#startDate#' and '#endDate#'
group by pad.address2;