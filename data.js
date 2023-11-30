// this package behaves just like the mysql one, but uses async await instead of callbacks.
const mysql = require(`mysql-await`); // npm install mysql-await
const { get } = require("prompt");

// first -- I want a connection pool: https://www.npmjs.com/package/mysql#pooling-connections
// this is used a bit differently, but I think it's just better -- especially if server is doing heavy work.
var connPool = mysql.createPool({
  connectionLimit: 5, // it's a shared resource, let's not go nuts.
  //host: "127.0.0.1",// this will work
  host: "localhost",// use this with the tunnel
  user: "C4131F23U240",
  database: "C4131F23U240",
  password: "57650", // we really shouldn't be saving this here long-term -- and I probably shouldn't be sharing it with you...
});

// later you can use connPool.awaitQuery(query, data) -- it will return a promise for the query results.

async function addContact(data) {
  // you CAN change the parameters for this function. please do not change the parameters for any other function in this file.
  let x = "INSERT INTO contacts (contact_name,contact_email,meet_date,ship_condition,new_customer) VALUES (" + data.name + "," + data.email + "," + data.date + "," + data.ship_condition + "," + data.new_customer + ")"
  return await connPool.awaitQuery(x)
}
addContact({ name: "test", email: "test@gmail.com", date: "2023-30-11", ship_condition: "No repairs needed", new_customer: true }).then(console.log)

async function deleteContact(id) {

}

async function getContacts() {


}

async function addSale(message) {

}

async function endSale() {

}

async function getRecentSales() {

}

module.exports = { addContact, getContacts, deleteContact, addSale, endSale, getRecentSales }