from functools import wraps
import sys
import os
import requests
from flask import Flask,render_template,redirect, request, url_for, session,flash
import pyrebase
app = Flask(__name__)
app.secret_key = os.urandom(24)
app.jinja_env.add_extension('jinja2.ext.loopcontrols')
#Config Firebase
config={
     "apiKey": "AIzaSyApH3WQJd3-IUlD4hqWa1GiMT_sT8UOZrE",
    "authDomain": "appi-ecf0e.firebaseapp.com",
    "databaseURL": "https://appi-ecf0e.firebaseio.com",
    "projectId": "appi-ecf0e",
    "storageBucket": "appi-ecf0e.appspot.com",
    "messagingSenderId": "168592718623",
    "appId": "1:168592718623:web:c82100b13c16a1f0e44e2a",
    "measurementId": "G-L9LJK2XBFC"
        }
#Iniciando los servicios de FB
firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db=firebase.database()
st=firebase.storage()
#Variables extras
@app.route('/')
def home():
    allProductos=db.child("Productos").get()
    return render_template('home.html',prod=allProductos.each())
#Login
@app.route('/Login',methods=['GET','POST'])
def Login():
    if request.method=='GET':
        flash("Por favor introduce tus datos para loguearte")
        return render_template("home.html")
    else:
        try:
            print(session['usr']+"  Primer try")
            return redirect(url_for('Productos'))
        except KeyError:
            if request.method=='POST':
                email=request.form['txtLoginEmail']
                password=request.form['txtLoginPassword']
                try:
                    user=auth.sign_in_with_email_and_password(email,password)
                    user=auth.refresh(user['refreshToken'])
                    user_id=user['idToken']
                    uid=user['userId']
                    usuario= db.child("Users").child(uid).get()
                    session['usuario']=usuario.val()['correo']
                    session['uid']=uid
                    session['usr']= user_id
                    total=0
                    session['total']=total
                    aute=db.child("Users/",uid).child("permiso").get()
                    usr=aute.val()
                    session['permiso']=usr
                    if usr==4:
                        flash("Logueado exitoso, Bienvenido")
                        return redirect(url_for('Productos'))
                    elif usr==3:
                        flash("Logueado exitoso, Bienvenido")
                        return redirect(url_for('productosDueno'))
                    elif usr==2:
                        flash("Logueado exitoso, Bienvenido")
                        return redirect(url_for('vendedor'))
                    elif usr==1:
                        flash("Logueado exitoso, Bienvenido")
                        return redirect(url_for('cliente'))
                    elif usr==0:
                        session.clear()
                        flash("Al parecer ya no tienes permiso")
                        return redirect(url_for('home'))
                except:
                    flash("Verificar nombre y contraseña sean correctos")
                    return redirect(url_for('home'))
            flash("Contraseña Invalida")
            return redirect(url_for('home'))
#Registro
@app.route('/Registro',methods=['GET','POST'])
def Registro():
    if request.method=='GET':
        flash("No lo hagas travieso")
        return redirect(url_for('home'))
    else:
        email=request.form['txtRegistroEmail']
        password=request.form['txtRegistroPassword']
        permiso=request.form['txtPermiso']
        try:
            user=auth.create_user_with_email_and_password(email,password)
            uid=user['localId']
            data={"correo":email,"permiso":int(permiso)}
            result=db.child('Users/',uid).set(data)
            if int(permiso)==1: 
                flash("Registro exitoso")
                return redirect(url_for('home'))
            if 3==int(session['permiso']):
                flash("Administrado agregado correctamente")
                return redirect(url_for('admins'))
        except:
            if int(permiso)==1: 
                flash("Al parecer este correo ya existe en la base de datos")
                return redirect(url_for('home'))
            if 3==int(session['permiso']):
                flash("Ya existe un administrador con este correo")
                return redirect(url_for('admins'))
