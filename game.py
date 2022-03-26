class Child:
    def __init__(self, child_spcode: int):
        self.m_spcode = child_spcode
        self.assert_ok()

    def assert_ok(self):
        assert isinstance(self.m_spcode, int)
        assert 0 <= self.m_spcode < 100

    def spcode(self):
        return self.m_spcode


def child_create(child_spcode: int) -> Child:
    return Child(child_spcode)


class Maybechild:
    def __init__(self, is_defined: bool, child: Child):
        self.m_defined = is_defined
        self.m_child = child
        self.assert_ok()

    def child(self) -> tuple[Child, bool]:
        return self.m_child, self.m_defined

    def assert_ok(self):
        assert isinstance(self.m_defined, bool)
        if self.m_defined:
            assert isinstance(self.m_child, Child)
            self.m_child.assert_ok()


def padded(u: int) -> str:
    s = str(u)
    if u < 10:
        return '00' + s
    else:
        if u < 100:
            return '0' + s
        else:
            return s


class Dollars:
    def __init__(self, dollars: int):
        self.m_dollars = dollars
        self.assert_ok()

    def assert_ok(self):
        assert isinstance(self.m_dollars, int)
        assert 0 <= self.m_dollars < 1 << 30

    def string(self):
        billion: int = 1000 * 1000 * 1000
        n = billion
        remainder: int = self.m_dollars

        result = ''
        finished = False
        while not finished:
            u = remainder // n
            if result != '':
                result = result + ',' + padded(u)
            elif u > 0 or n == 1:
                result = str(u)

            if n == 1:
                finished = True
            else:
                remainder = remainder - n * u
                n = n // 1000

        return result

    def int(self) -> int:
        return self.m_dollars


class Spec:
    def __init__(self, name: str, cost: Dollars, steps_to_make_child: int, maybechild: Maybechild):
        assert isinstance(maybechild, Maybechild)
        self.m_name = name
        self.m_cost = cost
        self.m_steps_to_make_child = steps_to_make_child
        self.m_child = maybechild
        self.assert_ok()

    def assert_ok(self):
        assert isinstance(self.m_name, str)
        assert isinstance(self.m_child, Maybechild)
        self.maybechild().assert_ok()

    def maybechild(self) -> Maybechild:
        return self.m_child

    def name(self) -> str:
        return self.m_name

    def cost(self) -> Dollars:
        return self.m_cost

    def steps_to_make_child(self) -> int:
        return self.m_steps_to_make_child

    def child(self) -> tuple[Child, bool]:
        return self.maybechild().child()


def maybechild_defined(child: Child) -> Maybechild:
    assert isinstance(child, Child)
    return Maybechild(True, child)


def spec_create(name: str, cost: Dollars, steps_to_make_child: int, maybechild: Maybechild) -> Spec:
    return Spec(name, cost, steps_to_make_child, maybechild)


def maybechild_undefined() -> Maybechild:
    return Maybechild(False, child_create(0))


def spec_which_makes_dollar(name: str, cost: Dollars, steps_to_make_child: int) -> Spec:
    return spec_create(name, cost, steps_to_make_child, maybechild_undefined())


