// executar: java -cp .:protobuf-java-3.22.3.jar ServidorTcpAddressBook

import java.net.*;
import java.io.*;
import java.util.Arrays;

/**
 *
 * @author rodrigo
 */
public class ServidorTcpAddressBook {

    public static void main(String args[]) {
        try {
            int serverPort = 7000; // porta do servidor
            /* cria um socket e mapeia a porta para aguardar conexão */
            ServerSocket listenSocket = new ServerSocket(serverPort);

            //while (true) {
                System.out.println("Servidor aguardando conexão ...");

                /* aguarda conexões */
                Socket clientSocket = listenSocket.accept();

                System.out.println("Cliente conectado ...");
                
                /* recebe os dados enviados pelo cliente*/
                DataInputStream inClient = new DataInputStream(clientSocket.getInputStream());
                InputStreamReader i;
                
                String valueStr = inClient.readLine();
                System.out.println("Valor lido:" + valueStr);
                
                int sizeBuffer = Integer.valueOf(valueStr);
                
                byte[] buffer = new byte[sizeBuffer];
                inClient.read(buffer);
                System.out.println(Arrays.toString(buffer));
                
                /* realiza o unmarshalling */
                Addressbook.Person p = Addressbook.Person.parseFrom(buffer);
                
                /* exibe na tela */
                System.out.println("--\n" + p + "--\n");
                
                
            //} //while

        } catch (IOException e) {
            System.out.println("Listen socket:" + e.getMessage());
        } //catch
    } //main
} //class    