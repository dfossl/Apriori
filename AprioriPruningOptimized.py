import time

class AprioriPruningOptimized:
    """
    Computation class for calculating Apriori with a more optimal candidate selection
    """

    def __init__(self):
        pass

    @staticmethod
    def _gettransobjects(line: str):
        """
        Processes text line.
        Extracts transactions objects and size.
        :param line: Line of input text file.
        :return: tuple (set of trans objects, transaction size)
        """
        holder = line.split("\t")

        transobjects = frozenset(holder[2].split(" "))

        transize = int(holder[1])

        return transobjects, transize

    @staticmethod
    def _generatecandidates(currentsize, candidates_list, candidates_set):
        """
        Joins frequent sets of current size with each other only keeping
        candidates of proper size.
        :param currentsize: size (k) of candidates to generate
        :param candidates_list: list of minimum support sets size currentsize - 1
        :param candidates_set: set containing the same elements as candidates_list, used
                for imporved lookup time.
        :return:
        """
        group_list = set()

        i = 0

        while i < len(candidates_list):
            j = i + 1
            set_1 = candidates_list[i]
            while j < len(candidates_list):

                set_2 = candidates_list[j]

                holder = set_1.union(set_2)

                add = False
                if len(holder) == currentsize:
                    add = True
                    for x in holder:
                        """
                        If any of the currentsize - 1 combinations of the
                        union set are not candidates then we skip
                        """
                        if not holder.difference({x}) in candidates_set:
                            add = False
                            break
                if add:
                    group_list.add(holder)

                j += 1
            i += 1

        return group_list


    def _performsupportcount(self, currentsize: int, transobjects: frozenset, candidates: list, iternum: float):
        """
        Function performs the support count for a given transaction. It updates the running count table.
        :param currentsize: Is the size of the current candidates
        :param transobjects: A set that holds the transaction objects.
        :param candidates: A list of the potential candidates
        :param iternum: a number to iterate count by. equal to (1/number of transactions)
        """
        if currentsize == 1:

            self.keepTesting = True

            for val in transobjects:
                try:
                    self.countTable[currentsize][frozenset([val])] += iternum
                except KeyError:
                    self.countTable[currentsize][frozenset([val])] = iternum
        else:
            for test_set in candidates:

                if test_set.issubset(transobjects):

                    self.keepTesting = True

                    try:
                        self.countTable[currentsize][test_set] += iternum
                    except KeyError:
                        self.countTable[currentsize][test_set] = iternum


    def apriori(self, filename: str, minimumsup: float = 50):
        """
        Runs apriori algorithm over a txt file. Reads and processes transaction line by line.
        Modfies class result table variable.
        :param filename: filename/director for txt file.
        :param minimumsup: the minimum support threshold.
        :return:
        """
        start = time.time()


        self.filename = filename

        self.numberFrequentItemSets = 0

        """
        countTable holds current supports
        dict of dict
        key1 = size of rule, int
        key2 = rule, frozenset
        value = support, float
        """
        self.countTable = {}

        """
        result table hold all frequent sets and their supports
        """
        self.resultTable = {}

        self.minimumsup = minimumsup/100.

        candidates = []

        currentsize = 1

        self.keepTesting = True

        # While loop terminates when no more sets are frequent
        while self.keepTesting:

            file = open(self.filename, "r")

            # Reading first line for number of transactions
            self.trans_num = int(file.readline().rstrip())

            iternum = 1./self.trans_num

            self.countTable[currentsize] = {}

            self.keepTesting = False

            while True:
                line = file.readline().rstrip()

                # reached end of file
                if not line:
                    break

                transobjects, transize = self._gettransobjects(line)


                if currentsize <= transize:
                    self._performsupportcount(currentsize=currentsize,
                                             transobjects=transobjects,
                                             candidates=candidates,
                                             iternum=iternum)

            file.close()

            if not self.keepTesting:
                end = time.time()
                self.executiontime = end - start
                continue


            """
            This code iterates over countTable accomplishing 2 things:
            1: Fills Candidate list
            2: Constructs result Table
            """
            candidates_list = []
            candidates_set = set() # sets used for constant time look up
            self.resultTable[currentsize] = {}
            for key in self.countTable[currentsize]:
                if self.countTable[currentsize][key] >= (self.minimumsup):
                    self.resultTable[currentsize][key] = self.countTable[currentsize][key]
                    candidates_list.append(key)
                    candidates_set.add(key)
                    self.numberFrequentItemSets += 1




            currentsize += 1

            candidates = self._generatecandidates(currentsize=currentsize,
                                                  candidates_list=candidates_list,
                                                  candidates_set=candidates_set)

    def printterminal(self):
        """
        Prints number of frequent item sets and the execution time to system out.
        :return:
        """
        print(f"|FPs| = {self.numberFrequentItemSets}")
        print(f"Execution Time = {self.executiontime}s\n")

    @staticmethod
    def _frequentset_to_string(set_1):
        """
        Takes in a set and formats it as a string for output.
        :param set_1: Set to format
        :return: Takes set and formats a string.
        """

        if len(set_1) == 1:
            for item in set_1:
                return str(item)
        else:
            holder_str = ""
            for item in set_1:
                holder_str = holder_str + item + ", "
            return holder_str[:-2]


    def results_to_file(self, filename: str):
        """
        Saves formatted results in filename
        :return:
        """

        keylist = self._getfrequentsetsorted()

        file = open(filename, "w")

        file.write(f"|FPs| = {self.numberFrequentItemSets}\n")
        for size in self.resultTable:
            keylist[size].sort()
            for set_1 in keylist[size]:
                set_1 = list(map(str, set_1))
                file.write(f"{self._frequentset_to_string(set_1)} : {self.resultTable[size][frozenset(set_1)]}\n")

        file.close()


    def _getfrequentsetsorted(self):
        """
        Used for output file formatting. Sorts all the frequent sets.
        :return: returns dict that holds frequent sets as sorted lists
                for file print out
        """
        keylist = {}

        for key in self.resultTable:
            keylist[key] = []
            for f_set in self.resultTable[key]:
                holder = list(f_set)
                try:
                    holder = list(map(int, holder))
                except ValueError:
                    pass
                holder.sort()
                keylist[key].append(holder)
        return keylist
