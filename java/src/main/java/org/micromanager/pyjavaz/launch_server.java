package org.micromanager.pyjavaz;

import java.io.UnsupportedEncodingException;
import java.net.URISyntaxException;
import java.util.HashSet;

public class launch_server {

   public static void main(String[] args) {
      int port = 4827; // which port the server will listen on
      new ZMQServer( port);
   }


}
