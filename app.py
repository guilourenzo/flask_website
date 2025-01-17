from flask import Flask, render_template, json, request, flash
from flaskext.mysql import MySQL
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.exceptions import abort
import logging

logging.basicConfig(filename='flask.log', filemode='a', level=logging.INFO, format='%(asctime)s - %(levelname)s:%(message)s')
mysql = MySQL()
app = Flask(__name__)
app.config['SECRET_KEY'] = '903041'
logging.info('PROCESSO INICIADO')

# MySQL configurations
try:
    app.config['MYSQL_DATABASE_USER'] = 'guilo'
    app.config['MYSQL_DATABASE_PASSWORD'] = '903041Jjg'
    app.config['MYSQL_DATABASE_DB'] = 'BucketList'
    app.config['MYSQL_DATABASE_HOST'] = 'localhost'
    mysql.init_app(app)
    logging.info('MYSQL CONFIGURADO COM SUCESSO')
except:
    logging.exception('OCORREU UM ERRO NA CONFIGURAÇÃO DO MYSQL')

def get_rule(rule_name):
    conn = mysql.connect()
    cursor = conn.cursor()

    query = "call sp_returnDQRule('"+str(rule_name)+"')"
    # rules = conn.execute(query)
    rules = cursor.fetchone()
    cursor.close()
    conn.close()
    if rules is None:
        abort(404)
    return rules

@app.route("/")
def main():
    return render_template('index.html')

@app.route('/showSignUp')
def showSignUp():
    return render_template('signup.html')

@app.route('/signUp',methods=['POST','GET'])
def signUp():
    try:
        _name = request.form['inputName']
        _email = request.form['inputEmail']
        _password = request.form['inputPassword']

        # validate the received values
        if _name and _email and _password:
            
            # All Good, let's call MySQL
            logging.info('CONEXÃO INICIADA')
            conn = mysql.connect()
            cursor = conn.cursor()
            _hashed_password = generate_password_hash(_password)
            cursor.callproc('sp_createUser',(_name,_email,_hashed_password))
            data = cursor.fetchall()
            logging.info('CONEXÃO FINALIZADA')

            if len(data) is 0:
                conn.commit()
                cursor.close() 
                conn.close()
                logging.info('USUÁRIO CRIADO COM SUCESSO')
                return json.dumps({'message':'User created successfully !'})
            else:
                logging.error('ERRO NA CRIAÇÃO DO USUÁRIO')
                return json.dumps({'error':str(data[0])})
        else:
            logging.warning('CAMPOS NÃO PREENCHIDOS')
            return json.dumps({'html':'<span>Enter the required fields</span>'})

    except Exception as e:
        logging.exception('OCORREU UM ERRO NA CAPTURA DOS DADOS DO FORM')
        return json.dumps({'error':str(e)})

@app.route('/showSignIn')
def showSignIn():
    return render_template('signin.html')

@app.route('/signIn',methods=['POST','GET'])
def signIn():
    try:
        _email = request.form['inputEmail']
        _password = request.form['inputPassword']

        # logging.info('CONEXÃO INICIADA:%s ', str(_email))

        # validate the received values
        if _email and _password:
            
            # All Good, let's call MySQL
            # logging.info('CONEXÃO INICIADA:%s ', len(str(_email)))
            conn = mysql.connect()
            cursor = conn.cursor()

            query = "call sp_returnUser('"+str(_email)+"')"
            cursor.execute(query)

            _hashed_password = cursor.fetchone()
            check_password = check_password_hash(_hashed_password[0], _password)
            logging.info('VALIDAÇÃO DE USUÁRIO: %s', check_password)
            
            logging.info('CONEXÃO FINALIZADA')

            if check_password:
                conn.commit()
                cursor.close() 
                conn.close()
                logging.info('USUÁRIO AUTENTICADO COM SUCESSO')
                return json.dumps({'message':'User authenticated successfully !'})
            else:
                logging.error('ERRO NA AUTENTICAÇÃO DO USUÁRIO')
                return json.dumps({'error':'<span>Wrong User or Password</span>'})
        else:
            logging.warning('CAMPOS NÃO PREENCHIDOS')
            return json.dumps({'html':'<span>Enter the required fields</span>'})

    except Exception as e:
        logging.exception('OCORREU UM ERRO NA CAPTURA DOS DADOS DO FORM')
        return json.dumps({'error':str(e)})

