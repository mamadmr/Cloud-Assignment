from task import start_container, stop_container
 

# res = start_container.delay("postgres")
# print(res.get(timeout=10))

stop_res = stop_container.delay("bf9a17d663d655fed7612761531dca69ac561d6c32cd95ae8e6a321359d64476")
print(stop_res.get())