#Vendedores
@app.route('/Vendedores')
def Vendedores():
    permiso=db.child("Users").child(session['uid']).get()
    if 'uid' in session and 4==int(permiso.val()['permiso']):
        allUsers=db.child("Users").get()
        allProductos=db.child("Productos").get()
        return render_template('admin/vendedores.html',u=allUsers.each(),productos=allProductos.each())
    else:
        flash("Al parecer usted ya no tiene permiso para entrar aquí")
        return redirect(url_for('home'))
#Validar Vendedor
@app.route('/validarProducto/<string:id>')
def validarProducto(id):
    permiso=db.child("Users").child(session['uid']).get()
    if 'uid' in session and 4==int(permiso.val()['permiso']):
        db.child("Productos").child(id).update({"estado":1})
        flash("Producto Verificado")
        return redirect(url_for('Vendedores'))
    else:
        flash("No puedes acceder a este metodo")
        return redirect(url_for('home'))
#Deshabilitar Vendedor 
@app.route('/deshabilitarProducto/<string:id>')
def deshabilitarProducto(id):
    permiso=db.child("Users").child(session['uid']).get()
    if 'uid' in session and 4==int(permiso.val()['permiso']):
        db.child("Productos").child(id).update({"estado":0})
        flash("Producto Deshabilitado")
        return redirect(url_for('Vendedores'))
    else:
        flash("No puedes acceder a este metodo")
        return redirect(url_for('home'))
# Listar Productos
@app.route('/Productos')
def Productos():
    permiso=db.child("Users").child(session['uid']).get()
    if 'uid' in session and 4==int(permiso.val()['permiso']):
        allCategorias=db.child("Categorias").get()
        allProductos=db.child("Productos").get()
        totalD=0
        if allProductos.val():
            for p in allProductos.each():
                if p.val()['Piezas']>0 and p.val()['Vendedor']=="Second Hand":
                    totalPz=p.val()['Precio']*p.val()['Piezas']
                    totalD=totalD+totalPz
            session['total']=totalD
            return render_template('admin/productos.html',r="required",act="/addProducto",msje="Ingresa una categoria",vId="",vProd="",vPie="",vPre="",vCate="",vImg="",vDes="",op="",product=allProductos.each(),cate=allCategorias.each())
        else:
            return render_template('admin/productos.html',cb="required",r="required",act="/addProducto",msje="Ingresa una categoria",vId="",vProd="",vPie="",vPre="",vCate="",vImg="",vDes="",op="",product=allProductos.each(),cate=allCategorias.each())
    else:
        flash("No se puede acceder")
        return redirect(url_for('home'))
#agregar Productos
@app.route('/addProducto',methods=['GET','POST'])
def addProducto():
    if request.method=='POST':
        producto=request.form['txtProducto']
        piezas=request.form['txtPieza']
        precio=request.form['txtPrecio']
        vendedor=request.form['txtVende']
        categoria=request.form['txtCategoria']
        descripcion=request.form['txtDescripcion']
        upload=request.files['upload']

        nameCategoria=db.child("Categorias").child(categoria).get()
        nameC=nameCategoria.val()['nombreCategoria']
        try:
            if session['permiso']==4:
                data={"Vendedor":vendedor,"Producto":producto,"Piezas":int(piezas),"Precio":float(precio),"Descripcion":descripcion,"Categoria":nameC,"enlace":"","estado":1}
                key=db.child("Productos").push(data)
                st.child("images/"+key['name']).put(upload)
                links = st.child("images/"+key['name']).get_url(None)
                data={"enlace":links}
                db.child("Productos").child(key['name']).update(data)
                flash("Producto agregado correctamente")
                return redirect(url_for('Productos'))
            if session['permiso']==1:
                data={"Vendedor":vendedor,"Producto":producto,"Piezas":int(piezas),"Precio":float(precio),"Descripcion":descripcion,"Categoria":nameC,"enlace":"","estado":0}
                key=db.child("Productos").push(data)
                st.child("images/"+key['name']).put(upload)
                links = st.child("images/"+key['name']).get_url(None)
                data={"enlace":links}
                db.child("Productos").child(key['name']).update(data)
                db.child("Users").child(session['uid']).child("Vendidos").child(key['name']).update({"producto":key['name']})
                flash("Producto a la espera de ser verificado")
                return redirect(url_for('Vender'))
        except:
            flash("Error al agregar el producto")
            return redirect(url_for('Productos'))
