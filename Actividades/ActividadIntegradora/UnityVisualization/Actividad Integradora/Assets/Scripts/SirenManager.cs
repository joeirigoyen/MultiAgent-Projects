using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class SirenManager : MonoBehaviour
{
    // Get serializable objects
    [SerializeField] GameObject siren;
    [SerializeField] Color firstColor, secondColor;
    [SerializeField] float fadeTime;
    private float t;
    private bool red;
    // Start is called before the first frame update
    void Start()
    {
        t = 0.0f;
    }

    // Update is called once per frame
    void Update()
    {
        if (t <= 1)
        {
            t += Time.deltaTime / fadeTime;
            siren.GetComponent<Light>().color = Color.Lerp(firstColor, secondColor, t);
        }
        else
        {
            Color tempColor = firstColor;
            firstColor = secondColor;
            secondColor = tempColor;
            t = 0.0f;
        }
    }
}
