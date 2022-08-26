import pyrebase
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
#Agregar categoria
#data={"nombreCategoria":"Video Juegos"}
#r=db.child("Categorias").push(data)
#obt=db.child("Categorias").get()
#print(r)

#Listar Categorias
#for cate in obt.each():
#    print("Id de Categoria ",cate.key())
#    nombre = cate.val()
#    name= nombre['nombreCategoria']
#    print(name)
#Eliminar Categorias

#db.child("Cateogorias").child("-MBzCb84Gt7NWzsh89-P").remove()    

#Editar Categorias
#db.child("Cateogorias").child("-MBzCq7kKa1u1Yvk2fZL").update({"nombreCategoria":"Cate02"})

#Agregar Producto
#data={"nombreProducto":"Prod3","precio":85}
#prod=db.child("Products").push(data)
#key=prod['name']
#db.child("Categorias").child("-MDRywPjlrUMelNMi-NW").child("Productos").push({"producto":key})


#db.child("Categorias").child("").child("Productos").update(dato)

#Listar Usuarios
#users=db.child("Users").get()
#print(users)
#for user in users.each():
#    nombre=user.val()
#    print(nombre)
#    name= nombre['permiso']
#    if name==3:
#        print(" Id ",user.key()," Permiso ",name)
#allCates=db.child("Categorias").child("-MEAFl3aIccFI9aG8yWz").get()
#allProds=db.child("Productos").get()
#v=0
#for p in allProds.each():
#    if p.val()['Categoria'] == allCates.val()['nombreCategoria']:
#        v=v+1
#        print(p.val()['Categoria'])
#        if v>0:
#            break
#if v>0:
#    print("No se puede")
#else:

#Datos de entrada
email="cliente@gmail.com"
password="cliente123"
try:
    auth.sign_in_with_email_and_password(email,password)
    print("Se logueo correctamente")
except:
    print("Al parecer hubo un error al hacer el login")
#Login del Dueño
#try:
#    key=auth.sign_in_with_email_and_password(email,password)
#    permiso=db.child("Users").child(key['localId']).get()
#    if permiso.val()['permiso']==3:
#        print("Inicio Sesion del Dueño")
#    else:
#        print("No tienes permiso para entrar")
#except:
#    print("Hubo algun error")

#Listar productos
#hijo="Productos"
#todosProductos=db.child(hijo).get()
#for p in todosProductos.each():
#    print("Id ",p.key()," Producto ",p.val()['Producto']," Precio ",p.val()['Precio'])

#Comprar Producto
#user="zDyAbt7PFcO9GWOKYyGEXWZ9TxG2"
#idProducto="-MDk060lYdNDViPj1HFo"
#data={"fkIdProducto":idProducto,"estado":1}
#try:
#    db.child("Users").child(user).child("Compras").push(data)
#    print("Compra realizada correctamente")
#except:
#    print("Al parecer hubo un error")

#Productos Comprados
#misCompras=db.child("Users").child(user).child("Compras").get()
#for mC in misCompras.each():
#    print("Id de Compra ",mC.key())
#    print("fk del Producto ",mC.val()['fkIdProducto'])
#Carrito
#user="zDyAbt7PFcO9GWOKYyGEXWZ9TxG2"
#idProducto="-MDk060lYdNDViPj1HFo"
#data={"fkIdProducto":idProducto,"estado":1}
#try:
#    db.child("Users").child(user).child("Carrito").push(data)
#    print("Producto agregado al carrito correctamente")
#except:
#    print("Al parecer hubo un error")

#AddVenta
#nombreProducto="Xbox One"
#Precio=3500
#userVendedor="zDyAbt7PFcO9GWOKYyGEXWZ9TxG2"
#data={"Producto":nombreProducto,"Precio":Precio,"Vendedor":userVendedor,"Estado":1}
#try:
#    db.child("Producto").push(data)
#    print("Se agrego el producto Correctamente")
#    print("Espera a que te lo verifiquen para que aparezca en nuestro sitio")
#except:
#    print("Hubo algun error")

#addVenta
#user="zDyAbt7PFcO9GWOKYyGEXWZ9TxG2"
#idProducto="-MDk060lYdNDViPj1HFo"
#data={"fkIdProducto":idProducto,"estado":1}
#try:
#    db.child("Users").child(user).child("Carrito").push(data)
#    print("Producto agregado al carrito correctamente")
#except:
#    print("Al parecer hubo un error")

#Datos
#idUser="zDyAbt7PFcO9GWOKYyGEXWZ9TxG2"
#Nombre="Juanito"
#Direccion="Calle San tiburcio #101"
#data={"Nombre":Nombre,"Direccion":Direccion}
#try:
#    db.child("Users").child(idUser).child("Datos").push(data)
#    print("Se agrego una dirección correctamente")
#except:
#    print("Hubo algun error")
#idProducto="-MEwpRoHt0Sm3CBFKbsq"
#nuevoNombe="Play Station 5"
#nuevoPrecio=8500
#data={"Producto":nuevoNombe,"Precio":nuevoPrecio}
#try:
#    db.child("Productos").child(idProducto).update(data)
#    print("Producto editado correctamente")
#except:
#    print("Al parecer hubo algun error")
#nombre="Domesticos"
#data={"nombreCategoria":nombre}
#try:
#    db.child("Categorias").push(data)
#    print("Categoria agregada satisfactoriamente")
#except:
#    print("Al parecer hubo algun error")
#idCategoria="-MDRz7SbKfgfiRIScVPQ"
#nuevoNombe="Celulares"
#data={"nombreCategoria":nuevoNombe}
#try:
#    db.child("Categorias").child(idCategoria).update(data)
#    print("Categoria editada correctamente")
#except:
#    print("Se genero un error")
data={"Producto":"Play Station 4","Precio":3500}
try:
    db.child("Producto").push(data)
    print("Se agrego el producto Correctamente")
except:
    print("Hubo algun error")