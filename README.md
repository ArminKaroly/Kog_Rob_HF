# Kognitív Robotika Házi feladat
### Felszolgáló robot tájékozódása markerek trackelésével
<p align="center">
    <img src="https://github.com/ArminKaroly/Kog_Rob_HF/assets/62290156/632631ce-033f-495b-8b4f-ee7d77f67101">
<p>

## Tartalom
1. [Környezet megalkotása](#elsofejezet)
2. [Robot modellezése](#masodikfejezet)
3. [Markerek](#harmadikfejezet)
4. [Trackelés működése](#negyedikfejezet)
5. [Telepítési útmutató](#otodikfejezet)
6. [Használt ROS csomagok](#hatodikfejezet)

mozgás, robot mi alapján megy asztalokhoz??


## Környezet megalkotása <a name="elsofejezet"></a>
A szimuláció környezetét Gazebo fizikai szimulációs környezet használatával építettük fel. A felszolgáló robot egy szimulált kávézóban viszi ki a vendégekhez a rendelésüket. Az "L" alakú alapterületű helységben ezért 8 db asztal is elhelyezésre került, amelyek között előre kijelölt útvonalakon képes közlekedni a robot.

<p align="center">
    <img src="https://github.com/ArminKaroly/Kog_Rob_HF/assets/62290156/87faf514-7485-459b-ba44-3918a837b195">
<p>


## Robot modellezése <a name="masodikfejezet"></a>
A felszolgáló robot a ROS Turtlebot3 alapcsomagjával van szimulálva. Azonban mivel a felszolgáló robot fizikai méretei jelentősen nagyobbak kell legyenek mint a turtlebot burger vagy a waffle verziójánál, ezért egy saját fizikai modellt rendeltünk hozzá. 

<p align="center">
    <img src="https://github.com/ArminKaroly/Kog_Rob_HF/assets/62290156/852bdd51-29eb-4940-9fbd-8b405c9ffee3">
<p>


## Markerek <a name="harmadikfejezet"></a>
A robot tájékozódása elsősorban nem a lidar adatai, vagy odometria alapján történik, hanem a virtuális kávézó plafonján elhelyezkedő markerek kamerás követésével. A markerek egy dinamikusan skálázható rács rácspontjaiban találhatóak, jelen esetben egy 10x10-es rácsot használunk, de a helység L alaperülete miatt nem 100 hanem csak 84 db marker látható.

<p align="center">
    <img src="https://github.com/ArminKaroly/Kog_Rob_HF/assets/62290156/91ad0a31-c4ef-4381-abb4-2c9224be0390">
<p>

A használt jelölők ún. ArUco ( "Augmented Reality" and "University of Cordoba") markerek, amelyeket kifejezetten tracking és kiterjesztett valóság alkalmazásokra fejlesztettek ki. Egyetlen ArUco marker is elegendő hogy a kamera képe alapján visszaszámolható legyen a robot térbeli poz<ciója (x,y,z és orientációja (A,B,C) is egyaránt. Ehhez szükséges a kamera torzításaink kompenzálása a képeken, a markerek pontos helyzetének ismerete a térben egy referencia ponthoz képest, illetve a kamera és robot koordinátarendszere közötti transzformáció is adott kell legyen. Célszerűazonban , hogy ne csupán egyetlen, hanem több markert is lásson egy idejűleg a kamera, így korrigálhatóak a hibák és nől a helymeghatározás pontossága.

<p align="center">
    <img src="https://github.com/ArminKaroly/Kog_Rob_HF/assets/62290156/677a3b74-c12d-48dd-a2e9-cedb970d6d17">
<p>
    

## Trackelés működése <a name="negyedikfejezet"></a>
## Telepítési útmutató <a name="otodikfejezet"></a>

1.Hozz létre egy mappát a munkaterületednek (például legyen a neve "catkin_ws"):

     mkdir -p ~/catkin_ws/src

2.Lépj be a létrehozott munkaterület src könyvtárába:

    cd ~/catkin_ws/src

3.Klónozd le a Git projektet:

    git clone [https://github.com/felhasznalonev/projekt.git](https://github.com/ArminKaroly/Kog_Rob_HF/)

4.Lépj be a munkaterület főkönyvtárába és buildeld a csomagokat a catkin_make paranccsal:

    cd ~/catkin_ws/
    catkin_make

5.Add hozzá a használt ROS csomagokat forrásként az aktuális környezetedhez:

    source ~/catkin_ws/devel/setup.bash

6.Indítsd el a ROS Mastert a 'roscore' paranccsal

7.Indítsd el a szimulációt

    rosrun "valami"
    

## Használt ROS csomagok <a name="hatodikfejezet"></a>

