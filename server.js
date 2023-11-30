const express = require('express')
const app = express()
const basicAuth = require('express-basic-auth')
const port = 4131 //change to 4131 when it works
let sale_active = false
let sale_message = ""
let next_id = 0;
let con = {
    name: "mr pirate",
    email: "mrpirate@gmail.com",
    date: "2023-12-31",
    ship_condition: "no repairs needed",
    new_customer: "no",
    id: next_id
}

const admin_login = {
    users: { 'admin': 'pass' },
    challenge: true,
    unauthorizedResponse: "You dont have access",
}
////
app.use(['/api/sale', '/admin/contactlog'], basicAuth(admin_login))
app.use('/api/sale', (req, res, next) => {
    if (req.method === 'POST' || req.method === 'DELETE') {
        basicAuth(admin_login)(req, res, next);
    } else {
        next();
    }
})
///
let contacts = [con]
const acceptable_keys = ["name", "email", "date", "ship_condition", "new_customer"]
function updateContacts(key, value) {
    next_id++;
    let c = {
        name: "mr pirate",
        email: "mrpirate@gmail.com",
        date: "2023-12-31",
        ship_condition: "no repairs needed",
        new_customer: "no",
        id: next_id
    }
    for (let i = 0; i < value.length; i++) {
        if (acceptable_keys.includes(key[i])) {
            c[key[i]] = value[i]
        }
        if (c.new_customer == "on") {
            c.new_customer = "yes"
        }
        c.name = c.name.replace(/\+/g, " ");
        c.ship_condition = c.ship_condition.replace(/\+/g, " ")
        contacts.push(c)
        return
    }
}

app.set("views", "templates")
app.set("view engine", "pug")

app.use(express.urlencoded({ extended: true }))
app.use(express.json())

app.use(express.static(__dirname + '/resoures'))
//app.use('/images', express.static('images'))
//app.use('/css', express.static("css"))
// look in "resource" folder for static files -- serve them on URLS starting with "/resource"

app.use("/js", express.static("resources/js"));
app.use("/css", express.static("resources/css"));



// get requests
app.get('/', (req, res) => {
    res.render("mainpage.pug")
})
app.get('/main', (req, res) => {
    res.render("mainpage.pug")
})

app.get('/resources/images/main', (req, res) => {
    res.status(200);
    res.contentType('image/jpeg');
    res.sendFile(__dirname + "/resources/images/pirate.jpeg")

})

app.get('/contact', (req, res) => {
    res.render("contactform.pug")
})
app.get('/admin/contactlog', (req, res) => {
    res.render("contactlog.pug", { contacts })
})
app.get('/testimonies', (req, res) => {
    res.render("testimonies.pug")
})
app.get("/api/sale", (req, res) => {
    if (sale_active) {
        let content = { active: "true", message: sale_message }
        res.setHeader("Content-Type", "application/json")
        res.status(200).json(content)
    }
    let content = { active: "false" }
    res.setHeader("Content-Type", "application/json")
    res.status(200).json(content)
})

//post requests
app.post('/contact', (req, res) => {
    if (req.body == null) {
        res.status(404).render("404.pug")
    }
    if (2 == 2) { //TODO fix logic here
        let info = req.body

        let key = Object.keys(info);
        let value = Object.values(info);


        updateContacts(key, value);
        res.status(201).render("contactsuccess.pug")
    } else {
        res.status(400).render("contactfail.pug")
    }
})
app.post("/api/sale", (req, res) => {
    if (req.body == null) {
        res.setHeader("Content-Type", "text/plain")
        res.status(400).send("no body")
    }
    else if (req.get("Content-Type") != null && req.header("Content-Type") != "application/json") {
        res.setHeader("Content-Type", "text/plain")
        res.status(400).send("send me json!")
    }
    else {
        if (sale_active) {
            sale_message = req.body.message
            let content = { message: sale_message }
            res.setHeader("Content-Type", "application/json")
            res.status(201).json(content)
        }
        sale_active = true
        sale_message = req.body.message
        let content = { message: sale_message }
        res.setHeader("Content-Type", "application/json");
        res.status(200).json(content)

    }
})
//Delete methods
app.delete("/api/contact", (req, res) => {
    if (req.get("Content-Type") != null && req.header("Content-Type") == "application/json") {
        let target = req.body.id
        contacts.forEach(contact => {
            if (contact.id == target) {
                contacts.pop(contact)
            }
            res.render("contactlog.pug", { contacts })
        });
    }
    else if (req.get("Content-Type") != null) {
        res.setHeader("Content-Type", "text/plain");
        res.status(400).send("Not the proper format")
    }
    else {
        res.setHeader("Content-Type", "text/plain");
        res.status(400).send("Must Include Content-Type header")
    }
})
//TODO: add api/sale delete
app.delete("/api/sale", (req, res) => {

    if (sale_active) {
        sale_active = false
        sale_message = ""
        //turn off sale

        res.status(200).render("contactlog.pug", { contacts })

    }
    res.status(400).render("contactlog.pug", { contacts })
})

//404 handling
app.use((req, res, next) => {
    res.status(404).render("404.pug")
})

app.listen(port, () => {
    console.log(`Example app listening on port ${port}`)
})