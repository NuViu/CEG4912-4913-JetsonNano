
import vlc
import time

def nav_mode_e():
	p = vlc.MediaPlayer("/home/nuviu/Desktop/NuViu_voice_prompts/nav-mode-e.mp3")
	p.play()
	time.sleep(5)
	p.stop()


def nav_mode_d():
	p = vlc.MediaPlayer("/home/nuviu/Desktop/NuViu_voice_prompts/nav-mode-d.mp3")
	p.play()
	time.sleep(5)
	p.stop()


def street_mode_e():
	p = vlc.MediaPlayer("/home/nuviu/Desktop/NuViu_voice_prompts/street-mode-e.mp3")
	p.play()
	time.sleep(5)
	p.stop()


def street_mode_d():
	p = vlc.MediaPlayer("/home/nuviu/Desktop/NuViu_voice_prompts/street-mode-d.mp3")
	p.play()
	time.sleep(5)
	p.stop()