class Specs:
    def __init__(self, li: list[Spec]):
        self.m_array = li
        self.assert_ok()

    def assert_ok(self):
        i = 0
        for sp in self.m_array:
            assert isinstance(sp, Spec)
            sp.assert_ok()
            mch = sp.maybechild()
            child, ok = mch.child()
            if ok:
                child.assert_ok()
                assert child.spcode() < i
            i += 1

    def add_with_non_dollar_child(self, name: str, cost_to_buy: int, steps_to_make_child: int, child_name: str):
        assert not (self.contains(name))
        spc, ok = self.spcode_from_string(child_name)
        assert ok
        self.add_spec(spec_non_dollar(name, Dollars(cost_to_buy), steps_to_make_child, child_create(spc)))

    def contains(self, name):
        spc, ok = self.spcode_from_string(name)
        return ok

    def spcode_from_string(self, name_of_created: str) -> tuple[int, bool]:
        for i in range(0, self.num_spcodes()):
            if self.name(i) == name_of_created:
                return i, True
        return -1, False

    def add_spec(self, sp: Spec):
        assert isinstance(sp, Spec)
        assert not self.contains(sp.name())
        self.m_array.append(sp)

    def steps_to_make_child(self, spc: int) -> int:
        return self.spec(spc).steps_to_make_child()

    def string(self) -> str:
        result = ''
        for i in range(0, self.num_spcodes()):
            result = result + self.spec_string(i)
        return result

    def num_spcodes(self) -> int:
        return len(self.m_array)

    def spec(self, spc) -> Spec:
        assert 0 <= spc < self.num_spcodes()
        return self.m_array[spc]

    def cost(self, spc: int) -> Dollars:
        return self.spec(spc).cost()

    def name(self, spc: int) -> str:
        return self.spec(spc).name()

    def child_name(self, spc: int) -> str:
        child_spc, ok = self.child_spcode(spc)
        if ok:
            return self.name(child_spc)
        else:
            return 'dollar'

    def spec_string(self, spc):
        sp = self.spec(spc)
        stm = sp.steps_to_make_child()
        cname = self.child_name(spc)
        return f'a {sp.name()} costs {sp.cost()} and takes {stm} to make a {cname}\n'

    def add_with_dollar_child(self, name: str, cost: int, steps_to_make_child: int):
        self.add(spec_which_makes_dollar(name, Dollars(cost), steps_to_make_child))

    def child_spcode(self, spc: int) -> tuple[int, bool]:
        ch, ok = self.child(spc)
        if ok:
            return ch.spcode(), True
        else:
            return 0, False

    def child(self, spc: int) -> tuple[Child, bool]:
        return self.spec(spc).child()

    def add(self, sp: Spec):
        self.m_array.append(sp)


class State:
    def __init__(self, steps_remaining: int):
        self.m_steps_remaining = steps_remaining
        self.assert_ok()

    def assert_ok(self):
        assert isinstance(self.m_steps_remaining, int)
        assert 0 <= self.m_steps_remaining
        assert self.m_steps_remaining < 100

    def steps_remaining(self) -> int:
        return self.m_steps_remaining

    def decrement_remaining(self):
        assert self.m_steps_remaining > 0
        self.m_steps_remaining -= 1

    def set_remaining(self, steps: int):
        self.m_steps_remaining = steps


class States:
    def __init__(self, count: int):
        self.m_count = count
        self.assert_ok()

    def assert_ok(self):
        assert isinstance(self.m_count, int)
        assert self.m_count >= 0

    def add(self, delta: int):
        self.m_count += delta

    def num_states(self):
        return self.m_count


def states_empty() -> States:
    return States(0)


def state_create(steps_remaining: int) -> State:
    return State(steps_remaining)


class Spates:
    def __init__(self, num_spcodes: int):
        self.m_states_array = []
        for i in range(0, num_spcodes):
            self.m_states_array.append(states_empty())
        self.assert_ok()

    def assert_ok(self):
        for i in range(0, self.num_spcodes()):
            sts = self.states(i)
            sts.assert_ok()

    def num_spcodes(self) -> int:
        return len(self.m_states_array)

    def states(self, spc: int) -> States:
        assert 0 <= spc < self.num_spcodes()
        return self.m_states_array[spc]

    def add(self, spc: int, delta: int):
        self.states(spc).add(delta)

    def num_states(self, spc):
        return self.states(spc).num_states()


def spates_create(num_spcodes: int) -> Spates:
    return Spates(num_spcodes)


