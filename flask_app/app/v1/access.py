from app.v1 import app , api , Resource , JWT , jwt_required , reqparse , request , current_identity , os , base64 , Fernet , hashes , PBKDF2HMAC , salt
from app.v1.security.auth import authenticate , identity
import paramiko
import base64
import logging
logging.basicConfig(level=logging.INFO)

jwt = JWT(app , authenticate , identity)

class Host:

    def __init__(self, **kwargs):
        self.name = kwargs.get('name')
        self.ip = kwargs.get('ip')

class Access:

    def __init__(self, host , **kwargs):

        self.method = kwargs.get('method')
        self.username = kwargs.get('username')
        self.password = kwargs.get('password')
        self.server = kwargs.get('server')
        self.host = host
        if self.server != self.host.name:
            raise Exception('Invalid Server Name: Server Name doesn\'t match the hostname')

    def ssh(self):
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            logging.info('SSH connection is started for the host {} for IP {}, trying to authenticate ... '.format(self.host.name , self.host.ip))
            client.connect(self.host.ip, username=self.username, password=self.password)
            return True
        except paramiko.ssh_exception.AuthenticationException:
            logging.info('Authentication Failed. Host {} was not authenticated with the given credentials'.format(self.host.ip))
        except paramiko.ssh_exception.SSHException:
            logging.info('SSH Connection: Authentication was successful but some Exception occurred while connecting to {}.'.format(self.host.ip))
        return False

class Ticket:

    def __init__(self , name, host , access):
        self.name =  name
        # **host unpacks the host dictionary and send to the __init__ object
        self.host = Host(**host)
        self.access = Access(self.host , **access)

    def verify(self):
        
        if self.access.method == 'ssh':
            return self.access.ssh()
        return False

class Access_flask(Resource):

    def post(self , name):

        if request.is_json:
            if request.json['kind'] != 'Ticket':
                return {'Message': 'Only Ticket rquest are served to this endpoint not {}'.format(request.json['kind'])}
            data = request.json

            host = data['spec']['host']
            access = data['spec']['access']
            name = data['metadata']['name']
            ticket = Ticket(name, host , access)
            if ticket.verify():
                return {'Message': 'Ticket with the name {} is successfully created'.format(ticket.name)}, 200
            else:
                return {'Mesage': 'Your Ticket is disapproved'} , 400
        else:
            return {'Message': 'Json request allowed only'} , 400

    # @staticmethod
    # def decrypt_text(text):

    #     password = current_identity.password.encode()
    #     kdf = PBKDF2HMAC(algorithm=hashes.SHA256() , length=32 , salt=salt , iterations=100000)
    #     key = base64.urlsafe_b64encode(kdf.derive(password))
    #     f = Fernet(key)
    #     return f.decrypt(text.encode()).decode()

    # @jwt_required()   
    # def post(self,name):
    #     """This function takes the GET req on /access API. 
    #     Used for accessing the VM/cloud over which the authentication will take place either to connect via SSH or deploy VMs. 

    #     Args:
    #         name ([string]): [kind of authentication. Allowed values are (ssh,aws,gcp,azure,k8s)]

    #     Returns:
    #         [dictionary]: [Will return successful if the authentication works fine.]
    #     """
    #     if request.is_json:
    #         data = request.get_json()
    #     else:
    #         return {'Message': 'Request Body type is not json'},400
    #     decrypted_text = Access_flask.decrypt_text(data['key'])
    #     print(decrypted_text)
    #     return decrypted_text,200

class SecureText(Resource):

    @staticmethod
    def encrypt_text(text):
        password = current_identity.password.encode()
        kdf = PBKDF2HMAC(algorithm=hashes.SHA256() , length=32 , salt=salt , iterations=100000)
        key = base64.urlsafe_b64encode(kdf.derive(password))
        f = Fernet(key)
        return f.encrypt(text.encode()).decode()

    @jwt_required()
    def get(self,text):
        """Function returns the encrypted text.

        Args:
            name ([string]): [text that is to be encrypted]

        Returns:
            [string]: [The encrypted string/token]
        """
        try:
            encrypted_text = SecureText.encrypt_text(text)
            return {'encrypted': encrypted_text},200
        except:
            return {'Message': 'Your text [{}] can\'t be encrypted'.format(text)} , 500



api.add_resource(Access_flask,'/access/<string:name>')
api.add_resource(SecureText,'/securetext/<string:text>')