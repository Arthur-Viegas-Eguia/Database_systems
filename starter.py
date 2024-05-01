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

#We generate the closure of a relation
def closure(attrs: atset, fds: fdset) -> fdset:
    result = fds

    #We start by creating all of the trivial dependencies
    #through the reflexivity rule
    reflexivityDeps = reflexivity(attrs)
    #Parsing results
    for i in reflexivityDeps:
        result.add(i)

    #We use this to keep track of the changes in the result
    #Once there were no changes, then we found all functional
    #Dependencies
    oldResult = fdset()
    while result != oldResult:
        oldResult = result.copy()

        #We generate all the possible functional dependencies 
        #given an attribute set and functional dependencies
        #through augmentation
        augResults = augmentation(attrs, result)
        #parsing results
        for i in augResults:
            result.add(i)

        #We generate all the possible functional dependencies 
        #given an attribute set and functional dependencies
        #Through transitivity
        transitiveDeps = transitivity(result)
        #Parsing the results
        for i in transitiveDeps:
            result.add(i)

    return result

#Creates the attribute closure of one attribute based on
#The attributes and the set of functional dependencies
def attributeClosure(attr, fds):
    #Our initial set of attributes
    result = attr

    #We are only stopping iterating once we have
    #found all the attributes that depend on alpha
    #In other words, when our result does not change
    oldResult = None
    while result != oldResult:
        oldResult = result.copy()
        #If the left hand side of a functional dependency is
        #contained within the right hand side of it, adds it
        #To the attribute closure
        for dep in fds:
            if dep.LHS.issubset(result):
                result = atset(list(result) + list(dep.RHS))
    return atset(result)


def bcnf(reln, fds) -> relnset:
    '''Given a relation represented as set of attributes (atset) and a set of
    functional dependencies (fdset), produces a set of relations that represents
    the BCNF decomposition of the original relation.'''
    #Creates a relation  set and adds one relation
    result = relnset()
    result.add(reln)

    #Puts all the relations in a queue, we are using this
    #to iterate through all of the relations, adding and 
    #popping relations to/from a queue in the loop. It is 
    #hard doing it with a regular for loop.
    relationQueue = []
    for relation in result:
        relationQueue.append(relation)

    #We iterate until we have decomposed all tables.
    while relationQueue:
        #Getting the relation to be decomposed
        relation = relationQueue.pop()
        print("Relation being decomposed ",relation)
        #Iterates through all dependencies, foer each one of the relations
        for dep in fds:
            #If the dependency does not involve a key and is not trivial, decomposes the relation
            if (not dep.RHS.issubset(dep.LHS)) and (not relation.issubset(attributeClosure(dep.LHS, fds))) and (dep.RHS.issubset(relation)) and (dep.LHS.issubset(relation)):
                print(dep)
                #Decomposes the relation into BCNF
                result.remove(relation)
                relation = relation - dep.RHS
                new_relation = atset(list(dep.RHS) + list(dep.LHS))
                #Adds the new relations to be decomposed to our queue
                relationQueue.append(relation)
                relationQueue.append(new_relation)
                #Prints the results
                print("Resulting relations are ", atset(relation), " and ", new_relation)
                result.add(atset(relation))
                result.add(new_relation)
                #If we have changed something, we break as we no longer have
                #the original relation in the queue
                break
    return result

#Gets all of the possible subsets from a series of attributes
def subsets(attributes):
    '''Copied (and slightly adapted) from https://neetcode.io/practice
    Watched the video at https://www.youtube.com/watch?v=REOH22Xwdkk&ab_channel=NeetCode
    to understand the logic. All the code was design and mostly written by Neetcode
    ''' 
    #We need to do some parsing to prevent errors
    attributes = list(attributes)


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

#Generates all the trivial dependencies through the reflexivity rule
def reflexivity(attributes):
    #Generates all the subsets of our attributes
    powerset = subsets(attributes)
    
    #Converts the output of our subsets function to the
    #appropriate type, to prevent errors
    alpha = set()
    for i in powerset:
        alpha.add(frozenset(i))

    beta = alpha.copy()
    fds = fdset()

    #Checks is an attribute b is a subset of alpha
    for b in beta:
        for a in alpha:
            if b.issubset(a):
                #If that is the case, it  is a trivial dependency, so it is added to our fds
                fds.add(fd(atset(a), atset(b)))
    return fds

#Generates all possible functional dependencies through augmentation
def augmentation(attributes, deps):
    #Generates all the subsets of our attributes
    gammas = subsets(attributes)
    fds = fdset()

    #Adds all the subsets, to both sides of our FDs, generating
    #All possible functional dependencies through augmentation
    for gamma in gammas:
        for dep in deps:
            Right_side = atset(gamma + list(dep.RHS))
            Left_side = atset(gamma + list(dep.LHS))
            fds.add(fd(Left_side, Right_side))

    return fds

#Generates all functional dependencies through transitivity
#if a->b, b->c, then a->c
def transitivity(deps):
    fds = fdset()

    #We are using  the size of our functional dependency set to know
    #When we have found all possible functional dependencies through transitivity
    #We start it to -1 as we must iterate through all dependencies at least once
    fdsLenOld = -1
    while fdsLenOld != len(fds):
        fdsLenOld = len(fds)
        #We iterate through all of the right hand sides of all the functional dependencies
        #if they are also a left hand side of another dependency, this implies the transitivity rule
        for beta in deps:
            for alpha in deps:
                #In which case, we add it to the set of dependencies
                right = beta.RHS
                left = alpha.LHS
                if right == left:
                    fds.add(fd(beta.LHS, alpha.RHS))
        
        #Formats the data
        for i in fds:
            deps.add(i)
    return fds

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
