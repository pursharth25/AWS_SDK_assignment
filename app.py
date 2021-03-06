import os
import boto3
import s3Bucket
from botocore.exceptions import ClientError
from flask import Flask, redirect,render_template,request, url_for
app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
BUCKET = "pursharth"

# Front Page

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/createbucket')
def add():
    return render_template('add.html',var='createbucket')



@app.route('/createbucket/success', methods=['POST'])
def function1():
    if request.method=='POST':
        bucket_name=request.form['name']
        location="us-east-2"
    return s3Bucket.createbucket(bucket_name, location)


@app.route('/listallbuckets')
def function2():
    bucketlist=[]
    bucketlist=s3Bucket.listallbuckets()
    return render_template('view.html',buckets=bucketlist,var='list')

@app.route('/uploadfile')
def functionupload():
    return render_template('add.html',var='upload')

@app.route('/uploadfile/success', methods=['POST'])
def function6():
    f = request.files['file']
    f.save(os.path.join(UPLOAD_FOLDER, f.filename))
    name=request.form['name']
    return s3Bucket.uploadfile(f"uploads/{f.filename}", name)
    


# list ec2 instances

# @app.route('/list')
# def get_instances():
#  @app.route('/list')
#  def get_instances():
#      ec2 = boto3.resource('ec2',region_name='us-east-1')
#      instances= ec2.instances.all()
#      if not(instances):
#          return render_template("confirmationPage.html",message="No Instances are there")
         
#      return response

@app.route('/list')
def get_instances():
    ec2 = boto3.resource('ec2',region_name='us-east-1')
    instances= ec2.instances.all()
    if not(instances):
     return render_template("confirmationPage.html",message="Zero instances running")

    return render_template("listec2.html",instances=instances)


  
#creating ec2 instance

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


