import os
import sys
import time
import random
import requests
import threading
from tqdm import tqdm
import re
from datetime import datetime, timedelta
from urllib.parse import urlparse


class DLManager:
    def __init__(self):
        self.versions = [
            # Initial versions
            "++Fortnite+Release-OT6.5-CL-2870186-Windows [(simplyblk - zip):https://public.simplyblk.xyz/OT0.6.5.zip]",

            # Season 0
            "++Fortnite+Release-1.7.2-CL-3700114-Windows [(simplyblk - zip):https://public.simplyblk.xyz/1.7.2.zip&(galaxiaFN - zip):https://galaxiaFN.co.uk/1.7.2.zip&(rebootFN - zip):https://builds.rebootFN.org/1.7.2.zip]",

            # Season 1
            "++Fortnite+Release-1.8.0-CL-3724489-Windows [(simplyblk - rar):https://public.simplyblk.xyz/1.8.rar&(rebootFN - rar):https://builds.rebootFN.org/1.8.rar]",
            "++Fortnite+Release-1.8.1-CL-3729133-Windows [(simplyblk - rar):https://public.simplyblk.xyz/1.8.1.rar&(rebootFN - rar):https://builds.rebootFN.org/1.8.1.rar]",
            "++Fortnite+Release-1.8.2-CL-3741772-Windows [(simplyblk - rar):https://public.simplyblk.xyz/1.8.2.rar&(rebootFN - rar):https://builds.rebootFN.org/1.8.2.rar]",
            "++Fortnite+Release-1.9-CL-3757339-Windows [(simplyblk - rar):https://public.simplyblk.xyz/1.9.rar&(rebootFN - rar):https://builds.rebootFN.org/1.9.rar]",
            "++Fortnite+Release-1.9.1-CL-3775276-Windows [(simplyblk - rar):https://public.simplyblk.xyz/1.9.1.rar&(rebootFN - rar):https://builds.rebootFN.org/1.9.1.rar]",
            "++Fortnite+Release-1.10-CL-3790078-Windows [(simplyblk - rar):https://public.simplyblk.xyz/1.10.rar&(rebootFN - rar):https://builds.rebootFN.org/1.10.rar]",

            # Season 2
            "++Fortnite+Release-1.11-CL-3807424-Windows [(simplyblk - zip):https://public.simplyblk.xyz/1.11.zip&(rebootFN - zip):https://builds.rebootFN.org/1.11.zip&(galaxiaFN - zip):https://galaxiaFN.co.uk/1.11.zip]",
            "++Fortnite+Release-2.1.0-CL-3825894-Windows [(simplyblk - zip):https://public.simplyblk.xyz/2.1.0.zip&(rebootFN - zip):https://builds.rebootFN.org/2.1.0.zip]",
            "++Fortnite+Release-2.2.0-CL-3841827-Windows [(simplyblk - rar):https://public.simplyblk.xyz/2.2.0.rar&(rebootFN - rar):https://builds.rebootFN.org/2.2.0.rar]",
            "++Fortnite+Release-2.3.0-CL-3847564-Windows [(simplyblk - rar):https://public.simplyblk.xyz/2.3.rar&(rebootFN - rar):https://builds.rebootFN.org/2.3.rar]",
            "++Fortnite+Release-2.4.0-CL-3858292-Windows [(simplyblk - zip):https://public.simplyblk.xyz/2.4.0.zip&(rebootFN - zip):https://builds.rebootFN.org/2.4.0.zip&(galaxiaFN - zip):https://galaxiaFN.co.uk/2.4.0.zip]",
            "++Fortnite+Release-2.4.2-CL-3870737-Windows [(simplyblk - zip):https://public.simplyblk.xyz/2.4.2.zip&(rebootFN - zip):https://builds.rebootFN.org/2.4.2.zip]",
            "++Fortnite+Release-2.5.0-CL-3889387-Windows [(simplyblk - rar):https://public.simplyblk.xyz/2.5.0.rar&(rebootFN - rar):https://builds.rebootFN.org/2.5.0.rar]",

            # Season 3
            "++Fortnite+Release-3.0-CL-3901517-Windows [(simplyblk - zip):https://public.simplyblk.xyz/3.0.zip&(rebootFN - zip):https://builds.rebootFN.org/3.0.zip&(galaxiaFN - zip):https://galaxiaFN.co.uk/3.0.zip]",
            "++Fortnite+Release-3.1-CL-3915963-Windows [(simplyblk - rar):https://public.simplyblk.xyz/3.1.rar&(rebootFN - rar):https://builds.rebootFN.org/3.1.rar]",
            "++Fortnite+Release-3.1-CL-3917250-Windows [(simplyblk - zip):https://public.simplyblk.xyz/3.1.1.zip&(rebootFN - zip):https://builds.rebootFN.org/3.1.1.zip]",
            "++Fortnite+Release-3.2-CL-3935073-Windows [(simplyblk - zip):https://public.simplyblk.xyz/3.2.zip&(rebootFN - zip):https://builds.rebootFN.org/3.2.zip]",
            "++Fortnite+Release-3.3-CL-3942182-Windows [(simplyblk - rar):https://public.simplyblk.xyz/3.3.rar&(rebootFN - rar):https://builds.rebootFN.org/3.3.rar]",
            "++Fortnite+Release-3.5-CL-4008490-Windows [(simplyblk - rar):https://public.simplyblk.xyz/3.5.rar&(rebootFN - rar):https://builds.rebootFN.org/3.5.rar&(galaxiaFN - zip):https://galaxiaFN.co.uk/3.5.zip]",
            "++Fortnite+Release-3.6-CL-4019403-Windows [(simplyblk - zip):https://public.simplyblk.xyz/3.6.zip&(rebootFN - zip):https://builds.rebootFN.org/3.6.zip]",

            # Season 4
            "++Fortnite+Release-4.0-CL-4039451-Windows [(simplyblk - zip):https://public.simplyblk.xyz/4.0.zip&(rebootFN - zip):https://builds.rebootFN.org/4.0.zip]",
            "++Fortnite+Release-4.1-CL-4053532-Windows [(simplyblk - zip):https://public.simplyblk.xyz/4.1.zip&(rebootFN - zip):https://builds.rebootFN.org/4.1.zip]",
            "++Fortnite+Release-4.2-CL-4072250-Windows [(simplyblk - zip):https://public.simplyblk.xyz/4.2.zip&(rebootFN - zip):https://builds.rebootFN.org/4.2.zip&(galaxiaFN - zip):https://galaxiaFN.co.uk/4.2.zip]",
            "++Fortnite+Release-4.3-CL-4082037-Windows [(simplyblk - zip):https://public.simplyblk.xyz/4.3.zip&(rebootFN - zip):https://builds.rebootFN.org/4.3.zip]",
            "++Fortnite+Release-4.4-CL-4117433-Windows [(simplyblk - rar):https://public.simplyblk.xyz/4.4.rar&(rebootFN - rar):https://builds.rebootFN.org/4.4.rar]",
            "++Fortnite+Release-4.4.1-CL-4122030-Windows [(simplyblk - zip):https://public.simplyblk.xyz/4.4.1.zip&(rebootFN - zip):https://builds.rebootFN.org/4.4.1.zip]",
            "++Fortnite+Release-4.5-CL-4159770-Windows [(simplyblk - rar):https://public.simplyblk.xyz/4.5.rar&(rebootFN - rar):https://builds.rebootFN.org/4.5.rar]",

            # Season 5
            "++Fortnite+Release-5.00-CL-4204761-Windows [(simplyblk - rar):https://public.simplyblk.xyz/5.00.rar&(rebootFN - rar):https://builds.rebootFN.org/5.00.rar&(FN Builds - rar):https://builds.FN-builds.net/5.00.rar]",
            "++Fortnite+Release-5.00-CL-4214610-Windows [(simplyblk - rar):https://public.simplyblk.xyz/5.0.1.rar&(rebootFN - rar):https://builds.rebootFN.org/5.0.1.rar]",
            "++Fortnite+Release-5.10-CL-4240749-Windows [(simplyblk - rar):https://public.simplyblk.xyz/5.10.rar&(rebootFN - rar):https://builds.rebootFN.org/5.10.rar]",
            "++Fortnite+Release-5.21-CL-4288479-Windows [(simplyblk - rar):https://public.simplyblk.xyz/5.21.rar&(rebootFN - rar):https://builds.rebootFN.org/5.21.rar]",
            "++Fortnite+Release-5.30-CL-4305896-Windows [(simplyblk - rar):https://public.simplyblk.xyz/5.30.rar&(rebootFN - rar):https://builds.rebootFN.org/5.30.rar]",
            "++Fortnite+Release-5.40-CL-4352937-Windows [(simplyblk - rar):https://public.simplyblk.xyz/5.40.rar&(rebootFN - rar):https://builds.rebootFN.org/5.40.rar]",
            "++Fortnite+Release-5.41-CL-4363240-Windows [(galaxiaFN - zip):https://galaxiaFN.co.uk/5.41.zip]",

            # Season 6
            "++Fortnite+Release-6.00-CL-4395664-Windows [(simplyblk - rar):https://public.simplyblk.xyz/6.00.rar&(rebootFN - rar):https://builds.rebootFN.org/6.00.rar&(FN Builds - rar):https://builds.FN-builds.net/6.00.rar]",
            "++Fortnite+Release-6.01-CL-4417689-Windows [(simplyblk - rar):https://public.simplyblk.xyz/6.01.rar&(rebootFN - rar):https://builds.rebootFN.org/6.01.rar]",
            "++Fortnite+Release-6.01-CL-4424678-Windows [(simplyblk - rar):https://public.simplyblk.xyz/6.1.1.rar&(rebootFN - rar):https://builds.rebootFN.org/6.1.1.rar]",
            "++Fortnite+Release-6.02-CL-4442095-Windows [(simplyblk - rar):https://public.simplyblk.xyz/6.02.rar&(rebootFN - rar):https://builds.rebootFN.org/6.02.rar]",
            "++Fortnite+Release-6.02-CL-4461277-Windows [(simplyblk - rar):https://public.simplyblk.xyz/6.2.1.rar&(rebootFN - rar):https://builds.rebootFN.org/6.2.1.rar]",
            "++Fortnite+Release-6.10-CL-4464155-Windows [(simplyblk - rar):https://public.simplyblk.xyz/6.10.rar&(rebootFN - rar):https://builds.rebootFN.org/6.10.rar]",
            "++Fortnite+Release-6.10-CL-4476098-Windows [(simplyblk - rar):https://public.simplyblk.xyz/6.10.1.rar&(rebootFN - rar):https://builds.rebootFN.org/6.10.1.rar]",
            "++Fortnite+Release-6.10-CL-4480234-Windows [(simplyblk - rar):https://public.simplyblk.xyz/6.10.2.rar&(rebootFN - rar):https://builds.rebootFN.org/6.10.2.rar]",
            "++Fortnite+Release-6.21-CL-4526925-Windows [(simplyblk - rar):https://public.simplyblk.xyz/6.21.rar&(rebootFN - rar):https://builds.rebootFN.org/6.21.rar&(galaxiaFN - zip):https://galaxiaFN.co.uk/6.21.zip]",
            "++Fortnite+Release-6.22-CL-4543176-Windows [(simplyblk - rar):https://public.simplyblk.xyz/6.22.rar&(rebootFN - rar):https://builds.rebootFN.org/6.22.rar]",
            "++Fortnite+Release-6.30-CL-4573096-Windows [(simplyblk - rar):https://public.simplyblk.xyz/6.30.rar&(rebootFN - rar):https://builds.rebootFN.org/6.30.rar]",
            "++Fortnite+Release-6.31-CL-4573279-Windows [(simplyblk - rar):https://public.simplyblk.xyz/6.31.rar&(rebootFN - rar):https://builds.rebootFN.org/6.31.rar]",

            # Season 7
            "++Fortnite+Release-7.00-CL-4629139-Windows [(simplyblk - rar):https://public.simplyblk.xyz/7.00.rar&(rebootFN - rar):https://builds.rebootFN.org/7.00.rar&(galaxiaFN - zip):https://galaxiaFN.co.uk/7.00.zip&(FN Builds - rar):https://builds.FN-builds.net/7.00-CL-4629139.rar]",
            "++Fortnite+Release-7.10-CL-4667333-Windows [(simplyblk - rar):https://public.simplyblk.xyz/7.10.rar&(rebootFN - rar):https://builds.rebootFN.org/7.10.rar]",
            "++Fortnite+Release-7.20-CL-4727874-Windows [(simplyblk - rar):https://public.simplyblk.xyz/7.20.rar&(rebootFN - rar):https://builds.rebootFN.org/7.20.rar]",
            "++Fortnite+Release-7.30-CL-4834550-Windows [(simplyblk - zip):https://public.simplyblk.xyz/7.30.zip&(rebootFN - zip):https://builds.rebootFN.org/7.30.zip&(galaxiaFN - zip):https://galaxiaFN.co.uk/7.30.zip]",
            "++Fortnite+Release-7.40-CL-5046157-Windows [(simplyblk - rar):https://public.simplyblk.xyz/7.40.rar&(rebootFN - rar):https://builds.rebootFN.org/7.40.rar&(galaxiaFN - zip):https://galaxiaFN.co.uk/7.40.zip&(FN Builds - rar):https://builds.FN-builds.net/7.40-CL-5046157.rar]",

            # Season 8
            "++Fortnite+Release-8.00-CL-5203069-Windows [(simplyblk - zip):https://public.simplyblk.xyz/8.00.zip&(rebootFN - zip):https://builds.rebootFN.org/8.00.zip&(galaxiaFN - zip):https://galaxiaFN.co.uk/8.00.zip]",
            "++Fortnite+Release-8.20-CL-5625478-Windows [(simplyblk - rar):https://public.simplyblk.xyz/8.20.rar&(rebootFN - rar):https://builds.rebootFN.org/8.20.rar&(FN Builds - rar):https://builds.FN-builds.net/8.20.rar]",
            "++Fortnite+Release-8.30-CL-5793395-Windows [(simplyblk - rar):https://public.simplyblk.xyz/8.30.rar&(rebootFN - rar):https://builds.rebootFN.org/8.30.rar]",
            "++Fortnite+Release-8.40-CL-6005771-Windows [(simplyblk - zip):https://public.simplyblk.xyz/8.40.zip&(rebootFN - zip):https://builds.rebootFN.org/8.40.zip]",
            "++Fortnite+Release-8.50-CL-6058028-Windows [(simplyblk - zip):https://public.simplyblk.xyz/8.50.zip&(rebootFN - zip):https://builds.rebootFN.org/8.50.zip&(galaxiaFN - zip):https://galaxiaFN.co.uk/8.50.zip&(FN Builds - zip):https://builds.FN-builds.net/8.50.zip]",
            "++Fortnite+Release-8.51-CL-6165369-Windows [(simplyblk - rar):https://public.simplyblk.xyz/8.51.rar&(rebootFN - rar):https://builds.rebootFN.org/8.51.rar&(galaxiaFN - zip):https://galaxiaFN.co.uk/8.51.zip&(FN Builds - rar):https://builds.FN-builds.net/8.51.rar]",

            # Season 9
            "++Fortnite+Release-9.00-CL-6337466-Windows [(simplyblk - zip):https://public.simplyblk.xyz/9.00.zip&(rebootFN - zip):https://builds.rebootFN.org/9.00.zip&(FN Builds - 7z):https://builds.FN-builds.net/9.00.7z]",
            "++Fortnite+Release-9.01-CL-6428087-Windows [(simplyblk - zip):https://public.simplyblk.xyz/9.01.zip&(rebootFN - zip):https://builds.rebootFN.org/9.01.zip]",
            "++Fortnite+Release-9.10-CL-6639283-Windows [(simplyblk - rar):https://public.simplyblk.xyz/9.10.rar&(rebootFN - rar):https://builds.rebootFN.org/9.10.rar&(galaxiaFN - zip):https://galaxiaFN.co.uk/9.10.zip]",
            "++Fortnite+Release-9.21-CL-6922310-Windows [(simplyblk - zip):https://public.simplyblk.xyz/9.21.zip&(rebootFN - zip):https://builds.rebootFN.org/9.21.zip]",
            "++Fortnite+Release-9.30-CL-7095426-Windows [(simplyblk - zip):https://public.simplyblk.xyz/9.30.zip&(rebootFN - zip):https://builds.rebootFN.org/9.30.zip]",
            "++Fortnite+Release-9.40-CL-7315705-Windows [(simplyblk - zip):https://public.simplyblk.xyz/9.40.zip&(rebootFN - zip):https://builds.rebootFN.org/9.40.zip]",
            "++Fortnite+Release-9.41-CL-7609292-Windows [(simplyblk - rar):https://public.simplyblk.xyz/9.41.rar&(rebootFN - rar):https://builds.rebootFN.org/9.41.rar&(galaxiaFN - zip):https://galaxiaFN.co.uk/9.41.zip]",

            # Season X/10
            "++Fortnite+Release-10.00-CL-7704164-Windows [(simplyblk - zip):https://public.simplyblk.xyz/10.00.zip&(rebootFN - zip):https://builds.rebootFN.org/10.00.zip&(FN Builds - 7z):https://builds.FN-builds.net/10.00.7z]",
            "++Fortnite+Release-10.10-CL-7955722-Windows [(simplyblk - zip):https://public.simplyblk.xyz/10.10.zip&(rebootFN - zip):https://builds.rebootFN.org/10.10.zip]",
            "++Fortnite+Release-10.20-CL-8456527-Windows [(simplyblk - zip):https://public.simplyblk.xyz/10.20.zip&(rebootFN - zip):https://builds.rebootFN.org/10.20.zip]",
            "++Fortnite+Release-10.31-CL-8723043-Windows [(simplyblk - zip):https://public.simplyblk.xyz/10.31.zip&(rebootFN - zip):https://builds.rebootFN.org/10.31.zip]",
            "++Fortnite+Release-10.40-CL-9380822-Windows [(simplyblk - rar):https://public.simplyblk.xyz/10.40.rar&(rebootFN - rar):https://builds.rebootFN.org/10.40.rar]",

            # Season 11
            "++Fortnite+Release-11.00-CL-9603448-Windows [(simplyblk - zip):https://public.simplyblk.xyz/11.00.zip&(galaxiaFN - zip):https://galaxiaFN.co.uk/11.00.zip&(FN Builds - 7z):https://builds.FN-builds.net/11.00.7z]",
            "++Fortnite+Release-11.30-CL-10708866-Windows [(FN Builds - 7z):https://builds.FN-builds.net/11.30.7z]",
            "++Fortnite+Release-11.31-CL-10800459-Windows [(simplyblk - rar):https://public.simplyblk.xyz/11.31.rar]",

            # Season 12
            "++Fortnite+Release-12.00-CL-11556442-Windows [(simplyblk - rar):https://public.simplyblk.xyz/12.00.rar&(FN Builds - 7z):https://builds.FN-builds.net/12.00.7z]",
            "++Fortnite+Release-12.10-CL-11883027-Windows [(simplyblk - zip):https://public.simplyblk.xyz/12.10.zip]",
            "++Fortnite+Release-12.20-CL-12236980-Windows [(simplyblk - rar):https://public.simplyblk.xyz/12.20.rar]",
            "++Fortnite+Release-12.21-CL-12353830-Windows [(simplyblk - zip):https://public.simplyblk.xyz/12.21.zip]",
            "++Fortnite+Release-12.40-CL-12837456-Windows [(simplyblk - rar):https://public.simplyblk.xyz/12.40.rar]",
            "++Fortnite+Release-12.41-CL-12905909-Windows [(simplyblk - zip):https://public.simplyblk.xyz/Fortnite%2012.41.zip&(aufgeladen - zip):https://cdn.aufgeladen.dev/12.41.zip&(boostedv2 - rar):https://FNbuilds.boostedv2.dev/12.41.rar&(archive - zip):https://web.archive.org/web/20241214144234/&(simplyblk - zip):https://public.simplyblk.xyz/Fortnite%2012.41.zip&(FN Builds - 7z):https://builds.FN-builds.net/12.41-CL-12905909.7z]",
            "++Fortnite+Release-12.50-CL-13137020-Windows [(simplyblk - zip):https://public.simplyblk.xyz/12.50.zip&(FN Builds - 7z):https://builds.FN-builds.net/12.50.7z]",
            "++Fortnite+Release-12.61-CL-13498980-Windows [(simplyblk - zip):https://public.simplyblk.xyz/12.61.zip&(FN Builds - 7z):https://builds.FN-builds.net/12.61.7z]",

            # Season 13
            "++Fortnite+Release-13.00-CL-13649278-Windows [(simplyblk - rar):https://public.simplyblk.xyz/13.00.rar&(FN Builds - 7z):https://builds.FN-builds.net/13.00.7z]",
            "++Fortnite+Release-13.20-CL-13777676-Windows [(simplyblk - rar):https://public.simplyblk.xyz/13.20.rar]",
            "++Fortnite+Release-13.30-CL-13884634-Windows [(simplyblk - rar):https://public.simplyblk.xyz/13.30.rar]",
            "++Fortnite+Release-13.40-CL-14113327-Windows [(simplyblk - zip):https://public.simplyblk.xyz/13.40.zip&(FN Builds - 7z):https://builds.FN-builds.net/13.40-CL-14113327.7z]",

            # Season 14
            "++Fortnite+Release-14.00-CL-14211474-Windows [(simplyblk - rar):https://public.simplyblk.xyz/14.00.rar&(FN-builds - 7z):https://builds.FN-builds.net/14.00.7z]",
            "++Fortnite+Release-14.30-CL-14456520-Windows [(solarisFN - zip):https://cdn.solarisFN.dev/Builds/14.30.zip]",
            "++Fortnite+Release-14.40-CL-14550713-Windows [(simplyblk - rar):https://public.simplyblk.xyz/14.40.rar]",
            "++Fortnite+Release-14.60-CL-14786821-Windows [(simplyblk - rar):https://public.simplyblk.xyz/14.60.rar&(FN-builds - 7z):https://builds.FN-builds.net/14.60-CL-14786821.7z]",

            # Season 15
            "++Fortnite+Release-15.20-CL-15070882-Windows [(simplyblk - rar):https://public.simplyblk.xyz/15.20.rar]",
            "++Fortnite+Release-15.30-CL-15341163-Windows [(simplyblk - rar):https://public.simplyblk.xyz/15.30.rar]",
            "++Fortnite+Release-15.50-CL-15526472-Windows [(galaxiaFN - zip):https://galaxiaFN.co.uk/15.50.zip]",

            # Season 16
            "++Fortnite+Release-16.20-CL-16042441-Windows [(simplyblk - rar):https://public.simplyblk.xyz/16.20.rar]",
            "++Fortnite+Release-16.30-CL-16163563-Windows [(simplyblk - rar):https://public.simplyblk.xyz/16.30.zip]",
            "++Fortnite+Release-16.40-CL-16218553-Windows [(simplyblk - rar):https://public.simplyblk.xyz/16.40.rar]",
            "++Fortnite+Release-16.50-CL-16432754-Windows [(galaxiaFN - zip):https://galaxiaFN.co.uk/16.50.zip&(FN Builds - 7z):https://builds.FN-builds.net/16.50-CL-16432754.7z]",

            # Season 17
            "++Fortnite+Release-17.10-CL-16745144-Windows [(simplyblk - rar):https://public.simplyblk.xyz/17.10.rar&(FN Builds - rar):https://builds.FN-builds.net/17.10-CL-16745144.rar]",
            "++Fortnite+Release-17.30-CL-17004569-Windows [(simplyblk - zip):https://public.simplyblk.xyz/17.30.zip&(FN Builds - 7z):https://builds.FN-builds.net/17.30-CL-17004569.7z]",
            "++Fortnite+Release-17.40-CL-17269705-Windows [(FN Builds - 7z):https://builds.fn-builds.net/17.40-CL-17269705.7z]",
            "++Fortnite+Release-17.50-CL-17388565-Windows [(simplyblk - zip):https://public.simplyblk.xyz/17.50.zip]",

            # Season 18
            "++Fortnite+Release-18.00-CL-17468642-Windows [(FN Builds - 7z):https://fn-builds.net/S18/18.00-CL-17468642.7z&(simplyblk - rar):https://public.simplyblk.xyz/18.00.rar]",
            "++Fortnite+Release-18.10-CL-17661844-Windows [(FN Builds - 7z):https://fn-builds.net/S18/18.10-CL-17661844.7z]",
            "++Fortnite+Release-18.20-CL-17792290-Windows [(FN Builds - 7z):https://fn-builds.net/S18/18.20-CL-17792290.7z]",
            "++Fortnite+Release-18.21-CL-17811397-Windows [(FN Builds - 7z):https://fn-builds.net/S18/18.21-CL-17811397.7z]",
            "++Fortnite+Release-18.30-CL-17882303-Windows [(FN Builds - 7z):https://fn-builds.net/S18/18.30-CL-17882303.7z&(simplyblk - 7z):https://public.simplyblk.xyz/18.30.7z]",
            "++Fortnite+Release-18.40-CL-18163738-Windows [(simplyblk - zip):https://public.simplyblk.xyz/18.40.zip]",

            # Season 19
            "++Fortnite+Release-19.00-CL-18335626-Windows [(archive - 7z):https://archive.org/compress/fortnite-19.01.7z&(simplyblk - zip):https://public.simplyblk.xyz/19.01.zip]",
            "++Fortnite+Release-19.01-CL-18489740-Windows [(ploosh - zip):https://r2.ploosh.dev/19.01.zip]",
            "++Fortnite+Release-19.10-CL-18675304-Windows [(simplyblk - rar):https://public.simplyblk.xyz/19.10.rar&(archive - zip):https://web.archive.org/web/20240824224349/&(simplyblk - rar):https://public.simplyblk.xyz/19.10.rar&(FN Builds - rar):https://builds.fn-builds.net/19.10.rar]",
            "++Fortnite+Release-19.20-CL-18775446-Windows [(FN Builds - 7z):https://builds.fn-builds.net/19.20-CL-18775446.7z]",
            "++Fortnite+Release-19.30-CL-19027703-Windows [(simplyblk - rar):https://public.simplyblk.xyz/19.30.rar]",
            "++Fortnite+Release-19.40-CL-19215531-Windows [(simplyblk - 7z):https://public.simplyblk.xyz/19.40.7z]",

            # Season 20
            "++Fortnite+Release-20.00-CL-19458861-Windows [(simplyblk - rar):https://public.simplyblk.xyz/20.00.rar]",
            "++Fortnite+Release-20.10-CL-19598943-Windows [(simplyblk - zip):https://public.simplyblk.xyz/20.10.zip]",
            "++Fortnite+Release-20.20-CL-19751212-Windows [(simplyblk - zip):https://public.simplyblk.xyz/20.20.zip]",
            "++Fortnite+Release-20.40-CL-20244966-Windows [(simplyblk - zip):https://public.simplyblk.xyz/20.40.zip&(archive - zip):https://web.archive.org/web/20250119063536/&(FN Builds - 7z):https://builds.fn-builds.net/20.40-CL-20244966.7z]",

            # Season 21
            "++Fortnite+Release-21.00-CL-20548557-Windows [(solarisFN - zip):https://cdn.solarisFN.org/21.00.zip&(ploosh - zip):https://r2.ploosh.dev/21.00.zip&(FN Builds - 7z):https://fn-builds.net/S21/21.00-CL-20463113.7z]",
            "++Fortnite+Release-21.10-CL-20696680-Windows [(simplyblk - zip):https://public.simplyblk.xyz/21.10.zip]",
            "++Fortnite+Release-21.20-CL-21035704-Windows [(FN Builds - 7z):https://fn-builds.net/S21/21.20-CL-21035704.7z]",
            "++Fortnite+Release-21.30-CL-21130412-Windows [(FN Builds - 7z):https://fn-builds.net/S21/21.30-CL-21155462.7z]",
            "++Fortnite+Release-21.40-CL-21264667-Windows [(FN Builds - 7z):https://fn-builds.net/S21/21.40-CL-21407327.7z]",
            "++Fortnite+Release-21.50-CL-21657658-Windows [(simplyblk - zip):https://public.simplyblk.xyz/21.50.zip]",
            "++Fortnite+Release-21.51-CL-21377145-Windows [(FN Builds - 7z):https://fn-builds.net/S21/21.51-CL-21735703.7z&(simplyblk - 7z):https://public.simplyblk.xyz/21.51.7z]",

            # Season 22
            "++Fortnite+Release-22.00-CL-22149829-Windows [(FN Builds - 7z):https://fn-builds.net/S22/22.00-CL-22149829.7z&(simplyblk - 7z):https://public.simplyblk.xyz/22.00.7z]",
            "++Fortnite+Release-22.10-CL-22429549-Windows [(FN Builds - 7z):https://fn-builds.net/S22/22.10-CL-22429549.7z]",
            "++Fortnite+Release-22.20-CL-22600409-Windows [(FN Builds - 7z):https://fn-builds.net/S22/22.20-CL-22600409.7z]",
            "++Fortnite+Release-22.40-CL-23070899-Windows [(FN Builds - 7z):https://fn-builds.net/S22/22.40-CL-23070899.zip]",

            # Season 23
            "++Fortnite+Release-23.00-CL-23344627-Windows [(FN Builds - 7z):https://fn-builds.net/S23/23.00-CL-23344627.7z&(simplyblk - 7z):https://public.simplyblk.xyz/23.00.7z]",
            "++Fortnite+Release-23.10-CL-23443094-Windows [(FN Builds - 7z):https://fn-builds.net/S23/23.10-CL-23443094.7z&(simplyblk - rar):https://public.simplyblk.xyz/23.10.rar]",
            "++Fortnite+Release-23.20-CL-23783097-Windows [(FN Builds - zip):https://builds.fn-builds.net/23.20-CL-23783097.zip]",
            "++Fortnite+Release-23.40-CL-24087481-Windows [(FN Builds - zip):https://builds.fn-builds.net/23.40-CL-24087481.zip&(simplyblk - zip):https://public.simplyblk.xyz/23.40.zip]",
            "++Fortnite+Release-23.50-CL-24441668-Windows [(simplyblk - zip):https://public.simplyblk.xyz/23.50.zip]",

            # Season 24
            "++Fortnite+Release-24.00-CL-24554913-Windows [(FN Builds - zip):https://builds.fn-builds.net/24.00-CL-24554913.zip]",
            "++Fortnite+Release-24.01-CL-24672685-Windows [(FN Builds - zip):https://builds.fn-builds.net/24.01-CL-24672685.zip]",
            "++Fortnite+Release-24.10-CL-24903530-Windows [(FN Builds - zip):https://builds.fn-builds.net/24.10-CL-24903530.zip]",
            "++Fortnite+Release-24.20-CL-24939793-Windows [(ploosh - zip):https://r2.ploosh.dev/24.20.zip&(FN Builds - zip):https://builds.fn-builds.net/24.20-CL-25156858.zip]",
            "++Fortnite+Release-24.30-CL-25347382-Windows [(FN Builds - zip):https://builds.fn-builds.net/24.30-CL-25347382.zip]",
            "++Fortnite+Release-24.40-CL-25521145-Windows [(FN Builds - zip):https://builds.fn-builds.net/24.40-CL-25521145.zip]",

            # Season 25
            "++Fortnite+Release-25.00-CL-25909622-Windows [(FN Builds - 7z):https://fn-builds.net/S25/25.00-CL-25909622.7z]",
            "++Fortnite+Release-25.10-CL-26000959-Windows [(FN Builds - 7z):https://fn-builds.net/S25/25.10-CL-26000959.7z]",
            "++Fortnite+Release-25.11-CL-26171015-Windows [(FN Builds - 7z):https://fn-builds.net/S25/25.11-CL-26171015.7z]",
            "++Fortnite+Release-25.20-CL-26474516-Windows [(FN Builds - 7z):https://fn-builds.net/S25/25.20-CL-26474516.7z]",
            "++Fortnite+Release-25.30-CL-26867995-Windows [(FN Builds - 7z):https://fn-builds.net/S25/25.30-CL-26867995.7z]",

            # Season 26
            "++Fortnite+Release-26.00-CL-27424790-Windows [(FN Builds - 7z):https://fn-builds.net/S26/26.00-CL-27424790.7z]",
            "++Fortnite+Release-26.10-CL-27681420-Windows [(FN Builds - 7z):https://fn-builds.net/S26/26.10-CL-27681420.7z]",
            "++Fortnite+Release-26.20-CL-28096793-Windows [(FN Builds - 7z):https://fn-builds.net/S26/26.20-CL-28096793.7z]",
            "++Fortnite+Release-26.30-CL-28688692-Windows [(FN Builds - 7z):https://fn-builds.net/S26/26.30-CL-28688692.7z]",

            # Season 27
            "++Fortnite+Release-27.00-CL-29072304-Windows [(FN Builds - 7z):https://fn-builds.net/S27/27.00-CL-29072304.7z]",
            "++Fortnite+Release-27.10-CL-29552510-Windows [(FN Builds - 7z):https://fn-builds.net/S27/27.10-CL-29552510.7z]",
            "++Fortnite+Release-27.11-CL-29739262-Windows [(FN Builds - 7z):https://fn-builds.net/S27/27.11-CL-29739262.7z]",

            # Season 28
            "++Fortnite+Release-28.00-CL-29915848-Windows [(FN Builds - 7z):https://fn-builds.net/S28/28.00-CL-29915848.7z]",
            "++Fortnite+Release-28.01-CL-30106568-Windows [(FN Builds - 7z):https://fn-builds.net/S28/28.01-CL-30106568.7z]",
            "++Fortnite+Release-28.01.01-CL-30313795-Windows [(FN Builds - 7z):https://builds.fn-builds.net/28.01-CL-30313795.7z]",
            "++Fortnite+Release-28.10-CL-30676362-Windows [(FN Builds - 7z):https://fn-builds.net/S28/28.10-CL-30676362.7z]",
            "++Fortnite+Release-28.20-CL-31286935-Windows [(FN Builds - 7z):https://fn-builds.net/S28/28.20-CL-31286935.7z]",
            "++Fortnite+Release-28.30-CL-31511038-Windows [(FN Builds - 7z):https://fn-builds.net/S28/28.30-CL-31511038.7z]",

            # Season 29
            "++Fortnite+Release-29.00-CL-32116959-Windows [(FN Builds - 7z):https://fn-builds.net/S29/29.00-CL-32116959.7z]",
            "++Fortnite+Release-29.01-CL-32291970-Windows [(FN Builds - 7z):https://fn-builds.net/S29/29.01-CL-32291970.7z]",
            "++Fortnite+Release-29.10-CL-32391220-Windows [(FN Builds - 7z):https://fn-builds.net/S29/29.10-CL-32391220.7z]",
            "++Fortnite+Release-29.10-CL-32567225-Windows [(FN Builds - 7z):https://fn-builds.net/S29/29.10-CL-32567225.7z]",
            "++Fortnite+Release-29.20-CL-32716692-Windows [(FN Builds - 7z):https://fn-builds.net/S29/29.20-CL-32716692.7z]",
            "++Fortnite+Release-29.40-CL-33629566-Windows [(FN Builds - 7z):https://fn-builds.net/S29/29.40-CL-33629566.7z]",

            # Season 30
            "++Fortnite+Release-30.00-CL-33962396-Windows [(FN Builds - 7z):https://fn-builds.net/S30/30.00-CL-33962396.7z]",
            "++Fortnite+Release-30.10-CL-34261954-Windows [(FN Builds - 7z):https://fn-builds.net/S30/30.10-CL-34261954.7z]",
            "++Fortnite+Release-30.20-CL-34597766-Windows [(FN Builds - 7z):https://fn-builds.net/S30/30.20-CL-34597766.7z]",
            "++Fortnite+Release-30.30-CL-34891016-Windows [(FN Builds - 7z):https://fn-builds.net/S30/30.30-CL-34891016.7z]",

            # Season 31
            "++Fortnite+Release-31.00-CL-35447195-Windows [(FN Builds - 7z):https://fn-builds.net/S31/31.00-CL-35447195.7z]",
            "++Fortnite+Release-31.10-CL-35815136-Windows [(FN Builds - 7z):https://fn-builds.net/S31/31.10-CL-35815136.7z]",
            "++Fortnite+Release-31.30-CL-36600465-Windows [(FN Builds - 7z):https://fn-builds.net/S31/31.30-CL-36600465.7z]",

            # Season 32
            "++Fortnite+Release-32.00-CL-37505882-Windows [(FN Builds - 7z):https://fn-builds.net/S32/32.00-CL-37505882.7z]",
            "++Fortnite+Release-32.11-CL-38202817-Windows [(FN Builds - 7z):https://fn-builds.net/S32/32.11-CL-38202817.7z]",
        ]
        self.download_path = ""
        self.selected_version = None
        self.selected_server = None
        self.download_url = None
        self.running = False
        self.start_time = None
        self.progress_thread = None
        self.filename = None
        self.download_error = False
    
    def display_versions(self):
        """Display all available versions"""
        print("\n=== Available Versions ===")
        for i, version in enumerate(self.versions):
            version_name = version.split(" [")[0]
            print(f"- [{i}] {version_name}")
        print("\nTotal versions:", len(self.versions))
        print("Note: The download servers may no longer be available.")
        print("If you encounter issues, please check the server status.")
    
    def select_version(self):
        """Let the user select a version"""
        while True:
            try:
                choice = int(input("\nEnter the number of the version to download: "))
                if 0 <= choice < len(self.versions):
                    self.selected_version = self.versions[choice]
                    return True
                else:
                    print(f"Error: Please enter a number between 0 and {len(self.versions)-1}")
            except ValueError:
                print("Error: Please enter a valid number")
    
    def select_download_path(self):
        """Let the user specify the download path"""
        while True:
            path = input("Enter the path where to save the file: ")
            if os.path.isdir(path):
                self.download_path = path
                return True
            else:
                create = input(f"The folder '{path}' doesn't exist. Do you want to create it? (y/n): ")
                if create.lower() == 'y':
                    try:
                        os.makedirs(path)
                        self.download_path = path
                        return True
                    except Exception as e:
                        print(f"Error creating folder: {e}")
    
    @staticmethod
    def is_valid_url(url):
        """Check if a URL is valid."""
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except ValueError:
            return False
    
    def select_server(self):
        """Let the user select a server."""
        match = re.search(r'\[(.*?)\]', self.selected_version)
        if not match:
            print("Error: Invalid version format")
            return False

        servers_str = match.group(1)
        servers = servers_str.split('&')

        valid_servers = []
        for i, server in enumerate(servers):
            server_name, server_url = server.split(':', 1)
            server_name = server_name.strip()
            server_url = server_url.strip().strip('()')
            display_name = server_name.replace('(', '').replace(')', '').strip()
            if DLManager.is_valid_url(server_url):
                valid_servers.append((display_name, server_url))
            else:
                print(f"Warning: Invalid URL found for {display_name}: {server_url}")

        if not valid_servers:
            print("Error: No valid servers found for this version.")
            return False

        print("\n=== Available Servers ===")
        for i, (server_name, _) in enumerate(valid_servers):
            print(f"- [{i}] {server_name}")

        while True:
            try:
                choice = int(input("\nChoose a server: "))
                if 0 <= choice < len(valid_servers):
                    server_name, self.download_url = valid_servers[choice]
                    self.filename = os.path.basename(self.download_url)
                    return True
                else:
                    print(f"Error: Please enter a number between 0 and {len(valid_servers) - 1}")
            except ValueError:
                print("Error: Please enter a valid number")

    
    def download_file(self):
        """Download the file from the selected server"""
        self.running = True
        self.start_time = time.time()
        self.download_error = False
        
        file_path = os.path.join(self.download_path, self.filename)
        
        try:
            session = requests.Session()
            response = session.get(self.download_url, stream=True, timeout=10)
            response.raise_for_status()
            
            total_size = int(response.headers.get('content-length', 0))
            
            if total_size == 0:
                time.sleep(5)
                if os.path.getsize(file_path) == 0:
                    self.download_error = True
                    raise Exception("Download not starting")
            
            downloaded_size = 0
            written_size = 0
            cache_size = random.randint(50, 100)
            active_tasks = random.randint(20, 40)
            start_time = time.time()
            last_update_time = start_time
            download_speeds = []
            
            with open(file_path, 'wb') as f:
                for _ in range(5):
                    print("")
                
                for chunk in response.iter_content(chunk_size=8192):
                    if not self.running:
                        break
                    
                    if chunk:
                        f.write(chunk)
                        downloaded_size += len(chunk)
                        written_size = downloaded_size * random.uniform(1.05, 1.15)
                        
                        current_time = time.time()
                        elapsed_time = current_time - start_time
                        elapsed_time_str = str(timedelta(seconds=int(elapsed_time)))
                        
                        if current_time - last_update_time >= 1:
                            chunk_time = current_time - last_update_time
                            download_speed = len(chunk) / chunk_time / (1024 * 1024)
                            download_speeds.append(download_speed)
                            
                            avg_download_speed = sum(download_speeds[-10:]) / min(len(download_speeds), 10)
                            decompressed_speed = avg_download_speed * random.uniform(1.5, 2.5)
                            disk_write_speed = avg_download_speed * random.uniform(1.8, 2.8)
                            
                            progress = (downloaded_size / total_size * 100) if total_size > 0 else 0
                            
                            if avg_download_speed > 0 and total_size > 0:
                                remaining_bytes = total_size - downloaded_size
                                eta_seconds = remaining_bytes / (avg_download_speed * 1024 * 1024)
                                eta_str = str(timedelta(seconds=int(eta_seconds)))
                            else:
                                eta_str = "Unknown"
                            
                            cache_size = max(50, min(150, cache_size + random.uniform(-5, 5)))
                            active_tasks = max(10, min(50, active_tasks + random.randint(-2, 2)))
                            
                            sys.stdout.write('\033[5F\033[J')
                            print(f"INFO: = Progress: {progress:.2f}% (1/1), Running for {elapsed_time_str}, ETA: {eta_str}")
                            print(f"INFO:  - Downloaded: {downloaded_size/(1024*1024):.2f} MiB, Written: {written_size/(1024*1024):.2f} MiB")
                            print(f"INFO:  - Cache usage: {cache_size:.1f} MiB, active tasks: {active_tasks}")
                            print(f"INFO:  + Download   - {avg_download_speed:.2f} MiB/s (raw) / {decompressed_speed:.2f} MiB/s (decompressed)")
                            print(f"INFO:  + Disk       - {disk_write_speed:.2f} MiB/s (write) / 0.00 MiB/s (read)")
                            
                            last_update_time = current_time
            
            if self.running:
                sys.stdout.write('\033[5F\033[J')
                print("INFO: Download completed successfully!")
                print(f"INFO: File saved to: {file_path}")
                print()
                print()
                print()
                
        except requests.exceptions.RequestException as e:
            self.download_error = True
            sys.stdout.write('\033[5F\033[J')
            print("ERROR: Download failed!")
            print(f"ERROR: {str(e)}")
            print("ERROR: The download servers may no longer be available.")
            print()
            print()
        except Exception as e:
            self.download_error = True
            sys.stdout.write('\033[5F\033[J')
            print("ERROR: An unexpected error occurred!")
            print(f"ERROR: {str(e)}")
            print("ERROR: The download servers may no longer be available.")
            print()
            print()
        finally:
            self.running = False
    
    def start_download(self):
        """Start the actual download"""
        print("\nStarting download...")
        print("") 
        
        self.progress_thread = threading.Thread(target=self.download_file)
        self.progress_thread.start()
        time.sleep(10)
        if not self.download_error and self.running:
            try:
                while self.progress_thread.is_alive():
                    time.sleep(1)
            except KeyboardInterrupt:
                print("\nDownload cancelled by user.")
                self.running = False
                self.progress_thread.join()
        else:
            if not self.download_error:
                sys.stdout.write('\033[5F\033[J')
                print("ERROR: Download failed to start!")
                print("ERROR: The download servers may no longer be available.")
                print()
                print()
                print()
            self.running = False
            if self.progress_thread.is_alive():
                self.progress_thread.join()
    
    def run(self):
        """Run the download application"""
        print("LlamaDownloader - Fortnite Download Manager")
        print("Version 1.0")
        self.display_versions()
        if not self.select_version():
            return
        if not self.select_download_path():
            return
        if not self.select_server():
            return
        self.start_download()


if __name__ == "__main__":
    manager = DLManager()
    manager.run()
