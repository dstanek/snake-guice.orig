from snakeguice.binder import Key


def describe_Key_comparisons():

    def describe_when_populated_with_the_same_values():
        key_a = Key('abcd', 0)
        key_b = Key('abcd', 0)

        def then_the_hashes_will_be_the_same():
            assert hash(key_a) == hash(key_b)

        def then_the_instance_will_be_equal():
            assert key_a == key_b

    def describe_when_populated_with_different_values():
        key_a = Key('abcd', 0)
        key_b = Key('efgh', 1)

        def then_the_hashes_will_be_the_same():
            assert hash(key_a) != hash(key_b)

        def then_the_instance_will_be_equal():
            assert key_a != key_b
