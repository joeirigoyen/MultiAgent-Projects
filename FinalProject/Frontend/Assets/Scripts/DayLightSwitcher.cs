using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class DayLightSwitcher : MonoBehaviour
{
    [SerializeField] Color dayColor;
    [SerializeField] Color nightColor;
    [SerializeField] float updateTime;
    [SerializeField] Transform dayTransform;
    [SerializeField] Transform nightTransform;
    public bool isDaytime;
    private Color currentColor;
    private int presses = 0;
    private float timer = 0;

    // Start
    void Start() {
        isDaytime = true;
        currentColor = nightColor;
    }

    // Update is called once per frame
    void Update()
    {
        transform.GetComponent<Light>().color = currentColor;
        if (Input.GetMouseButtonDown(0)) {
            timer = 0;
            presses++;
            Debug.Log("Key pressed " + presses + " times.");
        }
        if (presses % 2 == 0) {
            if (timer < updateTime) {
                isDaytime = true;
                Color lerped = Color.Lerp(dayColor, nightColor, 1.0f - timer / updateTime);
                Quaternion lerpedRot = Quaternion.Lerp(dayTransform.localRotation, nightTransform.localRotation, 1.0f - timer / updateTime);
                currentColor = lerped;
                transform.localRotation = lerpedRot;
                timer += Time.deltaTime;
            }
        } else {
            if (timer < updateTime) {
                isDaytime = false;
                Color lerped = Color.Lerp(nightColor, dayColor, 1.0f - timer / updateTime);
                Quaternion lerpedRot = Quaternion.Lerp(nightTransform.localRotation, dayTransform.localRotation, 1.0f - timer / updateTime);
                currentColor = lerped;
                transform.localRotation = lerpedRot;
                timer += Time.deltaTime;
            }
        }
    }



}
