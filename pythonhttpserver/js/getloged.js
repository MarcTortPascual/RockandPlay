fetch("/logedinfo",{method:'POST'})
.then(
    function(ret){
        if (ret.status ==200){
            return ret.json()
        }
    }
).then(function(data){
    let menu = document.getElementsByTagName("mt-vsiderbar")[0]
    let dest = document.getElementById("user")
    let username  = document.createElement("p")
    while(dest.hasChildNodes()){dest.remove(dest.childNodes[0])}
    if (data.loged){
       
        username.innerHTML= ` Usuario:  ${ convert_ascii(data.nombre)[0].toUpperCase() + convert_ascii(data.nombre).slice(1)}`
        
        dest.append(username)
        let logout = document.createElement("form")
        logout.setAttribute("action","/logout")
        logout.setAttribute("method","post")
        let buton = document.createElement("button")
        buton.innerHTML="Cerrar sessión"

        logout.append(buton)
        dest.append(logout)
        let rutas = JSON.parse(menu.getAttribute("items"))

        rutas.push({'Tittle':'Su catalogo', 'Adr':'catalogo.html'})

        menu.setAttribute("items", JSON.stringify(rutas))
       
    }else{
        dest.append(document.createElement("h1"))
    }
    
})
let ascii_dict = {
    "%40": "@",
    "%c3%a1": "á",
    "%c3%a9": "é",
    "%c3%ad": "í",
    "%c3%b3": "ó",
    "%c3%ba%0d%0a": "ú"
}

function convert_ascii(text){
    
    for (const [key, value] of Object.entries(ascii_dict)) {
        text = text.replaceAll(key,value)
    }
    return text     
    
}