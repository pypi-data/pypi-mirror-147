import dynamic_logger
# from pydantic import BaseModel, Field
import logging

'''
This example shows how to use the decorator 'log_extras' to log additional fields using the logging module easily
'''

# class UserModel(BaseModel):
    # user_id: int = Field(..., example='10000001', description='Business ID of the campaign owner' )

fmt = '[%(asctime)s] <%(app)s> [%(levelname)s] (%(funcName)s) [%(id)s] [%(customer_id)s] [%(int)s] --- %(message)s (%(filename)s:%(lineno)d)'
logging.basicConfig(format=fmt, datefmt='%d-%b-%y %H:%M:%S', level='INFO')
logging.setLoggerClass(dynamic_logger.DynamicLogger)
applogger = logging.getLogger(__name__)


@applogger.log_extras('id',int=0,customer_id='obj.customer_id') # Log value of 'id' and 'obj.customer_id'
def example_1(a,id=0,id2=0,obj=None):
    applogger.info('This example shows how to log values from function arguments')
    applogger.info('You can use both positional arguments as well as keyword arguments')
    applogger.info('*args are function argument variables. Value in **kwargs are function argument variables')

# @log_instance.log_extras(user_id='input_model.user_id')
# @applogger.log_extras(id='input_model.user_id')
# def example_2(input_model: UserModel):
    # applogger.info('This example shows how to extract fields from a pydantic model (or any other class with "dict" method)')

@applogger.log_extras()
def example_3(some_arg):
    applogger.set_extras({'app': 'special'})
    applogger.info('Logging without parameters')
    applogger.clear()

def example_4(x,y):
    applogger.info(f'sum of x & y is {x+y}')

@applogger.log_extras(id="0.user_id")
def example_5(input_model):
    applogger.info(f'This is to test positional arguments in decorator')

if __name__ == '__main__':
    example_1(0, id=7192370129382,id2=2,obj={'customer_id': 829201024})
    # Set-up model
    # u = UserModel(user_id=9999999)
    # u.user_id = 8888888
    # example_2(input_model=u)
    example_3('hello there')
    example_4(2,2)
    # example_5(u)

