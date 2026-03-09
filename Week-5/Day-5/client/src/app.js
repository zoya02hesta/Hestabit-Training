import { useEffect, useState } from "react";

function App() {

  const [message,setMessage] = useState("");

  useEffect(()=>{
    fetch("http://localhost:5000")
    .then(res=>res.text())
    .then(data=>setMessage(data))
  },[])

  return (
    <div style={{textAlign:"center"}}>
      <h1>Docker Compose Demo</h1>
      <h2>{message}</h2>
    </div>
  );
}

export default App;