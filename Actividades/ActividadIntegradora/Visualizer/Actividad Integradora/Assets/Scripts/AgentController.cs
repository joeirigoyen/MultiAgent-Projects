// C# client to interact with Python. Based on the code provided by Sergio Ruiz and Octavio Navarro.
// Youthan Irigoyen. November 2021.

using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Networking;

public class PathData
{
    public List<Vector3> posList;
}

public class AgentController : MonoBehaviour
{
    // Initialize server and declare endpoints
    private string serverURL = "http://localhost:8585";
    private string initEndpoint = "/init";
    private string robotEndpoint = "/getRobotPath";
    private string boxEndpoint = "/getBoxPath";
    private string depotEndpoint = "/getDepotPath";
    private string stepEndpoint = "/step";
    // Initialize position lists
    private PathData robotData, boxData, depotData;
    private GameObject[] robotInstances, boxInstances, depotInstances;
    private List<Vector3> oldRobotPos, oldBoxPos;
    private List<Vector3> newRobotPos, newBoxPos;
    // Simulation's play/pause switch
    private bool pause = false;
    // Get prefabs and initial values
    private int depots;
    [SerializeField] GameObject robotPrefab, boxPrefab, depotPrefab, floor;
    [SerializeField] int robots, boxes, depot_x, depot_y, width, height;
    [SerializeField] float updateTime = 5.0f, timer, dt;

    // Start is called before the first frame update
    void Start()
    {
        // Initialize path data of each agent
        robotData = new PathData();
        boxData = new PathData();
        depotData = new PathData();
        // Initialize position lists
        robotInstances = new GameObject[robots];
        boxInstances = new GameObject[boxes];
        depotInstances = new GameObject[depot_x * depot_y];
        // Adjust floor size
        floor.transform.localScale = new Vector3((float)(width / 10), 1, (float)(height / 10));
        floor.transform.localPosition = new Vector3((float)(width / 2 - 0.5f), 0, (float)(height / 2 - 0.5f));
        // Set timer
        timer = updateTime;
        // Create instances of every agent
        depots = depot_x * depot_y;
        // Send info through JSON
        StartCoroutine(SendConfig());
    }

    // Update is called once per frame
    void Update()
    {
        // Get variable t from timer and time to update
        float t = timer / updateTime;
        // Number of steps to be taken before an agent gets from one point to another
        dt = Mathf.Pow(t, 2) * (3.0f - 2.0f * t);
        // If timer's value is higher than the time to update, pause the simulation and make a new step
        if (timer >= updateTime)
        {
            timer = 0;
            pause = true;
            StartCoroutine(Step());
        }
        // Otherwise, update timer 
        else
        {
            timer += Time.deltaTime;
        }
        // If the simulation is not paused, move the agents smoothly using LERPs
        if (!pause)
        {
            // Move robots
            for (int r = 0; r < robots; r++)
            {
                Vector3 lerp = Vector3.Lerp(oldRobotPos[r], newRobotPos[r], dt);
                robotInstances[r].transform.localPosition = lerp;
                Vector3 facingDir = oldRobotPos[r] - newRobotPos[r];
                robotInstances[r].transform.localRotation = Quaternion.LookRotation(facingDir);
            }
            // Move boxes
            for (int b = 0; b < boxes; b++)
            {
                Vector3 lerp = Vector3.Lerp(oldBoxPos[b], newBoxPos[b], dt);
                boxInstances[b].transform.localPosition = lerp;
                Vector3 facingDir = oldBoxPos[b] - newBoxPos[b];
                boxInstances[b].transform.localRotation = Quaternion.LookRotation(facingDir);
            }
        }
    }

    // Update every agent's position in every step
    IEnumerator Step()
    {
        UnityWebRequest www = UnityWebRequest.Get(serverURL + stepEndpoint);
        yield return www.SendWebRequest();
        if (www.result != UnityWebRequest.Result.Success)
        {
            Debug.Log(www.error);
        }
        else
        {
            StartCoroutine(GetRobotData());
            StartCoroutine(GetBoxData());
        }
    }

