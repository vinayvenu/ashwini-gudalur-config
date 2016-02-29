SELECT * from (
    (SELECT count(*) as Tribal
  FROM visit v
  INNER JOIN person_attribute pa on pa.person_id = v.patient_id
  INNER JOIN person_attribute_type pat on pat.person_attribute_type_id = pa.person_attribute_type_id
    and pat.name='Is_Tribal'
    INNER JOIN concept_view cv on cv.concept_id = pa.value and cv.concept_full_name='True'
  where visit_type_id in (select visit_type_id from visit_type where name='OPD') and cast(date_started as DATE) between '#startDate#' and '#endDate#') as tribal,

    (SELECT count(*) as 'Non Tribal'
  FROM visit v
    INNER JOIN person_attribute pa on pa.person_id = v.patient_id
    INNER JOIN person_attribute_type pat on pat.person_attribute_type_id = pa.person_attribute_type_id
                                            and pat.name='Is_Tribal'
    INNER JOIN concept_view cv on cv.concept_id = pa.value and cv.concept_full_name='False'
  where visit_type_id in (select visit_type_id from visit_type where name='OPD') and cast(date_started as DATE) between '#startDate#' and '#endDate#') as Non_tribal,

    (SELECT count(*) as Sangam
  FROM visit v
    INNER JOIN person_attribute pa on pa.person_id = v.patient_id
    INNER JOIN person_attribute_type pat on pat.person_attribute_type_id = pa.person_attribute_type_id
                                            and pat.name='Is_Sangam'
    INNER JOIN concept_view cv on cv.concept_id = pa.value and cv.concept_full_name='True'
  where visit_type_id in (select visit_type_id from visit_type where name='OPD') and cast(date_started as DATE) between '#startDate#' and '#endDate#') as sangam,

    (SELECT count(*) as 'Non Sangam'
  FROM visit v
    INNER JOIN person_attribute pa on pa.person_id = v.patient_id
    INNER JOIN person_attribute_type pat on pat.person_attribute_type_id = pa.person_attribute_type_id
                                            and pat.name='Is_Sangam'
    INNER JOIN concept_view cv on cv.concept_id = pa.value and cv.concept_full_name='False'
  where visit_type_id in (select visit_type_id from visit_type where name='OPD') and cast(date_started as DATE) between '#startDate#' and '#endDate#') as non_sangam,

    (SELECT count(*) as 'Premium Paid'
  FROM visit v
    INNER JOIN person_attribute pa on pa.person_id = v.patient_id
    INNER JOIN person_attribute_type pat on pat.person_attribute_type_id = pa.person_attribute_type_id
                                            and pat.name='Is_Premium_Paid'
    INNER JOIN concept_view cv on cv.concept_id = pa.value and cv.concept_full_name='True'
  where visit_type_id in (select visit_type_id from visit_type where name='OPD') and cast(date_started as DATE) between '#startDate#' and '#endDate#') as premium,

    (SELECT count(*) as 'Non Premium Paid'
  FROM visit v
    INNER JOIN person_attribute pa on pa.person_id = v.patient_id
    INNER JOIN person_attribute_type pat on pat.person_attribute_type_id = pa.person_attribute_type_id
                                            and pat.name='Is_Premium_Paid'
    INNER JOIN concept_view cv on cv.concept_id = pa.value and cv.concept_full_name='False'
  where visit_type_id in (select visit_type_id from visit_type where name='OPD') and cast(date_started as DATE) between '#startDate#' and '#endDate#') as non_premium,
      (SELECT count(*) as 'Total Visit'
       FROM visit where visit_type_id=(select visit_type_id from visit_type where name='OPD' ) and cast(date_started as DATE) between '#startDate#' and '#endDate#') as total);

