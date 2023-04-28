import csv
from visualization.models import Patient

with open('./visualization/fixtures/haberman.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        patient = Patient(age=row[0], operation_year=row[1], nb_pos_detected=row[2], surv=row[3])
        patient.save()
        line_count += 1

print(f'Processed {line_count-1} lines.')

# 저장된 데이터 확인
patients = Patient.objects.all()
for patient in patients:
    print(patient)