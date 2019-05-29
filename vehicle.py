import logging
import math
import random


def correct_fuel_amount(capacity, litres, tanked=0):
    new_tanked = tanked + litres
    if new_tanked > capacity:
        return False
    return True


def roundup(number, digits=0):
    n = 10 ** -digits
    return round(math.ceil(number / n) * n, digits)


class Car:
    """
    Class Car

    Attributes:
    ----------
        brand (str, optional): Brand of a Car object. Defaults to None

        tank_capacity (float, optional): Capacity of the tank of a Car object.
            Defaults to None.

        tank_fuel (float, optional): The amount of fuel the tank was filled with. Defaults to 0.0

    """

    def __init__(self, brand=None, tank_capacity=None, tanked_fuel=0):
        logging.basicConfig(level=logging.INFO)
        self.percent_filled = 0
        self.brand = brand
        if not tank_capacity and tanked_fuel:
            raise Exception('Tanked fuel requires tank capacity')
        if tank_capacity:
            if tank_capacity > 0:
                self.tank_capacity = tank_capacity
                if tanked_fuel >= 0:
                    self.tanked_fuel = tanked_fuel
                else:
                    raise Exception('Tanked fuel must be > 0')
                if not correct_fuel_amount(self.tank_capacity, self.tanked_fuel):
                    raise Exception('Not sufficient tank capacity')
                else:
                    self.tanked_fuel = tanked_fuel
                    self.percent_filled = (self.tanked_fuel / self.tank_capacity) * 100
        else:
            self.tank_capacity = tank_capacity
        logging.info(f'New car of brand {self.brand}, with tank full in {roundup(self.percent_filled, digits=1)}%')

    def __str__(self):
        return f"Car brand: {self.brand},\ntank capacity {self.tank_capacity},\ntanked fuel: {self.tanked_fuel}"

    def __repr__(self):
        return f"<Car at {hex(id(self))} of brand {self.brand}, with tank full in {roundup(self.percent_filled, digits=1)}%>"

    def fill_tank(self, limit=None, litres=None):
        """
        Method fill_tank() adds fuel to the tank of a Car object.

        Note:
        -----
        If both of the parameters are None, the tank will be filled up to tank capacity.

        Args:
        ----------

            limit (float >= 0, optional): fills tank with fuel up to the given limit in range (0, 1)
                which means percentage of the filled tankpercent of a tank capacity that should be filled with fuel.
                Defaults to None.

            litres (float >= 0, optional): fills tank with given litres of fuel. If litres exceed tank capacity,
                exception will be raised. Defaults to None.


        Returns:
        -------

            float: The number of litres the tank was filled with.
            0.0: If object attribute "tank_capacity" doesn't exist.
            None: If incorrect parameters were given

        """
        if self.tank_capacity:
            if limit == None:
                limit = 0.0
            elif limit == 0:
                return 0
            if litres == None:
                litres = 0.0
            elif litres == 0:
                return 0.0
            if isinstance(limit, float) and isinstance(litres, float):
                try:
                    if limit < 0 or litres < 0:
                        raise ValueError("Parameters must be > 0")
                    if limit and litres:
                        raise Exception("Limit and litres not allowed together")
                    if limit > 1:
                        raise Exception("Limit must be a float in range (0,1)")
                    if litres and not correct_fuel_amount(self.tank_capacity, litres, self.tanked_fuel):
                        raise ValueError("Not sufficient tank capacity")
                except (Exception, ValueError) as e:
                    return e
                else:
                    if not limit and not litres:  # brak argumentów - bak na ful
                        fuel_added = self.tank_capacity - self.tanked_fuel
                        self.tanked_fuel += fuel_added
                    # if limit <= 1:
                    if limit:
                        fuel_added = self.tank_capacity * limit - self.tanked_fuel
                        if fuel_added > 0:
                            self.tanked_fuel += fuel_added
                        else:
                            fuel_added = 0
                    if litres:
                        fuel_added = litres
                        self.tanked_fuel += fuel_added
                    return fuel_added
            else:
                raise Exception("Limit and litres must be float")
        else:
            print("Tank capacity not known. Tank couldn't be filled")
            return 0.0

    @classmethod
    def get_carpool(cls, number_of_cars: int):
        brands = ['Abarth', 'Acura', 'Aixam', 'Alfa Romeo', 'Alpine', 'Aro', 'Asia', 'Aston', 'Martin', 'Audi',
                  'Austin', 'Autobianchi', 'Bentley', 'BMW', 'Brilliance', 'Bugatti', 'Buick', 'Cadillac', 'Casalini',
                  'Chatenet', 'Chevrolet', 'Chrysler', 'Citroën', 'Cupra', 'Dacia', 'Daewoo', 'Daihatsu', 'Lorean',
                  'DKW', 'Dodge', 'DS', 'Automobiles', 'Eagle', 'Ferrari', 'Fiat', 'Ford', 'Gaz', 'GMC', 'Gonow',
                  'GWM', 'Honda', 'Hummer', 'Hyundai', 'Infiniti', 'Isuzu', 'Iveco', 'Jaguar', 'Jeep', 'Kia', 'Lada',
                  'Lamborghini', 'Lancia', 'Land', 'Rover', 'Lexus', 'Ligier', 'Lincoln', 'Lotus', 'LTI', 'Mahindra',
                  'Maserati', 'Maybach', 'Mazda', 'McLaren', 'Mercedes-Benz', 'Mercury', 'MG', 'Microcar', 'Mini',
                  'Mitsubishi', 'Morgan', 'Moskwicz', 'Nissan', 'NSU', 'Nysa', 'Oldsmobile', 'Opel', 'Peugeot',
                  'Piaggio', 'Plymouth', 'Polonez', 'Pontiac', 'Porsche', 'RAM', 'Renault', 'Rolls-Royce', 'Rover',
                  'Saab', 'Saturn', 'Scion', 'Seat', 'Škoda', 'Smart', 'SsangYong', 'Subaru', 'Suzuki', 'Syrena',
                  'Tarpan', 'Tata', 'Tatra', 'Tesla', 'Toyota', 'Trabant', 'Triumph', 'TVR', 'Uaz', 'Vauxhall',
                  'Volkswagen', 'Volvo', 'Warszawa', 'Wartburg', 'Wołga', 'Yugo', 'Zaporożec', 'Żuk']

        set_of_cars = set()
        while len(set_of_cars) < number_of_cars:
            tank_capacity = random.randrange(20, 60, 5)
            tanked_fuel = random.randrange(0, tank_capacity, 5)
            brand = random.choice(brands)
            brands.remove(brand)
            car = Car(brand=brand, tank_capacity=tank_capacity, tanked_fuel=tanked_fuel)
            set_of_cars.add(car)
        return set_of_cars


