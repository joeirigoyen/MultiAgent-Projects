using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class SoundManager : MonoBehaviour
{
    [SerializeField] AudioSource source;
    [SerializeField] List<AudioClip> horns;
    [SerializeField] List<AudioClip> motorSounds;
    [SerializeField] List<AudioClip> animals;
    [SerializeField] List<AudioClip> musicBits;
    [SerializeField] float minSoundTime, maxSoundTime;
    [SerializeField] DayLightSwitcher switcher;
    private List<List<AudioClip>> sounds = new List<List<AudioClip>>();
    private AudioClip sound;
    private float timer = 0;
    private bool isDayTime = false;

    // Start
    void Start() {
        sounds.Add(horns);
        sounds.Add(motorSounds);
        sounds.Add(animals);
        sounds.Add(musicBits);
        isDayTime = switcher.isDaytime;
    }

    // Update is called once per frame
    void Update()
    {
        isDayTime = switcher.isDaytime;
        if (timer >= Random.Range(minSoundTime, maxSoundTime)) {
            int listSel = Random.Range(0, sounds.Count);
            sound = sounds[listSel][Random.Range(0, sounds[listSel].Count)];
            if (!isDayTime) {
                if (listSel != 2) {
                    source.PlayOneShot(sound);
                }
            } else {
                source.PlayOneShot(sound);
            }
            timer = 0;
        }
        timer += Time.deltaTime;
    }
}
