from enum import Enum


class TaiwanID:
    def __init__(self):
        self.issue_place = [
            '北市', '中市', '基市', '南市', '高市', '新北市', '宜縣', '桃市', '嘉市', '竹縣',
            '苗縣', '投縣', '彰縣', '竹市', '雲縣', '嘉縣', '屏縣', '花縣', '東縣', '金門',
            '澎縣', '連江', '北縣', '桃縣', '中縣', '南縣', '高縣'
        ]
        self.city = [
            self.City('A', 10, '臺北市', 'TW-TPE'),
            self.City('B', 11, '臺中市', 'TW-TXG'),
            self.City('C', 12, '基隆市', 'TW-KEE'),
            self.City('D', 13, '臺南市', 'TW-TNN'),
            self.City('E', 14, '高雄市', 'TW-KHH'),
            self.City('F', 15, '新北市', 'TW-NWT'),
            self.City('G', 16, '宜蘭縣', 'TW-ILA'),
            self.City('H', 17, '桃園市', 'TW-TAO'),
            self.City('I', 34, '嘉義市', 'TW-CYI'),
            self.City('J', 18, '新竹縣', 'TW-HSQ'),
            self.City('K', 19, '苗栗縣', 'TW-MIA'),
            self.City('L', 20, '臺中縣', 'TW-TXG'),
            self.City('M', 21, '南投縣', 'TW-NAN'),
            self.City('N', 22, '彰化縣', 'TW-CHA'),
            self.City('O', 35, '新竹市', 'TW-HSZ'),
            self.City('P', 23, '雲林縣', 'TW-YUN'),
            self.City('Q', 24, '嘉義縣', 'TW-CYQ'),
            self.City('R', 25, '臺南縣', 'TW-TNN'),
            self.City('S', 26, '高雄縣', 'TW-KHH'),
            self.City('T', 27, '屏東縣', 'TW-PIF'),
            self.City('U', 28, '花蓮縣', 'TW-HUA'),
            self.City('V', 29, '臺東縣', 'TW-TTT'),
            self.City('W', 32, '金門縣', 'TW-KIN'),
            self.City('X', 30, '澎湖縣', 'TW-PEN'),
            self.City('Y', 31, '陽明山管理局', 'TW-TPE'),
            self.City('Z', 33, '連江縣', 'TW-LIE')
        ]
        self.gender = [
            self.Gender(0, 'Female'),
            self.Gender(1, 'Male')
        ]

    class City:
        '''
        City class
        \nid_num_prefix: First letter of the ID number
        \nweight: Weight for verification
        \nname: Name of the city
        \ncode: Code of the city, ISO 3166-2:TW
        '''
        def __init__(self, id_num_prefix: str, weight: int, name: str, code: str):
            self.id_num_prefix = id_num_prefix
            self.weight = weight
            self.name = name
            self.code = code

    class Gender:
        '''
        Gender class
        \ncode: Index of the gender
        \nname: Name of the gender
        '''
        def __init__(self, index, name):
            self.code = index
            self.name = name

    class Citizenship(Enum):
        NATIVE = "Native"
        FOREIGN = "Foreign"

    class ValidateStatus(Enum):
        SUCCESS = "Success"
        LENGTH_ERROR = "Length error"
        FORMAT_ERROR = "Format error"
        CHECK_ERROR = "Check error"

    def validate(self, id: str) -> bool:
        '''
        Validate the ID number
        \nid: ID number
        '''
        # Check length
        if len(id) != 10:
            return self.ValidateStatus.LENGTH_ERROR
        # Check first letter
        if id[0] not in [c.id_num_prefix for c in self.city]:
            return self.ValidateStatus.FORMAT_ERROR
        # Check last 9 digits are numbers
        if not id[1:].isdigit():
            return self.ValidateStatus.FORMAT_ERROR
        # Check gender
        if int(id[1]) not in [g.code for g in self.gender]:
            return self.ValidateStatus.FORMAT_ERROR
        # Check check code
        city_weight = [c.weight for c in self.city if c.id_num_prefix == id[0]][0]
        sum = (city_weight // 10) + (city_weight % 10) * 9
        for i in range(1, 10):
            sum += int(id[i]) * ((9 - i) if i < 9 else 1)
        if sum % 10 != 0:
            return self.ValidateStatus.CHECK_ERROR
        # Return success
        return self.ValidateStatus.SUCCESS

    def get_city(self, id: str) -> City:
        '''
        Get the city of the ID number
        \nThis only represents the initial household or naturalization place
        \nid: ID number
        '''
        return [c for c in self.city if c.id_num_prefix == id[0]][0]

    def get_gender(self, id: str) -> Gender:
        '''
        Get the gender of the ID number
        \nid: ID number
        '''
        if int(id[1]) == 2 or int(id[1]) == 9:
            return self.gender[0]
        if int(id[1]) == 1 or int(id[1]) == 8:
            return self.gender[1]
        raise ValueError

    def get_citizenship(self, id: str) -> Citizenship:
        '''
        Get the citizenship of the ID number
        \nid: ID number
        '''
        if int(id[1]) == 1 or int(id[1]) == 2:
            return self.Citizenship.NATIVE
        if int(id[1]) == 8 or int(id[1]) == 9:
            return self.Citizenship.FOREIGN
        raise ValueError

    def info(self):
        raise NotImplementedError

    def generate(self):
        raise NotImplementedError