#eliminar Productos
@app.route('/deleteProducto/<string:id>')
def deleteProducto(id):
    permiso=db.child("Users").child(session['uid']).get()
    if 'uid' in session and 4==int(permiso.val()['permiso']):
        db.child("Productos").child(id).remove()
        flash("Se elimino el producto correctamente")
        return redirect(url_for('Productos'))
    else:
        flash("Al parecer ya no puede acceder a esta ruta")
#obtener datos Producto
@app.route('/getProducto/<string:id>')
def getProducto(id):
    getProd=db.child("Productos").child(id).get()
    data=getProd.val()
    allCategorias=db.child("Categorias").get()
    #nameCate=db.child("Categorias").child(data['fkCategoria']).get()
    #name=nameCate.val()
    allProductos=db.child("Productos").get()
    return render_template('admin/productos.html',r="",act="/editProducto",msje=data['Categoria'],vId=id,vProd=data['Producto'],vPie=data['Piezas'],vPre=data['Precio'],vCate="",vImg=data['enlace'],vDes=data['Descripcion'],op="",product=allProductos.each(),cate=allCategorias.each())
#Editar Producto
@app.route('/editProducto',methods=['GET','POST'])
def editProducto():
    nameC=""
    if request.method =='POST':
        upload=request.files['upload']
        producto=request.form['txtProducto']
        piezas=request.form['txtPieza']
        precio=request.form['txtPrecio']
        categoria=request.form['txtCategoria']
        cateA=request.form['txtCateA']
        descripcion=request.form['txtDescripcion']
        idProducto=request.form['txtId']
        if categoria:
            nameCategoria=db.child("Categorias").child(categoria).get()
            nameC=nameCategoria.val()['nombreCategoria']
        else:
            nameC=cateA
        if upload:
            try:
                data={"Producto":producto,"Piezas":int(piezas),"Precio":float(precio),"Descripcion":descripcion,"Categoria":nameC}
                db.child("Productos").child(idProducto).update(data)
                st.child("images/"+idProducto).put(upload)
                links = st.child("images/"+idProducto).get_url(None)
                data={"enlace":links}
                db.child("Productos").child(idProducto).update(data)
                flash("Producto editado correctamente")
                return redirect(url_for('Productos'))
            except:
                flash("No se pudo agregar la imagen")
        else:
            try:
                data={"Producto":producto,"Piezas":int(piezas),"Precio":float(precio),"Descripcion":descripcion,"Categoria":nameC}
                db.child("Productos").child(idProducto).update(data)
                flash("Producto editado correctamente sin imagen")
                return redirect(url_for('Productos'))
            except:
                flash("No se pudo")
                return redirect(url_for('Productos'))
#filtarPor
@app.route('/filtrarPor',methods=['GET','POST'])
def filtrarPor():
    if request.method=='POST':
        allCategorias=db.child("Categorias").get()
        allProductos=db.child("Productos").get()
        id=request.form['idCate']
        if id:
            cate=db.child("Categorias").child(id).get()
            return render_template('admin/productos.html',op=cate.val()['nombreCategoria'],product=allProductos.each(),cate=allCategorias.each())
        else:
            return(redirect(url_for('Productos')))
# Listar Categorias
@app.route('/Categorias')
def Categorias():
    allCategorias=db.child("Categorias").get()
    name = allCategorias.val() 
    return render_template('admin/categorias.html',act="/addCategoria",i="Agregar",estado="none",msje="",vA="",v="Introduce la categoria",c=allCategorias.each())
