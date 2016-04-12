Select (select  count(person_id) from patient p
  join person_attribute pa on p.patient_id=pa.person_id and pa.person_attribute_type_id=27 AND (pa.value=1 or pa.value= 2146)
  join visit v on p.patient_id = v.patient_id
  join visit_type vt on vt.visit_type_id = v.visit_type_id and vt.visit_type_id=(select visit_type_id from visit_type where name='IPD')
  join encounter e on e.visit_id=v.visit_id
where cast(v.date_created as DATE) between '#startDate#' and '#endDate#' ORDER BY v.visit_id) as TribalIPD,
       (select count( person_id) from patient p
         join person_attribute pa on p.patient_id=pa.person_id and pa.person_attribute_type_id=27 AND (pa.value=1 or pa.value= 2146)
         join visit v on p.patient_id = v.patient_id
         join visit_type vt on vt.visit_type_id = v.visit_type_id and vt.visit_type_id=(select visit_type_id from visit_type where name='OPD')
       where cast(v.date_created as DATE)between '#startDate#' and '#endDate#' ORDER BY v.visit_id) as TribalOPD,
       (select count(person_id) from patient p
         join person_attribute pa on p.patient_id=pa.person_id and pa.person_attribute_type_id=27 AND (pa.value=1 or pa.value= 2146)
         join visit v on p.patient_id = v.patient_id
         join visit_type vt on vt.visit_type_id = v.visit_type_id and vt.visit_type_id=(select visit_type_id from visit_type where name='Emergency')
       where cast(v.date_created as DATE) between '#startDate#' and '#endDate#' ORDER BY v.visit_id) as TribalEmergency,
       (select count(person_id) from patient p
         join person_attribute pa on p.patient_id=pa.person_id and pa.person_attribute_type_id=27 AND (pa.value=1 or pa.value= 2146)
         join visit v on p.patient_id = v.patient_id
         join visit_type vt on vt.visit_type_id = v.visit_type_id and vt.visit_type_id=(select visit_type_id from visit_type where name='Followup')
       where cast(v.date_created as DATE)  between '#startDate#' and '#endDate#' ORDER BY v.visit_id) as TribalFollowUp,
       (select count(person_id) from patient p
         join person_attribute pa on p.patient_id=pa.person_id and pa.person_attribute_type_id=27 AND (pa.value=1 or pa.value= 2146)
         join visit v on p.patient_id = v.patient_id
         join visit_type vt on vt.visit_type_id = v.visit_type_id and vt.visit_type_id=(select visit_type_id from visit_type where name='Lab Visit')
       where cast(v.date_created as DATE) between '#startDate#' and '#endDate#' ORDER BY v.visit_id)as TribalGeneral,
       (select count(person_id) from patient p
         join person_attribute pa on p.patient_id=pa.person_id and pa.person_attribute_type_id=27 AND (pa.value=2 or pa.value= 2147)
         join visit v on p.patient_id = v.patient_id
       join visit_type vt on vt.visit_type_id = v.visit_type_id and vt.visit_type_id=(select visit_type_id from visit_type where name='IPD')
         join encounter e on e.visit_id=v.visit_id
       where cast(v.date_created as DATE) between '#startDate#' and '#endDate#' ORDER BY v.visit_id) as NonTribalIPD,
       (select count(person_id) from patient p
         join person_attribute pa on p.patient_id=pa.person_id and pa.person_attribute_type_id=27 AND (pa.value=2 or pa.value= 2147)
         join visit v on p.patient_id = v.patient_id
         join visit_type vt on vt.visit_type_id = v.visit_type_id and vt.visit_type_id=(select visit_type_id from visit_type where name='OPD')
         join encounter e on e.visit_id=v.visit_id
       where cast(v.date_created as DATE)  between '#startDate#' and '#endDate#' ORDER BY v.visit_id) as NonTribalOPD,
       (select count(person_id) from patient p
         join person_attribute pa on p.patient_id=pa.person_id and pa.person_attribute_type_id=27 AND (pa.value=2 or pa.value= 2147)
         join visit v on p.patient_id = v.patient_id
         join visit_type vt on vt.visit_type_id = v.visit_type_id and vt.visit_type_id=(select visit_type_id from visit_type where name='Emergency')
         join encounter e on e.visit_id=v.visit_id
       where cast(v.date_created as DATE) between '#startDate#' and '#endDate#' ORDER BY v.visit_id) as NonTribalEmergency,
       (select count(person_id) from patient p
         join person_attribute pa on p.patient_id=pa.person_id and pa.person_attribute_type_id=27 AND (pa.value=2 or pa.value= 2147)
         join visit v on p.patient_id = v.patient_id
         join visit_type vt on vt.visit_type_id = v.visit_type_id and vt.visit_type_id=(select visit_type_id from visit_type where name='Followup')
         join encounter e on e.visit_id=v.visit_id
       where cast(v.date_created as DATE) between '#startDate#' and '#endDate#' ORDER BY v.visit_id) as NonTribalFollowUp,
       (select count(person_id) from patient p
         join person_attribute pa on p.patient_id=pa.person_id and pa.person_attribute_type_id=27 AND (pa.value=2 or pa.value= 2147)
         join visit v on p.patient_id = v.patient_id
         join visit_type vt on vt.visit_type_id = v.visit_type_id and vt.visit_type_id=(select visit_type_id from visit_type where name='Lab Visit')
         join encounter e on e.visit_id=v.visit_id
       where cast(v.date_created as DATE) between '#startDate#' and '#endDate#' ORDER BY v.visit_id)as NonTribalGeneral;