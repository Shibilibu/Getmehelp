from urllib import request
from Db import Db
from flask import Flask, render_template, request, redirect,session

app = Flask(__name__)

app.secret_key="12345"


@app.route('/', methods=['get'])
def login():
    return render_template('index.html')


@app.route('/loginhelp_post', methods=['post'])
def login_help():
    nm = request.form['name']
    pas = request.form['pass']

    obj = Db()
    q=obj.selectOne("select * from login where Name='"+nm+"' and Password='"+pas+"'")
    if q is None:
        return "<script>alert('Invalid user');window.location='/'</script>"
    else:
        session['lid']=q['Id']
        if q['Usertype'] == 'admin':
            return redirect('/AdminHomepage')
        if q['Usertype'] == 'worker':
            return redirect('/WorkerHomePage')
        if q['Usertype'] == 'user':
            return redirect('/UserHomePage')
# ===========================================Admin===============================================================================================================

@app.route('/ViewWorker',methods=['get'])
def ViewWorker():
    obj=Db()
    view=obj.select("select * from worker,login where worker.Id=login.Id and Usertype='pending'")
    print(view)
    return render_template('admin/ViewWork.html',view=view)

@app.route('/ViewApproved',methods=['get'])
def ViewApproved():
    obj=Db()
    approve=obj.select("select * from worker,login where worker.Id=login.Id and Usertype='worker'")
    return render_template('admin/Viewapproved.html',approve=approve)

@app.route('/Approve/<ai>',methods=['get'])
def approve(ai):
    obj=Db()
    obj.update("update login set Usertype='worker' where Id='"+ ai +"'")
    return "<script>alert('Values Approved Successfully');window.location='/ViewWorker'</script>"

@app.route('/Reject/<aid>',methods=['get'])
def reject(aid):
    obj=Db()
    obj.delete("delete from worker where id='"+aid+"'")
    obj.delete("delete from login where id='"+aid+"'")
    return "<script>alert('Values Rejected Successfully');window.location='/ViewWorker'</script>"

@app.route('/AdminHomepage',methods=['get'])
def homepage():
    return render_template('admin/Adminpge.html')

@app.route('/AddService',methods=['get'])
def add():
    return render_template('admin/AddService.html')

@app.route('/AddService_post',methods=['post'])
def add_post():
    ser=request.form['service']
    det=request.form['det']
    obj=Db()
    obj.insert("insert into `service`(`Services`,`Details`) values ( '"+ser+"','"+det+"')")
    return  "<script>alert('Details Added Successfully');window.location='/AddService'</script>"

@app.route('/ViewService',methods=['get'])
def View():
    obj=Db()
    vi=obj.select("select * from service")
    return render_template('/admin/ViewService.html',vi=vi)

# @app.route('/Edit/<eid>',methods=['get'])
# def edit(eid):
#     obj=Db()
#     obj.update("update service set")

@app.route('/Delete/<eid>',methods=['get'])
def delete(eid):
    obj=Db()
    obj.delete("delete from service where Id='"+eid+"'")
    return "<script>alert('Deleted Successfully');window.location='/ViewService'</script>"


@app.route('/EditService/<eid>',methods=['get'])
def edit(eid):
    obj=Db()
    q=obj.selectOne("select * from service where Id='"+eid+"'")
    return render_template('admin/EditService.html',eid=eid,data=q)

@app.route('/EditService_post/<eid>',methods=['post'])
def edit_post(eid):
    service=request.form['Service']
    Detail=request.form['Det']
    obj=Db()
    obj.update("update service set Services='"+service+"' , Details='"+Detail+"' where id='"+eid+"'")
    return "<script>alert('Edited Successfully');window.location='/ViewService'</script>"

@app.route('/ViewUser',methods=['get'])
def ViewUser():
    obj=Db()
    view=obj.select("select * from users")
    return render_template('admin/ViewUser.html',view=view)

@app.route('/ViewFeedback',methods=['get'])
def ViewFeed():
    obj=Db()
    Feed=obj.select("select * from feedback,users where   feedback.UserId = users.Id")
    return render_template('admin/ViewFeedback.html',Feed=Feed)

@app.route('/ViewComplaint',methods=['get'])
def complaint():
    obj=Db()
    com=obj.select("select complaint.*,users.*, complaint.Id as cid from complaint,users where complaint.UserId = users.Id")
    return render_template('admin/ViewComplaints.html',com=com)


@app.route('/AddSendReply/<i>',methods=['get'])
def SendReply(i):
    return render_template('admin/AddSendReply.html',i=i)

@app.route('/AddSendReply_post/<i>',methods=['post'])
def SendReply_post(i):
    repl=request.form['reply']
    obj=Db()
    obj.update("update complaint set Reply ='"+repl+"', ReplyDate =curdate() where Id='"+i+"'")
    return "<script>alert('Updated Successfully');window.location='/ViewComplaint'</script>"


# ===============================================worker=====================================================================================================

@app.route('/WorkSignup', methods=['get'])
def worker():
    return render_template('Workerlogin.html')


