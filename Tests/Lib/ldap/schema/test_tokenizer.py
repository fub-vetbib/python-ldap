import ldap.schema
from ldap.schema.tokenizer import split_tokens,extract_tokens

testcases_split_tokens = (
  ("BLUBBER DI BLUBB",["BLUBBER","DI","BLUBB"]),
  ("BLUBBER  DI   BLUBB  ",["BLUBBER","DI","BLUBB"]),
  ("BLUBBER  DI  'BLUBB'   ",["BLUBBER","DI","BLUBB"]),
  ("BLUBBER ( DI ) 'BLUBB'   ",["BLUBBER","(","DI",")","BLUBB"]),
  ("BLUBBER(DI)",["BLUBBER","(","DI",")"]),
  ("BLUBBER ( DI)",["BLUBBER","(","DI",")"]),
  ("BLUBBER ''",["BLUBBER",""]),
  ("( BLUBBER (DI 'BLUBB'))",["(","BLUBBER","(","DI","BLUBB",")",")"]),
  ("BLUBB DI 'BLU B B ER' DA 'BLAH' ",['BLUBB','DI','BLU B B ER','DA','BLAH']),
  ("BLUBB DI 'BLU B B ER' DA 'BLAH' LABER",['BLUBB','DI','BLU B B ER','DA','BLAH','LABER']),
)

for t,r in testcases_split_tokens:
  l = ldap.schema.tokenizer.split_tokens(t)
  if l!=r:
    print 'String:',repr(t)
    print '=>',l
    print 'differs from',r