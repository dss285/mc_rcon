from commandset import CommandSet
import concurrent.futures
komennot = [
    """execute at {target} run particle minecraft:elder_guardian ~ ~ ~""",
    """playsound entity.ghast.warn voice {target} ~ ~ ~ 100 2""",
    """playsound entity.ghast.warn voice {target} ~ ~ ~ 100 2""",
    """playsound entity.ghast.warn voice {target} ~ ~ ~ 100 2""",
    """playsound entity.ghast.warn voice {target} ~ ~ ~ 100 2""",
    """playsound entity.ghast.warn voice {target} ~ ~ ~ 100 2""",
    """playsound entity.ghast.warn voice {target} ~ ~ ~ 100 2""",
    """playsound entity.ghast.warn voice {target} ~ ~ ~ 100 2"""
]
print(komennot)
cmsetti = CommandSet(komennot, 0.5, '', '127.0.0.1', '', 25575)
cmsetti2 = CommandSet(komennot, 1, '', '127.0.0.1', '', 25575)
cmsetti3 = CommandSet(komennot, 1.5, '', '127.0.0.1', '', 25575)

with concurrent.futures.ThreadPoolExecutor(max_workers=8) as tp:
    future2 = tp.submit(cmsetti.run)
    future = tp.submit(cmsetti2.run)
    future3 = tp.submit(cmsetti3.run)
    print(future.result())
