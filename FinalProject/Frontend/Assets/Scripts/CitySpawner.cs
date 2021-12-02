using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Networking;

[System.Serializable]
public class PathData {
    public List<Vector3> positions;
}

public class CitySpawner : MonoBehaviour
{

    // Initialize server and declare endpoints
    private string serverURL = "http://localhost:8585"; //"https://traffic-model.us-south.cf.appdomain.cloud"
    private string beginEndpoint = "/begin";
    private string carEndpoint = "/cars";
    private string carStateEndpoint = "/carStates";
    private string lightsPosEndpoint = "/lightsPositions";
    private string lightsStatesEndpoint = "/lightStates";
    private string stepEndpoint = "/step";
    private bool connected = false;
    // Initialize position and state list
    private PathData carData, carStateData, lightPosData, lightStateData;
    private List<GameObject> carInstances, lightInstances;
    private List<Vector3> oldCarPos, oldLightPos, carStates, newCarPos, newLightPos, lightStates;

    // Get car prefabs
    [SerializeField] List<GameObject> carPrefabs, lightPrefabs;
    [SerializeField] int initial_cars;
    [SerializeField] int maxSteps;
    [SerializeField] float updateTime, timer, dt;
    private int new_cars = 4;
    private int total_cars = 0;
    private int light_count = 28;
    private int step;
    private bool pause = true;

    // Function to create a certain number of GameObjects
    void CreateGameObject(int count, List<GameObject> prefabList, List<GameObject> instances, bool is_car) {
        for (int i = 0; i < count; i++) {
            GameObject inst = Instantiate<GameObject>(prefabList[Random.Range(0, prefabList.Count)]);
            instances.Add(inst); // Random.Range(0, prefabList.Count)
            if (is_car) {
                total_cars++;
                inst.transform.Rotate(0f, 0f, 180f);
            }
        }
        oldCarPos = ResizeList(newCarPos);
    }

    List<Vector3> ResizeList(List<Vector3> newList) {
        // Create a temporary list with the elements from last newPos list
        List<Vector3> tempCarPos = new List<Vector3>(total_cars);
        for (int j = 0; j < newList.Count; j++) {
            tempCarPos.Insert(j, newList[j]);
        }
        // Copy temporary list to old list
        return new List<Vector3>(tempCarPos);
    }

    void PrintListContent(List<Vector3> list) {
        string debug_str = "";
        foreach (Vector3 elem in list) {
            debug_str += elem.ToString() + " ";
        }
        Debug.Log(debug_str);
    }

    void PrintListContent(List<int> list) {
        string debug_str = "(";
        foreach (int elem in list) {
            debug_str += elem + " ";
        }
        debug_str += ")";
        Debug.Log(debug_str);
    }

    void PrintListContent(List<bool> list) {
        string debug_str = "(";
        foreach (bool elem in list) {
            debug_str += elem + " ";
        }
        debug_str += ")";
        Debug.Log(debug_str);
    }

    // Start is called before the first frame update
    void Start()
    {
        // Initialize lists and timer
        carData = new PathData();
        carStateData = new PathData();
        lightPosData = new PathData();
        lightStateData = new PathData();
        oldCarPos = new List<Vector3>();
        newCarPos = new List<Vector3>();
        carStates = new List<Vector3>();
        oldLightPos = new List<Vector3>();
        newLightPos = new List<Vector3>();
        lightStates = new List<Vector3>();
        carInstances = new List<GameObject>();
        lightInstances = new List<GameObject>();
        timer = updateTime;
        // Create initial cars
        CreateGameObject(initial_cars, carPrefabs, carInstances, true);
        // Create lights
        CreateGameObject(light_count, lightPrefabs, lightInstances, false);
        // Send info through JSON
        StartCoroutine(SendConfig());
    }

    // Update is called once per frame
    void Update()
    {
        if (connected) {
            // Get variable t from timer and time to update
            float t = timer / updateTime;
            // Number of steps to be taken before an agent gets from one point to another
            dt = 1.0f - (timer / updateTime);
            // If timer's value is higher than the time to update, pause the simulation and make a new step
            if (timer >= updateTime)
            {
                step++;
                timer = 0;
                pause = true;
                StartCoroutine(Step());
            }

            // If the simulation is not paused, move the agents smoothly using LERPs
            if (!pause)
            {
                for (int c = 0; c < total_cars; c++)
                {
                    Vector3 lerp = Vector3.Lerp(newCarPos[c], oldCarPos[c], dt);
                    carInstances[c].transform.localPosition = lerp;
                    if (oldCarPos[c] != newCarPos[c]) {
                        Vector3 facingDir = oldCarPos[c] - newCarPos[c];
                        carInstances[c].transform.localRotation = Quaternion.LookRotation(facingDir);
                        carInstances[c].transform.Rotate(0f, 180f, 0f);
                    }
                    // Get info from car states list
                    float temp = carStates[c].x;
                    // Make cars disappear if they are already in their destination
                    if ((int)temp == 1) {
                        //carInstances[c].transform.localScale = new Vector3(10f, 10f, 10f);
                        carInstances[c].transform.GetChild(0).gameObject.SetActive(false);
                    }
                }

                for (int i = 0; i < light_count; i++)
                {   
                    Vector3 lerp = Vector3.Lerp(oldLightPos[i], newLightPos[i], dt);
                    lightInstances[i].transform.localPosition = lerp;
                    float temp = lightStates[i].x;
                    if ((int)temp == 0) {
                        lightInstances[i].transform.GetChild(0).GetComponent<LightCycler>().state = false;
                    } else {
                        lightInstances[i].transform.GetChild(0).GetComponent<LightCycler>().state = true;
                    }
                }
                timer += Time.deltaTime;
            } else {
                Debug.Log("Step: " + step);
                if (step > 2) {
                    // Check if position list has more agents than the current agents in the simulation
                    if (carData.positions.Count > total_cars) {
                        // Instantiate 4 new cars
                        CreateGameObject(new_cars, carPrefabs, carInstances, true);
                    }
                }
            }
        }
    }

