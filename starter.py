class atset(frozenset):
    '''A subclass of frozenset intended for storing a set of attributes.'''
    def __str__(self) -> str:
        result = ""
        for item in iter(self):
            result += str(item)
        result += ""
        return result


class fd:
    '''Class for storing a functional dependency, where the LHS and RHS are
    intendeded to each by atsets. This class is hashable, so it can be stored
    in a set of fds.
    '''
    def __init__(self, LHS: atset, RHS: atset):
        self.LHS = LHS
        self.RHS = RHS

    def __hash__(self) -> int:
        return hash(tuple((self.LHS, self.RHS)))

    def __eq__(self, other) -> bool:
        return self.LHS == other.LHS and self.RHS == other.RHS

    def __str__(self) -> str:
        return str(self.LHS) + " -> " + str(self.RHS)


class fdset(set):
    '''A subclass of set intended for storing a set of functional
    dependencies.'''
    def __str__(self) -> str:
        result = ""
        for item in iter(self):
            result += str(item) + "\n"
        return result


class relnset(set):
    '''A subclass of set intended for storing a set of relations. Relations are
    only just atsets, but they display differently when printing.'''
    def __str__(self) -> str:
        result = "{"
        for item in iter(self):
            result += str(item) + " "
        result += "}"
        return result


def closure(attrs: atset, fds: fdset) -> fdset:
    '''Given a set of attributes (atset) and a set of functional dependencies
    (fdset), produce a new set of functional dependencies (fdset) that
    represents the closure of the original fdset.'''

    return fds


def bcnf(reln, fds) -> relnset:
    '''Given a relation represented as set of attributes (atset) and a set of
    functional dependencies (fdset), produce a set of relations that represents
    the BCNF decomposition of the original relation.'''

    result = relnset()
    result.add(reln)
    return result


def main() -> None:
    attributes = atset([1, 2])
    print("Some attributes:", attributes)

    fds = fdset()
    fds.add(fd(atset([1]), atset([2])))
    fds.add(fd(atset([2]), atset([1])))
    print("Some fds:")
    print(fds)

    result = closure(attributes, fds)
    print("A closure:")
    print(result)

    decomp_result = bcnf(attributes, fds)
    print("A decomposition:", decomp_result)


if __name__ == "__main__":
    main()
