from zope.interface import Interface

class IApplication(Interface):
    """
    Interface for the root object (aka application).
    """
    
class IContainer(Interface):
    """
    Interface to mark container objects.
    """
    
class IMetaCompetences(Interface):
    """
    Container for meta competences.
    """
    
class IMetaCompetence(Interface):
    """
    A meta competence
    """
    
class IProjects(Interface):
    """
    Container for projects
    """
    
class IProject(Interface):
    """
    A project.
    """
    
class IObjectives(Interface):
    """
    Container for objectives
    """
    
class IObjective(Interface):
    """
    An objective.
    """
    
class ICompetences(Interface):
    """
    Container for competences.
    """
    
class ICompetence(Interface):
    """
    A competence.
    """
    
class IIndicatorSets(Interface):
    """
    Container for indicator sets.
    """
    
class IIndicatorSet(Interface):
    """
    An indicator set.
    """
    
class IIndicators(Interface):
    """
    Container for indicators.
    """
    
class IIndicator(Interface):
    """
    An indicator.
    """
    
class IUsers(Interface):
    """
    Container for users.
    """
    
class IUser(Interface):
    """
    A user.
    """

class IStudent(Interface):
    """
    A student.
    """
    
class IStudents(Interface):
    """
    Container for students.
    """
    
class ITeacher(Interface):
    """
    A teacher.
    """
    
class IJournal(Interface):
    """
    Student's journal.
    """
    
class IJournalEntry(Interface):
    """
    Journal entry.
    """
    
class IComments(Interface):
    """
    Container for comments.
    """ 
    
class IComment(Interface):
    """
    Comment entry.
    """   
    
class IMembers(Interface):
    """
    Container for project members.
    """
    
class IFiles(Interface):
    """
    Container for files.
    """
    
class IFile(Interface):
    """
    A file.
    """
    
class IPermissionProvider(Interface):
    """
    Adapter to register permissions for an object.
    """
    
    def acl():
        """
        Returns ACL for the adapted object.
        """  

class IMailService(Interface):

    def send(recipient, subject, body, attachments=[], sender=None):
        """
        Send email.
        """  