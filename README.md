Python module

  What is it?
  -----------
  This module map_films_population.py create a world map using google geocoding api <br>
  and requests library. Mapped films released in user specified year and <br>
  also countries are colored by its population. Used databases: locations.list and world.json<br>
  This module creates html file with a such structure:<br>
  <head><br>
  <meta> </meta><br>
  ...<br>
  <script> </script><br>
  ...<br>
  <link> </link><br>
  </head><br>
  <body><br>
    <div> </div><br>
    <scripts> </scripts><br>
  </body><br>
  Notes
  --------
  File coordinates_1960year.txt includes list of coordinates and title <br>
  of the films which were directed in 1960. That was done to reduce program execution time <br>
  to easily check it. If you want to rewrite these coordinates by another year just uncomment <br>
  112 line.
