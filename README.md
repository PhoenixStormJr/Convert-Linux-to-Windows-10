# convert Linux to Windows 10

Note: On GNOME you might have to move the Install Windows 10 Theme.desktop to your ACTUAL desktop to run it!!! But keep the rest of the files in your downloads!


This script will instantly convert your xfce desktop to a windows 10 like feel. (Now I'm trying to work on supporting other desktop environments!)

also IDK why it's saying its like 98% CSS, I wrote this in 100% bash, the language that Linux uses. Then again, this is my first project, it could be kali's windows 10 theme triggering it. IDK...

You will need to right click the datetime and change the font to **liberation sans size 9** however, if you want a near identical copy. I do not know the commands to do this automatically. (I think I found the commands to do it automatically and updated it!) Feel free to copy my project and add whatever you like to it, or make your own for KDE-plasma or GNOME.

Oh! I found a login screen copy!:

![Windows_10_Login_Screen](https://us1.discourse-cdn.com/spiceworks/optimized/4X/9/1/5/91576352dafff29c9de814e011e0232743d4e651_2_690x388.jpeg)

# CHANGE LOG:

I now made it grow the size of the disk to use all available disk space, 

AND I made it reduce the wait-until-online service wait time during boot!

# XFCE change:
![VirtualBox_Ubuntu_24_07_2023_18_43_44](https://github.com/PhoenixStormJr/xfce-to-windows-10-INCOMPLETE/assets/66498788/2bc6294a-0868-442b-a1e4-76ddbdb3b64d)
![VirtualBox_Ubuntu_24_07_2023_18_45_32](https://github.com/PhoenixStormJr/xfce-to-windows-10-INCOMPLETE/assets/66498788/19555d5b-c033-4241-92b4-df104c62e387)
![VirtualBox_Ubuntu_24_07_2023_18_44_32](https://github.com/PhoenixStormJr/xfce-to-windows-10-INCOMPLETE/assets/66498788/fa96f915-e7e1-4145-9764-68ea94de5a0c)


# GNOME change:
![Screenshot-gnome](https://github.com/user-attachments/assets/97c89831-d429-4cc9-946c-d3eea6ba6577)



# credits to:
https://github.com/B00merang-Artwork/Windows-10

B00merang-Artwork, 
Elbullazul Christian Medel, 
fauzie811 Fauzie, 
gitthubba, 

https://www.kali.org/get-kali/#kali-installer-images

Kali-Linux, no sources listed for icon theme. however, these people wrote the article.

https://www.kali.org/docs/introduction/kali-undercover/

Croluy , theGorkha.

Found some useful commands here:

https://github.com/SofianeHamlaoui/Go-undercover/blob/master/go-undercover.sh

SofianeHamlaoui Sofiane Hamlaoui, 
MS-Jahan Md. Sarwar Jahan Sabit

another one here:

https://askubuntu.com/questions/380550/xubuntu-how-to-set-the-wallpaper-using-the-command-line

scai

Also well... Windows-10 obviously...
mail icon is located in C:\Program Files\WindowsApps\microsoft.windowscommunicationsapps_16005.11629.20316.0_x64__8wekyb3d8bbwe\images\HxMail (followed by odd letters or whatnot. Its MANY logos.) however, you will need to right click, and add yourself to the security tab and stuff. Very complicated, not going into it.

windows media player icon is located in "C:\Program Files (x86)\Windows Media Player\wmplayer.exe" however you will need something like icon viewer in order to actually use this, and the convert the .exe to .ico and convert the .ico to .png

Photos icon is located in C:\Program Files\WindowsApps\Microsoft.Windows.Photos_2019.19071.12548.0_x64__8wekyb3d8bbwe\Assets\PhotosAppList.targetsize- (followed by the size of the image.) Again, you need to take ownership.

Groove Music Icon is in "C:\Program Files\WindowsApps\Microsoft.ZuneMusic_10.19071.19011.0_x64__8wekyb3d8bbwe\Assets\contrast-black\AppList.targetsize-" (again weird numbers)
