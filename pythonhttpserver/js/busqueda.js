export function search(source, filter, bodydest, what) {
    fetch(source)
        .then(ret => ret.text())
        .then(function (data) {

            let parser = new DOMParser()
            let xml = parser.parseFromString(data, "text/xml")

            let libros = xml.getElementsByTagName(what)
            let html = document.createElement("h1")

            let body = bodydest

            let select = document.getElementById(filter)
            let librodiv = document.createElement("div")
            while (body.hasChildNodes()) {
                body.removeChild(body.lastChild);
            }

            for (let libro of libros) {
                console.log(select.value)
                if (select.value == libro.getElementsByTagName(filter)[0].innerHTML) {
                    librodiv = document.createElement("div")
                    librodiv.setAttribute("class", "libro")
                    for (let item of libro.children) {
                        if (item.tagName == "titulo") {
                            html = document.createElement("h1")
                            html.innerHTML = item.innerHTML
                            librodiv.append(html)
                        }
                        if (item.tagName == "isbn" || item.tagName == "autor" || item.tagName == "genero" || item.tagName == "descripcion" || item.tagName == "fecha") {
                            html = document.createElement("p")
                            html.innerHTML = item.innerHTML
                            librodiv.append(html)
                        }
                        if (item.tagName == "miniatura") {
                            html = document.createElement("img")
                            html.setAttribute("src", item.getAttribute("src"))
                            html.style.width = "30%"
                            librodiv.append(html)
                        }
                    }
                    body.append(librodiv)
                }

            }

        })
}
export function searchtex(source, filter, bodydest) {
    fetch(source)
        .then(ret => ret.text())
        .then(function (data) {

            let parser = new DOMParser()
            let xml = parser.parseFromString(data, "text/xml")

            let libros = xml.getElementsByTagName("libro")
            let html = document.createElement("h1")

            let body = bodydest

            let select = document.getElementById(filter)
            let librodiv = document.createElement("div")
            while (body.hasChildNodes()) {
                body.removeChild(body.lastChild);
            }

            for (let libro of libros) {
                let lower = libro.getElementsByTagName(filter)[0].innerHTML.toLowerCase()
                if (lower.search(select.value.toLowerCase()) >= 0) {
                    librodiv = document.createElement("div")
                    librodiv.setAttribute("class", "libro")
                    for (let item of libro.children) {
                        if (item.tagName == "titulo") {
                            html = document.createElement("h1")
                            html.innerHTML = item.innerHTML
                            librodiv.append(html)
                        }
                        if (item.tagName == "isbn" || item.tagName == "autor" || item.tagName == "genero" || item.tagName == "descripcion") {
                            html = document.createElement("p")
                            html.innerHTML = item.innerHTML
                            librodiv.append(html)
                        }
                        if (item.tagName == "miniatura") {
                            html = document.createElement("img")
                            html.setAttribute("src", item.getAttribute("src"))
                            html.style.width = "30%"
                            librodiv.append(html)
                        }
                        if (item.tagName == "enlace") {
                            html = document.createElement("div")
                            let html2 = document.createElement("a")
                            html2.setAttribute("href", item.getAttribute("href"))
                            html.setAttribute("id", "botenlace")
                            html.append(html2)
                            librodiv.append(html)
                        }
                    }
                    body.append(librodiv)
                }

            }

        })
}