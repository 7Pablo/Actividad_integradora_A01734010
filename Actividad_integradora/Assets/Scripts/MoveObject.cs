using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Networking;

public static class JsonHelper
{
    public static T[] FromJson<T>(string json)
    {
        Wrapper<T> wrapper = JsonUtility.FromJson<Wrapper<T>>(json);
        return wrapper.Items;
    }

    public static string ToJson<T>(T[] array)
    {
        Wrapper<T> wrapper = new Wrapper<T>();
        wrapper.Items = array;
        return JsonUtility.ToJson(wrapper);
    }

    public static string ToJson<T>(T[] array, bool prettyPrint)
    {
        Wrapper<T> wrapper = new Wrapper<T>();
        wrapper.Items = array;
        return JsonUtility.ToJson(wrapper, prettyPrint);
    }

    [System.Serializable]
    private class Wrapper<T>
    {
        public T[] Items;
    }
}

[System.Serializable]
class MyObject
{
    public int x;
    public int y;

    override public string ToString()
    {
        return "X: " + x + ", Y: " + y;
    }
}

public class MoveObject : MonoBehaviour
{
    string simulationURL = null;
    private float waitTime = 0.2f;
    private float timer = 0.0f;
    public GameObject[] myObjects;

    // Start is called before the first frame update
    void Start()
    {
        StartCoroutine(ConnectToMesa());
    }

    IEnumerator ConnectToMesa()
    {
        WWWForm form = new WWWForm();

        using (UnityWebRequest www = UnityWebRequest.Post("http://localhost:5000/games", form))
        {
            yield return www.SendWebRequest();

            if (www.result != UnityWebRequest.Result.Success)
            {
                Debug.Log(www.error);
            }
            else
            {
                simulationURL = www.GetResponseHeader("Location");
                Debug.Log("Connected to simulation through Web API");
                Debug.Log(simulationURL);
            }
        }
    }

    IEnumerator UpdatePositions()
    {
        using (UnityWebRequest www = UnityWebRequest.Get(simulationURL))
        {
            if (simulationURL != null)
            {
                // Request and wait for the desired page.
                yield return www.SendWebRequest();

                Debug.Log("Data has been processed");
                MyObject[] agente = JsonHelper.FromJson<MyObject>(www.downloadHandler.text);
                
                for(int i = 0; i < 35; i++){
                    myObjects[i].transform.position = new Vector3(agente[i].x, 0, agente[i].y);
                }
            }
        }
    }

    // Update is called once per frame
    void Update()
    {
        timer += Time.deltaTime;
        if (timer > waitTime)
        {
            StartCoroutine(UpdatePositions());
            timer = timer - waitTime;
        }
    }
}
