# from asyncio.windows_events import NULL
from flask import Flask, jsonify, request
import boto3
from werkzeug.utils import secure_filename
import requests
import json
import datetime
import os

app = Flask(__name__)

timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

@app.route('/', methods = ['GET', 'POST'])
def home():
    if(request.method == 'POST'):
        try:
            image = request.files['logo']
            s3_client = boto3.client('s3',aws_access_key_id="AKIAQCJKNU2UC7Q3KF4H", aws_secret_access_key="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")

            filename = secure_filename(image.filename)
            image.save(filename)
            
            print("**************************")
            print(request.files)
            
            s3_client.upload_file(Bucket='greenlyncdoctorimages',Filename=filename, Key=filename+"_"+timestamp)
            bucket_location = s3_client.get_bucket_location(Bucket="greenlyncdoctorimages")
            image_s3url = "https://s3-{0}.amazonaws.com/{1}/{2}".format(bucket_location['LocationConstraint'],"greenlyncdoctorimages",filename+"_"+timestamp)

            os.system(f"rm {filename}")
        except:
            image_s3url = None


        url = "https://pjf2h7jnc5dtnhhgt7v7i5npxi.appsync-api.ap-south-1.amazonaws.com/graphql"

        payload="""
            mutation MyMutation($PK: String!,$doctor_name: String!,$clinic_name: String!,$about: String,$year_in_practice: Int,$speciality: String,$license_state: String!,$license_number: String!,$longitude: String,$latitude: String,$address: String!,$additional_location: String,$phone_no: String!,$email: String!,$website: String,$logo: String,$cons_ofc_visit_fees: Int,$videocall_fees: Int,$accept_new_patient_telehealth: Boolean,$accept_new_patient_in_person: Boolean,$insurance_accepted: Boolean,$office_hours: String,$military_veteran_discount: Boolean,$provide_MMC: Boolean,$provide_MMC_physical: Boolean,$provide_MMC_digital: Boolean,$payment_method_creditcard: Boolean,$payment_method_debitcard: Boolean,$payment_method_AndroidPay: Boolean,$payment_method_ApplePay: Boolean,$payment_method_Paypal: Boolean,$payment_method_Venmo: Boolean,
	$free_initial_consultation: Boolean,$city: String!,$state: String!,$postal_code: String!) {  createDoctorProfile(input: {PK: $PK, clinic_name: $clinic_name, doctor_name: $doctor_name, logo: $logo,about: $about,year_in_practice: $year_in_practice,speciality: $speciality,license_state: $license_state,license_number: $license_number,longitude: $longitude,latitude: $latitude,address: $address,additional_location: $additional_location, phone_no: $phone_no, email: $email, website: $website,cons_ofc_visit_fees: $cons_ofc_visit_fees,videocall_fees: $videocall_fees,accept_new_patient_telehealth: $accept_new_patient_telehealth, accept_new_patient_in_person: $accept_new_patient_in_person,insurance_accepted: $insurance_accepted,office_hours: $office_hours,military_veteran_discount: $military_veteran_discount,provide_MMC: $provide_MMC,provide_MMC_physical: $provide_MMC_physical,provide_MMC_digital: $provide_MMC_digital, payment_method_creditcard: $payment_method_creditcard, payment_method_debitcard: $payment_method_debitcard,payment_method_AndroidPay: $payment_method_AndroidPay,payment_method_ApplePay: $payment_method_ApplePay,payment_method_Paypal: $payment_method_Paypal,payment_method_Venmo: $payment_method_Venmo,free_initial_consultation: $free_initial_consultation,city: $city,state: $state,postal_code: $postal_code}) {
                PK
            }
            }
            """
    
        variables = {"PK":f"{request.form.get('doctor_name','')}#{request.form.get('clinic_name','')}","clinic_name":request.form.get('clinic_name',None),"doctor_name":request.form.get('doctor_name',None),"logo":image_s3url,"about":request.form.get("about",None),'year_in_practice': request.form.get("year_in_practice",None),"speciality": request.form.get("speciality",None),"license_state": request.form.get("license_state",None),"license_number":request.form.get("license_number",None),"longitude": request.form.get('longitude',None),"latitude": request.form.get('latitude',None),"address": request.form.get('address',None),"additional_location": request.form.get('additional_location',None),"phone_no":request.form.get("phone_no",None),"email":request.form.get("email",None),"website": request.form.get('website',None),"cons_ofc_visit_fees":request.form.get('cons_ofc_visit_fees',None),"videocall_fees":request.form.get('videocall_fees',None),"accept_new_patient_telehealth":request.form.get('accept_new_patient_telehealth',False),"accept_new_patient_in_person":request.form.get('accept_new_patient_in_person',False),"insurance_accepted":request.form.get('insurance_accepted',False),"office_hours":request.form.get('office_hours',None),"military_veteran_discount":request.form.get('military_veteran_discount',False),"provide_MMC":request.form.get('provide_MMC',False),"provide_MMC_physical":request.form.get('provide_MMC_physical',False),"provide_MMC_digital":request.form.get('provide_MMC_digital',False),"payment_method_creditcard":request.form.get('payment_method_creditcard',False),"payment_method_debitcard":request.form.get('payment_method_debitcard',False),"payment_method_AndroidPay":request.form.get('payment_method_AndroidPay',False),"payment_method_ApplePay":request.form.get('payment_method_ApplePay',False),"payment_method_Paypal":request.form.get('payment_method_Paypal',False),"payment_method_Venmo":request.form.get('payment_method_Venmo',False),"free_initial_consultation":request.form.get('free_initial_consultation',False),'city':request.form.get('city',None),'state':request.form.get('state',None),'postal_code':request.form.get('postal_code',None)}

        headers = {
        'x-api-key': 'da2-j7dlxf3uhjgi3omdk3tsi4bbyy',
        'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, json={'query':payload,'variables':variables})


        print(response.text)
        return jsonify({'data': "file get successfully","url":image_s3url})

if __name__ == '__main__':
    app.run(debug = True)
