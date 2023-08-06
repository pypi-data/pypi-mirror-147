class Concat_Remove_Class:
    """
    Instantiate concat remove operation -- ConcatRemove (s, t, k) .
    Consider a string containing lowercase characters from the Portuguese alphabet. You can perform two types of operations on this string:

    Concat a lowercase character from the Portuguese alphabet at the end of the string.
    Remove the last character from the string. If the string is empty, it will remain empty.
    Given an integer k and two strings s and t, determine if you can convert s to t using exactly k operations described above on s.
    If possible, the program prints 'yes', otherwise it prints 'no'.

    For example, string s = [a, b, c] and string t = [d, e, f].
    The number of moves k = 6. To convert s to t, we first remove all characters using 3 moves.
    Then we concatenate each of the characters of t in the order.
    In the sixth move, you will have the expected string s.
    If more movements are available than necessary, they can be eliminated by performing multiple removals on an empty string.
    If there are fewer movements, it would not be possible to create the new string.

    :param s: The starting string.
    :type s: string

    :param t: the  desired string
    :type t: string

    :param k: the total number of movements to get from s to t
    :type k: int
    """

    def __init__(self, startingString, desiredString, moves):
        self.s = startingString
        self.t = desiredString
        self.k = moves

    def checkLower(self, string_analised):
        for element in string_analised:
            if not element.isalpha():
                print("## Not a string format ## ")
                return False
            if (element < 'a') or (element > 'z'):
                print("## " + element + " is Not a Lowercase String ##" )
                return False
        return True

    def __concatRemove(self):
        length_s = len(self.s)
        length_t = len(self.t)
        eq_pos = 0
        total_removal = 0
        total_concat = 0
        min_string = min(length_s, length_t)

        j = 0
        for ind in range(0, length_s):

            if ((self.s[ind] == self.t[j]) and j < min_string-1):
                #print(ind)
                eq_pos = eq_pos + 1
                j = j+1

        total_removal = min_string - eq_pos
        total_concat = min_string - eq_pos

        if (total_removal + total_concat > self.k):
            return False

        return True

    def getData(self):

        print("################################################")
        print("Instructions!!! Read with attention!!!")
        print("Constrains")
        print("a) 1 <= | s | <= 100")
        print("b) 1 <= | t | <= 100")
        print("c) 1 <= k <= 100")
        print("d) s and t consists of lowercase letters of the Portuguese alphabet, ascii [a-z]")

        aux1 = 0

        if ((len(self.s)>100) or (len(self.s) <1)) or (self.checkLower(self.s) == False):
            print("Remember: 1 <= | s | <= 100 and Portuguese alphabet, ascii [a-z]")
            return False
        elif ((len(self.t)>100) or (len(self.t) <1)) or (self.checkLower(self.t) == False):
            print("Remember: 1 <= | t | <= 100 and Portuguese alphabet, ascii [a-z]")
            return False
        elif (self.k > 100) or (self.k <1):
            print("The number of operations must be 1 <= k <= 100")

            return False
        else:
            retorno = self.__concatRemove()

            if retorno:
                print("YES")
            else:
                print("NO")

        return True
s = "blablablabla"
t = "blablab"
k = 8
multiplication = Concat_Remove_Class(s,t,k)

if(multiplication.getData() == "YES"):
    print(multiplication.getData())