@app.route('/createRule')
def createRule():
    return render_template('create.html')

@app.route('/create',methods=['POST','GET'])
def create():
    try:
        _rules_name         = request.form['inputRulesName'],
        _rules_description  = request.form['inputRulesDescription'],
        _rules_environment  = request.form['inputRulesEnvironment'],
        _rules_command      = request.form['inputRulesCommand']
        _rules_active       = int(request.form.get('inputRulesActive'))

        # logging.info('VARIAVEIS - RULES: %s', _rules_name)
        # logging.info('VARIAVEIS - RULES: %s', _rules_description)
        # logging.info('VARIAVEIS - RULES: %s', _rules_environment)
        # logging.info('VARIAVEIS - RULES: %s', _rules_command)
        # logging.info('VARIAVEIS - RULES: %s', _rules_active)
        # logging.info('VARIAVEIS - RULES: %s', request.form.get('inputRulesActive'))
        
        # validate the received values
        if _rules_name and _rules_command and _rules_environment:
            
            # All Good, let's call MySQL
            logging.info('CONEXÃO INICIADA')
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.callproc('sp_createDQRule',(_rules_name,_rules_description,_rules_environment, _rules_command, _rules_active))
            data = cursor.fetchall()
            logging.info('CONEXÃO FINALIZADA')

            if len(data) is 0:
                conn.commit()
                cursor.close() 
                conn.close()
                logging.info('REGRA CADASTRADA COM SUCESSO')
                
                return json.dumps({'message':'Rule created successfully !'})
            else:
                logging.error('ERRO NO CADASTRO DA REGRA')
                return json.dumps({'error':str(data[0])})
        else:
            logging.warning('CAMPOS NÃO PREENCHIDOS')
            return json.dumps({'html':'<span>Enter the required fields</span>'})

    except Exception as e:
        logging.exception('OCORREU UM ERRO NA CAPTURA DOS DADOS DO FORM')
        return json.dumps({'error':str(e)})

@app.route('/editRule')
def editRule():
    return render_template('edit.html')

@app.route('/edit',methods=['POST','GET'])
def edit():
    try:
        _search_rule        = request.form['inputSearchRules'],
        _rules_name         = request.form['inputRulesName'],
        _rules_description  = request.form['inputRulesDescription'],
        _rules_environment  = request.form['inputRulesEnvironment'],
        _rules_command      = request.form['inputRulesCommand']
        _rules_active       = int(request.form.get('inputRulesActive'))

        # logging.info('VARIAVEIS - RULES: %s', _rules_name)
        # logging.info('VARIAVEIS - RULES: %s', _rules_description)
        # logging.info('VARIAVEIS - RULES: %s', _rules_environment)
        # logging.info('VARIAVEIS - RULES: %s', _rules_command)
        # logging.info('VARIAVEIS - RULES: %s', _rules_active)
        # logging.info('VARIAVEIS - RULES: %s', request.form.get('inputRulesActive'))
        
        # validate the received values
        if _rules_name and _rules_command and _rules_environment:
            
            # All Good, let's call MySQL
            logging.info('CONEXÃO INICIADA')
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.callproc('sp_createDQRule',(_rules_name,_rules_description,_rules_environment, _rules_command, _rules_active))
            data = cursor.fetchall()
            logging.info('CONEXÃO FINALIZADA')

            if len(data) is 0:
                conn.commit()
                cursor.close() 
                conn.close()
                logging.info('REGRA CADASTRADA COM SUCESSO')
                
                return json.dumps({'message':'Rule created successfully !'})
            else:
                logging.error('ERRO NO CADASTRO DA REGRA')
                return json.dumps({'error':str(data[0])})
        else:
            logging.warning('CAMPOS NÃO PREENCHIDOS')
            return json.dumps({'html':'<span>Enter the required fields</span>'})

    except Exception as e:
        logging.exception('OCORREU UM ERRO NA CAPTURA DOS DADOS DO FORM')
        return json.dumps({'error':str(e)})


if __name__ == "__main__":
    app.run()
