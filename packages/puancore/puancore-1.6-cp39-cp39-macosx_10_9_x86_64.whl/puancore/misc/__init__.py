import base64
import gzip
import pickle
import typing
import functools
import operator

# misc functions
def pickable(data) -> bool:

    """
        True if data is picklable, else False.
        
        NOTE 
            function tries to dump data into nothing,
            which may be expensive calculation cost.

        Return:
            bool
    """
    try:
        pickle.dumps(data)
        return True
    except:
        return False

def pack_b64(data: typing.Any, str_decoding: str = 'utf8') -> str:

    """
        Packs data into a base64 string.

        Return:
            str
    """
    return base64.b64encode(
        gzip.compress(
            pickle.dumps(
                data,
                protocol=pickle.HIGHEST_PROTOCOL,
            ),
            mtime=0,
        )
    ).decode(str_decoding)

def unpack_b64(base64_str: str) -> typing.Any:

    """
        Unpacks base64 string `base64_str` into some data.

        base64_str: str

        Return:
            dict
    """
    return pickle.loads(
        gzip.decompress(
            base64.b64decode(
                base64_str.encode()
            )
        )
    )

def or_get(d: dict, keys: list, default_value = None) -> typing.Any:

    """
        # or_get
        is useful when you are not sure exactly
        how the keys looks like. You pass a list
        of candidate keys. The first that matches
        will be returned. If no match, then a
        KeyError exception is raised.

        :param d: dictionary
        :param keys: list of candidate keys
        :default value: value that is returned if no key matches (and default is not None)

        :return: value of d[k]
    """

    for k in keys:
        if k in d:
            return d[k]

    if default_value is not None:
        return default_value

    raise KeyError(keys)

def or_replace(d: dict, keys: list, value: typing.Any):
    """
        # or_replace
        will replace the first key value in keys
        that exists, with `value`. If no keys exists,
        KeyError is raised.

        :param d: dictionary
        :param keys: list of candidate keys
        :value: value that is set

        :return: value of d[k]
    """
    for k in keys:
        if k in d:
            d[k] = value
            return d

    raise KeyError(keys)

# --- State functions
def list2boolean_vector(lst: typing.List[str], context: typing.List[str]) -> typing.List[bool]:
    """
        Turns a list of strings into a boolean (0/1) vector.

        Example:
            Input:
                variables   = ["a","c","b"]
                context     = ["a","b","c","d"]

            Output:
                result      = [1,1,1,0]

        Return:
            list
    """
    return list(
        map(
            lambda x: 1*(x in lst),
            context
        )
    )

def list2integer_vector(lst: typing.List[str], context: typing.List[str]) -> typing.List[bool]:
    """
        Turns a list of strings into an integer vector, where each value represents
        which order the string in lst was positioned.

        Example:
            Input:
                variables   = ["a","c","b"]
                context     = ["a","b","c","d"]
                
            Output:
                result      = [1,3,2,0]

        Return:
            list
    """
    return list(
        map(
            lambda x: 1*(x in lst) and (1+lst.index(x)),
            context
        )
    )

def dict2vector(d: typing.Dict[str, bool], context: typing.List[str]) -> typing.List[int]:
    """
        Returns a vector of size |context| with a 1 on
        all keys in d with True and -1 on all keys in
        d with False. Context is a list of all possible string
        combinations allowed.

        - key in context:
            * d[key] == True    ===  1 
            * d[key] == False   === -1
        - key not in context    ===  0

        Example:
            Inputs:
                d       = {"a": True, "b": False, "d": True}
                domain  = ["a","b","c","d","e"]

            Output:
                [ 1,-1, 0, 1, 0]

        Return:
            list
    """
    return list(
        map(
            lambda k: 1*(k in d) and (1*d.get(k, False) + d.get(k, False)-1),
            context
        )
    )


# math misc functions
def factacc(P: list, n: int, c: int = 1) -> int:

    """
        "Factorial accumulate" (or "factacc" for short) is a
        recursive function which grows exponentially with respect
        to the numbers in P. `P` is a list of numbers, `n` and `c` is a number.
        E.g P = [6,3,8], n = 2 and c = 1, then result is

            8(6 + 3(6+1) + 1) = 224

        or described with arguments

            P[2](
                factacc(P,0,c) + factacc(P,1,c) + c
            )

        NOTE if P=[1,1,1,1,1], then factacc(P,4) == 2**4 == 16, i.e. results
            in [1,2,4,8,16] if iterating all i=0 up to len(P).

        Return:
            int (number)
    """

    if n <= 0:
        return P[n]

    return P[n]*(
        sum(
            map(lambda i: factacc(P, i, c), range(n))
        ) + c
    )

def factacc_series(P: list, c: int = 1) -> list:
    """
        Computes all P's with factacc as in
        factacc(P,i,c) for all i's in i=0 up to |P|.

        Return:
            List[number]
    """

    return [factacc(P, i, c) for i in range(len(P))]

