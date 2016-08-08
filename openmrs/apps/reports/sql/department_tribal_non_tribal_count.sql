SELECT cv2.concept_full_name as Department,
 (case when cv3.concept_full_name  = 'False' then 'Non Tribe' else 'Tribe' END) as Tribe, count(obs_id) as count
FROM obs o
  INNER JOIN concept_view cv ON cv.concept_id = o.concept_id AND
                                cv.concept_full_name = 'Departments'
  INNER JOIN encounter en on en.encounter_id = o.encounter_id
INNER JOIN visit v on v.visit_id=en.visit_id and v.visit_type_id!=9
  INNER JOIN concept_view cv2 ON cv2.concept_id = o.value_coded

  inner JOIN  person_attribute pa on pa.person_id = o.person_id
  INNER JOIN person_attribute_type pat on pat.person_attribute_type_id = pa.person_attribute_type_id
                                          and pat.name='Is_Tribal'
  INNER JOIN concept_view cv3 on cv3.concept_id = pa.value
where cast(o.obs_datetime AS DATE) BETWEEN '#startDate#' and '#endDate#' AND o.voided = 0
GROUP BY cv2.concept_full_name,cv3.concept_full_name;