@app.route('/WorkSignup_post', methods=['post'])
def worker_post():
    name = request.form['name']
    house = request.form['house']
    area = request.form['area']
    pn = request.form['pin']
    ds = request.form['dist']
    em = request.form['email']
    mob = request.form['mobile']
    img = request.files['image']
    pas = request.form['pass']


    import datetime
    d = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    img.save(r"C:\Users\shibil\PycharmProjects\ProjectRiss\static\images\\" + d + '.jpg')
    img = '/static/images/' + d + '.jpg'
    obj = Db()
    q=obj.insert("insert into `login`(`Name`,`Password`) values ( '"+em+"','"+pas+"')")
    obj.insert("insert into `worker`(`Id`,`Name`,`HouseName`,`Area`,`PinCode`,`District`,`Mobile`,`Email`,`Image`) values ( '"+str(q)+"','"+name+"','"+house+"','"+area+"','"+pn+"','"+ds+"','"+em+"',"+mob+",'"+img+"')")
    return "<script>alert('Registered Successfully');window.location='/WorkSignup'</script>"


@app.route('/ViewAddService',methods=['get'])
def adds():
    obj=Db()
    # print(session['lid'])
    add=obj.select("select * from service")
    return render_template('worker/ViewaddService.html',add=add)

@app.route('/WorkerHomePage',methods=['get'])
def WorkHome():
    return render_template('Workers.html')

@app.route('/AddAmount/<aid>',methods=['get'])
def AddAmount(aid):
    return render_template('worker/AddAmount.html',aid=aid)

@app.route('/AddAmount_post/<aid>',methods=['post'])
def AddAmount_post(aid):
    am=request.form['amount']
    obj=Db()
    obj.insert("insert into `service_worker`(`SWId`,`WorkerId`,`ServiceId`,`Amount`) values ( '','"+str(session['lid'])+"','"+aid+"','"+am+"');")
    return "<script>alert('Amount Added Successfully');window.location='/ViewAmount'</script>"

@app.route('/ViewAmount',methods=['get'])
def ViewAmount():
    obj=Db()
    amount=obj.select("select * from service_worker,service where service.Id = service_worker.ServiceId and service_worker.WorkerId ='"+str(session['lid'])+"' ")
    return render_template('worker/ViewAmount.html',amount=amount)

@app.route('/EditAmountView/<eid>',methods=['get'])
def EditAmount(eid):
    obj=Db()
    ed=obj.selectOne("select * from service_worker where SWId = '"+eid+"'")
    return render_template('worker/EditAmountView.html',eid=eid,data=ed)

@app.route('/EditAmountView_post/<eid>',methods=['post'])
def EditAmount_post(eid):
    amt=request.form['amount']
    obj=Db()
    obj.update("update service_worker set Amount = '"+amt+"' where SWId ='"+eid+"'")
    return "<script>alert('Amount Updated Successfully');window.location='/ViewAmount'</script>"

@app.route('/DeleteAmountView/<did>',methods=['get'])
def DeleteAmount(did):
    obj=Db()
    obj.delete("delete from service_worker where SWId = '"+did+"'")
    return "<script>alert('Deleted Successfully');window.location='/ViewAmount'</script>"

@app.route('/WorkFeedback',methods=['get'])
def ViewWorkFeed():
    obj=Db()
    WFeed=obj.select("select * from feedback,users where feedback.UserId = users.Id")
    return render_template('worker/WorkerFeedback.html',WFeed=WFeed)

@app.route('/ViewRequest',methods=['get'])
def ViewRequest():
    obj=Db()
    req=obj.select(" select request.* ,service_worker.* ,users.* ,service.*,request.Id as rid from request ,service_worker ,users ,service  where request.UserId = users.Id and service_worker.ServiceId = service.Id and service_worker.WorkerId = '"+str(session['lid'])+"'  and Status='pending' ")
    # print(" select request.* ,service_worker.* ,users.* ,service.*,request.Id as rid from request ,service_worker ,users ,service  where request.ServiceId = service.Id and service_worker.ServiceId = service.Id and service_worker.WorkerId = '"+str(session['lid'])+"'  and Status='pending' ")
    return render_template('worker/ViewRequest.html',req=req)

@app.route('/ApproveRequest/<apid>',methods=['get'])
def appreq(apid):
    obj=Db()
    obj.update("update request set Status='approved' where Id ='"+apid+"'")
    return "<script>alert('Approved');window.location='/ViewRequest'</script>"

@app.route('/RejectRequest/<reid>',methods=['get'])
def rejected(reid):
    obj=Db()
    obj.update("update request set Status = 'Rejected' where Id = '"+reid+"'")
    return "<script>alert('Rejected');window.location='/ViewRequest'</script>"

@app.route('/viewappreq',methods=['get'])
def ViewApprovedReq():
    obj=Db()
    apr=obj.select("select request.* ,service_worker.* ,users.* ,service.*,request.Id as rid from request ,service_worker ,users ,service  where request.UserId = users.Id and service_worker.ServiceId = service.Id and service_worker.WorkerId = '"+str(session['lid'])+"' and  Status = 'approved' ")
    return render_template('worker/ViewappRequest.html',apr=apr)

