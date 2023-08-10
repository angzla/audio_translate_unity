using UnityEngine;
using System;
using System.Net;
using System.Net.Sockets;
using System.Text;
using System.Threading.Tasks;
using TMPro;

public class serverMessage : MonoBehaviour

{   
    [SerializeField]
    private TMP_Text messageText;

    private Socket listener;
    private string receivedMessage = "";

    private void Start()
    {
        IPAddress ipAddress = IPAddress.Parse("127.0.0.1");
        IPEndPoint ipEndPoint = new IPEndPoint(ipAddress, 65432);

        listener = new Socket(ipEndPoint.AddressFamily, SocketType.Stream, ProtocolType.Tcp);
        listener.Bind(ipEndPoint);
        listener.Listen(10);

        Debug.Log("Server started. Waiting for a connection...");

        AcceptClient();
        messageText.SetText("Waiting for server");
    }

    private async void AcceptClient()
    {
        while (true)
        {

            Socket handler = await listener.AcceptAsync();
            Debug.Log("Client connected.");

            _ = Task.Run(async () =>
            {

                byte[] buffer = new byte[1024];
                int bytesRead = await handler.ReceiveAsync(new ArraySegment<byte>(buffer), SocketFlags.None);
                string message = Encoding.UTF8.GetString(buffer, 0, bytesRead);

                Debug.Log("Received message: " + message);

                receivedMessage = message;

                //messageText.SetText(message); // Update the UI text box with the received message

                //handler.Shutdown(SocketShutdown.Both);
                //handler.Close();

                //AcceptClient(); // Continue listening for more clients

            });

        }
    }

    private void Update()
    {
        messageText.SetText(receivedMessage);
    }
}

