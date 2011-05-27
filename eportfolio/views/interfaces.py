from zope.interface import Interface, Attribute

class IMenu(Interface):
    
    entries = Attribute("Menu entries")
    
class IGlobalMenu(IMenu):
    """
    Global (i.e., context independent) menu.
    """
    
class ILocalMenu(IMenu):
    """
    Local (i.e., context dependent) menu.
    """
    
class IGlobalMenuEntry(Interface):
    """
    An entry in the global menu.
    """
    
class ILocalMenuEntry(Interface):
    """
    An entry in the local menu.
    """