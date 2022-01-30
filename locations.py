
class Locations():
    """Clase que simula la ubicacion en un cubo

    Ejemlo:
    En un Locations(3, 4, 7), si ejecutamos locations_a.add("hola mundo", 1,3,7), este
    elemento estará en la posición 79 de locations_a.element(). De igual manera, si ejecutamos
    locations_a.add("hola mundo", 2,2,2), este elemento estará en la posición 17 de
    locations_a.element()
    """
    def __init__(self, a, b, c):
        """Constructor of the class

        Args:
          a: Integer for X axis
          b: Integer for y axis
          x: Integer for z axis
        """
        self.__x = a
        self.__y = b
        self.__z = c
        # init list
        self.l = [i for i in range(1,(a*b*c)+1)]

    def add(self, val, a, b, c):
        """Change the value for the given coordenades
        Args:
          a: Integer value for X axis
          b: Integer value for y axis
          c: Integer value for z axis

        Returns:
          None
        """
        n = self.__get_location_index(a, b, c)
        self.l[n] = val

    def element(self, a, b, c):
        """Returns the value for the given coordenades
        Args:
          a: Integer value for X axis
          b: Integer value for y axis
          c: Integer value for z axis

        Returns:
          Value for the given coordenades
        """
        n = self.__get_location_index(a, b, c)
        return self.l[n]

    def __get_location_index(self, a, b, c):
        """Returns the index for the given coordenades

        Args:
          a: Integer value for X axis
          b: Integer value for y axis
          c: Integer value for z axis

        Returns:
          Integer for the given coordenades

        Raises:
          Exception: If no index is found.
        """
        index = 0
        for i in range(1,self.__z+1):
            for j in range(1,self.__y+1):
                for k in range(1,self.__x+1):
                    if c == i and b == j and a == k:
                        return index
                    index+=1
        raise Exception("Location not found")

    def list_all(self):
        """Returns the complete list"""
        return self.l

    def __get_location_fail(self, a, b, c, set_val=""):
        # TODO: delete
        # sclices create a new list, so is not useful
        x = self.__x
        y = self.__y
        z = self.__z
        for i in range(1,z+1):
            for j in range(1,y+1):
                if c == i and b == j:
                    if set_val:
                        self.l[x*y*(i-1):x*y*i][x*(j-1):x*j][a-1] = set_val
                        print(self.l[x*y*(i-1):x*y*i][x*(j-1):x*j][a-1])
                    else:
                        return self.l[x*y*(i-1):x*y*i][x*(j-1):x*j][a-1:a]
