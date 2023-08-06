import smartparams.utils.dictionary as dictutil
from tests.unit import UnitCase


class TestFindNested(UnitCase):
    def setUp(self) -> None:
        self.dict = dict(arg1='arg1', arg2=['arg2'], arg3={'arg31': 'a31', 'arg32': 'a32'})

    def test(self) -> None:
        name = 'arg3.arg31'

        dictionary, key = dictutil.find_nested(dictionary=self.dict, name=name)

        self.assertEqual('arg31', key)
        self.assertTupleEqual((('arg31', 'a31'), ('arg32', 'a32')), tuple(dictionary.items()))

    def test__not_in_dictionary(self) -> None:
        name = 'missing.any'

        self.assertRaises(KeyError, dictutil.find_nested, dictionary=self.dict, name=name)

    def test__required_true(self) -> None:
        name = 'arg3.missing'

        self.assertRaises(
            KeyError,
            dictutil.find_nested,
            dictionary=self.dict,
            name=name,
            required=True,
        )

    def test__is_not_dictionary(self) -> None:
        name = 'arg3.arg31.a31'

        self.assertRaises(ValueError, dictutil.find_nested, dictionary=self.dict, name=name)

    def test__set_mode(self) -> None:
        name = 'arg3.missing.key'

        dictionary, key = dictutil.find_nested(
            dictionary=self.dict,
            name=name,
            set_mode=True,
        )

        self.assertIsInstance(dictionary, dict)
        self.assertFalse(bool(dictionary))
        self.assertEqual('key', key)

    def test__set_mode_not_is_not_dictionary(self) -> None:
        name = 'arg3.arg31.a31'

        dictionary, key = dictutil.find_nested(
            dictionary=self.dict,
            name=name,
            set_mode=True,
        )

        self.assertIsInstance(dictionary, dict)
        self.assertFalse(bool(dictionary))
        self.assertEqual('a31', key)
