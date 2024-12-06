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
        self.assertEqual(self.taiwan_id.get_gender('A223456789').name, 'Female')
        self.assertEqual(self.taiwan_id.get_gender('A923456789').name, 'Female')

    def test_get_gender_male(self):
        self.assertEqual(self.taiwan_id.get_gender('A123456789').name, 'Male')
        self.assertEqual(self.taiwan_id.get_gender('A823456789').name, 'Male')

    def test_get_gender_value_error(self):
        with self.assertRaises(ValueError):
            self.taiwan_id.get_gender('A323456789')

    def test_get_citizenship_native(self):
        self.assertEqual(self.taiwan_id.get_citizenship('A123456789').value, 'Native')
        self.assertEqual(self.taiwan_id.get_citizenship('A223456789').value, 'Native')

    def test_get_citizenship_foreign(self):
        self.assertEqual(self.taiwan_id.get_citizenship('A823456789').value, 'Foreign')
        self.assertEqual(self.taiwan_id.get_citizenship('A923456789').value, 'Foreign')

    def test_get_citizenship_value_error(self):
        with self.assertRaises(ValueError):
            self.taiwan_id.get_citizenship('A723456789')


if __name__ == '__main__':
    unittest.main(verbosity=2)