class Game:
    def assert_ok(self):
        assert isinstance(self.m_dollars, Dollars)
        assert isinstance(self.m_spates, Spates)
        assert isinstance(self.m_specs, Specs)
        self.spates().assert_ok()
        self.specs().assert_ok()
        self.dollars().assert_ok()

    def __init__(self, steps: int, sps: Specs, dollars: Dollars, spas: Spates):
        self.m_steps = steps
        self.m_dollars = dollars
        self.m_spates = spas
        self.m_specs = sps
        self.assert_ok()

    def print(self):
        print(self.string())

    def string(self) -> str:
        result = f'\n**** Step {self.steps()}: You have ${self.dollars().string()}\n'
        for spc in range(0, self.num_spcodes()):
            result = result + self.string_from_spcode(spc) + '\n'
        return result

    def update_with_string(self, s: string):
        assert isinstance(s, str)
        if s != '':
            spc, ok = self.spcode_from_string(s)
            if ok:
                cost = self.specs().cost(spc)
                if self.dollars().int() >= cost.int():
                    self.decrement_dollars(cost)
                    self.add_state(spc, 1)
                else:
                    print('Cannot afford it!')
            else:
                print(f'No such thing as {s}')

        new_spates = spates_create(self.num_spcodes())
        for spc in range(0, self.num_spcodes()):
            sp = self.spec(spc)
            if self.steps() % sp.steps_to_make_child() == 0:
                ch, ok = sp.child()
                if not ok:
                    self.increment_dollars(self.num_states(spc))
                else:
                    assert 0 <= ch.spcode() < self.num_spcodes()
                    new_spates.add(ch.spcode(), self.num_states(spc))

        for spc in range(0, self.num_spcodes()):
            self.spates().add(spc, new_spates.num_states(spc))

        self.m_steps += 1

    def run(self):
        self.print()
        finished = False
        while not finished:
            s = input("Command> ")
            if s == "quit":
                finished = True
            else:
                self.update_with_string(s)
                self.print()

    def spates(self) -> Spates:
        return self.m_spates

    def states(self, spc: int) -> States:
        return self.spates().states(spc)

    def dollars(self) -> Dollars:
        return self.m_dollars

    def specs(self):
        return self.m_specs

    def num_states(self, spc: int) -> int:
        return self.states(spc).num_states()

    def num_spcodes(self) -> int:
        return self.specs().num_spcodes()

    def steps_to_make_child(self, spc: int) -> int:
        return self.spec(spc).steps_to_make_child()

    def spec(self, spc: int) -> Spec:
        return self.specs().spec(spc)

    def spcode_from_string(self, s: str) -> tuple[int, bool]:
        return self.specs().spcode_from_string(s)

    def increment_dollars(self, delta: int):
        self.m_dollars = Dollars(self.dollars().int()+delta)

    def add_state(self, spc: int, delta: int):
        self.states(spc).add(delta)

    def string_from_spcode(self, spc: int) -> str:
        return self.basic_string_from_spcode(spc) + ' ' + self.cost_string_from_spcode(spc)

    def basic_string_from_spcode(self, spc):
        ns = self.num_states(spc)
        name = self.spec(spc).name()
        child_name = self.child_name(spc)
        avg_steps = self.steps_to_make_child(spc)
        return f"You've {ns} * {name}, each making a new {child_name} every {avg_steps} steps."

    def cost_string_from_spcode(self, spc: int) -> str:
        return f'[cost = ${self.cost(spc).string()}]'

    def cost(self, spc: int) -> Dollars:
        return self.spec(spc).cost()

    def child_name(self, spc: int) -> str:
        return self.specs().child_name(spc)

    def steps(self) -> int:
        return self.m_steps

    def decrement_dollars(self, cost: Dollars):
        self.m_dollars = Dollars(self.dollars().int() - cost.int())


def specs_empty():
    return Specs([])


def spec_non_dollar(name, cost: Dollars, steps_to_make_child: int, ch: Child):
    return Spec(name, cost, steps_to_make_child, maybechild_defined(ch))


def specs_default():
    result = specs_empty()
    result.add_with_dollar_child('printer', 20, 5)
    result.add_with_dollar_child('laserjet', 50, 2)
    result.add_with_non_dollar_child('maker', 2000, 30, 'laserjet')
    result.add_with_non_dollar_child('factory', 60000, 15, 'maker')
    result.add_with_non_dollar_child('plant', 500000, 20, 'factory')
    result.add_with_non_dollar_child('mega', 9000000, 30, 'plant')
    return result


def spates_default(sps: Specs) -> Spates:
    result = spates_create(sps.num_spcodes())
    printer_spcode, ok = sps.spcode_from_string('printer')
    assert ok
    result.add(printer_spcode, 1)
    return result


def game_default() -> Game:
    sps = specs_default()
    sts = spates_default(sps)
    return Game(1, sps, Dollars(0), sts)


def run_accumulate_game():
    g = game_default()
    g.run()
