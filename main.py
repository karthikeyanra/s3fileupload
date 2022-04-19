from flask import Flask, redirect, render_template, url_for, request, flash
import boto3
from werkzeug.utils import secure_filename
import os

app=Flask(__name__)
app.secret_key = "my secret key"
cwd=os.getcwd()

#create a folder TEMPDIR to save the file temporary before upload to s3
if not os.path.isdir('TEMPDIR'):
    os.mkdir('TEMPDIR')

AllowedFileType=['pdf','txt','doc','docx']

@app.route('/')
def main():
    list_of_buckets=[]
    myS3Client=boto3.client(service_name="s3")
    response = myS3Client.list_buckets()
    for buckets in response['Buckets']:
        list_of_buckets.append(buckets['Name'])
    return render_template("index.html",bucketlist=list_of_buckets)

@app.route('/upload', methods=['POST'])
def fileupload():
    file = request.files['file']
    bucketname=request.form.get('bucketname')
 
    filename = secure_filename(file.filename)

    fextension=filename.split(".")

    if fextension[1] not in AllowedFileType:
        flash("Not a valid file to upload, Allowed extensions are .doc, .docx, .pdf, .txt")
        return redirect("/")

    if filename =="":
        flash("No files Selected.., Choose a file to upload")
        return redirect("/")



    filepath=cwd+"\\TEMPDIR\\"+filename
    file.save(filepath)
    #begin upload to S3
    myS3Client=boto3.client(service_name="s3")
    myS3Client.upload_file(filepath,bucketname,filename)
    flash("File Upload Succesful")
    #remote temp file
    os.remove(filepath)
    return redirect("/")


if __name__=='__main__':
    app.run()
