const express = require("express");

const app = express();
const PORT = 3000;

// 👇 ADD THIS
app.get("/", (req, res) => {
    res.send("Root working");
});

app.get("/api", (req, res) => {
    res.send(`Response from backend container: ${process.env.HOSTNAME}`);
});

app.listen(PORT, () => {
    console.log(`Backend running on port ${PORT}`);
});