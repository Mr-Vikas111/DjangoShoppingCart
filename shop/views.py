from django.shortcuts import render
from .models import Product, Contect ,Orders , OrderUpdate
from django.http import HttpResponse
from math import ceil
import json
from paytm import Checksum
from django.views.decorators.csrf import csrf_exempt
MERCHANT_KEY = 'uU&avtJfcNyXyzyO'



def index(request):
    allProds = []
    catProds = Product.objects.values('category','id')
    cats = {item['category'] for item in catProds}
    for cat in cats:
        prod = Product.objects.filter(category=cat)
        n = len(prod)
        nSlides = n//4 + ceil((n/4)-(n//4))
        allProds.append([prod, range(1,nSlides), nSlides])
    params ={'allProds':allProds}
    return render(request,'shop/index.html',params)


def searchMatch(query,item):
    if query in item.desc.lower() or query in item.product_name.lower() or query in item.category.lower():
        return True
    else:
        return False



def search(request):
    query = request.GET.get('query')
    allProds = []
    catProds = Product.objects.values('category','id')
    cats = {item['category'] for item in catProds}
    for cat in cats:
        prodtemp = Product.objects.filter(category=cat)
        prod = [item for item in prodtemp if searchMatch(query,item)]
        n = len(prod)
        nSlides = n//4 + ceil((n/4)-(n//4))
        if len(prod) != 0:
            allProds.append([prod, range(1,nSlides), nSlides])

    params ={'allProds':allProds,'msg':''}
    if len(allProds)== 0 or len(query)<4:
        params ={'msg':"Product not found"}

    return render(request,'shop/search.html',params)

def about(request):
    return render(request,'shop/about.html')

def contect(request):
    if request.method == "POST":
        name = request.POST.get('name','')
        email = request.POST.get('email','')
        phone = request.POST.get('phone','')
        desc =  request.POST.get('desc','')
        contect = Contect(name = name,email=email,phone=phone,desc=desc)
        contect.save()
    return render(request,"shop/contect.html ")

def tracker(request):
    if request.method =="POST":
        orderId= request.POST.get('orderId','')
        email = request.POST.get('email','')
        try:
            order = Orders.objects.filter(order_id =  orderId, email = email)
            if len(order)>0:
                update = OrderUpdate.objects.filter(order_id = orderId)
                updates = []
                for item in update:
                    updates.append({'text':item.update_desc, 'time':item.timestamp})
                    response = json.dumps({"status":"success","updates":updates,"itemJson":order[0].items_json},default=str)
                return HttpResponse(response)
            else:
                return HttpResponse('{"status":"noitem"}')

        except Exception as e:
            return HttpResponse('{"status":"error"}')
        
    return render(request,"shop/tracker.html")



def productview(request, myid):
   
    product = Product.objects.filter(id=myid)
    return render(request,"shop/prodView.html",{'product':product[0]})

def checkout(request):
    if request.method == "POST":
        items_json = request.POST.get('itemsJson','')
        name = request.POST.get('name','')
        amount = request.POST.get('amount','')
        email = request.POST.get('email','')
        address =  request.POST.get('address1','') + " " +  request.POST.get('address2','')
        city =  request.POST.get('city','')
        state =  request.POST.get('state','')
        zip_code =  request.POST.get('zip_code','')
        phone = request.POST.get('phone','')
       
        order = Orders(items_json = items_json,name = name,email=email,address=address,city=city,state=state,zip_code =zip_code,phone=phone,amount=amount)
        order.save()
        update = OrderUpdate(order_id=order.order_id,update_desc="This order has been placed")
        update.save()
        thank = True
        id = order.order_id
        return render(request, 'shop/checkout.html', {'thank':thank, 'id':id})
        #payment code operation..
        

        
    return render(request,"shop/checkout.html")

@csrf_exempt
def handlerequest(request):
    form = request.POST
    response_dict = {}
    for i in form.keys():
        response_dict[i] = form[i]
        if i == 'CHECKSUMHASH':
            checksum = form[i]

    verify = Checksum.verify_checksum(response_dict, MERCHANT_KEY, checksum)
    if verify:
        if response_dict['RESPCODE'] == '01':
            print('order successful')
        else:
            print('order was not successful because' + response_dict['RESPMSG'])
    return render(request, 'shop/paymentstatus.html', {'response': response_dict})