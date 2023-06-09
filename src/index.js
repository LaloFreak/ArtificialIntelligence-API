const port = process.env.PORT || 3000
const server = require('./app');
const { sequelize } = require("./db.js");

async function main() {
    try {
      await sequelize.sync({force: true});  
      console.log("succesfully connected");
      server.listen(port, ()=> console.log(`server listening on port ${port}`))
    } catch (error) {
      console.error("Unable to connect to database");
      server.listen(port, ()=> console.log(`server listening on port ${port}`))
    }
}
main();