################################################Users######################################################################################################################################################################################################################

@app.route('/UserHomePage',methods=['get'])
def UserHomePage():
    return render_template('User.html')


@app.route('/UserSignup', methods=['get'])
def User():
    return render_template('Userlogin.html')


@app.route('/UserSignup_post', methods=['post'])
def User_post():
    userid = request.form['userid']
    house = request.form['house']
    area = request.form['area']
    pn = request.form['pin']
    ds = request.form['dist']
    em = request.form['email']
    mob = request.form['mobile']
    img = request.files['image']
    pas = request.form['pass']


    import datetime
    d = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    img.save(r"C:\Users\shibil\PycharmProjects\ProjectRiss\static\images\\" + d + '.jpg')
    img = '/static/images/' + d + '.jpg'
    obj = Db()
    q=obj.insert("insert into `login`(`Name`,`Password`,Usertype) values ( '"+em+"','"+pas+"','user')")
    obj.insert("insert into `users`(`Id`,`UserId`,`HouseName`,`Area`,`PinCode`,`District`,`Mobile`,`Email`,`Image`) values ( '"+str(q)+"','"+userid+"','"+house+"','"+area+"','"+pn+"','"+ds+"','"+em+"','"+mob+"','"+img+"')")
    return "<script>alert('Registered Successfully');window.location='/UserSignup'</script>"

@app.route('/ViewServices',methods=['get'])
def Services():
    obj=Db()
    ser=obj.select("select * from worker,login where login.Id=worker.Id and Usertype='worker'")
    return render_template('User/ViewServiceWorker.html',ser=ser)


@app.route('/SendRequest/<i>',methods=['get'])
def SendReq(i):
    obj=Db()
    req=obj.select("select * from service,service_worker where service.Id = service_worker.ServiceId and service_worker.WorkerId ='"+i+"' ")
    return render_template('User/SendRequest.html',req=req)

######Request Status######
@app.route('/ViewStatus',methods=['get'])
def ViewStatus():
    obj=Db()
    stat=obj.select("select request.*,service_worker.*,service.*,worker.*,request.Id as rid from request,service_worker,service,worker  where  request.ServiceId = service.Id  and request.UserId  = '"+str(session['lid'])+"' and  worker.Id = service_worker.WorkerId and service_worker.ServiceId=service.Id ")
    return render_template('User/ViewStatus.html',stat=stat)





@app.route('/AddsendRequest/<i>',methods=['get'])
def Addsend(i):
    return render_template('User/AddSendRequest.html',i=i)

@app.route('/AddsendRequest_post/<i>',methods=['post'])
def AddsendRequest_post(i):
    house=request.form['house']
    ar=request.form['area']
    pin=request.form['pin']
    di=request.form['dist']
    lat=request.form['Latitude']
    long=request.form['Longitude']
    obj=Db()
    obj.insert("insert into `request`(`Id`,`UserId`,`ServiceId`,`HouseName`,`Area`,`PinCode`,`District`,`Latitude`,`Longitude`) values ( '','"+str(session['lid'])+"','"+i+"','"+house+"','"+ar+"','"+pin+"','"+di+"','"+lat+"','"+long+"')")
    return "<script>alert('Added Successfully');window.location='/AddsendRequest'</script>"

######send complaint##########################################################################  #####################
@app.route('/SendComplaint',methods=['get'])
def SendComplaint():
    return render_template('User/SendComplaint.html')

@app.route('/SendComplaint_post',methods=['post'])
def SendComplaint_post():
    send=request.form['complaint']
    obj=Db()
    obj.insert("insert into `complaint`(`Id`,`UserId`,`Complaint`,`ComplaintDate`,`Reply`,`ReplyDate`) values ( '','"+str(session['lid'])+"','"+send+"','curdate()','pending',NULL)")
    return "<script>alert('Complaint Added Successfully');window.location='/SendComplaint'</script>"

@app.route('/ViewReply',methods=['get'])
def ViewReply():
    obj=Db()
    rep=obj.select("select * from complaint where complaint.UserId = '"+str(session['lid'])+"'")
    return render_template('User/ViewReply.html',rep=rep)


##########Send Feedback#############################################################################################
@app.route('/SendFeedback',methods=['get'])
def SendFeed():
    return render_template('User/SendFeedback.html')

@app.route('/SendFeedback_post',methods=['post'])
def SendFeed_post():
    feed=request.form['feedback']
    obj=Db()
    obj.insert("insert into `feedback`(`Id`,`UserId`,`Feedback`,`Date`) values ( '','"+str(session['lid'])+"','"+feed+"',NULL) ")
    return "<script>alert('Feedback Added Successfully');window.location='/SendFeedback'</script>"

############View Feedback########################################################################################

@app.route('/ViewUserFeedback',methods=['get'])
def userfeed():
    obj=Db()
    view=obj.select("select * from feedback where feedback.UserId = '"+str(session['lid'])+"'")
    return render_template('User/UserViewFeedback.html',view=view)




if __name__ == '__main__':
    app.run(port=3000)
