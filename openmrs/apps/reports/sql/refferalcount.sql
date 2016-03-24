select count(*) from (SELECT count(*)
                             FROM referral ref left join analysis an on an.id = ref.analysis_id
                                 --   left join result res on an.id = res.analysis_id
                                 LEFT JOIN sample_item si on an.sampitem_id = si.id
                                 LEFT JOIN sample s on s.id=si.samp_id
                                 LEFT JOIN sample_human sh on sh.samp_id = s.id
                                 LEFT JOIN result res on res.analysis_id=an.id
                                 LEFT JOIN patient_identity pi on pi.patient_id = sh.patient_id and pi.identity_type_id=2
                                 LEFT JOIN test t on t.id = an.test_id
                                 LEFT JOIN status_of_sample st on st.id = an.status_id
                                 LEFT JOIN referral_type rt on rt.id = ref.referral_type_id
                                 left JOIN referral_reason refs on refs.id = ref.referral_reason_id
                                 LEFT JOIN organization org on org.id = ref.organization_id
                             where ref.referral_request_date between '#startDate#' and '#endDate#'
                             GROUP BY ref.referral_request_date) as NoofReferralTest;