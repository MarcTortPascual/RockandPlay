import { search } from "./busqueda.js"


fetch("../db/biblio/eventos.xml")
.then(ret=>ret.text())
.then(function(data){

    let parser = new DOMParser()
    let xml = parser.parseFromString(data,"text/xml")
    let libros = xml.getElementsByTagName("evento")
    let librodiv = document.createElement("div")
    let body = document.getElementById("eventos")
    let html = document.createElement("h1")
    for (let libro of libros){
        
        librodiv = document.createElement("div")
        librodiv.setAttribute("class", "evento")
        for (let item of libro.children){
            if (item.tagName=="titulo"){
                html = document.createElement("h1")
                html.innerHTML = item.innerHTML
                librodiv.append(html)
            }
            if (item.tagName=="fecha" || item.tagName=="descripcion" ){
                html = document.createElement("p")
                html.innerHTML = item.innerHTML
                librodiv.append(html)
            }
            if (item.tagName=="miniatura"){
                html = document.createElement("img")
                html.setAttribute ("src",item.getAttribute("src"))
                html.style.width ="30%"
                librodiv.append(html)
            }
            if (item.tagName == "enlace") {
                html = document.createElement("div")
                let html2 = document.createElement("a")
                html2.setAttribute("href", item.getAttribute("href"))
                html2.innerHTML="Mas información "
                html.setAttribute("id", "botenlace")
                html.append(html2)
                librodiv.append(html)
            }
        }
        body.append(librodiv)
    }

    
})

let fechain = document.getElementById("fecha")
fechain.addEventListener("input",function(){

    search("../db/biblio/eventos.xml","fecha",document.getElementById("eventos"),"evento")
})