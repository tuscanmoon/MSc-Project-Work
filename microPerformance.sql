select sum(t2.document_category_count) 'document_category_count',
sum(t2.true_positive) 'true_positive',
sum(t2.false_positive) 'false_positive'
from ((document t1 join document_audit t2 on t1.id = t2.document_id)
join document_category t3 on t1.id = t3.document_id)
where t1.type = 'TEST'
and t3.category_weight_type_id = 2