from crypt import methods
import os
import math
import boto3
from botocore.exceptions import ClientError
from flask import Flask, redirect,render_template,request, url_for
app = Flask(__name__)

# Front Page

@app.route('/')
def index():
    return render_template('index.html')


# list ec2 instances

@app.route('/list')
def get_instances():
    ec2 = boto3.client('ec2',region_name='us-east-1')
    response = ec2.describe_instances() 
    return response

#  creating ec2 instance

@app.route('/create',methods=["POST","GET"])
def create_instances():
    if request.method=='POST':
        ec2 = boto3.client('ec2',region_name='us-east-1')
        form = request.form
        image = form['image']
        type = form['type']
        group = form['group']
        ec2.run_instances(
        ImageId=image,
        MinCount=1,
        MaxCount=1,
        InstanceType=type,
        SecurityGroupIds= [group]
      )
        return render_template("confirmationPage.html",message="Successfully created")
    else:
        return render_template("create.html")
        
#  delete ec2 instance

@app.route('/terminate',methods=["POST","GET"])
def terminate_instances():
    if request.method=='POST':
        ec2 = boto3.client('ec2',region_name='us-east-1')
        form = request.form
        id = form['id']
        try:
            ec2.terminate_instances(InstanceIds=[id], DryRun=True)
        except ClientError as e:
                if 'DryRunOperation' not in str(e):
                    raise

        try:
            response = ec2.terminate_instances(InstanceIds=[id], DryRun=False)
            return render_template("confirmationPage",message="Successfully terminated")
        except ClientError as e:
            print(e)
      
    else:
        return render_template("delete.html")

# start ec2 instance

@app.route('/start',methods=["POST","GET"])
def start_instances():
    if request.method=='POST':
        ec2 = boto3.client('ec2',region_name='us-east-1')
        form = request.form
        id = form['id']
        try:
            ec2.start_instances(InstanceIds=[id], DryRun=True)
        except ClientError as e:
                if 'DryRunOperation' not in str(e):
                    raise

        try:
            response = ec2.start_instances(InstanceIds=[id], DryRun=False)
            return render_template("confirmationPage.html",message="Successfully started")
        except ClientError as e:
            print(e)
      
    else:
        return render_template("start.html")

#  stop ec2 instance

@app.route('/stop',methods=["POST","GET"])
def stop_instances():
    if request.method=='POST':
        ec2 = boto3.client('ec2',region_name='us-east-1')
        form = request.form
        id = form['id']
        try:
            ec2.stop_instances(InstanceIds=[id], DryRun=True)
        except ClientError as e:
                if 'DryRunOperation' not in str(e):
                    raise

        try:
            response = ec2.stop_instances(InstanceIds=[id], DryRun=False)
            return render_template("confirmationPage.html",message="Successfully stopped")
        except ClientError as e:
            print(e)
      
    else:
        return render_template("stop.html")


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)