    // Send initial configuration to server through JSON
    IEnumerator SendConfig()
    {
        // Initialize form
        WWWForm form = new WWWForm();
        // Add fields to form
        form.AddField("cars", initial_cars.ToString());
        form.AddField("max_steps", maxSteps.ToString());
        // Make post request
        UnityWebRequest www = UnityWebRequest.Post(serverURL + beginEndpoint, form);
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
            connected = true;
            StartCoroutine(GetCarData());
            StartCoroutine(GetCarState());
            StartCoroutine(GetLightPathData());
            StartCoroutine(GetLightState());
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
            StartCoroutine(GetCarData());
            StartCoroutine(GetCarState());
            StartCoroutine(GetLightPathData());
            StartCoroutine(GetLightState());
        }
    }

    // Update robots' positions through the given JSON data
    IEnumerator GetCarData()
    {
        // Attempt to get the robots' positions
        UnityWebRequest www = UnityWebRequest.Get(serverURL + carEndpoint);
        yield return www.SendWebRequest();
        // If attempt is successful, set the robots in their new positions
        if (www.result != UnityWebRequest.Result.Success)
        {
            Debug.Log(www.error);
        }
        else
        {
            carData = JsonUtility.FromJson<PathData>(www.downloadHandler.text);
            oldCarPos = ResizeList(newCarPos);
            newCarPos.Clear();
            // Add next positions
            foreach (Vector3 pos in carData.positions)
            {
                newCarPos.Add(new Vector3(pos.x, pos.y, pos.z));
            }
            pause = false;
        }
    }

    IEnumerator GetCarState()
    {
        // Attempt to get the robots' positions
        UnityWebRequest www = UnityWebRequest.Get(serverURL + carStateEndpoint);
        yield return www.SendWebRequest();
        // If attempt is successful, set the robots in their new positions
        if (www.result != UnityWebRequest.Result.Success)
        {
            Debug.Log(www.error);
        }
        else
        {
            carStateData = JsonUtility.FromJson<PathData>(www.downloadHandler.text);
            carStates.Clear();
            // Add next positions
            foreach (Vector3 pos in carStateData.positions)
            {
                carStates.Add(new Vector3(pos.x, 0, 0));
            }
            pause = false;
        }
    }

    IEnumerator GetLightPathData()
    {
        // Attempt to get the robots' positions
        UnityWebRequest www = UnityWebRequest.Get(serverURL + lightsPosEndpoint);
        yield return www.SendWebRequest();
        // If attempt is successful, set the robots in their new positions
        if (www.result != UnityWebRequest.Result.Success)
        {
            Debug.Log(www.error);
        }
        else
        {
            lightPosData = JsonUtility.FromJson<PathData>(www.downloadHandler.text);
            // Add and clear out any previous path data
            oldLightPos = new List<Vector3>(newLightPos);
            newLightPos.Clear();
            // Add next positions
            foreach (Vector3 pos in lightPosData.positions)
            {
                newLightPos.Add(new Vector3(pos.x, pos.y, pos.z));
            }
            
            pause = false;
        }
    }

    IEnumerator GetLightState()
    {
        // Attempt to get the robots' positions
        UnityWebRequest www = UnityWebRequest.Get(serverURL + lightsStatesEndpoint);
        yield return www.SendWebRequest();
        // If attempt is successful, set the robots in their new positions
        if (www.result != UnityWebRequest.Result.Success)
        {
            Debug.Log(www.error);
        }
        else
        {
            lightStateData = JsonUtility.FromJson<PathData>(www.downloadHandler.text);
            // Add and clear out any previous path data
            lightStates.Clear();
            // Add next positions
            foreach (Vector3 pos in lightStateData.positions)
            {
                lightStates.Add(new Vector3(pos.x, 0, 0));
            }
            pause = false;
        }
    }
}
