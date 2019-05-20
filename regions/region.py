from province import BaseProvince

class BaseRegion(object):
    """
    Represents an italian region (Marche, Sicilia...)
    """
    name = None
    _provinces = list()

    def __init__(self, name=None):
        """
        :param name: The region's name
        :raises TypeError: The param name is not specified
        """
        if self.name is None:
            if name is None: 
                raise TypeError('name of the region not set')
            else:
                self.name = name

    def __str__(self):
        return '<Region %s - %d provinces>' % (self.name, len(self.provinces))

    @property
    def provinces(self): return self.provinces

    def add_province(self, province):
        """
        :raises TypeError: `province` is not subclass of `~province.BaseProvince`
        :raises ValueError: The province is already present
        """
        if issubclass(province, BaseProvince):
            if province in self.provinces:
                raise ValueError('province %s is already present' % province)
            else:
                self.provinces.append(province)
        else:
            raise TypeError('province must subclass BaseProvice')


