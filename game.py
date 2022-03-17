class Spec:
    def __init__(self, name, n_created, spcode):
        self.m_name = name
        self.m_num_created = n_created
        self.m_spcode = spcode
        self.assert_ok()

    def assert_ok(self):
        assert isinstance(self.m_name, str)
        assert isinstance(self.m_num_created, int)
        assert isinstance(self.m_spcode, int)
        assert self.m_num_created > 0
        assert self.m_spcode >= 0

    def spcode(self):
        return self.m_spcode


class Specs:
    def __init__(self, li):
        self.m_array = li
        self.assert_ok()

    def assert_ok(self):
        i = 0
        for sp in self.m_array:
            assert isinstance(sp, Spec)
            sp.assert_ok()
            assert sp.spcode() == i
            i += 1

    def add(self, name, n_created, name_of_created):
        assert not (self.contains(name))
        spc, ok = self.spcode_from_name(name_of_created)
        assert ok
        self.add_spec(spec_create(name, n_created, spc))

    def contains(self, name):
        spc, ok = self.spcode_from_name(name)
        return ok

    def spcode_from_name(self, name_of_created):
        for sp in self.m_array:
            if sp.name() == name_of_created:
                return sp.spcode, True
        return -1, False

    def add_spec(self, sp):
        assert isinstance(sp, Spec)
        self.m_array.append(sp)


class Game:
    def assert_ok(self):
        assert isinstance(self.m_dollars, int)
        assert isinstance(self.m_specs, Specs)
        assert self.m_dollars >= 0

    def __init__(self, dollars, sps):
        self.m_dollars = dollars
        self.m_specs = sps
        self.assert_ok()

    def print(self):
        print(self.string())

    def string(self):
        return str(self.m_dollars) + '\n' + self.m_specs.string()

    def update_with_string(self, s):
        assert isinstance(s, str)
        if s.isdigit():
            self.m_dollars = int(s)
        else:
            print('Ignoring non-int value')

    def run(self):
        print('a at start:')
        self.print()
        finished = False
        while not finished:
            s = input("Command> ")
            if s == "quit":
                finished = True
            else:
                self.update_with_string(s)
                print('a at finish:')
                self.print()


def specs_empty():
    return Specs([])


def spec_create(name, n_created, name_of_created):
    return Spec(name, n_created, name_of_created)


def specs_default():
    result = specs_empty()
    result.add('printer', 1, 'dollar')
    result.add('maker', 1, 'printer')
    result.add('multiprinter', 10, 'dollar')
    result.add('factory', 1, 'maker')
    return result


def run_accumulate_game():
    a = Game(42, specs_default())
    a.run()
