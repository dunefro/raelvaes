from app.v1 import app , api , Resource , JWT , jwt_required , reqparse , request , current_identity , os , base64 , Fernet , hashes , PBKDF2HMAC , salt
from app.v1.security.auth import authenticate , identity

jwt = JWT(app , authenticate , identity)

class Host:

    def __init__(self,**kwargs):
        self.name = kwargs['name']
        self.ip = kwargs['ip']

class Access:

    def __init__(self , name, host , access):
        self.name =  name
        self.host = Host(host)
        self.access = access


class Access_flask(Resource):

    def post(self , name):
        data = request.json()
        print(data)

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