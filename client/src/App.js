// importing components from react-router-dom package
import { Route, Routes } from "react-router-dom";
import Home from "./Home.jsx";
import Login from "./components/Login.js";
import Call from "./components/Call.js";
import Record from "./components/Record.js";



const App = () => {
  return (
      <div className="app">
      <Routes> 
        <Route path="/" element={<Login />}/>
        <Route path="/Call" element={<Call/>}/>
        <Route path="/Record" element={<Record />}/>
      </Routes>
      </div>
  );
};

// ReactDOM.render(<App />, document.getElementById("root"));
export default App;
