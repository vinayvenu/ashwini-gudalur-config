SELECT
  cv2.concept_full_name as 'Departments',if(cv.concept_full_name='True','Tribe','Non Tribe') Caste,
  count(DISTINCT (e.patient_id)) as 'Patient Count'
FROM obs o
  inner JOIN  person_attribute pa on pa.person_id = o.person_id
  INNER JOIN person_attribute_type pat on pat.person_attribute_type_id = pa.person_attribute_type_id
                                          and pat.name='Is_Tribal'
  INNER JOIN concept_view cv on cv.concept_id = pa.value
  INNER JOIN encounter e ON o.encounter_id = e.encounter_id
                            AND cast(o.obs_datetime AS DATE) BETWEEN '#startDate#' and '#endDate#' AND o.voided = 0
                            AND o.obs_id IN (SELECT obs_id
                                             FROM obs
                                               INNER JOIN concept_view cv ON cv.concept_id = obs.concept_id AND
                                                                             cv.concept_full_name = 'Departments'
  )
  INNER JOIN concept_view cv2 ON cv2.concept_id = o.value_coded

GROUP BY cv2.concept_full_name,cv.concept_full_name
ORDER BY cv.concept_full_name;