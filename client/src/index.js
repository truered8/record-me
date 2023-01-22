import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './Home';
import { BrowserRouter, Switch, Route, Routes } from "react-router-dom";
import SocialPage from './SocialPage';
import Call from './components/Call';
import Record from './components/Record';
import Login from './components/Login';



const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Login />}>
          <Route path="/Call" element={<Call />}></Route>
          <Route path="/Record" element={<Record />}></Route>
        </Route>
      </Routes>
    </BrowserRouter>
  </React.StrictMode>,
  document.getElementById('root')
);