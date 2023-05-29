# Kognitív Robotika Házi feladat
### #6 Emberek vagy tárgyak trackelése - Felszolgáló robot tájékozódása ArUco markerek trackelésével

Projektfeladatunk során egy kávézóban működő felszolgáló robotot szimuláltunk le, amely a plafonra helyezett ArUco markerek kamerás trackelésével határozza meg a saját helyzetét.
A robot a kezdő pozícióbpól (pulttól) indulva egy előre meghatározott útvonalon képes bármelyik asztalhoz kivinni a rendelést, a felhasználó utasítása szerint.

<p align="center">
    <img src="https://github.com/ArminKaroly/Kog_Rob_HF/assets/62290156/632631ce-033f-495b-8b4f-ee7d77f67101">
<p>

## Tartalom
1. [Környezet megalkotása](#elsofejezet)
2. [Robot modellezése](#masodikfejezet)
3. [Markerek](#harmadikfejezet)
4. [Trackelés működése](#negyedikfejezet)
    1. [Kamera kép feldolgozása](#negypontegy)
    2. [Robot pozíció kiszámolása](#negypontketto)
5. [Robot irányítása](#otodikfejezet)
6. [Felhasználói felület](#hatodikfejezet)
7. [Telepítési útmutató](#hetedikfejezet)
8. [Használt ROS csomagok és Python könyvtárak](#nyolcadikfejezet)

mozgás, robot mi alapján megy asztalokhoz??


## Környezet megalkotása <a name="elsofejezet"></a>
A szimuláció környezetét Gazebo fizikai szimulációs környezet használatával építettük fel. A felszolgáló robot egy szimulált kávézóban viszi ki a vendégekhez a rendelésüket. Az "L" alakú 12x10m alapterületű helységben 8 db asztal is elhelyezésre került, amelyek között előre kijelölt útvonalakon képes közlekedni a robot.

<p align="center">
    <img src="https://github.com/ArminKaroly/Kog_Rob_HF/assets/62290156/87faf514-7485-459b-ba44-3918a837b195">
<p>


## Robot modellezése <a name="masodikfejezet"></a>
A felszolgáló robot a ROS Turtlebot3 alapcsomagjával van szimulálva. Azonban mivel a felszolgáló robot fizikai méretei jelentősen nagyobbak kell legyenek mint a turtlebot burger vagy a waffle verziójánál, ezért egy saját fizikai modellt rendeltünk hozzá, ehhez egyszerűen módosítottuk a fájlt amely a turtlebot fizikai leírását tartalmazta. A felszolgáló robot két hajtott és egy támasztó keréken gurul, kb. 1m magas és a tetején került elhelyezésre egy szállító tálca és a plafonra rögzített markereket figyelő kamera is.

<p align="center">
    <img src="https://github.com/ArminKaroly/Kog_Rob_HF/assets/62290156/852bdd51-29eb-4940-9fbd-8b405c9ffee3">
<p>


## Markerek <a name="harmadikfejezet"></a>
A robot tájékozódása elsősorban nem a lidar adatai, vagy odometria alapján történik, hanem a virtuális kávézó plafonján elhelyezkedő markerek kamerás követésével. A markerek egy dinamikusan skálázható rács rácspontjaiban találhatóak, jelen esetben egy 11x9-es 1m-es osztású rácsot használunk, de a helység L alaperülete miatt nem 99 hanem csak 85 db marker látható. 

<p align="center">
    <img src="https://github.com/ArminKaroly/Kog_Rob_HF/assets/62290156/91ad0a31-c4ef-4381-abb4-2c9224be0390">
<p>

A használt jelölők ún. ArUco ( "Augmented Reality" and "University of Cordoba") markerek, amelyeket kifejezetten tracking és kiterjesztett valóság alkalmazásokra fejlesztettek ki. Egyetlen ArUco marker is elegendő hogy a kamera képe alapján visszaszámolható legyen a robot térbeli poz<ciója (x,y,z és orientációja (A,B,C) is egyaránt. Ehhez szükséges a kamera torzításaink kompenzálása a képeken, a markerek pontos helyzetének ismerete a térben egy referencia ponthoz képest, illetve a kamera és robot koordinátarendszere közötti transzformáció is adott kell legyen. Célszerűazonban , hogy ne csupán egyetlen, hanem több markert is lásson egy idejűleg a kamera, így korrigálhatóak a hibák és nől a helymeghatározás pontosság. A robot legrosszabb esetben 2, maximálisan pedig 9 db markert lát és követ egyszerre.

<p align="center">
    <img src="https://github.com/ArminKaroly/Kog_Rob_HF/assets/62290156/677a3b74-c12d-48dd-a2e9-cedb970d6d17">
<p>
       
## Trackelés működése <a name="negyedikfejezet"></a>
A kamera képének feldolgozása az OpenCV könyvtár Aruco alkönyvtárának használatával történik. A feldolgozás és számolás egyaránt a saját készítésű "TODO.py" scriptben van megírva, ahol definiáltuk a "Locate_robot" osztályt.
    
 ### Kamera kép feldolgozása <a name="negypontegy"></a>
 A feldolgozási folyamat szempontjából az "image_callback" metódus az első lépés. A függvény kinyeri a megfelelő topicból a Gazebo kamera plugin által pusholt képet és szürkeárnyalatossá konvertálja. Az Aruco könyvtár függvényei ezután detektálják a képen a markerek sarokpontjait és azonosítóit. A kinyert információ alapján a másik aruco könyvtárba tartozó függvény a kódokoz rendelt koordinátarendszer és a kamera paramétereinek ismeretében minden markerre visszaadja a tengelyek menti koorindiátákat és az azok körüli szögelfordulást, amelyeket az "rvesc" és "tvecs" vektorok tartalmazzák.
  
<p align="center">
    <img src="https://github.com/ArminKaroly/Kog_Rob_HF/assets/62290156/9e147885-59f2-42ea-9d9e-a0ddf2bb16ff">
<p>
     
### Robot pozíció kiszámolása <a name="negypontketto"></a>
 A markerektől való távolságok és szöghelyzetek ismeretében kiszámolható a robot pozíciója a rögzített origójú térben, amelyet a "Calculate_robot_pos" függvény végez. Első lépésként azonban megfelelő formába kell alakítani a Rodrigez paraméterekként megkapott orientációt, ami tömör, általános de nehezen kezelhető struktúra. Ezért a "rodrigues_vec_to_rotation_mat" saját metódus segítségével könnyebben kezelhető forgatási mátrix formájába transzformáljuk.
   Ezt követően a kapott adatokból minden markerhez legenrálódik egy homogén transzformációs mátrix ami a robot koorinátarendszerében írja le az ArUco kód helyzetét. A markerek origóhoz képesti helyzete pedig ismert és ID alapján kikereshető egy .csv fájlból. A transzformációs mátrixok ismeretében így azok szorzataként előáll a global koordinátarendszer és a robot koordináta rendszer közötti transzformáció, annyiszor ahány markert látott a kamera. Természetesen a pontatlanságok miatt ezek nem azonosak, de átlagolásukkal elégséges, kb. 1 cm-es pontosságot adnak. Mivel a robot síkban moozog így az x,y körüli szögelfordulás és a z koordináta mindig azonosak, csak a többi változik.
    A kiszámolt x,y pozíciót és z körüli elfordulást végül egy topicba publish-eli az osztály metódusa. A script végén értelemszerűen példányosításra kerül az osztály a megfelelő argumentumokkal.
    
## Robot irányítása <a name="otodikfejezet"></a>
A felhasználó által kijelölt asztal alapján kerül meghatározásra a célpozíció koordinátája, a robot aktuális helyzete pedig mindig ismert a markerek trackelésének köszönhetően. A kezdő és célpont közötti útvonalat a "TODO.py" scrip TODO függvénye generálja le. A pályqa az egyszerűség kedvéért egyenesekből és 90°-os fordulásokból épül fel. Ezután a robot a "TODO velocity_control" irányításával mozog végig az útvonal szakaszain, amely az aktuális X,Y koordináták és Z körüli szögelfordulás alapján szabályozzák a hajtott kerekek sebesség vektorait attól függe, hogy egyenes mentén haladásra vagy forgásra van szükség. TODO
    
## Felhasználói felület <a name="hatodikfejezet"></a>
    Egy egyszerű terminal alapú felhasználói felületet is készítettünk, amely segítségével lehetséges a cél asztal kiválasztása. Illetve folyamatosan információt biztosít a robot aktuális állapotáról, minthogy szabad, vagy dolgozik, és pzíciójáról.
    TODO
    
## Telepítési útmutató <a name="hetedikfejezet"></a>

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

    roslaunch "valami" 
    
Ezzel a paranccsal minden a szimuláció futtatásához, a robot kezeléséhez szükséges program elindul, és a UI és információs terminálok is megnyílnak.
    

## Használt ROS csomagok és Python könyvtárak <a name="nyolcadikfejezet"></a>
* ROS csomagok:
    * aruco_ros http://wiki.ros.org/aruco_ros
    * gazebo_ros_pkgs http://wiki.ros.org/gazebo_ros_pkgs
    * cv_bridge http://wiki.ros.org/cv_bridge
    * sensors_msgs http://wiki.ros.org/sensor_msgs
    * std_msgs http://wiki.ros.org/std_msgs
    * rospy http://wiki.ros.org/rospy
    * urdf http://wiki.ros.org/urdf
    * geometry_msgs http://wiki.ros.org/geometry_msgs
* Python könyvtárak:
    * OpenCV https://pypi.org/project/opencv-python/
    * NumPy https://numpy.org/
    * SciPy https://scipy.org/

