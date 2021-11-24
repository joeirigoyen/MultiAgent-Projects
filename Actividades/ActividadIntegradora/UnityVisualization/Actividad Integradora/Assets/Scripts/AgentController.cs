// C# client to interact with Python. Based on the code provided by Sergio Ruiz and Octavio Navarro.
// Youthan Irigoyen. November 2021.

using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Networking;

public class PathData
{
    public List<Vector3> positions;
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
    private List<Vector3> oldRobotPos, oldBoxPos, oldDepotPos;
    private List<Vector3> newRobotPos, newBoxPos, newDepotPos;
    // Simulation's play/pause switch
    private bool pause = false;
    // Get prefabs and initial values
    private int depots;
    [SerializeField] GameObject robotPrefab, boxPrefab, depotPrefab, floor;
    [SerializeField] int robots, boxes, depot_x, depot_y, width, height, max_steps;
    [SerializeField] float updateTime = 0.5f, timer, dt;

    // Start is called before the first frame update
    void Start()
    {
        // Initialize path data of each agent
        robotData = new PathData();
        boxData = new PathData();
        depotData = new PathData();
        oldRobotPos = new List<Vector3>();
        newRobotPos = new List<Vector3>();
        oldBoxPos = new List<Vector3>();
        newBoxPos = new List<Vector3>();
        oldDepotPos = new List<Vector3>();
        newDepotPos = new List<Vector3>();
        // Initialize position lists
        robotInstances = new GameObject[robots];
        boxInstances = new GameObject[boxes];
        depotInstances = new GameObject[depot_x * depot_y];
        // Adjust floor size
        floor.transform.localScale = new Vector3((float)(width / 10) + 1.0f, 1, (float)(height / 10) + 1.0f);
        floor.transform.position = new Vector3((float)(width / 2 - 0.5f), 0, (float)(height / 2 - 0.5f));
        // Set timer to make a step immediately on start
        timer = updateTime;
        // Create instances of every agent
        depots = depot_x * depot_y;
        Debug.Log("Creating robots...");
        for (int r = 0; r < robots; r++)
        {
            robotInstances[r] = Instantiate(robotPrefab, Vector3.zero, Quaternion.identity);
            robotInstances[r].transform.Rotate(0f, 90f, 0f);
            Debug.Log("Created " + (r + 1) + " robots.");
        }
        Debug.Log("Creating boxes...");
        for (int b = 0; b < boxes; b++)
        {
            boxInstances[b] = Instantiate(boxPrefab, Vector3.zero, Quaternion.identity);
            Debug.Log("Created " + (b + 1) + " boxes");
        }
        Debug.Log("Creating depots...");
        for (int d = 0; d < depots; d++)
        {
            depotInstances[d] = Instantiate(depotPrefab, Vector3.zero, Quaternion.identity);
            Debug.Log("Created " + (d + 1) + " depots");
        }
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

        // If the simulation is not paused, move the agents smoothly using LERPs
        if (!pause)
        {
            // Move robots
            Debug.Log("Updating robots...");
            for (int r = 0; r < robots; r++)
            {
                Debug.Log("Updating robot " + r);
                Vector3 lerp = Vector3.Lerp(oldRobotPos[r], newRobotPos[r], dt);
                robotInstances[r].transform.localPosition = lerp;
                Vector3 facingDir = oldRobotPos[r] - newRobotPos[r];
                robotInstances[r].transform.localRotation = Quaternion.LookRotation(facingDir);
                robotInstances[r].transform.Rotate(-90f, 0f, 180f);
            }
            // Move boxes
            Debug.Log("Updating boxes...");
            for (int b = 0; b < boxes; b++)
            {
                Debug.Log("Updating box " + b);
                Vector3 lerp = Vector3.Lerp(oldBoxPos[b], newBoxPos[b], dt);
                boxInstances[b].transform.localPosition = lerp;
                Vector3 facingDir = oldBoxPos[b] - newBoxPos[b];
                boxInstances[b].transform.localRotation = Quaternion.LookRotation(facingDir);
            }
            Debug.Log("Updating depots...");
            for (int d = 0; d < depots; d++)
            {
                Debug.Log("Updating depot " + d);
                Vector3 lerp = Vector3.Lerp(oldDepotPos[d], newDepotPos[d], dt);
                depotInstances[d].transform.localPosition = lerp;
                Vector3 facingDir = oldDepotPos[d] - newDepotPos[d];
                depotInstances[d].transform.localRotation = Quaternion.LookRotation(facingDir);
            }
            timer += Time.deltaTime;
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
            StartCoroutine(GetDepotData());
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
        form.AddField("max_steps", max_steps.ToString());
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
            Debug.Log("Post completed. Getting agents' positions.");
            StartCoroutine(GetRobotData());
            StartCoroutine(GetDepotData());
            StartCoroutine(GetBoxData());
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
            Debug.Log(www.error);
        }
        else
        {
            robotData = JsonUtility.FromJson<PathData>(www.downloadHandler.text);
            Debug.Log("Got robot position list with " + robotData.positions.Count + " elements");
            // Add and clear out any previous path data
            oldRobotPos = new List<Vector3>(newRobotPos);
            newRobotPos.Clear();
            // Add next positions
            Debug.Log("Adding robot positions.");
            foreach (Vector3 pos in robotData.positions)
            {
                newRobotPos.Add(new Vector3(pos.x + 0.5f, pos.y, pos.z + 0.5f));
            }
            Debug.Log("Finished adding robot positions.");
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
            Debug.Log("Got box position list with " + boxData.positions.Count + " elements");
            // Clear out any previous path data
            oldBoxPos = new List<Vector3>(newBoxPos);
            newBoxPos.Clear();
            // Add next positions
            Debug.Log("Adding box positions.");
            foreach (Vector3 pos in boxData.positions)
            {
                newBoxPos.Add(new Vector3(pos.x + 0.5f, pos.y, pos.z + 0.5f));
            }
            // Resume simulation
            Debug.Log("Finished adding box positions.");
            pause = false;
        }
    }

    // Update depots' positions through the given JSON data
    IEnumerator GetDepotData()
    {
        // Attempt to get the depots' positions
        UnityWebRequest www = UnityWebRequest.Get(serverURL + depotEndpoint);
        yield return www.SendWebRequest();
        // If attempt is successful, set the depots in their new positions
        if (www.result != UnityWebRequest.Result.Success)
        {
            Debug.LogFormat(www.error);
        }
        else
        {
            depotData = JsonUtility.FromJson<PathData>(www.downloadHandler.text);
            Debug.Log("Got depot position list with " + depotData.positions.Count + " elements");
            // Clear out any previous path data
            oldDepotPos = new List<Vector3>(newDepotPos);
            newDepotPos.Clear();
            // Add next positions
            Debug.Log("Adding depot positions.");
            foreach (Vector3 pos in depotData.positions)
            {
                newDepotPos.Add(new Vector3(pos.x + 0.5f, pos.y, pos.z + 0.5f));
            }
            Debug.Log("Finished adding depot positions.");
            pause = false;
        }
    }
}
