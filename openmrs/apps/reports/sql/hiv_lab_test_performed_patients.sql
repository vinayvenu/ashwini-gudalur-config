SELECT  ROW_NUMBER() OVER (ORDER BY p.first_name) as "Sl No",p.first_name As "Patient First Name",p.last_name "Patient Last Name",pa.gender as Gender,EXTRACT(YEAR from AGE(pa.birth_date)) 
as "Age",paa.value As Address,t.name as "Test Name",d.dict_entry as "Result",cast(a.lastupdated as date) 
as "Order Date",cast(r.lastupdated as Date) As "Result Date"  FROM result r
LEFT JOIN analysis a on r.analysis_id=a.id  and cast(r.lastupdated as DATE) between '#startDate#' and '#endDate#'
LEFT JOIN test t on t.id=a.test_id
LEFT JOIN sample_item si on si.id=a.sampitem_id
LEFT JOIN sample s on s.id=si.samp_id
LEFT JOIN sample_human sh on sh.samp_id = si.samp_id
LEFT JOIN patient pa on pa.id=sh.patient_id
LEFT JOIN person p on p.id=pa.person_id 
LEFT JOIN person_address paa on paa.person_id=pa.person_id
LEFT JOIN address_part app on app.id = paa.address_part_id
LEFT JOIN dictionary d on d.id = cast(r.value as int)
WHERE t.name like 'HIV' and p.first_name IS NOT NULL and app.id = 8;
