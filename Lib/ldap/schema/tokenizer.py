"""
ldap.schema.tokenizer - Low-level parsing functions for schema element strings
written by Michael Stroeder <michael@stroeder.com>

See http://python-ldap.sourceforge.net for details.

\$Id$
"""


def split_tokens(s,keywordDict):
  # First step: divide the string into tokens at each space character

  tokenList = s.split(" ")
  
  # Split parenthesises correctly from other strings
  tmpList = []
  stringList = []
  for x in tokenList:
    if ("(" in x) or (")" in x):
      for y in x:
        if "(" == y:
          tmpList.append("".join(stringList))
          tmpList.append(y)
          stringList = []
        elif ")" == y:
          tmpList.append("".join(stringList))
          tmpList.append(y)
          stringList = []
        else:
          stringList.append(y)
    else:
      tmpList.append(x)
        
    if len(stringList) > 0:
      tmpList.append("".join(stringList))
      stringList = []
        
  tokenList = tmpList
  

  # Second step: Strip colons and put eventual descriptions together
  # The iterate through the token list and append the items to resultList.
  # If we have a "'" at the beginning of a token, a description starts. We 
  # iterate further until we find the end of the description. 
  length = len(tokenList)
  pos = 0
  begin = 0
  resultList = []
  
  # Indicates if we concatenate description tokens
  inDesc = 0
  
  # List of tokens which represent the whole description.
  descList = []
  while pos < length:
    # Get token string
    tmpString = tokenList[pos]

    # Sometimes empty tokens appear. Ignore them and continue 
    # with the next token
    if 0 == len(tmpString):
      pos += 1
      continue

    # We are building a description
    if inDesc:

      # Do we have the end of a description?
      if tmpString[-1] == "'":
        descList.append(tmpString[:-1])
        resultList.append(''.join(descList))
        descList = []
        inDesc = 0
      else:
        # Sometimes Oracle has no spaces between keywords and descriptions.
        tmpList = tmpString.split("'")
        lastEl = tmpList[-1]
        if keywordDict.has_key(lastEl):
          descList.append("'".join(tmpList[:-1]))
          resultList.append(''.join(descList))
          resultList.append(lastEl)
          inDesc = 0
        else:
          descList.append(tmpString)


    # This one is done if we are not building a description
    else:

      # Test if a description starts
      if tmpString[0] == "'":

        # Test if description ends. If True, we have a complete description 
        # and can append it to the result list
        if tmpString[-1] == "'":
          resultList.append(tmpString[1:-1])

        # Description doesn't end right now, so we set the inDescription flag.
        else:
          inDesc = 1
          descList.append(tmpString[1:])
      else:
        resultList.append(tmpString)

    pos += 1

  # End of second step

  return resultList # split_tokens()



def extract_tokens(l,known_tokens):
  """
  Returns dictionary of known tokens with all values
  """
  assert l[0].strip()=="(" and l[-1].strip()==")",ValueError(l)
  result = {}
  result_has_key = result.has_key
  result.update(known_tokens)
  i = 0
  l_len = len(l)
  while i<l_len:
    if result_has_key(l[i]):
      token = l[i]
      i += 1 # Consume token
      if i<l_len:
        if result_has_key(l[i]):
          # non-valued
          result[token] = (())
        elif l[i]=="(":
          # multi-valued
          i += 1 # Consume left parentheses
          start = i
          while i<l_len and l[i]!=")":
            i += 1
          result[token] = tuple(filter(lambda v:v!='$',l[start:i]))
          i += 1 # Consume right parentheses
        else:
          # single-valued
          result[token] = l[i],
          i += 1 # Consume single value
    else:
      i += 1 # Consume unrecognized item
  return result

