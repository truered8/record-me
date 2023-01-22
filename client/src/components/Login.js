import React, { useRef, useEffect, useState } from "react";
import io from "socket.io-client";
import { Typography, Button } from "@mui/material";
import Suggestions from "./suggestions";
import { RecordButton } from "./styles";
import useSound from "use-sound";

function Login() {
  return (
    <div>
      <Typography variant="title">Ghostwriter</Typography>
      <div style={{ marginTop: "1rem" }}>
        <form className="form" onSubmit={this.handleSubmit}>
          <div className="input-group">
            <label htmlFor="email">Email</label>
            <input type="email" name="email" placeholder="nome@email.com.br" />
          </div>
          <div className="input-group">
            <label htmlFor="password">Senha</label>
            <input type="password" name="password" />
          </div>
          <button className="primary">ENTRAR</button>
        </form>
        <button className="secondary" onClick={this.handleClick}>
          Criar uma nova conta
        </button>
      </div>
    </div>
  );
}

export default Login;
