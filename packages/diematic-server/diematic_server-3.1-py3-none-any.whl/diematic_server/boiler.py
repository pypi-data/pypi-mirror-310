import logging

from datetime import datetime
import threading
from typing import Any

log = logging.getLogger()

class Boiler:
    """ Class representation of a De Dietrich boiler with capacity to read registers
        :param index: instance of the yaml configuration file
    """
    def __init__(self, uuid, index):
        self.uuid = uuid
        self.registers = []
        self.attribute_list = []
        self.index = index
        self.lock = threading.Lock()
        with self.lock: 
            for register in self.index:
                influx = True
                if 'influx' in register:
                    influx = register['influx']

                if 'type' in register and register['type'] == 'bits':
                    for varname in register['bits']:
                        realvarname = varname if type(varname) is str else varname['name']
                        self._init_register_value(realvarname, register['id'], influx)
                        self.attribute_list.append(realvarname)
                
                elif 'name' in register and 'id' in register:
                    is_bits = 'type' in register and register['type'] == 'bits'

                    self._init_register_value(register['name'], register['id'], influx and not is_bits)
                    self.attribute_list.append(register['name'])


    def _init_register_value(self, varname, id, influx):
        # this method is protected by self.lock
        setattr(self, varname, {'name': varname, 'status': 'init', 'value': None, 'id': id, 'influx': influx})
