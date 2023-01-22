import React, { useRef, useEffect, useState } from "react";
import io from "socket.io-client";
import { Typography, Button } from "@mui/material";
import Suggestions from "./suggestions";
import { RecordButton } from "./styles";
import useSound from "use-sound";


function Call() {

  return (
    <div>
      <Typography variant="title">Ghostwriter</Typography>
      <div style={{ marginTop: "1rem" }}>
        <Typography variant="subtitle">
          Rapping is a form of poetry, one to ease the mind and provide clarity.
          We are hacking the mental health space by giving literal poetic
          justice to users around the world.
        </Typography>
      </div> 
      </div>
    
  );
}

export default Call;
