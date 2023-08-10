using UnityEngine;
using TMPro;

public class textUpdate : MonoBehaviour
{
    // Start is called before the first frame update
    [SerializeField]
    public TMP_Text messageText;

    void Update()
    {
        messageText.SetText("New message");
    }
}