#       {
#           'name': varname,
#           'value': registervalue, 
#           'read': datetime.now().isoformat(), 
#           'status': can be 'init', 'read', 'writepending' or 'checking' or 'error'
#           'newvalue': this is the new value to be written, checked etc. status goes to 'read' when 'newvalue' exist and is equal to 'registervalue'
#           'error': error message after writing a value and a failure received
#       }


    def _set_register_value(self, varname, registervalue):
        # this method is protected by self.lock
        realvarname = varname if type(varname) is str else varname['name']
        previous_value = getattr(self, realvarname, {'name': realvarname, 'status': 'init', 'value': registervalue})
        varvalue = previous_value.copy()
        prestatus = previous_value.get('status')
        if prestatus == 'init':
            status = 'read'
        else:
            status = prestatus
        if status != 'init':
            varvalue['value'] = registervalue
            varvalue['read'] = datetime.now().isoformat()
        varvalue['status'] = status
        setattr(self, realvarname, varvalue)

    def _add_register_field(self, varname, field, value):
        previous_value = getattr(self, varname)
        new_value = previous_value.copy()
        new_value[field] = value
        setattr(self, varname, new_value)

    def _decode_model(self, value_int: int) -> str:
        models = {
            0: '3-25LP',
            1: '3-15LP',
            2: '3-25SOLO',
            3: '3-25K',
            4: '3-15SOLO',
            30: 'MC 35 E',
            5: '3-E25LP',
            31: 'MC 45',
            6: 'DOMOLIGHT',
            32: 'MC 65',
            7: '3-35', 
            33: 'MC 90',
            8: '3-50',
            34: 'C210',
            9: '3-25 BIC',
            35: 'C310',
            10: '3-15ECO',
            36: 'C610',
            11: '3-25ECO',
            37: 'C230',
            12: '3-35ECO',
            13: '3-50ECO',
            14: '3-65ECO',
            40: 'Robur HP',
            20: 'Diematic 3',
            21: 'Diematic m2',
            22: 'Diematic m3',
            23: 'MIT',
            24: 'D4',
            25: 'MB/OT interface'
        }
        return models.get(value_int,'Unknown')

    def _decode_decimal(self, value_int, decimals=0):
        if (value_int == 65535):
            return None
        else:
            output = value_int & 0x7FFF
        if (value_int >> 15 == 1):
            output = -output
        return float(output)/10**decimals

    def _encode_decimal(self, value, decimals=0):
        decimalvalue = int(value*10**decimals)
        if decimalvalue < 0:
            positivevalue = -decimalvalue
            return (positivevalue & 0x7FFF) | 0x8000
        return decimalvalue & 0x7FFF

    def _decode_errorcode(self, value_int):
        if (value_int == 0x0000):
            return 'OK'
        if (value_int == 0x0001):
            return 'BOILER S.FAIL.'
        if (value_int == 0x0002):
            return 'OUTL S.A FAIL.'
        if (value_int == 0x0003):
            return 'OUTL S.B FAIL.'
        if (value_int == 0x0004):
            return 'OUTL S.C FAIL.'
        if (value_int == 0x0005):
            return 'OUTSI. S.FAIL.'
        if (value_int == 0x0006):
            return 'SMOKE S. FAIL.'
        if (value_int == 0x0007):
            return 'AUX. F. DEFEKT'
        if (value_int == 0x0009):
            return 'DHW S. FAILURE'
        if (value_int == 0x000A):
            return 'BACK S.FAILURE'
        if (value_int == 0x000B):
            return 'ROOM S.A FAIL.'
        if (value_int == 0x000C):
            return 'ROOM S.B FAIL.'
        if (value_int == 0x000D):
            return 'ROOM S.C FAIL.'
        if (value_int == 0x000E):
            return 'SOLAR S. FAIL'
        if (value_int == 0x000F):
            return 'ST.TANK S.FAIL'
        if (value_int == 0x0010):
            return 'SWIM.P.A S.FAIL'
        if (value_int == 0x0011):
            return 'DHW 2 S. FAIL'
        if (value_int == 0x0012):
            return 'CDI.A COM.FAIL'
        if (value_int == 0x0013):
            return 'CDI.B COM.FAIL'
        if (value_int == 0x0014):
            return 'CDI.C COM.FAIL'
        if (value_int == 0x001B):
            return 'I-CURRENT FAIL'
        if (value_int == 0x001C):
            return 'BURNER FAILURE'
        if (value_int == 0x001D):
            return 'PARASIT FLAME'
        if (value_int == 0x001E):
            return 'STB BOILER'
        if (value_int == 0x001F):
            return 'STB BACK'
        if (value_int == 0x0020):
            return 'VALVE FAIL'
        if (value_int == 0x0022):
            return 'PCU BLOCKING'
        if (value_int == 0x0023):
            return 'EXCHAN.S.FAIL'
        if (value_int == 0x0024):
            return 'STB EXCHANGE'
        if (value_int == 0x0025):
            return 'TA-S SHORT-CIR'
        if (value_int == 0x0026):
            return 'TA-S DISCONNEC'
        if (value_int == 0x0027):
            return 'TA-S FAILURE'
        if (value_int == 0x0028):
            return 'MC COM.FAIL'
        if (value_int == 0x0029):
            return 'AUX2.SENS.FAIL'
        if (value_int == 0x002A):
            return 'UNIV.SENS.FAIL'
        if (value_int == 0x002B):
            return 'SWIM.P.B S.FAIL'
        if (value_int == 0x002C):
            return 'SWIM.P.C S.FAIL'
        if (value_int == 0x002D):
            return 'PCU COM. FAIL'
        if (value_int == 0x002E):
            return 'LOCKING'
        if (value_int == 0x002F):
            return 'PSU FAIL'
        if (value_int == 0x0030):
            return 'PSU PARAM FAIL'
        if (value_int == 0x0031):
            return 'CCE TEST FAIL'
        if (value_int == 0x0032):
            return 'FAN FAILURE'
        if (value_int == 0x0033):
            return 'SMOKE.P.FAIL'
        if (value_int == 0x0034):
            return 'SU COM.FAIL'
        if (value_int == 0x0035):
            return 'PCU-M3 COM.FAIL'
        if (value_int == 0x0036):
            return 'CS OPEN FAIL'
        if (value_int == 0x0037):
            return 'EXCH-BACK<MIN'
        if (value_int == 0x0038):
            return 'EXCH-BACK>MAX'
        if (value_int == 0x0039):
            return 'BACK>BOIL FAIL'
        if (value_int == 0x003A):
            return 'FAIL UNKNOWN'
        return "Unknown error 0x{errno:x}".format(errno=value_int)

    def _decode_modeflag(self, value_int):
       """ Decodes and normalizes the working mode of the boiler.
            0 -> Anti-freeze
            2 -> Night
            4 -> Day
       """ 
       if value_int not in (0, 2, 4):
           return None
       if value_int == 4:
           return 1
       if value_int == 2:
           return 0
       if value_int == 0:
           return -1

    def _encode_modeflag(self, value):
        if value not in (1,0,-1):
            return None
        if value == 1:
            return 4
        if value == 0:
            return 2
        if value == -1:
            return 0

    def _decode_circtype(self, value_int):
        """ Decodes and normalizes the circuit type mode of the boiler.
            0 -> Disable
            1 -> Direct
            2 -> 3 Way Valve
            3 -> Direct+
            4 -> 3 Way Valve+
            5 -> Swimingpool
        """ 
        if value_int == 0:
           return 'DISABLE'
        if value_int == 1:
            return 'DIRECT'
        if value_int == 2:
            return '3WV'
        if value_int == 3:
            return 'DIRECT+'
        if value_int == 4:
            return '3WV+'
        if value_int == 5:
            return 'SWIM.'
        return 'UNKOWN'

    def _encode_circtype(self, value):
        if value == 'DISABLE':
            return 0
        if value == 'DIRECT':
            return 1
        if value == '3WV':
            return 2
        if value == 'DIRECT+':
            return 3
        if value == '3WV+':
            return 4
        if value == 'SWIM.':
            return 5
        return None

    def _decode_program(self, value_int):
        """ Decodes program applied to circuit.
            0 -> P1
            1 -> P2
            2 -> P3
            3 -> P4
        """ 
        return value_int + 1

    def _encode_program(self, value):
        return value - 1

    def _register(self, varname):
        for register in self.index:
            if not isinstance(register['id'], int):
                return
            if register['type'] == 'bits':
                for i in range(len(register['bits'])):
                    bit_varname = register['bits'][i]
                    checkname = bit_varname if type(bit_varname) is str else bit_varname['name']
                    if checkname == varname:
                        return register
            else:
                if register.get('name') == varname:
                    return register
        return None

    def _update_register(self, register):
        # this method is protected by self.lock
        if not isinstance(register['id'], int):
            return
        register_value = self.registers[register['id']]
        if register_value is None:
            log.debug('Browsing register id {:d} value: None'.format(register['id']))
            return
        log.debug('Browsing register id {:d} value: {:#04x}'.format(register['id'], register_value))
        if register['type'] == 'bits':
            if 'name' in register:
                varname = register.get('name')
                self._set_register_value(varname, register_value)
            for i in range(len(register['bits'])):
                bit_varname = register['bits'][i]
                realvarname = bit_varname if type(bit_varname) is str else bit_varname['name']
                if realvarname == 'io_unused':
                    continue
                bit_value = register_value >> i & 1
                self._set_register_value(realvarname, bit_value)
                if 'desc' in bit_varname:
                    self._add_register_field(bit_varname['name'], 'desc', bit_varname['desc'])
        else:
            if 'name' in register:
                varname = register.get('name')
                if varname and varname.strip(): #test name exists
                    if register['type'] == 'DiematicOneDecimal':
                        self._set_register_value(varname, self._decode_decimal(register_value, 1))
                    elif register['type'] == 'DiematicModeFlag':
                        self._set_register_value(varname, self._decode_modeflag(register_value))
                    elif register['type'] == 'ErrorCode':
                        self._set_register_value(varname, self._decode_errorcode(register_value))
                    elif register['type'] == 'DiematicCircType':
                        self._set_register_value(varname, self._decode_circtype(register_value))
                    elif register['type'] == 'DiematicProgram':
                        self._set_register_value(varname, self._decode_program(register_value))
                    elif register['type'] == 'Model':
                        self._set_register_value(varname, self._decode_model(register_value))
                    else:
                        self._set_register_value(varname, register_value)
                if 'desc' in register:
                    self._add_register_field(varname, 'desc', register['desc'])

    def browse_registers(self):
        with self.lock:
            for register in self.index:
                self._update_register(register)

    def dump_registers(self):
        output = ''
        for id in range(len(self.registers)):
            if self.registers[id] is None:
                output += "{:d}: None\n".format(id)
            else:
                output += "{:d}: {:#04x}\n".format(id, self.registers[id])
        return output

    def fetch_data(self) -> dict[str, Any]:
        """ 
        Returns a dictionary of values from the boiler. 
        """
        with self.lock:
            output = { }
            output['uuid'] = self.uuid
            for varname in self.attribute_list:
                register = getattr(self, varname)
                if register['influx']:
                    output[varname] = register['value']
            return output

    def get_register_field(self, varname: str, field: str) -> str:
        register = getattr(self, varname, None)
        if register is None or not field in register:
            return f'No value set for field {field} in register {varname}'
        return register.get(field)

    def dump(self):
        output = ''
        for varname,value in self.fetch_data().items():
            output += varname + ' = ' + str(value) + "\n"
        return output

    def toJSON(self):
        return self.fetch_data()

    def set_write_pending(self, varname, newvalue, callback = None):
        with self.lock:
            value = getattr(self, varname, None)
            if value is None:
                return
            value['newvalue'] = newvalue
            value['status'] = 'writepending'
            if callback is not None:
                value['callback'] = callback
            setattr(self, varname, value)
                

    def next_write(self):
        """ returns the next register that contains a pending write or None
        """
        with self.lock:
            for varname in self.attribute_list:
                value = getattr(self, varname, {})
                if 'status' in value and value['status'] == 'writepending':
                    value['status'] = 'checking'
                    return value
            return None

    def prepare_write(self, write):
        """ returns a dictionary with two keys:
            the 'address' key contains the register address to write to,
            the 'value' key contains the new value
        """
        with self.lock:
            register = self._register(write['name'])
            encodedValue = write['newvalue']
            if register['type'] == 'bits':
                overallvalue = 0
                for i in range(len(register['bits'])):
                    bit_varname = register['bits'][i]
                    checkvarname = bit_varname if type(bit_varname) is str else bit_varname['name']
                    if checkvarname == 'io_unused':
                        continue
                    if checkvarname != write['name']:
                        bit_value = getattr(self, checkvarname)['value'] << i
                        overallvalue = overallvalue | bit_value
                    else:
                        bit_value = write['newvalue'] << i
                        overallvalue = overallvalue | bit_value
                encodedValue = overallvalue
            if register['type'] == 'DiematicOneDecimal':
                encodedValue = self._encode_decimal(encodedValue, 1)
            elif register['type'] == 'DiematicModeFlag':
                encodedValue = self._encode_modeflag(encodedValue)
            elif register['type'] == 'ErrorCode':
                raise ValueError('Cannot write read only value')
            elif register['type'] == 'DiematicCircType':
                encodedValue = self._encode_circtype(encodedValue)
            elif register['type'] == 'DiematicProgram':
                encodedValue = self._encode_program(encodedValue)

            return {
                "address": register['id'],
                "value": encodedValue
            }

    def write_error(self, varname, message):
        """ The write operation failed to compare values """
        with self.lock:
            value = getattr(self, varname, {})
            value['error'] = message
            value['status'] = 'error'
            if 'callback' in value:
                value['callback'] = None

    def clear_error(self, varname):
        """ clear error on varname """
        with self.lock:
            value = getattr(self, varname, {})
            value.pop('error', None)
            value.pop('newvalue', None)
            value['status'] = 'read'
            if 'callback' in value:
                value['callback'] = None

    def write_ok(self, varname):
        """ write operation succeed """
        with self.lock:
            value = getattr(self, varname, {})
            newvalue = value.pop('newvalue')
            value.pop('error', None)
            value['value'] = newvalue
            value['status'] = 'read'
            if 'callback' in value:
                value['callback']()
                value['callback'] = None

