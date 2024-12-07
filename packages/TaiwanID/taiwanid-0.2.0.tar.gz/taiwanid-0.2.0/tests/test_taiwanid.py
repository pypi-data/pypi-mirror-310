import unittest
from taiwanid import TaiwanID


class TestTaiwanID(unittest.TestCase):
    def setUp(self):
        self.taiwan_id = TaiwanID()

    def test_validate_success(self):
        self.assertEqual(self.taiwan_id.validate('A123456789'), self.taiwan_id.ValidateStatus.SUCCESS)

    def test_validate_length(self):
        self.assertEqual(self.taiwan_id.validate('A12345678'), self.taiwan_id.ValidateStatus.LENGTH_ERROR)

    def test_validate_format(self):
        self.assertEqual(self.taiwan_id.validate('0123456789'), self.taiwan_id.ValidateStatus.FORMAT_ERROR)
        self.assertEqual(self.taiwan_id.validate('A12345678A'), self.taiwan_id.ValidateStatus.FORMAT_ERROR)

    def test_validate_check(self):
        self.assertEqual(self.taiwan_id.validate('A123456780'), self.taiwan_id.ValidateStatus.CHECK_ERROR)

    def test_get_city_A(self):
        self.assertEqual(self.taiwan_id.get_city('A123456789').name, '臺北市')

    def test_get_city_E(self):
        self.assertEqual(self.taiwan_id.get_city('E123456789').name, '高雄市')

    def test_get_city_Y(self):
        self.assertEqual(self.taiwan_id.get_city('Y123456789').name, '陽明山管理局')

    def test_get_city_index_error(self):
        with self.assertRaises(IndexError):
            self.taiwan_id.get_city('.123456789')

    def test_get_gender_female(self):
        self.assertEqual(self.taiwan_id.get_gender('A223456789'), self.taiwan_id.Genders.Female)
        self.assertEqual(type(self.taiwan_id.get_gender('A223456789')), type(self.taiwan_id.Genders.Gender))
        self.assertEqual(self.taiwan_id.get_gender('A923456789'), self.taiwan_id.Genders.Female)
        self.assertEqual(type(self.taiwan_id.get_gender('A923456789')), type(self.taiwan_id.Genders.Gender))

    def test_get_gender_male(self):
        self.assertEqual(self.taiwan_id.get_gender('A123456789'), self.taiwan_id.Genders.Male)
        self.assertEqual(type(self.taiwan_id.get_gender('A123456789')), type(self.taiwan_id.Genders.Gender))
        self.assertEqual(self.taiwan_id.get_gender('A823456789'), self.taiwan_id.Genders.Male)
        self.assertEqual(type(self.taiwan_id.get_gender('A823456789')), type(self.taiwan_id.Genders.Gender))

    def test_get_gender_value_error(self):
        with self.assertRaises(ValueError):
            self.taiwan_id.get_gender('A323456789')

    def test_get_citizenship_native(self):
        self.assertEqual(self.taiwan_id.get_citizenship('A123456789'), self.taiwan_id.Citizenships.Native)
        self.assertEqual(self.taiwan_id.get_citizenship('A223456789'), self.taiwan_id.Citizenships.Native)

    def test_get_citizenship_foreign(self):
        self.assertEqual(self.taiwan_id.get_citizenship('A823456789'), self.taiwan_id.Citizenships.Foreign)
        self.assertEqual(self.taiwan_id.get_citizenship('A923456789'), self.taiwan_id.Citizenships.Foreign)

    def test_get_citizenship_value_error(self):
        with self.assertRaises(ValueError):
            self.taiwan_id.get_citizenship('A723456789')

    def test_get_naturalization_national(self):
        self.assertEqual(self.taiwan_id.get_naturalization('A123456789'), self.taiwan_id.Naturalizations.National)
        self.assertEqual(self.taiwan_id.get_naturalization('A223456789'), self.taiwan_id.Naturalizations.National)

    def test_get_naturalization_formerly_foreign(self):
        self.assertEqual(self.taiwan_id.get_naturalization('A163456789'), self.taiwan_id.Naturalizations.NationalFormerlyForeign)
        self.assertEqual(self.taiwan_id.get_naturalization('A263456789'), self.taiwan_id.Naturalizations.NationalFormerlyForeign)

    def test_get_naturalization_formerly_without_household_registration(self):
        self.assertEqual(self.taiwan_id.get_naturalization('A173456789'), self.taiwan_id.Naturalizations.NationalFormerlyWithoutHouseholdRegistration)
        self.assertEqual(self.taiwan_id.get_naturalization('A273456789'), self.taiwan_id.Naturalizations.NationalFormerlyWithoutHouseholdRegistration)

    def test_get_naturalization_formerly_hongkong_or_macao_resident(self):
        self.assertEqual(self.taiwan_id.get_naturalization('A183456789'), self.taiwan_id.Naturalizations.NationalFormerlyHongKongOrMacaoResident)
        self.assertEqual(self.taiwan_id.get_naturalization('A283456789'), self.taiwan_id.Naturalizations.NationalFormerlyHongKongOrMacaoResident)

    def test_get_naturalization_formerly_china_resident(self):
        self.assertEqual(self.taiwan_id.get_naturalization('A193456789'), self.taiwan_id.Naturalizations.NationalFormerlyChinaResident)
        self.assertEqual(self.taiwan_id.get_naturalization('A293456789'), self.taiwan_id.Naturalizations.NationalFormerlyChinaResident)

    def test_get_naturalization_non_national(self):
        self.assertEqual(self.taiwan_id.get_naturalization('A823456789'), self.taiwan_id.Naturalizations.NonNational)
        self.assertEqual(self.taiwan_id.get_naturalization('A923456789'), self.taiwan_id.Naturalizations.NonNational)

    def test_get_info_success_A_male_native_national(self):
        id_info = self.taiwan_id.parse('A123456789')
        self.assertEqual(id_info.validate, self.taiwan_id.ValidateStatus.SUCCESS)
        self.assertEqual(id_info.city.name, '臺北市')
        self.assertEqual(id_info.gender, self.taiwan_id.Genders.Male)
        self.assertEqual(id_info.citizenship, self.taiwan_id.Citizenships.Native)
        self.assertEqual(id_info.naturalization, self.taiwan_id.Naturalizations.National)

    def test_get_info_success_A_male_native_national_formerly_foreign(self):
        id_info = self.taiwan_id.parse('A163456781')
        self.assertEqual(id_info.validate, self.taiwan_id.ValidateStatus.SUCCESS)
        self.assertEqual(id_info.city.name, '臺北市')
        self.assertEqual(id_info.gender, self.taiwan_id.Genders.Male)
        self.assertEqual(id_info.citizenship, self.taiwan_id.Citizenships.Native)
        self.assertEqual(id_info.naturalization, self.taiwan_id.Naturalizations.NationalFormerlyForeign)

    def test_get_info_success_A_male_foreign_non_national(self):
        id_info = self.taiwan_id.parse('A823456783')
        self.assertEqual(id_info.validate, self.taiwan_id.ValidateStatus.SUCCESS)
        self.assertEqual(id_info.city.name, '臺北市')
        self.assertEqual(id_info.gender, self.taiwan_id.Genders.Male)
        self.assertEqual(id_info.citizenship, self.taiwan_id.Citizenships.Foreign)
        self.assertEqual(id_info.naturalization, self.taiwan_id.Naturalizations.NonNational)

    def test_get_info_format_error(self):
        id_info = self.taiwan_id.parse('0123456789')
        self.assertEqual(id_info.validate, self.taiwan_id.ValidateStatus.FORMAT_ERROR)
        self.assertEqual(id_info.city, None)
        self.assertEqual(id_info.gender, None)
        self.assertEqual(id_info.citizenship, None)
        self.assertEqual(id_info.naturalization, None)

    def test_generate(self):
        for _ in range(100):
            self.assertEqual(self.taiwan_id.validate(self.taiwan_id.generate()), self.taiwan_id.ValidateStatus.SUCCESS)

if __name__ == '__main__':
    unittest.main(verbosity=2)