#Agregar Categoria
@app.route('/addCategoria',methods=['GET','POST'])
def addCategoria():
    if request.method=='POST':
        categoria=request.form['txtCategoria']
        try:
            data={"nombreCategoria":categoria}
            db.child("Categorias").push(data)
            flash("Registro Exitoso")
            return redirect(url_for('Categorias'))
        except:
            flash("Registro Fallido")
            return redirect(url_for('Categorias'))
#Eliminar Categoria
@app.route('/deleteCategoria/<string:id>')
def deleteCategoria(id):
    allCates=db.child("Categorias").child(id).get()
    allProds=db.child("Productos").get()
    v=0
    for p in allProds.each():
        if p.val()['Categoria'] == allCates.val()['nombreCategoria']:
            v=v+1
            print(p.val()['Categoria'])
            if v>0:
                break
    if v>0:
        if 4==session['permiso']:
            flash("No se puede eliminar la categoria por que productos dependen de ella")
            return redirect(url_for('Categorias'))
        if 3==session['permiso']:
            flash("No se puede eliminar la categoria por que productos dependen de ella")
            return redirect(url_for('duenoCategorias'))
    else:
        db.child("Categorias").child(id).remove()
        if 4==session['permiso']:
            flash("Se elimino la categoria correctamente")
            return redirect(url_for('Categorias'))
        if 3==session['permiso']:
            flash("Se elimino la categoria correctamente")
            return redirect(url_for('duenoCategorias'))

#obtener datos Categoria
@app.route('/getCategoria/<string:id>')
def getCategoria(id):
    allCategorias=db.child("Categorias").get()
    data=db.child("Categorias").child(id).get()
    dat=data.val()
    return render_template("admin/categorias.html",act="/editCategoria",ide=id,i="Editar",r=data,estado="none",msje="",v=dat['nombreCategoria'],c=allCategorias.each())
#editar Categoria
@app.route('/editCategoria',methods=['GET','POST'])
def editCategoria():
    if request.method=='POST':
        ide=request.form['txtId']
        categoria=request.form['txtCategoria']
        aCategoria=request.form['antiguaCategoria']
        db.child("Categorias").child(ide).update({"nombreCategoria":categoria})
        all_prod_ids=db.child("Productos").get()
        for ids in all_prod_ids.each():
            if ids.val()['Categoria'] == aCategoria:
                db.child("Productos").child(ids.key()).update({"Categoria":categoria})
        return redirect(url_for('Categorias'))
#Ventas
@app.route('/Ventas')
def Ventas():
    if 'usr' in session and 4==int(session['permiso']):
        allUsers=db.child("Users").get()
        allVentas=db.child("Ventas").get()
        allProductos=db.child("Productos").get()
        return render_template('admin/ventas.html',ventas=allVentas.each(),users=allUsers.each(),productos=allProductos.each())
    else:
        flash("No tiene permiso para hacer esto")
        return redirect(url_for('home'))
@app.route('/dueno',methods=['GET','POST'])
#Dueño
def dueno():
    if 'usr' in session:
        if 3 == int(session['permiso']):
            flash("Bienvenido")
            return render_template("dueno/productos.html")
        else:
            flash("No intentes eso")
            render_template('home.html') 
    else:
        flash("No se pudo acceder al crud")
        return render_template("home.html")
#Categorias Dueño
@app.route('/duenoCategorias')
def duenoCategorias():
    if 'usr' in session and 3==int(session['permiso']):
        misCategorias=db.child("Categorias").get()
        return render_template("dueno/categorias.html",cates=misCategorias.each())
    else:
        flash("No tienes acceso a esta ruta")
        return redirect(url_for('home'))
