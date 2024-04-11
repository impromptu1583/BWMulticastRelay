from tkinter import *
from tkinter import ttk
import requests, time
from scapy.all import send, IP, UDP

class Cm_matchmaker:

    def __init__(self, root):
        
        self.delay = 1000
        self.solicitation = bytes.fromhex("2a9c14000200000057424d4382ecf98f00000000")
        root.title("CMBW WAN Matchmaker")

        mainframe = ttk.Frame(root, padding="3 3 12 12")
        mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
       
        ttk.Label(mainframe, text="Host IP").grid(column=1, row=1, sticky=W)

        self.host_ip = StringVar()
        host_ip_entry = ttk.Entry(mainframe, width=15, textvariable=self.host_ip)
        host_ip_entry.grid(column=1,row=2, sticky=(W,E))

        ttk.Label(mainframe, text="Non-host player IPs").grid(column=2, row=1, sticky=W)
        
        self.logstring = StringVar()
        self.loglist = []
        ttk.Label(mainframe, text="Log:").grid(column=1, row=4, sticky=(N,W))        
        ttk.Label(mainframe, textvariable=self.logstring).grid(column=1, row=5, rowspan=4, sticky=(N,W))                
        
        self.player_ips = []
        self.player_entries = []
        for i in range(0,7):
            self.player_ips.append(StringVar())
            self.player_entries.append(ttk.Entry(mainframe, width=15, textvariable=self.player_ips[i]))
            self.player_entries[i].grid(column=2,row=i+2,sticky=(W,E))
        
#        ttk.Button(mainframe, text="Get Current", command=
        
        ttk.Button(mainframe, text="Get WAN IP", command=self.get_wan_ip).grid(column=1, row=3, sticky=W)
        self.startstop = ttk.Button(mainframe, text="Start", command=self.start)
        self.startstop.grid(column=1, row=8, sticky=(S,W))
        for child in mainframe.winfo_children(): 
            child.grid_configure(padx=5, pady=5)

        host_ip_entry.focus()
        self.add_log('loaded, press start to begin')
        self.interrupt = False
        
##        root.bind("<Return>", self.calculate)

    def add_log(self,log_text):
        self.loglist.append(log_text)
        self.logstring.set('\n'.join(self.loglist[-5:]))
        
    def get_wan_ip(self, *args):
        try:
            response = requests.get('https://httpbin.org/ip')
            if response.status_code == 200:
                ip_data = response.json()
                self.host_ip.set(ip_data.get('origin'))
                self.add_log(f'identified WAN IP as {self.host_ip.get()}')
            else: 
                print(f"Failed to retrieve IP (Status code: {response.status_code})") 
        except Exception as e:
            print(f"Error: {e}")

    def start(self, *args):
        #todo check data
        self.startstop.configure(text='Stop', command=self.stop)
        self.interrupt = False
        root.after(1,self.send_solicitation)
        
    
    def send_solicitation(self, *args):
        if self.interrupt:
            return
        t = time.localtime()
        self.add_log(f"Sending Solicitation ({t.tm_hour}:{t.tm_min}:{t.tm_sec})")
        try:            
            for ip in self.player_ips:
                # todo add error checking lol
                send(IP(src=ip.get(),dst=self.host_ip.get())/UDP(sport=6111,dport=6111)/self.solicitation)
        except Exception as e:
            print(f"error: {e}")
            
        # need to capture return packet and spoof wan IP
            
        root.after(self.delay,self.send_solicitation)
    
    def stop(self, *args):
        self.interrupt = True
        self.startstop.configure(text='Start', command=self.start)

root = Tk()
Cm_matchmaker(root)
root.mainloop()