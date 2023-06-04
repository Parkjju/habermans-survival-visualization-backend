from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Patient
from .serializers import PatientSerializer
from lifelines import CoxPHFitter
from lifelines import KaplanMeierFitter
from visualization.models import Patient
import random
import pandas as pd

@api_view(['POST'])
def create_patient(request):
    # POST 요청을 처리합니다.
    serializer = PatientSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_random_patients(request):
    # Patient 모델에 저장된 모든 데이터를 가져옵니다.
    all_patients = Patient.objects.all()

    # 랜덤으로 3개의 Patient 데이터를 뽑습니다.
    random_patients = random.sample(list(all_patients), 3)

    # 뽑은 Patient 데이터를 직렬화합니다.
    serializer = PatientSerializer(random_patients, many=True)

    # 직렬화된 데이터를 응답합니다.
    return Response(serializer.data)

@api_view(['GET'])
def predict_new(request):
    # database
    patients = list(Patient.objects.all())

    # new data
    age = request.GET.get('age')
    operation_year = request.GET.get('operation_year')
    nb_pos_detected = request.GET.get('nb_pos_detected')
    surv = request.GET.get('surv')

    # 쿼리 파라미터로 DataFrame 생성
    selected_data = pd.DataFrame([[age, operation_year, nb_pos_detected, surv]], columns=['age', 'operation_year', 'nb_pos_detected', 'surv'])

    # CoxPH instance
    cph = CoxPHFitter()

    # all database to list
    all_list = []

    for object in patients:
        all_list.append([object.age, object.operation_year,object.nb_pos_detected, object.surv])

    all_data = pd.DataFrame(all_list, columns=['age', 'operation_year', 'nb_pos_detected', 'surv'])

    # cox fitting
    cph.fit(all_data, 'age', event_col='surv')

    # predict
    sf = cph.predict_survival_function(selected_data)
    return Response({'results': sf})

@api_view(['GET'])
def predict_kaplan(request):
    # Fetch data from the database
    patients = Patient.objects.all()

    # Kaplan-Meier instance
    km = KaplanMeierFitter()

    # Convert database data to a list
    all_list = [[patient.age, patient.operation_year, patient.nb_pos_detected, patient.surv] for patient in patients]

    all_data = pd.DataFrame(all_list, columns=['age', 'operation_year', 'nb_pos_detected', 'surv'])

    # Fit the data into the model
    km.fit(all_data['age'], event_observed=all_data['surv'])

    # Predict survival probability
    time_points = range(0, 100, 5)
    kf = km.predict(time_points)

    # Print the predicted survival probability
    return Response({'results': kf.tolist()})

@api_view(['GET'])
def predict_kaplan2(request):
    # Retrieve all patients from the database
    patients = Patient.objects.all()

    # Create cohorts based on Nb_pos_detected
    i1 = [patient for patient in patients if patient.nb_pos_detected >= 1]
    i2 = [patient for patient in patients if patient.nb_pos_detected < 1]

    # Fit the model for the first cohort
    km_1 = KaplanMeierFitter()
    km_1.fit([patient.age for patient in i1], [patient.surv for patient in i1], label='at least one positive axillary detected')

    # Fit the model for the second cohort
    km_2 = KaplanMeierFitter()
    km_2.fit([patient.age for patient in i2], [patient.surv for patient in i2], label='no positive axillary nodes detected')

    # Plot the survival curves
    time_points = range(0, 100, 5)
    kf1 = km_1.predict(time_points)
    kf2 = km_2.predict(time_points)

    return Response({'km1': kf1.tolist(), 'km2': kf2.tolist()})




@api_view(['GET'])
def predict_survival(request):
    # Patient 모델 전체 리스트에서 랜덤으로 3개를 뽑습니다.
    patients = list(Patient.objects.all())
    rows_selected = random.sample(patients, 3)

    # lifelines 라이브러리를 사용합니다.
    cph = CoxPHFitter()
    selected_list = []
    all_list = []

    for object in patients:
        all_list.append([object.age, object.operation_year,object.nb_pos_detected, object.surv])

    for object in rows_selected:
        selected_list.append([object.age, object.operation_year,object.nb_pos_detected, object.surv])
    
    # rows_selected를 기반으로 데이터 프레임을 생성합니다.
    selected_data = pd.DataFrame(selected_list, columns=['age', 'operation_year', 'nb_pos_detected', 'surv'])
    all_data = pd.DataFrame(all_list, columns=['age', 'operation_year', 'nb_pos_detected', 'surv'])

    # Cox proportional hazards model을 fit합니다.
    cph.fit(all_data, 'age', event_col='surv')

    # predict_survival_function 메서드를 사용하여 각 데이터에 대한 예측 생존 곡선을 생성합니다.
    sf = cph.predict_survival_function(selected_data)


    # 결과를 JsonResponse로 반환합니다.
    return Response({'results': sf})

@api_view(['GET'])
def get_summary(request):
    # Patient 모델 전체 리스트에서 랜덤으로 3개를 뽑습니다.
    patients = list(Patient.objects.all())

    # lifelines 라이브러리를 사용합니다.
    cph = CoxPHFitter()
    selected_list = []
    all_list = []

    for object in patients:
        all_list.append([object.age, object.operation_year,object.nb_pos_detected, object.surv])
    
    # rows_selected를 기반으로 데이터 프레임을 생성합니다.
    all_data = pd.DataFrame(all_list, columns=['age', 'operation_year', 'nb_pos_detected', 'surv'])

    # Cox proportional hazards model을 fit합니다.
    cph.fit(all_data, 'age', event_col='surv')

    sf = cph.summary


    # 결과를 JsonResponse로 반환합니다.
    return Response({'results': sf})