#Agregar category por Dueño
@app.route('/newCategory',methods=['GET','POST'])
def newCategory():
    if 'usr' in session and 3==int(session['permiso']):
        if request.method=='POST':
            cate=request.form['txtCategoria']
            comp=db.child("Categorias").get()
            v=0
            for c in comp.each():
                if cate==c.val()['nombreCategoria']:
                    v=v+1
                    if v>0:
                        break
            if v>0:
                flash("Esta categoria ya existe, prueba con otra")
                return redirect(url_for('duenoCategorias'))
            else:
                db.child("Categorias").push({"nombreCategoria":cate})
                flash("Categoria  Agregada correctamente")
                return redirect(url_for('duenoCategorias'))
        else:
            flash("No intentes eso por favor")
            return redirect(url_for("duenoCategorias"))
    else:
        flash("No tienes acceso a esta ruta")
        return redirect(url_for('home'))
#Ventas del dueño
@app.route('/misVentas')
def misVentas():
    if 'usr' in session and 3==session['permiso']:
        misVentas=db.child("Ventas").get()
        misProductos=db.child("Productos").get()
        users=db.child("Users").get()
        totalD=0
        for p in misProductos.each():
            if p.val()['Vendedor']=="Second Hand" and p.val()['Piezas']==-1:
                totalPz=(p.val()['Precio']*p.val()['Piezas'])*-1
                totalD=totalD+totalPz
        session['total']=totalD
        return render_template("dueno/misVentas.html",us=users.each(),ventas=misVentas.each(),productos=misProductos.each())
    else:
        flash("No tienes permiso para acceder a esta ruta")
        return redirect(url_for('home'))       
#Lista de admins 
@app.route('/admins')
def admins():
    if 'usr' in session and 3==int(session['permiso']):
        allUsers=db.child("Users").get()
        return render_template('dueno/admins.html',users=allUsers.each())
    else:
        flash("No tienes permiso para entrar a esta ruta")
        return redirect(url_for('home'))
#Deshabilitar admins
@app.route('/deshabilitarAdmin/<string:id>')
def deshabilitarAdmin(id):
    if 'usr' in session and 3==int(session['permiso']):
        try:
            db.child("Users").child(id).update({"permiso":0})
            flash("Se deshabilito el usuario correctamente")
            return redirect(url_for('admins'))
        except:
            flash("Al parecer hubo un error")
            return redirect(url_for('admins'))
    else:
        flash("No tienes permiso para entrar a esta ruta")
        return redirect(url_for('dueno'))
#Habilitar admins
@app.route('/habilitarAdmin/<string:id>')
def habilitarAdmin(id):
    if 'usr' in session and 3==int(session['permiso']):
        try:
            db.child("Users").child(id).update({"permiso":4})
            flash("Se habilito el usuario correctamente")
            return redirect(url_for('admins'))
        except:
            flash("Al parecer hubo un error")
            return redirect(url_for('admins'))
    else:
        flash("No tienes permiso para entrar a esta ruta")
        return redirect(url_for('dueno'))
#productosDueno
@app.route('/productosDueno')
def productosDueno():
    misProductos=db.child("Productos").get()
    misCategorias=db.child("Categorias").get()
    totalD=0
    for p in misProductos.each():
        if p.val()['Vendedor']=="Second Hand" and p.val()['Piezas']>0:
            totalPz=p.val()['Precio']*p.val()['Piezas']
            totalD=totalD+totalPz
    session['total']=totalD
    return render_template("dueno/productos.html",categorias=misCategorias.each(),productos=misProductos.each())
#Vendedor
@app.route('/vendedor',methods=['GET','POST'])
def vendedor():
    if 'usr' in session:
        if 2 == int(session['permiso']):
            flash("Bienvenido")
            return render_template("vendedor/index.html")
        else:
            flash("No intentes eso")
            render_template('home.html') 
    else:
        flash("No se pudo acceder al crud")
        return render_template("home.html")
#Cliente
@app.route('/cliente',methods=['GET','POST'])
def cliente():
    if 'usr' in session:
        if 1 == int(session['permiso']):
            allProductos=db.child("Productos").get()
            return render_template("cliente/index.html",prod=allProductos.each())
        else:
            flash("No intentes eso")
            render_template('home.html') 
    else:
        flash("No se pudo acceder al crud")
        return render_template("home.html")
