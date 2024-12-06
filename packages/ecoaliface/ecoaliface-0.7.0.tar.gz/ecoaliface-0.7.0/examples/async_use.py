#!/usr/bin/env python3

import asyncio

import ecoaliface.simple

async def get_ecif():
    ## ecif = ecoaliface.simple.ECoalController("192.168.9.2", "admin", "admin")
    # https://stackoverflow.com/questions/41063331/how-to-use-asyncio-with-existing-blocking-library/53719009#53719009
    loop = asyncio.get_event_loop()    
    ecif = await loop.run_in_executor(None, ecoaliface.simple.ECoalController, "192.168.9.2", "admin", "admin")
    print(f"ecif.version {ecif.version}")
    return ecif
        
        
async def get_cached_status(ecif):
    loop = asyncio.get_event_loop()    
    ec_status = await loop.run_in_executor(None, ecif.get_cached_status)
    return ec_status
    

if __name__ == "__main__":
    import time
    s = time.perf_counter()
    ecif = asyncio.run(get_ecif())
    elapsed = time.perf_counter() - s
    print(f"{__file__} executed in {elapsed:0.2f} seconds. Got ecif: {ecif}")  # Takes around 0.04 seconds
    
    s = time.perf_counter()
    ec_status = ecif = asyncio.run(get_cached_status(ecif))
    elapsed = time.perf_counter() - s
    print(f"Got ec_status: {ec_status} in {elapsed:0.2f} seconds") # Takes around 0.03 seconds
    
    
    



