from factordb.factordb import FactorDB as factordb
from time import perf_counter
import cypari,requests

def superscript(n):
    return "".join(["⁰¹²³⁴⁵⁶⁷⁸⁹"[ord(c) - ord('0')] for c in (n)])

def querystrip(query):
    if 'th' in query:
        num = query.replace('th', '')
        return (int(num))
    elif 'st' in query:
        num = query.replace('st', '')
        return (int(num))
    elif 'nd' in query:
        num = query.replace('nd', '')
        return (int(num))
    elif 'rd' in query:
        num = query.replace('rd', '')
        return (int(num))

def getstatus(n):
  f = factordb(n)
  f.connect()
  fact = f.get_factor_from_api()
  status = f.get_status()
  return (status,fact)

def fdbprint(n,fact):
  dp=0
  tp=0
  ans = "\n" + str(n) + " = "
  for i in range(0, len(fact)):
      dp = dp + 1
      ans = ans + str(fact[i][0])
      pow = fact[i][1]
      tp = tp + pow
      if (pow != 1):
          ans = ans + superscript("%d" % pow)
      if (i != len(fact) - 1):
          ans = ans + "×"
  if (tp == 1 and dp == 1):
      ans = "It is a Prime Number"
  elif (tp == dp):
      ans = ans + " (" + "%d" % tp + " distinct prime factors)"
  else:
      ans = ans + " (" + "%d" % tp + " prime factors, " + "%d" % dp + " distinct)"
  print(ans)

  
def bypari(num):
  flag=True
  while flag:
    try:
      cyp = cypari.pari('factor({})'.format(num))
      flag=False
    except:
      cypari.pari.allocatemem()
  dp = len(cyp[0])
  res = str(num) + " = "
  for i in range(0, len(cyp[0])):
      j = i
      res = res + str(cyp[0][i])
      if cyp[1][j] != 1:
          res = res
      if i != (dp - 1):
          res = res + "*"
  requests.get('http://www.factordb.com/report.php?report=%s'%res)

while True:
    query = input(
        "\nEnter a Positive Integer to factorize or Ordinal number to get the prime number: "
    )
    stopper = [
        '0', 'exit', 'Exit', 'EXIT', 'quit', 'Quit', 'QUIT', 'close', 'Close',
        'CLOSE'
    ]
    if query in stopper:
        break
    try:
        query = str(eval(query))
    except:
        pass
    st=perf_counter()
    if query.isdigit():
        n = int(query)
        st=perf_counter()
        bitcount = n.bit_length()
        dig=len(str(n))
        print("It is a %s bit number"%bitcount + " with %s digits"%dig)
        try :
            (status,fact)=getstatus(n)
            if status == "FF" or status == "P":
                fdbprint(n,fact)    
            elif status == "PRP":
              flag=True
              while flag:
                try:
                  if cypari.pari('isprime({})'.format(n))==1:
                    print("It is a Prime Number")
                  flag=False   
                except:
                  cypari.pari.allocatemem()

            elif status == "CF":
              bypari(int(fact[-1][0]))
              (status,fact)=getstatus(n)
              fdbprint(n,fact)
            else:
              bypari(n)
              (status,fact)=getstatus(n)
              fdbprint(n,fact)
        except:
            bypari(n)
            (status,fact)=getstatus(n)
            fdbprint(n,fact)
    else:
        try:
          m=querystrip(query)
          if m>1000000000000:
            print("Depending on your query, it may take time to execute")
            print(query, "prime number is",
                  cypari.pari('prime({})'.format(m)))
          else:
            r=requests.get('https://primes.utm.edu/nthprime/index.php?n=%s#nth'%m)
            ans=r.text[5530:5572]
            for i in [',','/','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','B','<','>',""]:
             ans=ans.replace(i,'')
            pn=""
            for k in ans:
             if k.isdigit():
              pn=pn+k
             if "." in k:
              break
            print("%s prime number is %s"%(query,int(pn)))
        except:
            print("Invalid Input")
    et=perf_counter()
    print("Execution time : ",et-st,"seconds")