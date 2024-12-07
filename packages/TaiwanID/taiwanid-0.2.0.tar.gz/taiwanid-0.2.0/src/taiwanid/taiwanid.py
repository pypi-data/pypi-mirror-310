from enum import Enum
import random


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

    class Genders:
        class Gender:
            def __init__(self, index: int, name: str, codes: list[int]):
                self.index: int = index
                self.name: str = name
                self.codes: list[int] = codes

        class Male:
            index = 0
            name = 'Male'
            codes = [1, 8]

        class Female:
            index = 1
            name = 'Female'
            codes = [2, 9]

        def get_list(self) -> list[Gender]:
            return [
                self.Male,
                self.Female
            ]

        def get_code_list(self) -> list[int]:
            codes = []
            for g in self.get_list():
                codes.extend(g.codes)
            return codes

    class Citizenships:
        class Citizenship:
            def __init__(self, index: int, name: str, codes: list[int]):
                self.index: int = index
                self.name: str = name
                self.codes: list[int] = codes

        class Native:
            index = 0
            name = 'Native'
            codes = [1, 2]

        class Foreign:
            index = 1
            name = 'Foreign'
            codes = [8, 9]

        def get_list(self) -> list[Citizenship]:
            return [
                self.Native,
                self.Foreign
            ]

        def get_code_list(self) -> list[int]:
            codes = []
            for c in self.get_list():
                codes.extend(c.codes)
            return codes

    class Naturalizations:
        class Naturalization:
            def __init__(self, index: int, name: str, description: str, codes: list[int], national: bool):
                self.index: int = index
                self.name: str = name
                self.description: str = description
                self.codes: list[int] = codes

        class National:
            index = 0
            name = 'National'
            description = 'Born in Taiwan'
            codes = [0, 1, 2, 3, 4, 5]

        class NationalFormerlyForeign:
            index = 1
            name = 'National'
            description = 'formerly foreign'
            codes = [6]

        class NationalFormerlyWithoutHouseholdRegistration:
            index = 2
            name = 'National'
            description = 'formerly without household registration'
            codes = [7]

        class NationalFormerlyHongKongOrMacaoResident:
            index = 3
            name = 'National'
            description = 'formerly Hong Kong or Macao resident'
            codes = [8]

        class NationalFormerlyChinaResident:
            index = 4
            name = 'National'
            description = 'formerly China resident'
            codes = [9]

        class NonNational:
            index = 5
            name = 'Non-national'
            description = ''
            codes = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

        def get_list(self) -> list[Naturalization]:
            return [
                self.National,
                self.NationalFormerlyForeign,
                self.NationalFormerlyWithoutHouseholdRegistration,
                self.NationalFormerlyHongKongOrMacaoResident,
                self.NationalFormerlyChinaResident,
                self.NonNational
            ]

    class ValidateStatus(Enum):
        SUCCESS = 'Success'
        LENGTH_ERROR = 'Length error'
        FORMAT_ERROR = 'Format error'
        CHECK_ERROR = 'Check error'

    def validate(self, id: str) -> ValidateStatus:
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
        if int(id[1]) not in self.Genders().get_code_list():
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

    def get_gender(self, id: str) -> Genders.Gender:
        '''
        Get the gender of the ID number
        \nid: ID number
        '''
        if int(id[1]) == 2 or int(id[1]) == 9:
            return self.Genders.Female
        if int(id[1]) == 1 or int(id[1]) == 8:
            return self.Genders.Male
        raise ValueError

    def get_citizenship(self, id: str) -> Citizenships.Citizenship:
        '''
        Get the citizenship of the ID number
        \nid: ID number
        '''
        if int(id[1]) in self.Citizenships().Native().codes:
            return self.Citizenships.Native
        if int(id[1]) in self.Citizenships().Foreign().codes:
            return self.Citizenships.Foreign
        raise ValueError

    def get_naturalization(self, id: str) -> Naturalizations.Naturalization:
        '''
        Check if the ID number is a naturalization
        \nid: ID number
        '''
        if int(id[1]) != 1 and int(id[1]) != 2:
            return self.Naturalizations.NonNational
        if int(id[2]) >= 0 and int(id[2]) <= 5:
            return self.Naturalizations.National
        if int(id[2]) == 6:
            return self.Naturalizations.NationalFormerlyForeign
        if int(id[2]) == 7:
            return self.Naturalizations.NationalFormerlyWithoutHouseholdRegistration
        if int(id[2]) == 8:
            return self.Naturalizations.NationalFormerlyHongKongOrMacaoResident
        if int(id[2]) == 9:
            return self.Naturalizations.NationalFormerlyChinaResident
        raise ValueError

    class IDInfo:
        def __init__(self, id: str):
            self.id: str = id
            self.validate: TaiwanID.ValidateStatus = None
            self.city: TaiwanID.City = None
            self.gender: TaiwanID.Genders.Gender = None
            self.citizenship: TaiwanID.Citizenships.Citizenship = None
            self.naturalization: TaiwanID.Naturalizations.Naturalization = None

    def parse(self, id: str) -> IDInfo:
        '''
        Get the information of the ID number
        \nid: ID number
        '''
        id_info = self.IDInfo(id)
        id_info.validate = self.validate(id_info.id)
        if id_info.validate != self.ValidateStatus.SUCCESS:
            return id_info
        id_info.city = self.get_city(id_info.id)
        id_info.gender = self.get_gender(id_info.id)
        id_info.citizenship = self.get_citizenship(id_info.id)
        id_info.naturalization = self.get_naturalization(id_info.id)
        return id_info

    def generate(self, city: City = None, gender: Genders.Gender = None, citizenship: Citizenships.Citizenship = None, naturalization: Naturalizations.Naturalization = None) -> str:
        '''
        Generate a random ID number
        \ncity: City of the ID number
        \ngender: Gender of the ID number
        \ncitizenship: Citizenship of the ID number
        \nnaturalization: Naturalization of the ID number
        '''
        id_result = ''
        check_sum = 0
        # Add city
        if city is None:
            city = random.choice(self.city)
        id_result += city.id_num_prefix
        check_sum += (city.weight // 10) + (city.weight % 10) * 9
        # Add gender with citizenship
        if gender is None:
            gender = random.choice(self.Genders().get_list())
        if citizenship is None:
            citizenship = random.choice(self.Citizenships().get_list())
        # if citizenship is foreign, can not set naturalization parameter except NonNational
        if citizenship == self.Citizenships.Foreign and (naturalization is not None and naturalization != self.Naturalizations.NonNational):
            raise ValueError('Foreign citizenship can not set naturalization parameter except NonNational')
        # find gender.codes 和 citizenship.codes intersection
        gender_code = list(set(gender.codes).intersection(citizenship.codes))[0]
        id_result += str(gender_code)
        check_sum += gender_code * 8
        # Add naturalization
        if citizenship == self.Citizenships.Foreign:
            # if citizenship is foreign, naturalization must be NonNational
            naturalization = self.Naturalizations.NonNational
        elif naturalization is None:
            naturalization = random.choice(self.Naturalizations().get_list())
        naturalization_code = random.choice(naturalization.codes)
        id_result += str(naturalization_code)
        check_sum += naturalization_code * 7
        # Add random numbers
        for i in range(6):
            num = random.randint(0, 9)
            id_result += str(num)
            check_sum += num * (6 - i)
        # Add check code
        remainder = check_sum % 10
        check_code = 10 - remainder if remainder != 0 else 0
        id_result += str(check_code)
        return id_result
