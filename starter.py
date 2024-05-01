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
    result = fds
    # reflexivityDeps = reflexivity(attrs)
    # for i in reflexivityDeps:
    #     result.add(i)

    oldResult = fdset()
    while result != oldResult:
        oldResult = result.copy()

        augResults = augmentation(attrs, result)
        for i in augResults:
            result.add(i)

        transitiveDeps = transitivity(result)
        for i in transitiveDeps:
            result.add(i)

    return result

def attributeClosure(attr, fds):
    result = attr
    #print(type(result))
    oldResult = None
    while result != oldResult:
        oldResult = result.copy()
        for dep in fds:
            #print(dep.LHS.issubset(result))
            #print(dep)
            #print(dep.LHS," is a subset of ",result)
            if dep.LHS.issubset(result):
                #print("Here")
                result = atset(list(result) + list(dep.RHS))
    #print("Post ", result)
    return atset(result)


def bcnf(reln, fds) -> relnset:
    '''Given a relation represented as set of attributes (atset) and a set of
    functional dependencies (fdset), produce a set of relations that represents
    the BCNF decomposition of the original relation.'''
    counter = 0
    result = relnset()
    result.add(reln)
    changes = True
    resultOld = None
    relationQueue = []
    for relation in result:
        relationQueue.append(relation)
    while relationQueue:
        relation = relationQueue.pop()
        print("Relation being decomposed ",relation)
        resultOld = result.copy()
        for dep in fds:
            if (not dep.RHS.issubset(dep.LHS)) and (not relation.issubset(attributeClosure(dep.LHS, fds))) and (dep.RHS.issubset(relation)) and (dep.LHS.issubset(relation)):
                print(dep)
                print("LHS closure", attributeClosure(dep.LHS, fds))
                counter += 1
                print("counter ", counter)
                result.remove(relation)
                relation = relation - dep.RHS
                new_relation = atset(list(dep.RHS) + list(dep.LHS))
                relationQueue.append(relation)
                relationQueue.append(new_relation)
                if result == None:
                    result = relnset()
                result.add(atset(relation))
                result.add(new_relation)
                if result != resultOld:
                    changes = True
                    break
            if counter == 3:
                break
            if not changes:
                break
        if counter == 3:
            break
    return result

#Gets all of the possible subsets from a series of attributes
def subsets(attributes):
    '''Copied (and slightly adapted) from https://neetcode.io/practice
    Watched the video at https://www.youtube.com/watch?v=REOH22Xwdkk&ab_channel=NeetCode
    to understand the logic. All the code was design and mostly written by Neetcode
    '''
    #This is our powerset (i.e.) all subsets of our attributes
    powerset = []

    subsets = []

    #This is a recursive DFS that goes through all possibilities of
    #Including and not including each attribute through a decision 
    #tree Putting it into our result
    def decisionTree(i):
        if i >= len(attributes):
            #Prevents from adding the empty array
            if len(subsets) != 0:
                powerset.append(subsets.copy())
            return
        # decision to include nums[i]
        subsets.append(attributes[i])
        decisionTree(i + 1)
        # decision NOT to include nums[i]
        subsets.pop()
        decisionTree(i + 1)

    decisionTree(0)
    return powerset

def reflexivity(attributes):
    powerset = subsets(attributes)
    alpha = set()
    for i in powerset:
        alpha.add(frozenset(i))
    beta = alpha.copy()
    fds = fdset()
    for b in beta:
        for a in alpha:
            if b.issubset(a):
                fds.add(fd(atset(a), atset(b)))
    return fds

def augmentation(attributes, deps):
    gammas = subsets(attributes)
    fds = fdset()
    for gamma in gammas:
        for dep in deps:
            Right_side = atset(gamma + list(dep.RHS))
            Left_side = atset(gamma + list(dep.LHS))
            fds.add(fd(Left_side, Right_side))
    return fds

def transitivity(deps):
    fds = fdset()
    fdsLenOld = -1
    while fdsLenOld != len(fds):
        fdsLenOld = len(fds)
        for beta in deps:
            for alpha in deps:
                right = beta.RHS
                left = alpha.LHS
                if right == left:
                    fds.add(fd(beta.LHS, alpha.RHS))
        for i in fds:
            deps.add(i)
    return fds




            


    


# def main() -> None:
#     attributes = atset([1, 2])
#     print("Some attributes:", attributes)

#     fds = fdset()
#     fds.add(fd(atset([1]), atset([2])))
#     fds.add(fd(atset([2]), atset([1])))
#     print("Some fds:")
#     print(fds)

#     result = closure(attributes, fds)
#     print("A closure:")
#     print(result)

#     decomp_result = bcnf(attributes, fds)
#     print("A decomposition:", decomp_result)


# if __name__ == "__main__":
#     main()

attrs = atset([1, 2, 3, 4, 5, 7])
fds = fdset()
fds.add(fd(atset([1]), atset([3, 4])))
fds.add(fd(atset([2]), atset([5])))
fds.add(fd(atset([3]), atset([4])))
fds.add(fd(atset([1, 2]), atset([1,2,3,4,5,7])))
res = bcnf(attrs, fds)
for i in res:
    print(i)
# print("Finally")
# for sti in a:
#     print(sti)

# set1 = {frozenset({1, 2}), frozenset({2, 3}), frozenset({3, 4})}
# set2 = {frozenset({2, 3}), frozenset({3, 4}), frozenset({4, 5})}
# set3 = {frozenset({3, 4}), frozenset({4, 5}), frozenset({5, 6})}

# # Perform subtraction on sets of frozensets
# result = set1 - set2 - set3
# print(result)  # Out
# fdTest = fdset()
# fdTest.add(fd(atset([1]), atset([3, 4])))
# attributeClosure(atset([1, 3, 4]), fdTest)