    // Send initial configuration to server through JSON
    IEnumerator SendConfig()
    {
        // Initialize form
        WWWForm form = new WWWForm();
        // Add fields to form
        form.AddField("agents", robots.ToString());
        form.AddField("boxes", boxes.ToString());
        form.AddField("depot_x", depot_x.ToString());
        form.AddField("depot_y", depot_y.ToString());
        form.AddField("width", width.ToString());
        form.AddField("height", height.ToString());
        // Make post request
        UnityWebRequest www = UnityWebRequest.Post(serverURL + initEndpoint, form);
        www.SetRequestHeader("Content-Type", "application/x-www-form-urlencoded");
        yield return www.SendWebRequest();
        // Debug any errors
        if (www.result != UnityWebRequest.Result.Success)
        {
            Debug.Log(www.error);
        }
        else
        {
            Debug.Log("Post completed. Initializing agents' positions.");
            StartCoroutine(GetInitRobotData());
            StartCoroutine(GetInitBoxData());
            StartCoroutine(GetInitDepotData());
        }
    }

    // Instantiate robots through the given JSON data
    IEnumerator GetInitRobotData()
    {
        // Attempt to get the robots' positions
        UnityWebRequest www = UnityWebRequest.Get(serverURL + robotEndpoint);
        yield return www.SendWebRequest();
        // If attempt is successful, set the robots in their initial positions
        if (www.result != UnityWebRequest.Result.Success)
        {
            Debug.LogFormat(www.error);
        }
        else
        {
            robotData = JsonUtility.FromJson<PathData>(www.downloadHandler.text);
            Debug.Log(robotData.posList);

            foreach (Vector3 pos in robotData.posList)
            {
                Instantiate(robotPrefab, pos, Quaternion.identity);
            }
        }
    }

    IEnumerator GetInitBoxData()
    {
        // Attempt to get the boxes' positions
        UnityWebRequest www = UnityWebRequest.Get(serverURL + boxEndpoint);
        yield return www.SendWebRequest();
        // If attempt is successful, set the boxes in their initial positions
        if (www.result != UnityWebRequest.Result.Success)
        {
            Debug.LogFormat(www.error);
        }
        else
        {
            boxData = JsonUtility.FromJson<PathData>(www.downloadHandler.text);
            Debug.Log(boxData.posList);

            foreach (Vector3 pos in boxData.posList)
            {
                Instantiate(boxPrefab, pos, Quaternion.identity);
            }
        }
    }

    IEnumerator GetInitDepotData()
    {
        // Attempt to get the depots' positions
        UnityWebRequest www = UnityWebRequest.Get(serverURL + depotEndpoint);
        yield return www.SendWebRequest();
        // If attempt is successful, set the depots in their initial positions
        if (www.result != UnityWebRequest.Result.Success)
        {
            Debug.LogFormat(www.error);
        }
        else
        {
            depotData = JsonUtility.FromJson<PathData>(www.downloadHandler.text);
            Debug.Log(depotData.posList);

            foreach (Vector3 pos in depotData.posList)
            {
                Instantiate(depotPrefab, pos, Quaternion.identity);
            }
        }
    }

    // Update robots' positions through the given JSON data
    IEnumerator GetRobotData()
    {
        // Attempt to get the robots' positions
        UnityWebRequest www = UnityWebRequest.Get(serverURL + robotEndpoint);
        yield return www.SendWebRequest();
        // If attempt is successful, set the robots in their new positions
        if (www.result != UnityWebRequest.Result.Success)
        {
            Debug.LogFormat(www.error);
        }
        else
        {
            robotData = JsonUtility.FromJson<PathData>(www.downloadHandler.text);
            Debug.Log(robotData.posList);
            // Add and clear out any previous path data
            oldRobotPos = new List<Vector3>(newRobotPos);
            newRobotPos.Clear();
            // Add next positions
            foreach (Vector3 pos in robotData.posList)
            {
                newRobotPos.Add(pos);
            }
            // Resume simulation
            pause = false;
        }
    }

    // Update boxes' positions through the given JSON data
    IEnumerator GetBoxData()
    {
        // Attempt to get the boxes' positions
        UnityWebRequest www = UnityWebRequest.Get(serverURL + boxEndpoint);
        yield return www.SendWebRequest();
        // If attempt is successful, set the boxes in their new positions
        if (www.result != UnityWebRequest.Result.Success)
        {
            Debug.LogFormat(www.error);
        }
        else
        {
            boxData = JsonUtility.FromJson<PathData>(www.downloadHandler.text);
            Debug.Log(boxData.posList);
            // Clear out any previous path data
            oldBoxPos = new List<Vector3>(newBoxPos);
            newBoxPos.Clear();
            // Add next positions
            foreach (Vector3 pos in boxData.posList)
            {
                newBoxPos.Add(pos);
            }
            // Resume simulation
            pause = false;
        }
    }
}
