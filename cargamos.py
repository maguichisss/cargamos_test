import uuid
from datetime import datetime, timedelta

SECONDS_TO_EXPIRE = 120

def singleton(class_):
    instances = {}
    def getinstance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]
    return getinstance

@singleton
class ClassCounter():
    instances = {}
    def add_sku(self, SKU):
        self.instances[SKU] = True
    def get_total(self):
        return len(self.instances)

class Package():
    def __init__(self, *args, **kwargs):
        self.SKU = kwargs.get("sku") or uuid.uuid4()
        self.size = kwargs.get("size") or 1
        self.__created_at = kwargs.get("created_at") or datetime.now()
        s_2_x = int(kwargs.get("seconds") or SECONDS_TO_EXPIRE)
        expired_at = self.__created_at + timedelta(seconds=s_2_x)
        self.expired_at = kwargs.get("expired_at") or expired_at
        self.counter = ClassCounter()
        self.counter.add_sku(self.SKU)

    @property
    def total_instances(self):
        return self.counter.get_total()
    @property
    def get_created_at(self):
        return self.__created_at

    def time_to_expire(self, seconds=True):
        """
        """
        t_2_expire = self.expired_at - datetime.now()
        return t_2_expire.total_seconds() if seconds else t_2_expire

    def has_expired(self):
        return self.time_to_expire() <= 0

    def time_since_created(self, seconds=True):
        """
        """
        t_created = datetime.now() - self.__created_at
        return t_created.total_seconds() if seconds else t_created

class Address():
    def __init__(self,
        address_line_1,
        postal_code,
        locality,
        city,
        state,
        country,
        address_line_2="",
        notes="",
        *args, **kwargs
    ):
        self.address_line_1 = address_line_1
        self.postal_code = postal_code
        self.locality = locality
        self.city = city
        self.state = state
        self.country = country
        self.address_line_2 = address_line_2
        self.notes = notes

    def get_full_address(self):
        line1_2 = self.address_line_1+", "+self.address_line_2 if self.address_line_2 else self.address_line_1
        notes = " - "+self.notes if self.notes else ""
        address = f"{line1_2}, {self.locality}, {self.city}, {self.state}, {self.country}{notes}"
        return address

    def __str__(self):
        return self.get_full_address()

class Order(Package):
    def __init__(self, *args, **kwargs):
        self.delivered_at = None
        self.delivery_address = Address(*args, **kwargs)
        super().__init__(*args, **kwargs)

    def mark_as_delivered(self):
        if self.has_expired():
            raise Exception(f"La orden '{self.SKU}' ha expirado")

        self.delivered_at = datetime.now()

    @property
    def alive_time(self):
        return (self.expired_at - self.get_created_at).total_seconds()

    def __str__(self):
        s = f"{self.SKU},{self.delivered_at},{self.alive_time},{self.total_instances}"
        return s
