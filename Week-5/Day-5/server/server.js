const express = require("express");
const mongoose = require("mongoose");
const cors = require("cors");

const app = express();

app.use(cors());
app.use(express.json());

mongoose.connect("mongodb://mongo:27017/docker-demo")
.then(() => console.log("MongoDB connected"))
.catch(err => console.log(err));

app.get("/", (req,res)=>{
    res.send("Server running with Docker Compose 🚀");
})

app.listen(5000,()=>{
    console.log("Server running on port 5000");
});