#Comprar Producto
@app.route('/comprarProducto/<string:id>')
def comprarProducto(id):
    if 'usr' in session:
        producto=db.child("Productos").child(id).get()
        prod=producto.val()
        if prod['Piezas']>=1:
            flash("Llena los campos para completar la compra")
            return render_template("cliente/comprar.html",idP=id,name=prod['Producto'],desc=prod['Descripcion'],precio=prod['Precio'],link=prod['enlace'],vende=prod['Vendedor'])
        else:
            flash("Al parecer alguien ya compro el producto primero que tu")
            return redirect(url_for('cliente'))
    else:
        flash("Para poder comprar un producto necesitas loguearte")
        return redirect(url_for('home'))
#Finalizar Compra
@app.route('/finalizarCompra',methods=['GET','POST'])
def finalizarCompra():
    if request.method =='POST':
        ideP=request.form['idProducto']
        nombre=request.form['nombre']
        direccion=request.form['direccion']
        data={"fkProducto":ideP,"fkUser":session['uid'],"direccion":direccion,"nombre":nombre,"estado":1}
        try:
            #uid=session['uid']
            db.child("Productos").child(ideP).update({"Piezas":0})
            key=db.child("Ventas").push(data)
            db.child("Users").child(session['uid']).child("Detalles").child(key['name']).set({"fkIdCompra":key['name']})
            flash("Compra realizada satisfactoriamente")
            return redirect(url_for('compras'))
        except:
            flash("Al parecer hubo un error...")
            return redirect(url_for('cliente'))
#Marcar como recibido
@app.route('/recibido/<string:id>')
def recibido(id):
    try:
        db.child("Users").child(session['uid']).child("Detalles").child(id).update({"estado":-1})
        flash("Producto marcado como recibido")
        return redirect(url_for('compras'))
    except:
        flash("Al parecer hubo algun error")
        return redirect(url_for('compras'))
#Eliminar Detalle
@app.route('/eliminarDetalle/<string:id>')
def eliminarDetalle(id):
    try:
        flash("Detalle de compra eliminada correctamente")
        db.child("Users").child(session['uid']).child("Detalles").child(id).update({"estado":3})
        return redirect(url_for('compras'))
    except:
        flash("Al parecer hubo un error")
        return redirect(url_for('compras'))
#Mis compras
@app.route('/compras')
def compras():
    uid=session['uid']
    misCompras=db.child("Users").child(uid).child("Detalles").get()
    misVentas=db.child("Ventas").get()
    allProds=db.child("Productos").get()
    allUsers=db.child("Users").get()
    return render_template('cliente/compras.html',compras=misCompras.val(),ventas=misVentas.each(),users=allUsers.each(),productos=allProds.each())


#Cancelar Compra
@app.route('/cancelarCompra')
def cancelarCompra():
    flash("Has cancelado la compra")
    return redirect(url_for('cliente'))
#Marcar como prodcuto Recibido
@app.route('/productoRecibido/<string:id>')
def productoRecibido(id):
    if 'usr' in session:
        try:
            result=db.child("Ventas").child(id).get()
            db.child("Ventas").child(id).update({"estado":-1})
            db.child("Productos").child(result.val()['fkProducto']).update({"Piezas":-1})
            flash("Este producto se ha marcado como recibido")
            return redirect(url_for('compras'))
        except:
            flash("No se pudo marcar como recibido")
            return redirect(url_for('compras'))
    else:
        flash("Te hemos castigado enviado al inicio")
        return redirect(url_for('home'))