class DieselCar(Car):

    def __str__(self):
        return f"DieselCar brand: {self.brand},\ntank capacity {self.tank_capacity},\ntanked fuel: {self.tanked_fuel}"

    def fill_tank(self):
        try:
            raise EnvironmentalError("Diesel fuel not available due to enviromental reasons")
        except EnvironmentalError as e:
            print(e)


class EnvironmentalError(Exception):
    pass


car = Car(brand='brand_name', tank_capacity=100, tanked_fuel=30)
print(car.fill_tank(limit = 0.1))

# <- zwraca -20, powinno zwrócić 0, gdyż żadne paliwo nie powinno byćdotankowane.

car = Car(brand='brand_name', tank_capacity=100, tanked_fuel=30)
print(car.fill_tank(litres = 80.0))

# <- powinno nastąpić rzucenie wyjątku, zwracane jest None

car = Car(brand='brand_name', tank_capacity=100, tanked_fuel=30)
print(car.fill_tank(litres = 10.0, limit = 0.5))

# <- zwraca None, powinno nastąpić wyrzucenie wyjątku

car = Car(brand='brand_name')
print(car.fill_tank(litres = 10.0, limit = 0.5))

car = Car(brand='brand_name', tank_capacity=100, tanked_fuel=30)
print(car.fill_tank(litres = 20.0))

