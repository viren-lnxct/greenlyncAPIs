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
            
            s3_client.upload_file(Bucket='greenllyncdespensariesimagevideos',Filename=filename_logo, Key=filename_logo+"_"+timestamp)
            bucket_location = s3_client.get_bucket_location(Bucket="greenllyncdespensariesimagevideos")
            image_s3url_logo = "https://s3-{0}.amazonaws.com/{1}/{2}".format(bucket_location['LocationConstraint'],"greenllyncdespensariesimagevideos",filename_logo+"_"+timestamp)
            os.system(f"rm {filename_logo}")

        except:
            image_s3url_logo = None

        try:
            image_video = request.files['image_or_video']
            filename_image_video = secure_filename(image_video.filename)
            image_video.save(filename_image_video)
            
            s3_client.upload_file(Bucket='greenllyncdespensariesimagevideos',Filename=filename_image_video, Key=filename_image_video+"_"+timestamp)
            bucket_location = s3_client.get_bucket_location(Bucket="greenllyncdespensariesimagevideos")
            image_s3url_imagevideo = "https://s3-{0}.amazonaws.com/{1}/{2}".format(bucket_location['LocationConstraint'],"greenllyncdespensariesimagevideos",filename_image_video+"_"+timestamp)
            os.system(f"rm {filename_image_video}")
        
        except:
            image_s3url_imagevideo = None


        url = "https://m6u2i2dya5egnp5axrmhxehzam.appsync-api.ap-south-1.amazonaws.com/graphql"

        payload="""
            mutation MyMutation($PK: String!,$business_name: String!,$first_name: String!,$last_name: String!,$about: String,$license_state: String!,$license_no: String!,$address: String!,$store_front: Boolean,$phone_no: String!,$delivery_only: Boolean,$website: String,$logo: String,$email: String!,$image_or_video: String,$city: String!,$state: String!,$postal_code: String!) {  createDespensaries(input: {PK: $PK, business_name: $business_name,first_name:$first_name,last_name:$last_name, about: $about, license_state: $license_state,license_no: $license_no,address: $address,store_front: $store_front,phone_no: $phone_no,delivery_only: $delivery_only,website: $website,logo: $logo,email: $email,image_or_video: $image_or_video,city:$city,state:$state,postal_code:$postal_code}) {
                PK
            }
            }
            """
        
        variables = {"PK":f"{request.form.get('first_name','')}#{request.form.get('business_name','')}","business_name":request.form.get('business_name',""),"about":request.form.get('about',None),"logo":image_s3url_logo,"license_state":request.form.get("license_state",None),'license_no': request.form.get("license_no",None),"address": request.form.get("address",None),"store_front": request.form.get("store_front",False),"phone_no":request.form.get("phone_no",None),"delivery_only": request.form.get('delivery_only',False),"website": request.form.get('website',None),"email": request.form.get('email',None),"image_or_video": image_s3url_imagevideo,'first_name':request.form.get('first_name',None),'last_name':request.form.get('last_name',None),'city':request.form.get('city',None),'state':request.form.get('state',None),'postal_code':request.form.get('postal_code',None)}

        headers = {
        'x-api-key': 'da2-4gltnyo7vzav5a3kwthe7ibu3u',
        'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, json={'query':payload,'variables':variables})


        print(response.text)
        return jsonify({'data': "file get successfully","url":image_s3url_logo})

if __name__ == '__main__':
  
    app.run(debug = True)
