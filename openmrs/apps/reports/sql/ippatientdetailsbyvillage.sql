SELECT rp.name,rp.ref,rpa.address2 as Area,rpa.city_village as Village, rpt."x_Is_Tribal",spe.gender,
  date_part('year',age(spe.birthdate)) as age, sv.diagnoses,
  sv.visit_startdate as admitdate,sv.visit_stopdate as dischargedate,
  sum(t.amount_total+t.discount_amount) billed,sum(paid) paid from syncjob_visit sv
  LEFT JOIN res_partner_address rpa on sv.erp_patient_id=rpa.partner_id
  LEFT JOIN syncjob_patient_extn spe on spe.erp_id = sv.erp_patient_id
  LEFT JOIN res_partner rp on rp.id = sv.erp_patient_id
  LEFT JOIN res_partner_attributes rpt on rpt.partner_id = sv.erp_patient_id
  LEFT JOIN visit_so_payment_rln t on t.visit_id = sv.id
where sv.visit_type_id=1 and cast(sv.visit_stopdate as DATE) between '#startDate#' and '#endDate#'
GROUP BY sv.visit_uuid,rp.ref,rp.name,rpa.address2,sv.diagnoses, admitdate, dischargedate,
rpa.city_village,spe.gender,rpt."x_Is_Tribal",age
ORDER BY rpa.address2;
