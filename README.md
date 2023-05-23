# Kognitív Robotika Házi feladat
### Felszolgáló robot pozíci korrigálása markerek trackelésével
![image](https://github.com/ArminKaroly/Kog_Rob_HF/assets/62290156/87faf514-7485-459b-ba44-3918a837b195)

## Tartalom
1. [Környezet megalkotása](#elsofejezet)
2. [Robot modellezése](#masodikfejezet)
3. [Markerek](#harmadikfejezet)
4. [Trackelés működése](#negyedikfejezet)
5. [Telepítési útmutató](#otodikfejezet)
6. [Használt ROS csomagok](#hatodikfejezet)

mozgás, robot mi alapján megy asztalokhoz

## Környezet megalkotása <a name="elsofejezet"></a>

## Robot modellezése <a name="masodikfejezet"></a>

## Markerek <a name="harmadikfejezet"></a>

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

