import ldap
import ldap.modlist
import ldif
from io import StringIO
from ldap.cidict import cidict

class LibLDAP:
    base_dn="ou=People,dc=gonzalonazareno,dc=org"
    con=""
    isbind=False

    
    def __init__(self,username="",password=""):
        self.conectar(username,password)        
 
    def conectar(self,username,password):
        try:
            #self.con=ldap.initialize("ldap://papion-ldap.gonzalonazareno.org")
            self.con=ldap.initialize("ldap://192.168.202.5")
            self.con.protocol_version = ldap.VERSION3
            if username!="":
                username="uid=%s,ou=People,dc=gonzalonazareno,dc=org" % username
                respuesta=self.con.simple_bind_s(username,password)[0]
            else:
                respuesta=self.con.simple_bind_s()[0]
            if respuesta==97:
                self.isbind=True
            else:
                self.isbind=False
        except ldap.LDAPError as e:
            self.isbind=False

    def buscar(self,filter):
        result=self.con.search_s(self.base_dn, ldap.SCOPE_SUBTREE, filter)
        return get_search_results(result)
    def add(self,uid,attrs):
        self.con.add_s("uid="+uid+","+self.base_dn,self.addldif(attrs))
        self.con.unbind_s()
    def addldif(self,attrs):
        return ldap.modlist.addModlist(attrs)
    def delete(self,uid):
        self.con.delete_s("uid="+uid+","+self.base_dn)
        self.con.unbind_s()
    def modify(self,uid,new,old):
        self.con.modify_s("uid="+uid+","+self.base_dn,self.modldif(old,new))
        self.con.unbind_s()
    def modldif(self,old,new):
        return ldap.modlist.modifyModlist(old,new)




        
def get_search_results(results):
    """Given a set of results, return a list of LDAPSearchResult
    objects.
    """
    res = []

    if type(results) == tuple and len(results) == 2 :
        (code, arr) = results
    elif type(results) == list:
        arr = results

    if len(results) == 0:
        return res

    for item in arr:
        res.append( LDAPSearchResult(item) )

    return res

class LDAPSearchResult:
    """A class to model LDAP results.
    """

    dn = 'dc=gonzalonazareno,dc=org'

    def __init__(self, entry_tuple):
        """Create a new LDAPSearchResult object."""
        (dn, attrs) = entry_tuple
        if dn:
            self.dn = dn
        else:
            return

        self.attrs = cidict(attrs)

    def get_attributes(self):
        """Get a dictionary of all attributes.
        get_attributes()->{'name1':['value1','value2',...], 
				'name2: [value1...]}
        """
        return self.attrs

    def set_attributes(self, attr_dict):
        """Set the list of attributes for this record.

        The format of the dictionary should be string key, list of
        string alues. e.g. {'cn': ['M Butcher','Matt Butcher']}

        set_attributes(attr_dictionary)
        """

        self.attrs = cidict(attr_dict)

    def has_attribute(self, attr_name):
        """Returns true if there is an attribute by this name in the
        record.

        has_attribute(string attr_name)->boolean
        """
        return self.attrs.has_key( attr_name )

    def get_attr_values(self, key):
        """Get a list of attribute values.
        get_attr_values(string key)->['value1','value2']
        """
        return self.attrs[key]

    def get_attr_names(self):
        """Get a list of attribute names.
        get_attr_names()->['name1','name2',...]
        """
        return self.attrs.keys()

    def get_dn(self):
        """Get the DN string for the record.
        get_dn()->string dn
        """
        return self.dn

                         
    def pretty_print(self):
        """Create a nice string representation of this object.

        pretty_print()->string
        """
        str = "DN: " + self.dn + "n"
        for a, v_list in self.attrs.iteritems():
            str = str + "Name: " + a + "n"
            for v in v_list:
                str = str + "  Value: " + v + "n"
        str = str + "========"
        return str

    def to_ldif(self):
        """Get an LDIF representation of this record.

        to_ldif()->string
        """
        out = StringIO()
        ldif_out = ldif.LDIFWriter(out)
        ldif_out.unparse(self.dn, self.attrs)
        return out.getvalue()