#addCarrito
@app.route('/addCarrito/<string:id>')
def addCarrito(id):
    if 'usr' in session:
        idUser=session['uid']
        try:
            ex=db.child("Users").child(idUser).child("Carrito").child(id).get()
            for e in ex.each():
                if id == e.val():
                    flash("Este producto ya lo tienes en el carrito")
                    return redirect(url_for('cliente'))
        except:
            db.child('Users').child(idUser).child("Carrito").child(id).set({"producto":id,"estado":1})
            flash("Se agrego correctamente a tu carrito de compras")
            return redirect(url_for('cliente'))
    else:
        flash("Necesitas loguearte para tener un carrito")
        return redirect(url_for('home'))
#carrito
@app.route('/carrito')
def carrito():
    if 'usr' in session:
        if 1 == int(session['permiso']):
            myId=session['uid']
            allProds=db.child("Productos").get()
            miCarrito=db.child("Users").child(myId).child("Carrito").get()
            totalDinero=0
            if miCarrito.val():
                for c in miCarrito.each():
                    for p in allProds.each():
                        if c.val()['producto'] == p.key() and p.val()['Piezas']>0 and c.val()['estado']>0:
                            costo=p.val()['Precio']
                            totalDinero=totalDinero+costo
                return render_template("cliente/carrito.html",v=totalDinero,prod=allProds.each(),carr=miCarrito.each())
            else:
                flash("Ya no tienes productos en tu carrito")
                return redirect(url_for('cliente'))
    else:
        flash("No puedes hacer eso")
        return render_template("home.html")
#Eliminar Producto Carrito
@app.route('/eliminarCarrito/<string:id>')
def eliminarCarrito(id):
    if 'usr' in session:
        if 1 == int(session['permiso']):
            myId=session['uid']
            db.child("Users").child(myId).child("Carrito").child(id).remove()
            flash("Se elimino el producto correctamente")
            return redirect(url_for('carrito'))
    else:
        flash("No lo hagas porfavor")
        return redirect(url_for('carrito'))
#Deseleccionar Producto del carrito
@app.route("/darBaja/<string:id>")
def darBaja(id):
    userId=session['uid']
    db.child("Users").child(userId).child("Carrito").child(id).update({"estado":0})
    flash("Deseleccionado correctamente")
    return redirect(url_for("carrito"))
#Seleccionar Producto del carrito
@app.route("/darAlta/<string:id>")
def darAlta(id):
    userId=session['uid']
    db.child("Users").child(userId).child("Carrito").child(id).update({"estado":1})
    flash("Seleccionado correctamente")
    return redirect(url_for("carrito"))
@app.route('/Prueba',methods=['GET','POST'])
#Vender
@app.route('/Vender')
def Vender():
    misProductos=db.child("Productos").get()
    Categorias=db.child("Categorias").get()
    misVentas=db.child("Ventas").get()
    misVendidos=db.child("Users").child(session['uid']).child("Vendidos").get()
    return render_template("cliente/vender.html",ventas=misVentas.each(),productos=misProductos.each(),vendidos=misVendidos.each(),cate=Categorias.each())
#Simulador de banco
@app.route('/banco/<string:id>')
def banco(id):
    if 'usr' in session:
        ventas=db.child("Ventas").child(id).get()
        productos=db.child("Productos").child(ventas.val()['fkProducto']).get()
        idCompra=ventas.key()
        nombreProducto=productos.val()['Producto']
        precioProducto=productos.val()['Precio']
        return render_template("cliente/banco.html",idVenta=id,producto=nombreProducto,precio=precioProducto,compra=idCompra)
    else:
        flash("No puedes acceder a esta ruta")
        return redirect(url_for('compras')) 
#Pagar
@app.route('/pagar/<string:id>')
def pagar(id):
    if 'usr' in session:
        try:
            db.child("Ventas").child(id).update({"estado":0})
            flash("Producto comprado")
            return redirect(url_for('compras'))
        except:
            flash("Al parecer hubo un error")
            return redirect(url_for('compras'))
    else:
        flash("No se pude acceder a estar ruta")
        return redirect(url_for('home'))

#Cerrar Sesión
@app.route('/logOut')
def logOut():
    session.clear()
    flash("Se salio")
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)