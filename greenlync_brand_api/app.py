# from asyncio.windows_events import NULL
from flask import Flask, jsonify, request
import boto3
from werkzeug.utils import secure_filename
import requests
import os
import datetime

app = Flask(__name__)

timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

@app.route('/', methods = ['GET', 'POST'])
def home():
    if(request.method == 'POST'):
        s3_client = boto3.client('s3',aws_access_key_id="AKIAQCJKNU2UC7Q3KF4H", aws_secret_access_key="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")
        try:
            image_logo = request.files['logo']
            filename_logo = secure_filename(image_logo.filename)
            image_logo.save(filename_logo)
            
            s3_client.upload_file(Bucket='greenlyncbrandlogo',Filename=filename_logo, Key=filename_logo+"_"+timestamp)
            bucket_location = s3_client.get_bucket_location(Bucket="greenlyncbrandlogo")
            image_s3url_logo = "https://s3-{0}.amazonaws.com/{1}/{2}".format(bucket_location['LocationConstraint'],"greenlyncbrandlogo",filename_logo+"_"+timestamp)
            os.system(f"rm {filename_logo}")

        except:
            image_s3url_logo = None



        url = "https://jtlz6bijebh5rhlfm3kvc7ssmy.appsync-api.ap-south-1.amazonaws.com/graphql"

        payload="""
            mutation MyMutation($PK: String!,$first_name: String!,$last_name: String!,$title: String,$about: String,$business_name: String!,$license_state: String!,$license_no: String!,$address: String!,$phone_no: String!,$website: String,$logo: String,$email: String!,$city: String!,$state: String!,$postal_code: String!) {  createGreenlyncBrand(input: {PK: $PK, business_name: $business_name, about: $about, license_state: $license_state,license_no: $license_no,address: $address,phone_no: $phone_no,website: $website,logo: $logo,email: $email,first_name: $first_name,last_name: $last_name,title:$title,city:$city,state:$state,postal_code:$postal_code}) {
                PK
            }
            }
            """
        
        variables = {"PK":f"{request.form.get('first_name','')}#{request.form.get('business_name','')}","business_name":request.form.get('business_name',""),"about":request.form.get('about',None),"logo":image_s3url_logo,"license_state":request.form.get("license_state",None),'license_no': request.form.get("license_no",None),"address": request.form.get("address",None),"phone_no":request.form.get("phone_no",None),"website": request.form.get('website',None),"email": request.form.get('email',None),'first_name': request.form.get('first_name',None),'last_name':request.form.get('last_name',None),'title':request.form.get('title',None),'city':request.form.get('city',None),'state':request.form.get('state',None),'postal_code':request.form.get('postal_code',None)}

        headers = {
        'x-api-key': 'da2-67hwapxmobb6jkpotf5b67hfba',
        'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, json={'query':payload,'variables':variables})


        print(response.text)
        return jsonify({'data': "file get successfully","url":image_s3url_logo})

if __name__ == '__main__':
  
    app.run(debug = True)
